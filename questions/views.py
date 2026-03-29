from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from subjects.models import Quiz
from .models import Question
from results.models import Result, StudentAnswer

@login_required
def take_quiz(request, quiz_id):
    if request.user.role != 'student':
        return redirect('subject_list')
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    questions = Question.objects.filter(quiz=quiz)

    previous_attempt = Result.objects.filter(
        student=request.user, quiz=quiz
    ).first()

    if previous_attempt:
        if previous_attempt.score >= 8:
            return render(request, 'questions/already_attempted.html', {
                'quiz': quiz,
                'result': previous_attempt,
                'can_retake': False
            })
        else:
            return render(request, 'questions/already_attempted.html', {
                'quiz': quiz,
                'result': previous_attempt,
                'can_retake': True
            })

    return render(request, 'questions/take_quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'time_limit': quiz.time_limit * 60
    })

@login_required
def retake_quiz(request, quiz_id):
    if request.user.role != 'student':
        return redirect('subject_list')
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    Result.objects.filter(student=request.user, quiz=quiz).delete()
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'questions/take_quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'time_limit': quiz.time_limit * 60
    })

@login_required
def submit_quiz(request, quiz_id):
    if request.method != 'POST':
        return redirect('subject_list')

    quiz      = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    score     = 0

    # ✅ Check if quiz has descriptive questions
    has_descriptive = questions.filter(
        question_type='descriptive'
    ).exists()

    result = Result.objects.create(
        student=request.user,
        quiz=quiz,
        score=0,
        total_questions=questions.count(),
        # ✅ Mark as pending review if has descriptive
        is_pending_review=has_descriptive,
        is_reviewed=not has_descriptive
    )

    answer_results = []

    for question in questions:
        if question.question_type == 'mcq':
            # ✅ MCQ — auto check
            selected   = request.POST.get(
                f'question_{question.id}', ''
            ).upper()
            is_correct = selected == question.correct_answer.upper()
            if is_correct:
                score += question.marks

            StudentAnswer.objects.create(
                result=result,
                question=question,
                selected_answer=selected,
                is_correct=is_correct,
                marks_awarded=question.marks if is_correct else 0,
                is_reviewed=True
            )
            answer_results.append({
                'question':       question,
                'selected':       selected,
                'is_correct':     is_correct,
                'correct_answer': question.correct_answer.upper(),
                'type':           'mcq'
            })

        else:
            # ✅ Descriptive — save answer for teacher review
            descriptive_answer = request.POST.get(
                f'question_{question.id}', ''
            )
            StudentAnswer.objects.create(
                result=result,
                question=question,
                descriptive_answer=descriptive_answer,
                is_correct=False,
                marks_awarded=0,
                is_reviewed=False
            )
            answer_results.append({
                'question':          question,
                'descriptive_answer': descriptive_answer,
                'type':              'descriptive'
            })

    result.score = score
    result.save()

    return render(request, 'results/result.html', {
        'quiz':            quiz,
        'score':           score,
        'total':           questions.count(),
        'answer_results':  answer_results,
        'has_descriptive': has_descriptive
    })