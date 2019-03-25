import os
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as u_login, logout as u_logout
from django.template.loader import get_template
from django.template import Context
from django.conf import settings as conf_settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.contrib.auth.forms import (
    PasswordChangeForm,
    AdminPasswordChangeForm)
from django.contrib import messages
from social_django.models import UserSocialAuth
from xhtml2pdf import pisa
from io import StringIO
from .forms import RegisterForm, UpdateForm, PasswordResetForm
from .models import Employee


def Information(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            object = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            object.set_password(password)
            object.save()
            profile = Employee()
            profile.user = object
            profile.Mobile_No = form.cleaned_data["Mobile_No"]
            profile.gender = form.cleaned_data["gender"]
            profile.Date_of_Birth = form.cleaned_data["Date_of_Birth"]
            profile.Address = form.cleaned_data["Address"]
            profile.Programming_Languages = form.cleaned_data["Programming_Languages"]
            profile.Country = form.cleaned_data["Country"]
            profile.Image = form.cleaned_data["Image"]
            if not profile.Image:
                profile.Image = 'media/default.jpg'
            profile.File = form.cleaned_data["File"]
            profile.save()
            messages.success(
                request, 'Your account has been created! You are now able to login')
            return HttpResponseRedirect('login')
    else:
        form = RegisterForm()
    return render(request, 'formapp/register.html', {'form': form})


def show(request):
    # employees = Employee.objects.all()
    employees = Employee.objects.order_by("-id").all()
    paginator = Paginator(employees, 6)

    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)
    return render(request, "formapp/show.html", {'employees': employees})


def view_profile(request, id):
    if id:
        employee = Employee.objects.get(user_id=id)
    else:
        employee = request.employee
    args = {'employee': employee}
    return render(request, 'formapp/home.html', args)


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active and user.is_superuser:
                u_login(request, user)
                if request.GET.get('next', None):
                    return redirect(request.GET.get['next'])
                return redirect('formapp:show')
            else:
                if user.is_active:
                    u_login(request, user)
                return redirect('formapp:home')
        else:
            return redirect('password_reset')
    else:
        return render(request, 'formapp/login.html', {})


def home(request):
    print(request.user)
    employee = Employee.objects.get(user_id=request.user.id)
    return render(request, 'formapp/home.html', {'employee': employee})


def logout(request):
    u_logout(request)
    return redirect('login')


def UpdateView(request, id):
    employee = get_object_or_404(Employee, user_id=request.user.id)
    data = {}
    data['email'] = employee.user.email
    data['gender'] = employee.gender
    data['Address'] = employee.Address
    data['Mobile_No'] = employee.Mobile_No
    data['Date_of_Birth'] = employee.Date_of_Birth
    data['Programming_Languages'] = employee.Programming_Languages
    data['Country'] = employee.Country

    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            employee.email = request.POST.get('email')
            employee.gender = request.POST.get('gender')
            employee.Address = request.POST.get('Address')
            employee.Mobile_No = request.POST.get('Mobile_No')
            employee.Date_of_Birth = request.POST.get('Date_of_Birth')
            employee.Programming_Languages = request.POST.get(
                'Programming_Languages')
            employee.Country = request.POST.get('Country')
            employee.save()
        return redirect('formapp:home')
    else:
        form = UpdateForm(initial=data)
    return render(request, 'formapp/update.html', {'form': form})


def delete(request, id):
    employee = get_object_or_404(User, id=id)
    employee.delete()
    return redirect('formapp:info')


def password_change_view(request, id):
    employee = get_object_or_404(User, id=id)
    data = {}
    data['password'] = employee.password
    if request.method == 'POST':
        form = PasswordResetForm(request.POST, instance=employee)
        if form.is_valid():
            object = form.save(commit=False)
            password = form.cleaned_data['password']
            object.set_password(password)
            object.save()
            # password = request.POST.get('password')
            # employee.set_password(password)
            # employee.save()
        return redirect('login')
        # return HttpResponse('home')
    else:
        form = PasswordResetForm(initial=data)
    return render(request, 'formapp/change_password.html', {'form': form})


def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
        employee, created = Employee.objects.get_or_create(
            user=github_login.user
        )
        print(employee.user_id)
    except UserSocialAuth.DoesNotExist:
        github_login = None

    can_disconnect = (user.social_auth.count() >
                      1 or user.has_usable_password())

    return render(request, 'formapp/settings.html', {
        'github_login': github_login,
        'can_disconnect': can_disconnect,
        'employee': employee
    })


def html_to_pdf_view(request, id):
    employee = Employee.objects.get(user_id=id)
    template_path = 'formapp/pdf.html'
    context = {'pagesize': 'A4',
               'employee': employee,
               }    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisaStatus = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def link_callback(uri, rel):
    path = os.path.join(conf_settings.MEDIA_ROOT,
                        uri.replace(conf_settings.MEDIA_URL, ""))
    return path


def csv_view(request, id):
    employee = Employee.objects.get(user_id=id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', employee.user.username])
    writer.writerow(['email', employee.user.email])
    writer.writerow(['Mobile_No', employee.Mobile_No])
    writer.writerow(['Date_of_Birth', employee.Date_of_Birth])
    writer.writerow(['Gender', employee.gender])
    writer.writerow(['Address', employee.Address])
    writer.writerow(['Country', employee.Country])
    writer.writerow(['Programming_Languages', employee.Programming_Languages])
    return response
