# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import *

from  django.http import JsonResponse,HttpResponse
from django.db.models import Avg, Max, Min, Sum
from django.core.files.storage import FileSystemStorage
from django.core import serializers
from datetime import *
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import json
countqna=0
count1=0

# Create your views here.

def index(request):
    return render(request,'index.html',{})

def login(request):
    return render(request,'login.html',{})

##def signup(request):
##    return render(request,'register.html',{})


##
def logincheck(request):
    
    print("login check")
    username=request.POST.get("username")
    password=request.POST.get("password")
    print(username,password)
    if username=="admin" and password=="admin":
        return HttpResponse("<script>alert('Successfull Login');window.location.href='/adminhome/'</script>")
    else:
        print("else")
        obj=login_tb.objects.filter(username=username,password=password)
        objcount=obj.count()
        print(objcount)
        if objcount==1:
            
            obj1=login_tb.objects.get(username=username,password=password)
            role=obj1.role
            
            if role=="hod":
                obj2=login_tb.objects.get(username=username,password=password)
                request.session["lid"]=obj2.logid
                return HttpResponse("<script>alert('Successfull Login');window.location.href='/hodhome/'</script>")
            
            elif role=="faculty":
                obj2=login_tb.objects.get(username=username,password=password)
                request.session["lid"]=obj2.logid
                return HttpResponse("<script>alert('Successfull Login');window.location.href='/facultyhome/'</script>")
            
            elif role=="student":
                obj2=login_tb.objects.get(username=username,password=password)
                request.session["lid"]=obj2.logid
                return HttpResponse("<script>alert('Successfull Login');window.location.href='/studenthome/'</script>")

            elif role=="po":
                obj2=login_tb.objects.get(username=username,password=password)
                request.session["lid"]=obj2.logid
                return HttpResponse("<script>alert('Successfull Login');window.location.href='/pohome/'</script>")
            
            elif role=="co_worker":
                obj2=login_tb.objects.get(username=username,password=password)
                request.session["lid"]=obj2.logid
                return HttpResponse("<script>alert('Successfull Login');window.location.href='/co_work_home/'</script>")
                
            

            else:
                return HttpResponse("<script>alert('Invalid Login');window.location.href='/login/'</script>")
        else:
            return HttpResponse("<script>alert('Invalid Login');window.location.href='/login/'</script>")

################################################# ADMIN   ########################################################################################

def adminhome(request):
    
    return render(request,'adminhome.html',{})

     
       

def dept(request):

    return render(request,'adminadddeparment.html',{})

def add_dept(request):
    
    dept=request.POST.get("dept")
    print(dept)
    obj=dept_tb(dept_name=dept)
    obj.save()
    return HttpResponse("<script>alert('Added Successfully');window.location.href='/dept/'</script>")


## Add placement officers ##

def po(request):
    
    obj=dept_tb.objects.all()
    return render(request,'adminaddpo.html',{'dept':obj})

def addpo(request):
    name=request.POST.get("name")
    email=request.POST.get("email")
    username=request.POST.get("username")
    password=request.POST.get("password")
    address=request.POST.get("address")
    phone=request.POST.get("phone")
    gender=request.POST.get("gender")
    dept_id=request.POST.get("dept")
    objdept=dept_tb.objects.get(dept_id=int(dept_id))
    dept=objdept.dept_name
    print(name,email,username,password,address,phone,dept,type(dept),type(gender))
    
    role='po'
    obj=login_tb(username=username,password=password,role=role)
    obj.save()
    userid=login_tb.objects.all().aggregate(Max('logid'))
    logid=userid['logid__max']
    obj1=po_tb(name=name,email=email,username=username,password=password,address=address,phone=phone,gender=gender,logid=logid,dept_id=int(dept_id),dept_name=dept)
    obj1.save()
    return HttpResponse('<script>alert("Added Successfully");window.location.href="/po/"</script>')


def hod(request):
 
    obj=dept_tb.objects.all()
    return render(request,'adminaddhod.html',{'dept':obj})
    

