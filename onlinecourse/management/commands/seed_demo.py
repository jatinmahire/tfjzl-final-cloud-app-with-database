import os
from datetime import date
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from onlinecourse.models import Course, Lesson, Enrollment, Question, Choice


class Command(BaseCommand):
    help = 'Create a local demo admin, enrolled learner, lessons, and mock exam.'

    def handle(self, *args, **options):
        password = os.environ.get('DEMO_ADMIN_PASSWORD')
        if not password:
            raise CommandError('Set DEMO_ADMIN_PASSWORD before running seed_demo.')
        user, _ = User.objects.get_or_create(username='jatinmahire')
        user.first_name = 'Jatin'
        user.last_name = 'Mahire'
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        course, _ = Course.objects.update_or_create(name='Learning Django', defaults={
            'description': 'Learn Django models, templates, and views, then test your knowledge with a course assessment.',
            'pub_date': date.today(), 'total_enrollment': 1,
        })
        Enrollment.objects.get_or_create(user=user, course=course)
        for order, title, content in [
            (0, 'What is Django?', 'Django is a high-level Python web framework for building secure and maintainable web applications.'),
            (1, 'Models and migrations', 'A model defines database fields and relationships. Migrations apply model changes to the database.'),
        ]:
            Lesson.objects.update_or_create(course=course, order=order, defaults={'title': title, 'content': content})
        for content, answers in [
            ('Is Django a Python framework?', [('Yes', True), ('No', False)]),
            ('Which Django features are used by this course app?', [('Models define database data', True), ('Templates render HTML pages', True), ('Migrations replace authentication', False)]),
        ]:
            question, _ = Question.objects.update_or_create(course=course, content=content, defaults={'grade': 50})
            for label, correct in answers:
                Choice.objects.update_or_create(question=question, content=label, defaults={'is_correct': correct})
        self.stdout.write(self.style.SUCCESS(f'Demo course {course.pk} and user jatinmahire are ready.'))
