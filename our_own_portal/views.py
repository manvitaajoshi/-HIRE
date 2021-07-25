

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#from django.db.models.functions import datetime
from django.http import HttpResponse, HttpResponseRedirect
from .models import CustomUser, Student, Company, Job, AppliedStudent, SelectedStudent
# Create your views here.
from django.shortcuts import render
from django.db.models import Count
'''from django.contrib import admin'''


def data_count(request):
    company = Company.objects.count()
    student = Student.objects.count()
    job = Job.objects.count()
    apply = AppliedStudent.objects.count()
    select = SelectedStudent.objects.count()
    user = CustomUser.objects.filter(user_type=2).values('id')
    students = Student.objects.filter(admin_id__in=user).order_by('-cgpa')[:5]
    user = CustomUser.objects.filter(user_type=3).values('id')
    companies = Company.objects.filter(admin_id__in=user).order_by('world_rank')[:5]
    return render(request, 'data_count.html', {"company": company, "student": student, "job": job, "apply": apply, "select": select, "students": students, "companies": companies})


def index(request):
    return render(request, 'index.html')


def register(request):
    return render(request, 'register.html')


def loginform(request):
    return render(request, 'loginform.html')


def invalid_login(request):
    return render(request, 'invalid_login.html')


def studentform(request):
    return render(request, 'studentform.html')


def addjobform(request):
    companies = Company.objects.raw('select * from our_own_portal_company')
    return render(request, 'addjob.html', {"companies": companies})


def companyform(request):
    return render(request, 'companyform.html')


def admin_base_page(request):
    return render(request, 'admin_base_page.html')


def company_base_page(request):
    return render(request, 'company_base_page.html')


def student_base_page(request):
    return render(request, 'student_base_page.html')


def company_profile(request):
    companies = Company.objects.raw('select *from our_own_portal_company')
    return render(request, 'company_profile.html', {"companies": companies})


def student_profile_for_company(request, id):
    student = Student.objects.get(student_id=id)
    return render(request, 'student_profile_for_company.html', {"student": student})


def student_profile(request):
    students = Student.objects.raw('select *from our_own_portal_student')
    return render(request, 'student_profile.html', {"students": students})


def edit_student_profile(request):
    students = Student.objects.raw('select *from our_own_portal_student')
    return render(request, 'edit_student_profile.html', {"students": students})


