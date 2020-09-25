from django.shortcuts import render
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io
import requests

# Create your views here.

def accept(request):
    if request.method == "POST":
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        phone = request.POST.get("phone","")
        summary = request.POST.get("summary","")
        degree = request.POST.get("degree","")
        school = request.POST.get("school","")
        university = request.POST.get("university","")
        previous_work = request.POST.get("previous_work","")
        skills = request.POST.get("skills","")

        profile = Profile(name=name,email=email,phone=phone,summary=summary,
                          degree=degree,school=school, university=university, previous_work=previous_work, skills = skills)
        profile.save()
    return render(request,'cvpdf/accept.html')

def resume(request, id):
    path_wkhtmltopdf = r'D:\Software and Driver Installers\wkhtmltox-0.12.6-1.mxe-cross-win64\wkhtmltox\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    # pdfkit.from_url("http://google.com", "out.pdf", configuration=config)

    user_profile = Profile.objects.get(pk=id)
    template = loader.get_template('cvpdf/resume.html')
    html = template.render({'user_profile':user_profile})
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
    }

    pdf = pdfkit.from_string(html,False,options, configuration=config)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    filename = 'resume.pdf'

    return response

def list(request):
    profile = Profile.objects.all()
    return render(request,'cvpdf/list.html',{'profile':profile})




