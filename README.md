# Online Course App — Assessment Feature

A Django course app extended with graded questions, answer choices, enrollment-linked
submissions, instructor admin tools, and detailed exam results. Based on the IBM
Skills Network `tfjzl-final-cloud-app-with-database` starter.

## Run locally

```sh
python -m venv .venv
# Activate the environment, then:
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

For optional demo lessons and a two-question mock exam, set `DEMO_ADMIN_PASSWORD`
in your environment and run `python manage.py seed_demo`. The demo admin/learner
username is `jatinmahire`. No password or local database is committed.

Visit `/admin/` to manage courses, lessons, questions, choices and submissions.
Visit `/onlinecourse/`, sign in, open Learning Django, and complete the assessment.
Select all correct answers for each question; extra wrong answers receive no credit.
Each question is worth 50 points. The passing score is greater than 80/100.

## Implementation

- `onlinecourse/models.py`: Question, Choice, Submission and exact-answer scoring.
- `onlinecourse/admin.py`: seven model imports and inline/admin editors.
- `onlinecourse/templates/onlinecourse/course_details_bootstrap.html`: lessons and exam form.
- `onlinecourse/views.py`: authenticated submission and owner-only exam results.
- `onlinecourse/urls.py`: submission and result routes.
- Bootstrap CSS is bundled locally for reliable rendering.

Run `python manage.py test onlinecourse` for assessment and access-control tests.
Set `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS` when deploying. The development
server and default SQLite configuration are intended for this learning project.