def addhod(request):
    
    name=request.POST.get("name")
    email=request.POST.get("email")
    username=request.POST.get("username")
    password=request.POST.get("password")
    address=request.POST.get("address")
    phone=request.POST.get("phone")
    dept=request.POST.get("department")
    gender=request.POST.get("gender")
    print(name,email,username,password,address,phone,dept,type(dept),type(gender))
    objdept=dept_tb.objects.get(dept_id=int(dept))
    name1=objdept.dept_name
    role='hod'
    obj=login_tb(username=username,password=password,role=role)
    obj.save()
    userid=login_tb.objects.all().aggregate(Max('logid'))
    logid=userid['logid__max']
    obj1=hod_tb(name=name,email=email,username=username,password=password,address=address,phone=phone,dept=name1,gender=gender,logid=logid,dept_id=int(dept))
    obj1.save()
    return HttpResponse('<script>alert("Added Successfully");window.location.href="/hod/"</script>')

######################################### HOD ##############################################################################################################

def hodhome(request):
    return render(request,'hodhome.html',{})

def teacher(request):
    logid=request.session["lid"]
    obj=hod_tb.objects.get(logid=logid)
    return render(request,'hodaddteacher.html',{'dept':obj})

def addteacher(request):
    
    name=request.POST.get("name")
    email=request.POST.get("email")
    username=request.POST.get("username")
    password=request.POST.get("password")
    address=request.POST.get("address")
    phone=request.POST.get("phone")
    dept=request.POST.get("department")
    gender=request.POST.get("gender")
    print(name,email,username,password,address,phone,dept,type(dept),type(gender))
    objdept=dept_tb.objects.get(dept_id=int(dept))
    name1=objdept.dept_name
    role='faculty'
    obj=login_tb(username=username,password=password,role=role)
    obj.save()
    userid=login_tb.objects.all().aggregate(Max('logid'))
    logid=userid['logid__max']
    obj1=faculty_tb(name=name,email=email,username=username,password=password,address=address,phone=phone,dept=name1,gender=gender,logid=logid,dept_id=dept)
    obj1.save()
    return HttpResponse('<script>alert("Added Successfully");window.location.href="/teacher/"</script>')


def sem(request):
    
    return render(request,'hodaddsem.html',{})

def add_sem(request):
    sem=request.POST.get("sem")
   
    obj1=sem_tb(sem=sem)
    obj1.save()
    return HttpResponse('<script>alert("Added Successfully");window.location.href="/sem/"</script>')

def class_teacher(request):
    
    obj=sem_tb.objects.all()
    obj2=faculty_tb.objects.all()
    return render(request,'hodassignclassteacher.html',{'sem':obj,'faculty':obj2})


def assign_faculty(request):
    logid=request.session["lid"]
    sem_id=request.POST.get("sem")
    fac_id=request.POST.get("faculty")
    sem=sem_tb.objects.get(sem_id=sem_id)
    facu=faculty_tb.objects.get(logid=fac_id)
    stype=request.POST.get("stype")
    sem_name=sem.sem
    fac_name=facu.name
    print(sem_id,fac_id,sem_name,fac_name)
    try:
        if stype=="Incharge":
            semobj=class_assign_tb.objects.filter(sem_id=int(sem_id))
            count=semobj.count()
            if count>2:
                return HttpResponse('<script>alert("Already Incharge  Assigned");window.location.href="/class_teacher/"</script>')
            else:
                
                obj=class_assign_tb(logid=logid,teach_id=fac_id,teach_name=fac_name,sem_id=sem_id,sem_name=sem_name,stype=stype)
                obj.save()
                return HttpResponse('<script>alert("Faculty Assigned Successfully");window.location.href="/class_teacher/"</script>')
        else:
             obj=class_assign_tb(logid=logid,teach_id=fac_id,teach_name=fac_name,sem_id=sem_id,sem_name=sem_name,stype=stype)
             obj.save()
             return HttpResponse('<script>alert("Faculty Assigned Successfully");window.location.href="/class_teacher/"</script>')
       
    except Exception as err:
        return HttpResponse('<script>alert("Faculty Assigned Successfully");window.location.href="/class_teacher/"</script>')


#####################################################   Faculty #############################################################

def facultyhome(request):
    return render(request,'facultyhome.html',{})


def add_stud_page(request):
    logid=request.session["lid"]
    obj=faculty_tb.objects.get(logid=logid)
    return render(request,'register.html',{'dept':obj})

