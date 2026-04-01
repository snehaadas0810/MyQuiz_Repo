from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Result, StudentAnswer


# ===========================
# 🔹 ALL RESULTS (TEACHER)
# ===========================
@login_required
def all_results(request):
    if request.user.role != "teacher":
        messages.error(request, "Access denied ❌")
        return redirect("student_results")

    results = Result.objects.all().order_by("-date_taken")

    return render(request, "results/all_results.html", {"results": results})


# ===========================
# 🔹 STUDENT RESULTS
# ===========================
@login_required
def student_results(request):
    results = Result.objects.filter(student=request.user).order_by("-date_taken")

    return render(request, "results/student_results.html", {"results": results})


# ===========================
# 🔹 REVIEW RESULT (TEACHER)
# ===========================
@login_required
def review_result(request, result_id):
    if request.user.role != "teacher":
        messages.error(request, "Access denied ❌")
        return redirect("student_results")

    result = get_object_or_404(Result, id=result_id)
    answers = StudentAnswer.objects.filter(result=result)

    if request.method == "POST":

        # 🔥 FIX: Recalculate from scratch (no duplicate addition)
        total_score = 0

        for answer in answers:

            # =====================
            # MCQ (already checked)
            # =====================
            if answer.question.question_type == "mcq":
                total_score += answer.marks_awarded
                continue

            # =====================
            # DESCRIPTIVE
            # =====================
            marks_key = f"marks_{answer.id}"
            feedback_key = f"feedback_{answer.id}"

            # Safe fetch
            try:
                marks_awarded = int(request.POST.get(marks_key, 0))
            except ValueError:
                marks_awarded = 0

            feedback = request.POST.get(feedback_key, "")

            # Cap marks
            max_marks = answer.question.marks
            marks_awarded = min(marks_awarded, max_marks)

            # Save answer
            answer.marks_awarded = marks_awarded
            answer.teacher_feedback = feedback
            answer.is_reviewed = True
            answer.is_correct = marks_awarded > 0
            answer.save()

            total_score += marks_awarded

        # =====================
        # FINAL RESULT UPDATE
        # =====================
        result.score = total_score
        result.is_reviewed = True
        result.is_pending_review = False
        result.save()

        messages.success(request, "Result reviewed successfully ✅")

        return redirect("all_results")

    return render(
        request, "results/review_result.html", {"result": result, "answers": answers}
    )
