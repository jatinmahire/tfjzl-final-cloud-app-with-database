from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Choice, Course, Enrollment, Question, Submission


class AssessmentTests(TestCase):
    def setUp(self):
        self.learner = User.objects.create_user('learner', password='test-password123')
        self.other = User.objects.create_user('other', password='test-password123')
        self.course = Course.objects.create(name='Django course', description='Learn Django')
        self.enrollment = Enrollment.objects.create(user=self.learner, course=self.course)
        self.question = Question.objects.create(course=self.course, question_text='Select correct answers', grade=100)
        self.first = Choice.objects.create(question=self.question, choice_text='Correct one', is_correct=True)
        self.second = Choice.objects.create(question=self.question, choice_text='Correct two', is_correct=True)
        self.wrong = Choice.objects.create(question=self.question, choice_text='Wrong', is_correct=False)
        self.submit_url = reverse('onlinecourse:submit', args=[self.course.pk])

    def test_exact_answer_scoring(self):
        self.assertTrue(self.question.is_get_score([self.first.pk, self.second.pk]))
        self.assertFalse(self.question.is_get_score([self.first.pk]))
        self.assertFalse(self.question.is_get_score([self.first.pk, self.second.pk, self.wrong.pk]))
        self.assertFalse(self.question.is_get_score([]))

    def test_anonymous_submission_requires_login(self):
        self.assertEqual(self.client.post(self.submit_url).status_code, 302)
        self.assertEqual(Submission.objects.count(), 0)

    def test_submission_requires_post_and_enrollment(self):
        self.client.force_login(self.other)
        self.assertEqual(self.client.post(self.submit_url).status_code, 404)
        self.client.force_login(self.learner)
        self.assertEqual(self.client.get(self.submit_url).status_code, 405)

    def test_correct_mock_exam_and_saved_choices(self):
        self.client.force_login(self.learner)
        response = self.client.post(self.submit_url, {'choice_1': [self.first.pk, self.second.pk]}, follow=True)
        self.assertContains(response, 'Congratulations')
        self.assertContains(response, '100/100')
        self.assertEqual(Submission.objects.get().choices.count(), 2)

    def test_wrong_answer_has_no_partial_credit_and_allows_retest(self):
        self.client.force_login(self.learner)
        response = self.client.post(self.submit_url, {'choice_1': [self.first.pk, self.second.pk, self.wrong.pk]}, follow=True)
        self.assertEqual(response.context['grade'], 0)
        self.assertContains(response, 'Re-test')

    def test_results_are_private_to_owner_and_course(self):
        submission = Submission.objects.create(enrollment=self.enrollment)
        url = reverse('onlinecourse:show_exam_result', args=[self.course.pk, submission.pk])
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_choices_from_another_course_are_rejected(self):
        other_course = Course.objects.create(name='Other course')
        question = Question.objects.create(course=other_course, question_text='Another course question')
        foreign_choice = Choice.objects.create(question=question, choice_text='Other answer', is_correct=True)
        self.client.force_login(self.learner)
        self.assertEqual(self.client.post(self.submit_url, {'choice_1': foreign_choice.pk}).status_code, 400)
        self.assertEqual(Submission.objects.count(), 0)

    def test_invalid_choice_id_does_not_create_submission(self):
        self.client.force_login(self.learner)
        self.assertEqual(self.client.post(self.submit_url, {'choice_1': 'invalid'}).status_code, 400)
        self.assertEqual(Submission.objects.count(), 0)

    def test_course_page_uses_requested_template(self):
        self.client.force_login(self.learner)
        response = self.client.get(reverse('onlinecourse:course_details', args=[self.course.pk]))
        self.assertTemplateUsed(response, 'onlinecourse/course_details_bootstrap.html')
        self.assertContains(response, 'Submit exam')

    def test_weighted_score_and_selected_choices_are_available_to_template(self):
        self.question.grade = 1
        self.question.save()
        other_question = Question.objects.create(course=self.course, question_text='Another weighted question', grade=3)
        Choice.objects.create(question=other_question, choice_text='Correct', is_correct=True)
        self.client.force_login(self.learner)
        response = self.client.post(self.submit_url, {'choice_1': [self.first.pk, self.second.pk]}, follow=True)
        self.assertEqual(response.context['grade'], 25)
        self.assertEqual(response.context['possible'], 4)
        self.assertEqual(response.context['possible_score'], 4)
        self.assertEqual(response.context['selected_ids'], {self.first.pk, self.second.pk})