def add_stud(request):
    print("sign up")
    student_name=request.POST.get("name")
    student_email=request.POST.get("email")
    username=request.POST.get("username")
    password=request.POST.get("password")
    student_phone=request.POST.get("phone")
    student_dob=request.POST.get("dob")
    student_address=request.POST.get("address")
    student_gender=request.POST.get("gender")
    dept_id=request.POST.get("dept")
    guardian_name=request.POST.get("guardian_name")
    guardian_number=request.POST.get("guardian_number")
    guardian_email=request.POST.get("guardian_email")
    role='student'
    teac=request.session["lid"]
    print(student_name,student_email,username,password,student_phone,student_dob,student_address,student_gender,guardian_name,guardian_number,guardian_email)
    obj=login_tb(username=username,password=password,role=role)
    obj.save()
    userid=login_tb.objects.all().aggregate(Max('logid'))
    logid=userid['logid__max']
    print(logid)
    obj1=reg_tb(student_name=student_name,student_email=student_email,username=username,password=password,student_phone=student_phone,student_dob=student_dob,student_address=student_address,student_gender=student_gender,guardian_name=guardian_name,guardian_number=guardian_number,guardian_email=guardian_email,logid=logid,role=role,dept_id=int(dept_id),teach_id=teac)
    obj1.save()    
    return HttpResponse("<script>alert('Successfull Registration');window.location.href='/add_stud_page/'</script>")

def view_stud_page(request):
    uid=request.session["lid"]
    print("uid",uid)
    obj=reg_tb.objects.filter(teach_id=uid)
    print(obj)
    return render(request,'faculty_view_students.html',{'stud':obj})


def subject_page(request):
    obj=sem_tb.objects.all()
    return render(request,'facultyaddsubjects.html',{'sem':obj})

def add_subject_page(request):
    sub=request.POST.get("sub")
    sem_id=request.POST.get("sem")
    objsem=sem_tb.objects.get(sem_id=int(sem_id))
    sem=objsem.sem
    lid=request.session["lid"]
    print("lid",lid)
    try:
        deptobj=faculty_tb.objects.get(logid=lid)
        dept_name=deptobj.dept
        dept_id=deptobj.dept_id
        fac_name=deptobj.name
        print(sub,sem_id)
        obj=subject_tb(subject=sub,dept_id=dept_id,dept_name=dept_name,teach_id=lid,sem_id=sem_id,sem=sem,faculty_name=fac_name)
        obj.save()
        return HttpResponse("<script>alert('Added Successfully');window.location.href='/subject_page/'</script>")

    except Exception as err:
        print("error",err)
        return HttpResponse("<script>alert('Operation Fails; Try Again');window.location.href='/subject_page/'</script>")


## Assign Subjects To faculty

def subject_assign_page(request):
    lid=request.session["lid"]
    obj=sem_tb.objects.all()
    obj1=faculty_tb.objects.all()
    obj2=subject_tb.objects.filter(teach_id=lid)
    return render(request,'assign_faculty.html',{'sem':obj,'fac':obj1,'sub':obj2})

def subject_assign(request):
    sem_id=request.POST.get("sem")
    faculty_id=request.POST.get("faculty")
    sub_id=request.POST.get("sub")
    objsem=sem_tb.objects.get(sem_id=int(sem_id))
    objfac=faculty_tb.objects.get(logid=int(faculty_id))
    objsub=subject_tb.objects.get(sub_id=int(sub_id))
    sem=objsem.sem
    faculty_assigned=objfac.name
    sub=objsub.subject
    lid=request.session["lid"]
    objfaculty=faculty_tb.objects.get(logid=lid)
    faculty_name=objfaculty.name
    print(sem_id,faculty_id,sub_id)
    print(sem,faculty_assigned,sub)
    print(lid,faculty_name)
    obj=subject_assign_tb(logid=lid,faculty_name=faculty_name,sub_id=int(sub_id),subject=sub,sem_id=int(sem_id),sem=sem,assign_teach_id=int(faculty_id),assign_faculty=faculty_assigned)
    obj.save()
    return HttpResponse("<script>alert('Assigned Successfully');window.location.href='/subject_assign_page/'</script>")

 ## Assign Work to student

def assign_work_page(request):
    sub=subject_tb.objects.all()
    dept=dept_tb.objects.all()
    return render(request,'faculty_assign_work.html',{'sub':sub,'dept':dept})

