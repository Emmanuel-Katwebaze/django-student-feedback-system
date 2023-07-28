from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from apps.core.models import Student
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.hashers import make_password


def signin(request):
    if request.method == "POST":
        student_id = request.POST['student_number']
        password = request.POST['password']

        try:
            student = Student.objects.get(student_id=student_id)

        except ObjectDoesNotExist:
            # If the student with the given student_id does not exist, show an error message
            messages.info(request, 'Invalid Credentials')
            return redirect('signin')
        print(student.check_password(password))
        if student.check_password(password):

            request.session['authenticated_student_id'] = student.student_id

            return redirect('student_dashboard')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('signin')

    else:
        return render(request, 'students/students_auth/signin.html')


def signup(request):
    if request.method == 'POST':
        # Get form data from POST request
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        course = request.POST.get('course')
        enrollment_year = request.POST.get('enrollment_year')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')  # Redirect to the sign-up page

        # Validate the uniqueness of the email
        if Student.objects.filter(email=email).exists():
            messages.error(request, 'Email address is already in use.')
            return redirect('signup')  # Redirect to the sign-up page

        try:
            # Create the student with the provided data
            student = Student.objects.create_user(
                student_id=student_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                course=course,
                enrollment_year=enrollment_year,
                password=make_password(password)
            )
            messages.success(request, 'You have successfully signed up.')
            request.session['authenticated_student_id'] = student.student_id
            return redirect('student_dashboard')
        except ValidationError as e:
            # Handle validation errors
            messages.error(request, e.message)
            return redirect('signup')  # Redirect to the sign-up page

    return render(request, 'students/students_auth/signup.html')


def student_dashboard(request):
    # Retrieve the authenticated student's ID from the session
    authenticated_student_id = request.session.get('authenticated_student_id')
    print(authenticated_student_id)

    if authenticated_student_id:
        # Retrieve the student from the database using the ID
        try:
            student = Student.objects.get(student_id=authenticated_student_id)

            # Pass the student into the context
            context = {'student': student, 'segment': 'index'}
            return render(request, 'students/index.html', context)
        except Student.DoesNotExist:
            messages.info(request, 'Invalid Credentials')
            return redirect('signin')
    else:
        # If the authenticated student ID is not found in the session, redirect to the signin page
        return redirect('signin')

def student_logout(request):
    auth.logout(request)
    return redirect('signin')
