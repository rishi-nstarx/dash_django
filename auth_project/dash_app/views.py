from django.shortcuts import render, redirect
from django.views import View
from .models import StudentData, StudentInfo
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from auth_app.models import CustomUser
from .models import StudentInfo, AttendenceData


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
        # print(student_info.dob if student_info else None, 
        #       student_info.admission_date if student_info else None, 
        #       student_info.branch if student_info else None)

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
    initial_arguments = {
        'user_id': request.user.id
    }
    return render(request, 'attendence_graph.html', {'dash_context': initial_arguments})


def fetch_user_data(args):
    from dash_app.utils import get_current_user
    user = get_current_user(args)  # Lazy import avoids initialization conflict
    return user


# @login_required(login_url='login')
# def try_function(request):
#     user = fetch_user_data(request)

#     # Month ordering
#     MONTH_ORDER = {
#         'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7,
#         'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
#     }

#     # Query attendance data for the user
#     attendence_data = AttendenceData.objects.filter(student_id=5)

#     sorted_attendence_data = sorted(attendence_data, key=lambda record: MONTH_ORDER[record.month])



#     print(sorted_attendence_data)

#     line_data = {
#         "Months": [],
#         "Days": []
#     }

#     for attendenec in sorted_attendence_data:
#         line_data["Months"].append(attendenec.month)
#         line_data["Days"].append(attendenec.days_in_month)

#     month_labels = {
#         'JAN': 'January', 'FEB': 'February', 'MAR': 'March', 'APR': 'April',
#         'MAY': 'May', 'JUN': 'June', 'JUL': 'July', 'AUG': 'August',
#         'SEP': 'September', 'OCT': 'October', 'NOV': 'November', 'DEC': 'December'
#     }

#     full_month_names = [month_labels[month] for month in line_data["Months"]]

#     x=line_data["Days"]
#     y=line_data["Months"]

#     print(x)
#     print(y)
#     print(full_month_names)



    # # Sort data by month
    # sorted_attendence_data = sorted(
    #     attendence_data,
    #     key=lambda record: MONTH_ORDER[record.month]
    # )


    # # Prepare data for graphs
    # months = [data.month for data in sorted_attendence_data]
    # days = [data.days_in_month for data in sorted_attendence_data]

    # # Map month codes to full names for better display
    # month_labels = {
    #     'JAN': 'January', 'FEB': 'February', 'MAR': 'March', 'APR': 'April',
    #     'MAY': 'May', 'JUN': 'June', 'JUL': 'July', 'AUG': 'August',
    #     'SEP': 'September', 'OCT': 'October', 'NOV': 'November', 'DEC': 'December'
    # }
    # full_month_names = [month_labels[month] for month in months]

    # print(months)
    # print(days)
    # print(full_month_names)