def add_assign_work_page(request):
    lid=request.session["lid"]
    objfac=faculty_tb.objects.get(logid=lid)
    fac_name=objfac.name
    print(lid,fac_name)
    sub_id=request.POST.get("subject")
    topic=request.POST.get("topic")
    print(sub_id)
    status="Not Submitted"
    objsub=subject_tb.objects.get(sub_id=int(sub_id))
    subject=objsub.subject
    assign_date=request.POST.get("assign_date")
    submit_date=request.POST.get("submit_date")
    work=request.POST.get("work")
    dept_id=request.POST.get("dept")
    worktype=request.POST.get("work_type")
    objdept=dept_tb.objects.get(dept_id=int(dept_id))
    dept_name=objdept.dept_name
    print("values",subject,assign_date,submit_date,work,dept_id,dept_name)
    obj=assign_work_tb(sub_id=sub_id,subject=subject,work=work,assigned_date=assign_date,submit_date=submit_date,dept_id=int(dept_id),
                       dept_name=dept_name,logid=lid,faculty_name=fac_name,work_type=worktype,topic=topic,status=status)
    obj.save()
    return HttpResponse("<script>alert('Assigned Successfully');window.location.href='/assign_work_page/'</script>")

## Dispaly Dept

def dis_dept(request):
    print("dis_dept")
    dept_id=request.GET.get("id")
    print(dept_id)
    data={}
    obj=subject_tb.objects.filter(dept_id=int(dept_id))
    print(obj)
    if obj:
        value=serializers.serialize("json",obj)
        data['sub1']=json.loads(value)
        print("dataaa",data)
        return JsonResponse(data,safe=False)
    else:
        print("else")
        return HttpResponse("No Data")

##view students work ###

def view_students_works(request):
    lid=request.session["lid"]
    obj=stud_work_tb.objects.filter(teach_logid=lid)
    return render(request,'faculty_view_stuents_work.html',{'stud':obj})


### Assign mark to students ###

def studt_assign_mark(request):
    
    lid=request.session["lid"]
    
    stud_wrk__id=request.GET.get("id")
    mark=request.GET.get("mark")
    about_wrk=request.GET.get("about")
    print(stud_wrk__id,mark,about_wrk)
    try:
        objfac=faculty_tb.objects.get(logid=lid)
        fac=objfac.name
        dept_name=objfac.dept
        obj=stud_work_tb.objects.get(student_wk_id=int(stud_wrk__id))
        work=obj.work
        logid=obj.logid
        subject=obj.subject
        submit_date=obj.submit_date
        objsave=stud_wrk_mark_tb(logid=logid,work=work,subject=subject,submit_date=submit_date,mark=mark,about=about_wrk,teach_logid=lid,faculty_name=fac,dept_name=dept_name)
        objsave.save()
        status="Mark Added"
        objmark=stud_work_tb.objects.get(student_wk_id=int(stud_wrk__id))
        objmark.mark_status=status
        objmark.mark=mark
        objmark.about=about_wrk
        objmark.save()
        
        return HttpResponse("Added Successfully")
    except Exception as err:
        print("error",err)
        return HttpResponse("Error Occured")


def offline_work(request):
    print("offline  work")
    lid=request.session["lid"]
    print("logid",lid)
    try:
        
        work_type="Offline"
        obj=assign_work_tb.objects.filter(logid=lid,work_type=work_type)
        print("object",obj)
        return render(request,'offline_work.html',{'work':obj})
    except Exception as err:
        print("error",err)
        return HttpResponse('<script>alert("Error Occured");window.location.href="/facultyhome/"</script>')

def send_mail(request):
    try:
        id1=request.GET.get("id")
        print("id valueeeeee",id1)
        obj=assign_work_tb.objects.get(ass_work_id=int(id1))
        dept_id=obj.dept_id
        print("department",dept_id)
        l=[]
        objstud=reg_tb.objects.filter(dept_id=dept_id)
        for i in objstud:
            l.append(i.student_email)
        print("student emailllll",l)
        message="Dear Students, you are assigned a "+obj.work+" work on the subject "+obj.subject+". The submit date will be "+obj.submit_date+ " By, "+obj.faculty_name
        print("message",message)
        for j in l:
            print("email",j)
            email = EmailMessage('Work Assigned', message, to=[j])
            email.send()
        return HttpResponse("Sended Successfully")
    except Exception as err:
        print("exceptiio",err)
        return HttpResponse("Error Occured")
        

    

########################################################## Student ###########################################

def studenthome(request):
    return render(request,'studenthome.html',{})

def stud_work_assign_page(request):
    print("assign page")
    lid=request.session["lid"]
    print("logid",lid)
    try:
        dept=reg_tb.objects.get(logid=lid)
        dept_id=dept.dept_id
        print("dept_id",dept_id)
        work_type="Online"
        obj=assign_work_tb.objects.filter(dept_id=dept_id,work_type=work_type)
        print("object",obj)
        return render(request,'stud_view_assignedwork.html',{'work':obj})
    except:
        return HttpResponse('<script>alert("No Works are assigned");window.location.href="/studenthome/"</script>')

