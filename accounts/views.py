from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from .forms import StudentRegistrationForm, TeacherRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib import messages



# Create your views here.
def register_student(request):

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, 'accounts/pending.html')

    else:
        form = StudentRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'accounts/register_teacher.html', {'form': form})


def login_user(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_approved:
                return render(request, 'accounts/notapproved.html')
            login(request, user)
            if user.role == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            error = 'Invalid username or password'
    return render(request, 'accounts/login.html', {'error': error})

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return redirect('login')
    from subjects.models import Subject
    subject_count   = Subject.objects.count()
    student_count   = User.objects.filter(role='student', is_approved=True).count()
    pending_count   = User.objects.filter(role='student', is_approved=False).count()
    pending_students = User.objects.filter(role='student', is_approved=False)
    return render(request, 'accounts/teacher_dashboard.html', {
        'subject_count':    subject_count,
        'student_count':    student_count,
        'pending_count':    pending_count,
        'pending_students': pending_students,
    })



def teacher_profile(request):
    user = request.user

    if request.method == 'POST':
        action = request.POST.get('action')

        # 🔐 CHANGE PASSWORD
        if action == "change_password":
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if not user.check_password(old_password):
                messages.error(request, "Old password incorrect ❌")

            elif new_password != confirm_password:
                messages.error(request, "Passwords do not match ❌")

            else:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password updated ✅")
                return redirect('login')

        # ✏️ UPDATE PROFILE
        elif action == "update_profile":
            email = request.POST.get('email')
            user.email = email
            user.save()
            messages.success(request, "Profile updated ✅")

    return render(request, 'accounts/teacher_profile.html', {'user': user})

@login_required
def update_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')
        
        # Security check: Ensure email isn't empty or already taken
        if User.objects.filter(email=new_email).exclude(id=request.user.id).exists():
            messages.error(request, "This email is already in use.")
        else:
            request.user.email = new_email
            request.user.save()
            messages.success(request, "Email updated successfully!")
            
    return redirect('teacher_profile')

@login_required
def change_password(request):
    if request.method == 'POST':
        old_pass = request.POST.get('old_password')
        new_pass = request.POST.get('new_password')
        confirm_pass = request.POST.get('confirm_password')

        # 1. Check if old password is correct
        if not request.user.check_password(old_pass):
            messages.error(request, "Your current password was entered incorrectly.")
        # 2. Check if new passwords match
        elif new_pass != confirm_pass:
            messages.error(request, "The two new password fields didn't match.")
        else:
            # 3. Save new password
            request.user.set_password(new_pass)
            request.user.save()
            # Important: Keep the user logged in after password change
            update_session_auth_hash(request, request.user)
            messages.success(request, "Your password was successfully updated!")
            
    return redirect('teacher_profile')


@login_required
def manage_students(request):

    if request.user.role != 'teacher':
        return redirect('login')

    students = User.objects.filter(role='student')

    return render(request, 'accounts/manage_students.html', {'students': students})

@login_required
def approve_student(request, user_id):

    if request.user.role != 'teacher':
        return redirect('login')

    student = User.objects.get(id=user_id)
    student.is_approved = True
    student.save()

    return redirect('manage_students')

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('login')
    from subjects.models import Subject
    subjects = Subject.objects.all()
    return render(request, 'accounts/student_dashboard.html', {
        'subjects': subjects
    })

def student_profile(request):
    user = request.user

    if request.method == 'POST':
        action = request.POST.get('action')

        # 🔐 CHANGE PASSWORD
        if action == "change_password":
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if not user.check_password(old_password):
                messages.error(request, "Old password incorrect ❌")

            elif new_password != confirm_password:
                messages.error(request, "Passwords do not match ❌")

            else:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password updated ✅")
                return redirect('login')

        # ✏️ UPDATE PROFILE
        elif action == "update_profile":
            email = request.POST.get('email')
            user.email = email
            user.save()
            messages.success(request, "Profile updated ✅")

    return render(request, 'accounts/student_profile.html', {'user': user})

@login_required
def update_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')
        
        # Security check: Ensure email isn't empty or already taken
        if User.objects.filter(email=new_email).exclude(id=request.user.id).exists():
            messages.error(request, "This email is already in use.")
        else:
            request.user.email = new_email
            request.user.save()
            messages.success(request, "Email updated successfully!")
            
    return redirect('student_profile')

@login_required
def change_password(request):
    if request.method == 'POST':
        old_pass = request.POST.get('old_password')
        new_pass = request.POST.get('new_password')
        confirm_pass = request.POST.get('confirm_password')

        # 1. Check if old password is correct
        if not request.user.check_password(old_pass):
            messages.error(request, "Your current password was entered incorrectly.")
        # 2. Check if new passwords match
        elif new_pass != confirm_pass:
            messages.error(request, "The two new password fields didn't match.")
        else:
            # 3. Save new password
            request.user.set_password(new_pass)
            request.user.save()
            # Important: Keep the user logged in after password change
            update_session_auth_hash(request, request.user)
            messages.success(request, "Your password was successfully updated!")
            
    return redirect('student_profile')