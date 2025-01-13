from django.shortcuts import render, redirect
from django.views import View
from .models import StudentData, StudentInfo
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from asgiref.sync import sync_to_async

from auth_app.models import CustomUser
from .models import StudentInfo, AttendenceData
from .dash_apps.attendence_graph import fetch_data

# Create your views here.
class DashView(View):

    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        return render(request, 'dash_home.html')

    @method_decorator(login_required(login_url='login'))
    def post(self, request):
        form_data = request.POST
        year = form_data["year"]
        mech = form_data["mech"]
        civil = form_data["civil"]
        ee = form_data["ee"]
        cse = form_data["cse"]

        student_data = StudentData(
            year=year,
            mech=mech,
            civil=civil,
            ee=ee,
            cse=cse
        )
        student_data.save()
        return redirect("dash_home")
    

class StudentProfile(View):
    def get(self, request):
        try:
            student_info = StudentInfo.objects.get(student=request.user)
        except StudentInfo.DoesNotExist:
            student_info = None

        return render(request, 'student_creation.html', {'user': student_info})

    def post(self, request):
        form_data = request.POST
        dob = form_data.get("dob")  # Always retrieve these fields
        admission_date = form_data.get("admission_date")
        branch = form_data.get("branch")

        try:
            user = StudentInfo.objects.get(student=request.user)
        except StudentInfo.DoesNotExist:
            user = None

        if user:
            # Update the existing user data
            user.dob = dob
            user.admission_date = admission_date
            user.branch = branch
            user.save()
        else:
            # Create a new StudentInfo object
            student_info = StudentInfo(
                student=request.user, 
                dob=dob, 
                admission_date=admission_date, 
                branch=branch
            )
            student_info.save()

        return redirect("student_profile")
    

class AttendenecView(View):

    def get(self, request):
        students_info = StudentInfo.objects.all()
        return render(request, 'attendence_form.html', {"students_info": students_info})

    def post(self, request):
        form_data = request.POST
        student_id = form_data["student"]

        student = CustomUser.objects.get(id=student_id)

        year = form_data["year"]
        month = form_data["month"]
        days_in_month = form_data["days_in_month"]

        try:
            student_1 = AttendenceData.objects.get(student=student, month=month, year=year)
        except:
            student_1 = None

        if student_1:
            print(student_1)
            student_1.student = student
            student_1.year = year
            student_1.month = month
            student_1.days_in_month = days_in_month
            student_1.save()
            return redirect('attendence_update')

        
        attendence = AttendenceData(student=student, year=year, month=month, days_in_month=days_in_month)
        attendence.save()
        return redirect('attendence_update')



@login_required(login_url='login')
def dash_home(request):
    return render(request, 'dash_home_graph.html')


@login_required(login_url='login')
def graph_explained(request):
    return render(request, 'graph_explained.html')


@login_required(login_url='login')
def attendence_graph(request):
    fetch_data(request.user.id)
    return render(request, 'attendence_graph.html')

@sync_to_async
@login_required(login_url='login')
def live_graph(request):
    from .dash_apps.live_users import wait, thread_status
    if not thread_status:
        wait()
    return render(request, 'live_app.html')