def stud_feedback_page(request):
    return render(request,'student_feedback.html',{})


def stud_add_feedback(request):
    feedback=request.POST.get("feedback")
    lid=request.session["lid"]
    obj=reg_tb.objects.get(logid=lid)
    student_name=obj.student_name
    print(feedback,lid,student_name)
    objsave=feedback_tb(feedback=feedback,logid=lid,student_name=student_name)
    objsave.save()
    return HttpResponse("<script>alert('Thanks For Your Feedback');window.location.href='/stud_feedback_page/'</script>")

def idea_page(request):
    return render(request,'stud_idea.html',{})

def stud_add_idea(request):
    idea=request.POST.get("idea")
    lid=request.session["lid"]
    obj=reg_tb.objects.get(logid=lid)
    student_name=obj.student_name
    print(idea,lid,student_name)
    objsave=idea_tb(idea=idea,logid=lid,student_name=student_name)
    objsave.save()
    return HttpResponse("<script>alert('Thanks For Your Valuable Idea');window.location.href='/idea_page/'</script>")

#####  Aptitude ###########

def stud_aptitude_page(request):
    return render(request,'stud_add_aptitude_question.html',{})

### Add Aptitude Question ###

def stud_add_aptitude_ques(request):
    question=request.POST.get("question")
    answer=request.POST.get("answer")
    print(answer,question)
    lid=request.session["lid"]
    obj=stud_aptitude_tb(stud_ques=question,stud_answer=answer,logid=lid)
    obj.save()
    return HttpResponse("<script>alert('Thanks For Your Contribution');window.location.href='/stud_aptitude_page/'</script>")

#### Online Exam ####

def online_exam_page(request):
    print("online eaxm page")
    
    return render(request,'stud_online_exam.html',{})

def exam1(request):
    print("exam")
    data={}
    obj=po_aptitude_tb.objects.all().order_by('apt_id')[:10]
##    print(obj)
    if obj:
        value=serializers.serialize("json",obj)
        data['sub']=json.loads(value)
##        print("dataaa",data)
        return JsonResponse(data,safe=False)
    else:
        return HttpResponse("No Data")
    return HttpResponse("Success")


def answer1_exam(request):
    m=[]
    global count1
    global countqna
    print("EXAM ANSWERRRRRRRRR")
    qn1=request.GET.get("qn1")
    qn2=request.GET.get("qn2")
    qn3=request.GET.get("qn3")
    qn4=request.GET.get("qn4")
    qn5=request.GET.get("qn5")
    qn6=request.GET.get("qn6")
    qn7=request.GET.get("qn7")
    qn8=request.GET.get("qn8")
    qn9=request.GET.get("qn9")
    qn10=request.GET.get("qn10")
##    print("qqqqqqqqqqqqqqqqnnnnnnnnnnnnnn",qn1,qn2,qn3,qn4,qn5,qn6,qn7,qn8,qn9,qn10)
    ans1=request.GET.get("ans1")
    ans2=request.GET.get("ans2")
    ans3=request.GET.get("ans3")
    ans4=request.GET.get("ans4")
    ans5=request.GET.get("ans5")
    ans6=request.GET.get("ans6")
    ans7=request.GET.get("ans7")
    ans8=request.GET.get("ans8")
    ans9=request.GET.get("ans9")
    ans10=request.GET.get("ans10")
    print("ans1111111111",ans1)
    if ans1=="" or ans2=="" or ans3=="" or ans4=="" or ans5=="" or ans6=="" or ans7=="" or ans8=="" or ans9=="" or ans10=="":
        return HttpResponse("Attend all the questions")
    else:

        m.append(ans1.lower())
        m.append(ans2.lower())
        m.append(ans3.lower())
        m.append(ans4.lower())
        m.append(ans5.lower())
        m.append(ans6.lower())
        m.append(ans7.lower())
        m.append(ans8.lower())
        m.append(ans9.lower())
        m.append(ans10.lower())
        print("lowerrrrrrrr",ans1.lower())
        
    ##    print("answerrrrrrrrrrrrrrrrrrrrr",ans1,ans2,ans3,ans4,ans5,ans6,ans7,ans8,ans9,ans10)

        obj=po_aptitude_tb.objects.all().order_by('apt_id')[:10]
        l=[]
        
        for i in obj:
            l.append(i.po_answer)
        
        
    ##    print("listtttttt",l)
        
        setl=set(l)
        setm=set(m)
    ##    print("setl",setl,"setm",setm)
        if (setl & setm):
            print("ok")
            setlm=setl & setm
    ##        print("lmmmmmm",setlm)
            listlm=list(setlm)
            countqna=len(listlm)
            print("countssssss",countqna)
            return HttpResponse("Submitted Successfully")
        else:
            countqna=0
            
            print("countqnaaaaaa",countqna)
            return HttpResponse("Submitted Successfully")


