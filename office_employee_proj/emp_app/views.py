from django.shortcuts import render, HttpResponse
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def all_emp(request):
    employees = Employee.objects.all()
    context = {'employees': employees}
    return render(request, 'view_all_emp.html', context)

def add_emp(request):
    if request.method == 'POST':
        try:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            salary = int(request.POST['salary'])
            bonus = int(request.POST['bonus'])
            phone = int(request.POST['phone'])
            dept = int(request.POST['dept'])
            role = int(request.POST['role'])

            new_emp = Employee(
                first_name=first_name,
                last_name=last_name,
                salary=salary,
                bonus=bonus,
                phone=phone,
                dept_id=dept,
                role_id=role,
                hire_date=datetime.now()
            )
            new_emp.save()
            return HttpResponse('Employee added Successfully')
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")

    return render(request, 'add_emp.html')

def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Successfully")
        except Employee.DoesNotExist:
            return HttpResponse("Please Enter A Valid EMP ID")

    employees = Employee.objects.all()
    context = {'employees': employees}
    return render(request, 'remove_emp.html', context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        dept = request.POST.get('dept', '')
        role = request.POST.get('role', '')

        employees = Employee.objects.all()

        if name:
            employees = employees.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            employees = employees.filter(dept__name__icontains=dept)
        if role:
            employees = employees.filter(role__name__icontains=role)

        context = {'employees': employees}
        return render(request, 'view_all_emp.html', context)

    return render(request, 'filter_emp.html')