def save_student_profile(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        sid = request.POST.get("sid")
        student = Student.objects.get(student_id=sid)
        id = student.admin_id
        user = CustomUser.objects.get(id=id)
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        email = request.POST.get("email")
        college_id = request.POST.get("college_id")
        clgname = request.POST.get("clgname")
        degree = request.POST.get("degree")
        cgpa = request.POST.get("cgpa")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        contact = request.POST.get("contact")
        gender = request.POST.get("gender")
        skills = request.POST.get("skills")
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        student.college_id = college_id
        student.college_name = clgname
        student.college_degree = degree
        student.cgpa = cgpa
        student.city = city
        student.state = state
        student.pin_code = pincode
        student.contact_no = contact
        student.gender = gender
        student.skills = skills
        student.save()
    return HttpResponseRedirect('student_profile')


def save_company_profile(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        cid = request.POST.get("cid")
        company = Company.objects.get(company_id=cid)
        id = company.admin_id
        user = CustomUser.objects.get(id=id)
        email = request.POST.get("email")
        sector = request.POST.get("sector")
        rank = request.POST.get("rank")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        contact = request.POST.get("contact")
        mode = request.POST.get("mode")
        holiday = request.POST.get("weekly_off")
        sick = request.POST.get("sick")
        revenue = request.POST.get("revenue")
        user.email = email
        user.save()
        company.city = city
        company.state = state
        company.pin_code = pincode
        company.contact_no = contact
        company.sector = sector
        company.world_rank = rank
        company.mode = mode
        company.weekly_off = holiday
        company.sick_leaves = sick
        company.revenue = revenue
        company.save()
    return HttpResponseRedirect('company_profile')


def save_edit_job(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        id = request.POST.get("id")
        job = Job.objects.get(id=id)
        position = request.POST.get("position")
        vacancy = request.POST.get("vacancy")
        level = request.POST.get("level")
        min_sal = request.POST.get("min_sal")
        avg_sal = request.POST.get("avg_sal")
        max_sal = request.POST.get("max_sal")
        skills = request.POST.get("skills")
        job.position = position
        job.vacancy = vacancy
        job.experience_level = level
        job.min_salary_LPA = min_sal
        job.avg_salary_LPA = avg_sal
        job.max_salary_LPA = max_sal
        job.required_skills = skills
        job.save()
        return HttpResponseRedirect("view_job_for_company")


def edit_company_profile(request):
    companies = Company.objects.raw('select *from our_own_portal_company')
    return render(request, 'edit_company_profile.html', {"companies": companies})


def edit_job(request, id):
    job = Job.objects.get(id=id)
    companies = Company.objects.raw('select * from our_own_portal_company')
    return render(request, 'edit_job.html', {"job": job, "companies":companies})


def delete_company(request, id):
    company = Company.objects.get(admin_id=id)
    user = CustomUser.objects.get(id=id)
    company.delete()
    user.delete()
    return render(request, 'index.html')


def delete_student(request, id):
    student = Student.objects.get(admin_id=id)
    user = CustomUser.objects.get(id=id)
    student.delete()
    user.delete()
    return render(request, 'index.html')


def view_job(request):
    jobs = Job.objects.raw('select *from our_own_portal_job')
    companies = Company.objects.raw('select *from our_own_portal_company order by world_rank')
    return render(request, "view_job.html", {"jobs": jobs, "companies": companies})


def view_job_for_student(request):
    jobs = Job.objects.raw('select *from our_own_portal_job')
    companies = Company.objects.raw('select *from our_own_portal_company order by world_rank')
    return render(request, "view_job_for_student.html", {"jobs": jobs, "companies": companies})


def view_job_for_company(request):
    jobs = Job.objects.raw('select *from our_own_portal_job')
    companies = Company.objects.raw('select *from our_own_portal_company')
    return render(request, "view_job_for_company.html", {"jobs": jobs, "companies": companies})


def view_all_student(request):
    students = Student.objects.raw('Select * from our_own_portal_student order by cgpa desc')
    return render(request, "view_all_student.html", {"students": students})


def view_all_company(request):
    companies = Company.objects.raw('Select * from our_own_portal_company order by world_rank')
    return render(request, "view_all_company.html", {"companies": companies})



def applied_for_student(request):
    students = Student.objects.raw('select *from our_own_portal_student')
    applied = AppliedStudent.objects.raw('select *from our_own_portal_appliedstudent')
    companies = Company.objects.raw('select *from our_own_portal_company')
    return render(request, "applied_for_student.html", {"students": students, "applied": applied, "companies": companies})


def applied_for_company(request):
    students = Student.objects.raw('select *from our_own_portal_student')
    applied = AppliedStudent.objects.raw('select *from our_own_portal_appliedstudent')
    companies = Company.objects.raw('select *from our_own_portal_company')
    return render(request, "applied_for_company.html", {"students": students, "applied": applied, "companies": companies})


def applied_for_admin(request):
    students = Student.objects.raw('select *from our_own_portal_student')
    applied = AppliedStudent.objects.raw('select *from our_own_portal_appliedstudent')
    companies = Company.objects.raw('select *from our_own_portal_company')
    return render(request, "applied_for_admin.html", {"students": students, "applied": applied, "companies": companies})


def apply_for_job(request, id):
    jobs = Job.objects.get(id=id)
    students = Student.objects.raw('select *from our_own_portal_student')
    return render(request, "apply_for_job.html", {"jobs": jobs, "students": students})


def save_applied_job(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        cid = request.POST.get("cid")
        sid = request.POST.get("sid")
        position = request.POST.get("position")
#        company_id = Company.objects.get(company_id=cid)
#        student_id = Student.objects.get(student_id=sid)
        apply = AppliedStudent(company_id_id=cid, student_id_id=sid, position=position)
        apply.save()
        return HttpResponseRedirect("view_job_for_student")


def selected_for_company(request):
    students = Student.objects.raw('select *from our_own_portal_student')
    selected = SelectedStudent.objects.raw('select *from our_own_portal_selectedstudent')
    companies = Company.objects.raw('select *from our_own_portal_company')
    return render(request, "selected_for_company.html", {"students": students, "selected": selected, "companies": companies})


def selected_for_student(request):
    students = Student.objects.raw('select *from our_own_portal_student')
    selected = SelectedStudent.objects.raw('select *from our_own_portal_selectedstudent')
    companies = Company.objects.raw('select *from our_own_portal_company')
    return render(request, "selected_for_student.html", {"students": students, "selected": selected, "companies": companies})


def selected_for_admin(request):
    students = Student.objects.raw('select *from our_own_portal_student')
    selected = SelectedStudent.objects.raw('select *from our_own_portal_selectedstudent')
    companies = Company.objects.raw('select *from our_own_portal_company')
    return render(request, "selected_for_admin.html", {"students": students, "selected": selected, "companies": companies})


def select_student(request, id):
    apply = AppliedStudent.objects.get(id=id)
    apply.status = "selected"
    apply.save()
    cid = apply.company_id_id
    sid = apply.student_id_id
    company = Company.objects.get(company_id=cid)
    mode = company.mode
    position = apply.position
    select = SelectedStudent(mode=mode, position=position, student_id_id=sid, company_id_id=cid)
    select.save()
    return HttpResponseRedirect("/applied_for_company")


def reject_student(request, id):
    apply = AppliedStudent.objects.get(id=id)
    apply.status = "rejected"
    apply.save()
    return HttpResponseRedirect("/applied_for_company")


def logout_user(request):
    logout(request)
    return render(request, 'index.html')

def do_add_job(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        cid = request.POST.get("cid")
        position = request.POST.get("position")
        vacancy = request.POST.get("vacancy")
        level = request.POST.get("level")
        min_sal = request.POST.get("min_sal")
        avg_sal = request.POST.get("avg_sal")
        max_sal = request.POST.get("max_sal")
        skills = request.POST.get("skills")
        company_id = Company.objects.get(company_id=cid)
        job = Job(company_id=company_id, position=position, vacancy=vacancy, experience_level=level, min_salary_LPA=min_sal, avg_salary_LPA=avg_sal, max_salary_LPA=max_sal, required_skills=skills)
        job.save()
        messages.success(request, "Successfully added")
#        return HttpResponse("Successfully")
        return HttpResponseRedirect("company_base_page")


def do_login(request):
    if request.method != "POST":
        return HttpResponse("<h2>not allowed</h2>")
    else:
        user = authenticate(request, username=request.POST.get("user"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect("admin_base_page")
            if user.user_type == "2":
                return HttpResponseRedirect("student_base_page")
            if user.user_type == "3":
                return HttpResponseRedirect("company_base_page")
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("invalid_login")



def do_student_register(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        '''user = authenticate(request, username=request.POST.get("user"))'''
        '''register(request)'''
        try:
            username = "admin"
            first_name = request.POST.get("fname")
            last_name = request.POST.get("lname")
            username = request.POST.get("user")
            email = request.POST.get("email")
            password = request.POST.get("password")
            college_id = request.POST.get("college_id")
            clgname = request.POST.get("clgname")
            degree = request.POST.get("degree")
            cgpa = request.POST.get("cgpa")
            city = request.POST.get("city")
            state = request.POST.get("state")
            pincode = request.POST.get("pincode")
            contact = request.POST.get("contact")
            dob = request.POST.get("dob")
            gender = request.POST.get("gender")
            skills = request.POST.get("skills")
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.student.college_id = college_id
            user.student.college_name = clgname
            user.student.college_degree = degree
            user.student.cgpa = cgpa
            user.student.city = city
            user.student.state = state
            user.student.pin_code = pincode
            user.student.contact_no = contact
            user.student.gender = gender
            user.student.dob = dob
            user.student.skills = skills
            user.save()

            messages.success(request, "Successfully added")
            return render(request, 'loginform.html')
        except:
            messages.error(request, "Failed")
            return HttpResponseRedirect("studentform")


def do_company_register(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        username = "admin"
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        username = request.POST.get("user")
        email = request.POST.get("email")
        password = request.POST.get("password")
        company_name = request.POST.get("cname")
        sector = request.POST.get("sector")
        rank = request.POST.get("rank")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        contact = request.POST.get("contact")
        mode = request.POST.get("mode")
        holiday = request.POST.get("weekly_off")
        sick = request.POST.get("sick")
        hours = request.POST.get("hours")
        revenue = request.POST.get("revenue")

        user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
        user.company.company_name = company_name
        user.company.sector = sector
        user.company.world_rank = rank
        user.company.city = city
        user.company.state = state
        user.company.pin_code = pincode
        user.company.contact_no = contact
        user.company.mode = mode
        user.company.weekly_off = holiday
        user.company.sick_leaves = sick
        user.company.working_hours = hours
        user.company.revenue = revenue
        user.save()
        return render(request, 'loginform.html')


def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("user: "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")