def mark_assessment(request):
    global countqna
    print("count value`",countqna)
    countqna1="You Got "+str(countqna)
    return HttpResponse(countqna1)

def updl_assign(request):
    print("work assign detail")

    id1=request.GET.get("id")
    print("idddddddddddddddddddd",id1)
    obj=assign_work_tb.objects.filter(ass_work_id=int(id1))
    data1={}
    
    print("objjjjjjjjjjjjjjjjjjjjjjjjj",obj)
    if obj:
        value=serializers.serialize("json",obj)
        data1['sub']=json.loads(value)
        print("dataaa",data1)
        return JsonResponse(data1,safe=False)
    else:
        print("else")
        return HttpResponse("No Data")


def uploaded_wk(request):
    print("uploaded work")

    if request.method=="POST":
        status="Submitted"

        lid=request.session["lid"]
      
        assign_id=request.POST.get("assign_id")
        mywork=request.POST.get("mywork")
        
        if request.FILES["myfile"]=="None":
            return HttpResponse("<script>alert('no files');window.location.href='studenthome'</script>")
        else:
            
            myfile=request.FILES["myfile"]
            print(assign_id,mywork,myfile,"haiiiiii")
            fs=FileSystemStorage("college_app/static/works")
            try:
                obj=assign_work_tb.objects.get(ass_work_id=int(assign_id))
                subject=obj.subject
                work=obj.work
                assigned_date=obj.assigned_date
                submit_date=obj.submit_date
                dept_id=obj.dept_id
                dept_name=obj.dept_name
                teach_logid=obj.logid
               
                print(subject,work,assigned_date,submit_date,dept_id,dept_name,teach_logid)
                m=datetime.today()
                s=m.strftime("%Y-%m-%d")
                if s>submit_date:
                    return HttpResponse("<script>alert('Submit Date Exceeded. Unable to submit');window.location.href='studenthome'</script>")
                else:
                    if obj.status=="Not Submitted":
                        obj.status=status
                        obj.save()
                        objinfo=reg_tb.objects.get(logid=int(lid))
                        student_name=objinfo.student_name
                        print(student_name)
                        fs.save(myfile.name,myfile)
                        mark="Need to Add Mark"
                        mark1='0'
                        about="About work"
                        objsave=stud_work_tb(student_name=student_name,logid=lid,ass_work_id=assign_id,subject=subject,work=work,submit_date=s,dept_id=dept_id,dept_name=dept_name,teach_logid=teach_logid,text=mywork,ufile=myfile,mark_status=mark,mark=mark1,about=about)
                        objsave.save()
                        return HttpResponse("<script>alert('Uploaded');window.location.href='studenthome'</script>")
                    else:
                        return HttpResponse("<script>alert('Alredy Submitted');window.location.href='studenthome'</script>")
            except Exception as err:
                print(err)
                return HttpResponse("<script>alert('Error occured');window.location.href='studenthome'</script>")

    else:
       
        return render(request,'studenthome.html',{})

def view_assess1(request):
    print("view_assess1")
    data={}
    obj=po_aptitude_tb.objects.all().order_by('apt_id')[:10]
##    print(obj)
    if obj:
        value=serializers.serialize("json",obj)
        data['sub']=json.loads(value)
##        print("dataaa",data)
        return JsonResponse(data,safe=False)
    else:
        return HttpResponse("No Data")
    return HttpResponse("Success")



#####################    Exam Test 2   ############


def exam2(request):

    print("`13411")
    data={}
    obj=po_aptitude_tb.objects.all().order_by('apt_id')[10:20]
    print(obj)
    
    if obj:
        value=serializers.serialize("json",obj)
        data['sub']=json.loads(value)
##        print("dataaa",data)
        return JsonResponse(data,safe=False)
    else:
        return HttpResponse("No Data")
    return HttpResponse("Success")


