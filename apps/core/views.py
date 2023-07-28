from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Student
from django.contrib.auth.hashers import make_password



def admin_signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        admin = auth.authenticate(username=username, password=password)
        print(admin)
        if admin is not None:
            auth.login(request, admin)
            return redirect('admin-dashboard')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('admin-signin')
    else:
        return render(request, 'project_admin/admin_auth/signin.html')


@login_required(login_url='admin-signin')
def dashboard(request):
    # Get the total number of student records in the database
    total_students = Student.objects.count()

    context = {
        'segment': 'index',
        'total_students': total_students,  # Add the count to the context
    }

    return render(request, 'project_admin/index.html', context)


@login_required(login_url='admin-signin')
def admin_students(request):

    student_records = Student.objects.all()
    context = {'segment': 'students', 'student_records': student_records}

    return render(request, 'project_admin/students.html', context)


@login_required(login_url='admin-signin')
@require_POST
def add_student(request):
    first_name = request.POST['new_first_name']
    student_id = request.POST['new_student_id']
    last_name = request.POST['new_last_name']
    email = request.POST['new_email']
    course = request.POST['new_course']
    enrollment_year = request.POST['new_enrollment_year']
    password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']

    # Check if passwords match
    if password != confirm_password:
        messages.error(request, 'Passwords do not match.')
        return redirect('admin-dashboard-students')

    # Validate the uniqueness of the email
    if Student.objects.filter(email=email).exists():
        messages.error(request, 'Email address is already in use.')
        return redirect('admin-dashboard-students')

    # Create a new Student object and save it to the database
    student = Student(
        student_id=student_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        course=course,
        enrollment_year=enrollment_year,
        password=make_password(password)
    )
    if student is not None:
        student.save()
        messages.success(request, 'New student added successfully.')
    else:
        messages.error(request, 'Error adding student.')
    return redirect('admin-dashboard-students')


@login_required(login_url='admin-signin')
@require_POST
def delete_student(request, pk):
    student = Student.objects.get(student_id=pk)
    student.delete()
    messages.success(
        request, "Student Deleted Successfully")
    return redirect('admin-dashboard-students')


@login_required(login_url='admin-signin')
@require_POST
def update_student(request, student_id):
    # Retrieve the student object based on the provided student_id
    student = get_object_or_404(Student, pk=student_id)
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    course = request.POST['course']
    enrollment_year = request.POST['enrollment_year']
    password_edit = request.POST['password_edit']

    try:
            # Check if the new password is not already hashed
        if password_edit and not password_edit.startswith('pbkdf2_sha256'):
            student.password = make_password(password_edit)
        else:
            # If the password is already hashed or not provided, use the original form data
            student.password = password_edit

        student.first_name = first_name
        student.last_name = last_name
        student.email = email
        student.course = course
        student.enrollment_year = enrollment_year
        student.save()
        messages.success(request, "Student Update Successfully")
    except:
        messages.error(request, "Error Updating Student")

    return redirect('admin-dashboard-students')


@login_required(login_url='admin-signin')
def admin_logout(request):
    auth.logout(request)
    return redirect('admin-signin')
