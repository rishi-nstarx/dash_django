from django.db import models
from auth_app.models import CustomUser
# Create your models here.
class StudentData(models.Model):

    class Meta:
        db_table = "student_data"

    year = models.CharField(max_length=4)
    mech = models.IntegerField()
    civil = models.IntegerField()
    ee = models.IntegerField()
    cse = models.IntegerField()
    
    def __str__(self):
        return self.year
    

class StudentInfo(models.Model):
    class Meta:
        db_table = "student_info"

    BRANCH_CHOICES = [
        ('CSE', 'Computer Science Engineering'), # 'CSE' will be stored and 'Computer Science Engineering' will be displayed.
        ('EE', 'Electrical Engineering'),
        ('MECH', 'Mechanical Engineering'),
        ('CIVIL', 'Civil Engineering')

    ]
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile", null=False)
    dob = models.DateField()
    admission_date = models.DateField()
    branch = models.CharField(max_length=5, choices=BRANCH_CHOICES)


class AttendenceData(models.Model):
        
    class Meta:
        db_table = "attendence_data"

    MONTH_CHOICES = [
        ('JAN', 'January'),
        ('FEB', 'February'),
        ('MAR', 'March'),
        ('APR', 'April'),
        ('MAY', 'May'),
        ('JUN', 'June'),
        ('JUL', 'July'),
        ('AUG', 'August'),
        ('SEP', 'September'),
        ('OCT', 'October'),
        ('NOV', 'November'),
        ('DEC', 'December')
    ]


    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="attendence", null=False)
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=3, choices=MONTH_CHOICES)
    days_in_month = models.IntegerField()