def answer2_exam(request):
    global count1
    m1=[]
    global countqna
    print("EXAM ANSWERRRRRRRRR")
    qn1=request.GET.get("qn12")
    qn2=request.GET.get("qn22")
    qn3=request.GET.get("qn32")
    qn4=request.GET.get("qn42")
    qn5=request.GET.get("qn52")
    qn6=request.GET.get("qn62")
    qn7=request.GET.get("qn72")
    qn8=request.GET.get("qn82")
    qn9=request.GET.get("qn92")
    qn10=request.GET.get("qn102")
##    print("qqqqqqqqqqqqqqqqnnnnnnnnnnnnnn",qn1,qn2,qn3,qn4,qn5,qn6,qn7,qn8,qn9,qn10)
    ans1=request.GET.get("ans12")
    ans2=request.GET.get("ans22")
    ans3=request.GET.get("ans32")
    ans4=request.GET.get("ans42")
    ans5=request.GET.get("ans52")
    ans6=request.GET.get("ans62")
    ans7=request.GET.get("ans72")
    ans8=request.GET.get("ans82")
    ans9=request.GET.get("ans92")
    ans10=request.GET.get("ans102")

    m1.append(ans1)
    m1.append(ans2)
    m1.append(ans3)
    m1.append(ans4)
    m1.append(ans5)
    m1.append(ans6)
    m1.append(ans7)
    m1.append(ans8)
    m1.append(ans9)
    m1.append(ans10)
    
##    print("answerrrrrrrrrrrrrrrrrrrrr",ans1,ans2,ans3,ans4,ans5,ans6,ans7,ans8,ans9,ans10)

    obj=po_aptitude_tb.objects.all().order_by('apt_id')[10:20]
    l1=[]
    
    for i in obj:
        l1.append(i.po_answer)
    
    
##    print("listtttttt",l)
    
    setl1=set(l1)
    setm1=set(m1)
##    print("setl",setl,"setm",setm)
    if (setl1 & setm1):
        print("ok")
        setlm=setl1 & setm1
##        print("lmmmmmm",setlm)
        listlm=list(setlm)
        count1=len(listlm)
        print("countssssss",count1)
        return HttpResponse("Submitted Successfully")
    else:
        count1=0
        
        print("countqnaaaaaa",count1)
        return HttpResponse("Submitted Successfully")


def mark_assessment1(request):

    global count1
    print("Assesment %%%%%%%%%%%%%%%%%%",count1)
    count1="You Got "+str(count1)
    return HttpResponse(count1)


def view_assess2(request):
    print("view_assess1")
    data={}
    obj=po_aptitude_tb.objects.all().order_by('apt_id')[10:20]
##    print(obj)
    if obj:
        value=serializers.serialize("json",obj)
        data['sub']=json.loads(value)
##        print("dataaa",data)
        return JsonResponse(data,safe=False)
    else:
        return HttpResponse("No Data")
    return HttpResponse("Success")


### View Marks #####

def view_their_mark(request):
    lid=request.session["lid"]
    obj=stud_wrk_mark_tb.objects.filter(logid=lid)
    return render(request,'student_view_mark.html',{'stud':obj})




 
##################### Placement Officer ##########################################

def pohome(request):
    return render(request,'pohome.html',{})

def co_worker_page(request):
    lid=request.session["lid"]
    print("%%%%%%%%logid %%%",lid)
    try:
        obj=po_tb.objects.get(logid=lid)
        return render(request,'po_add_co_worker.html',{'dept':obj})
    except Exception as err:
        print("error occured",err)
        return HttpResponse('<script>alert("Error Occured");window.location.href="/pohome/"</script>')

def po_add_co_worker(request):
    logid=request.session["lid"]
    name=request.POST.get("name")
    email=request.POST.get("email")
    username=request.POST.get("username")
    password=request.POST.get("password")
    address=request.POST.get("address")
    phone=request.POST.get("phone")
    gender=request.POST.get("gender")
    dept_id=request.POST.get("dept")
    objdept=dept_tb.objects.get(dept_id=int(dept_id))
    dept=objdept.dept_name
    print(name,email,username,password,address,phone,dept,type(dept),type(gender))
    
    role='co_worker'
    obj=login_tb(username=username,password=password,role=role)
    obj.save()
    userid=login_tb.objects.all().aggregate(Max('logid'))
    co_logid=userid['logid__max']
    obj1=po_coworker_tb(name=name,email=email,username=username,password=password,address=address,phone=phone,gender=gender,co_logid=co_logid,dept_id=int(dept_id),dept_name=dept,logid=logid)
    obj1.save()
    return HttpResponse('<script>alert("Added Successfully");window.location.href="/co_worker_page/"</script>')

