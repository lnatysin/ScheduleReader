from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Employee  # Import your Employee model

def index(request):
    employees = Employee.objects.all()
    return render(request, 'index.html', {'employees': employees})
