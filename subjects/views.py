from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from questions.models import Question
from subjects.models import Quiz, Subject
from results.models import Result


# ===========================
# Subject Views
# ===========================

@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects/subject_list.html', {
        'subjects': subjects
    })


@login_required
def create_subject(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        if not name:
            messages.error(request, "Subject name is required ❌")

        elif Subject.objects.filter(name=name).exists():
            messages.warning(request, "Subject already exists ⚠️")

        else:
            Subject.objects.create(name=name)
            messages.success(request, "Subject created successfully ✅")
            return redirect('subject_list')

    return render(request, 'subjects/create_subject.html')


# ===========================
# 🔥 UPDATED SUBJECT DETAIL
# ===========================

@login_required
def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    quizzes = subject.quizzes.all()

    quiz_data = []

    for quiz in quizzes:
        result = Result.objects.filter(
            student=request.user,
            quiz=quiz
        ).order_by('-date_taken').first()

        total_questions = quiz.questions.count()

        # ✅ Dynamic pass logic (60%)
        pass_marks = int(total_questions * 0.6)

        already_passed = False
        can_retake = False

        if result:
            if result.score >= pass_marks:
                already_passed = True
            else:
                can_retake = True

        quiz_data.append({
            'quiz': quiz,
            'question_count': total_questions,
            'already_passed': already_passed,
            'can_retake': can_retake,
        })

    return render(request, 'subjects/subject_detail.html', {
        'subject': subject,
        'quiz_data': quiz_data
    })


@login_required
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.user.role != 'teacher':
        messages.error(request, "Access denied ❌")
        return redirect('subject_list')

    subject.delete()
    messages.success(request, "Subject deleted successfully 🗑️")

    return redirect('subject_list')


# ===========================
# Quiz Views
# ===========================

@login_required
def create_quiz(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        time_limit = request.POST.get('time_limit', 10)

        try:
            time_limit = int(time_limit)
        except ValueError:
            time_limit = 10

        if not title:
            messages.error(request, "Quiz title is required ❌")

        else:
            quiz = Quiz.objects.create(
                title=title,
                subject=subject,
                time_limit=time_limit
            )

            messages.success(request, "Quiz created successfully ✅")
            return redirect('add_question', quiz_id=quiz.id)

    return render(request, 'subjects/create_quiz.html', {
        'subject': subject
    })


@login_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.user.role != 'teacher':
        messages.error(request, "Access denied ❌")
        return redirect('subject_detail', subject_id=quiz.subject.id)

    quiz.delete()
    messages.success(request, "Quiz deleted 🗑️")

    return redirect('subject_detail', subject_id=quiz.subject.id)


# ===========================
# Question Views
# ===========================

@login_required
def add_question(request, quiz_id):
    if request.user.role != 'teacher':
        return redirect('subject_list')

    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':

        # =====================
        # ADD QUESTION
        # =====================
        if 'add_question' in request.POST:

            question_text = request.POST.get('question_text', '').strip()
            question_type = request.POST.get('question_type', 'mcq')
            marks = request.POST.get('marks', 1)

            try:
                marks = int(marks)
            except ValueError:
                marks = 1

            if not question_text:
                messages.error(request, "Question cannot be empty ❌")
                return redirect('add_question', quiz_id=quiz.id)

            # =====================
            # MCQ QUESTION
            # =====================
            if question_type == 'mcq':
                Question.objects.create(
                    quiz=quiz,
                    question_text=question_text,
                    question_type='mcq',
                    option_a=request.POST.get('option_a', ''),
                    option_b=request.POST.get('option_b', ''),
                    option_c=request.POST.get('option_c', ''),
                    option_d=request.POST.get('option_d', ''),
                    correct_answer=request.POST.get('correct_answer', '').upper(),
                    marks=marks
                )

            # =====================
            # DESCRIPTIVE QUESTION
            # =====================
            else:
                Question.objects.create(
                    quiz=quiz,
                    question_text=question_text,
                    question_type='descriptive',
                    correct_answer=request.POST.get('model_answer', ''),
                    marks=marks
                )

            messages.success(request, "Question added ✅")
            return redirect('add_question', quiz_id=quiz.id)

        # =====================
        # FINISH BUTTON
        # =====================
        elif 'finish' in request.POST:
            return redirect('subject_detail', subject_id=quiz.subject.id)

    return render(request, 'subjects/add_question.html', {
        'quiz': quiz,
        'questions': questions
    })