### Add Aptitude Question #####

def po_question_answ(request):
    return render(request,'po_add_aptitude_question.html',{})

def po_add_question_answ(request):
    question=request.POST.get("question")
    answer=request.POST.get("answer")
    option1=request.POST.get("option1")
    option2=request.POST.get("option2")
    print(answer,question)
    lid=request.session["lid"]
    obj=po_aptitude_tb(po_ques=question,po_answer=answer.lower(),logid=lid,option1=option1.lower(),option2=option2.lower())
    obj.save()
    return HttpResponse("<script>alert('Added Successfully');window.location.href='/po_question_answ/'</script>")

#### View students added aptitude question ####

def view_stud_add_apt_question_page(request):
    obj=stud_aptitude_tb.objects.all()
    return render(request,'po_view_stud_aptques.html',{'quest':obj})


######### Teacher #######

def teacher_notes(request):
    obj=dept_tb.objects.all()
    objsem=sem_tb.objects.all()
    return render(request,'addnotes.html',{'dept':obj,'sem':objsem})


def add_notes(request):
    dept_id=request.POST.get("dept")
    subject_id=request.POST.get("subject")
    links=request.POST.get("link")
    sem=request.POST.get("sem")
    objsem=sem_tb.objects.get(sem_id=int(sem))
    semdata=objsem.sem
    print("*********sem*********",semdata)
    print("subject id",subject_id,"dept_id",dept_id)
    myfile=request.FILES["notes"]
    fs=FileSystemStorage("college_app/static/notes")
    fs.save(myfile.name,myfile)
    objdept=dept_tb.objects.get(dept_id=int(dept_id))
    objsubject=subject_tb.objects.get(sub_id=int(subject_id))
    dept=objdept.dept_name
    subject=objsubject.subject
    lid=request.session["lid"]
    logid=faculty_tb.objects.get(logid=lid)
    faculty_name=logid.name
    obj=note_tb(dept_id=int(dept_id),subject=subject,dept_name=dept,notes=myfile,logid=lid,faculty_name=faculty_name,links=links,sem_id=int(sem),sem=semdata)
    obj.save()
    return HttpResponse('<script>alert("Added Successfully");window.location.href="/teacher_notes/"</script>')



def fac_view_note(request):
    lid=request.session["lid"]
    obj=note_tb.objects.filter(logid=lid)
    return render(request,'teacher_view_notes.html',{'data':obj})
    
######## Student #########
def view_notes(request):
    lid=request.session["lid"]
    obj=reg_tb.objects.get(logid=lid)
    dept=obj.dept_id
    print("depatment_id",dept)
    obj1=note_tb.objects.filter(dept_id=dept)
    print("obj111111111111111111",obj1)
    return render(request,'student_view_notes.html',{'data':obj1})


###########    Co Worker      ###############################################################################################################


def co_work_home(request):
    return render(request,'co_worker.html',{})


def co_worker_view_stud_apt(request):
    obj=stud_aptitude_tb.objects.all()
    return render(request,'co_worker_view_stud_apt.html',{'quest':obj})
    

####################    UPDATION   ######################################################

## Admin View Feedback
def ad_vw_feedback(request):
    print("admin view feedback")
    obj=feedback_tb.objects.all()
    print("####################",obj)
    return render(request,'admin_view_feedback.html',{'data':obj})

##Admin View Idea

def vw_idea(request):
    obj=idea_tb.objects.all()
    return render(request,'admin_view_idea.html',{'data':obj})


###### User changing Username And Password #############


def profile(request):
    lid=request.session["lid"]
    obj=reg_tb.objects.get(logid=lid)
    
    return render(request,'stud_profile.html',{'data':obj})


def update_prfle(request):
    lid=request.session["lid"]
    username=request.POST.get("username")
    password=request.POST.get("password")
    print("username",username,"password",password)
    obj=reg_tb.objects.get(logid=lid)
    obj.username=username
    obj.password=password
    obj1=login_tb.objects.get(logid=lid)
    obj1.username=username
    obj1.password=password
    obj.save()
    obj1.save()
    return render(request,'studenthome.html',{})





    
