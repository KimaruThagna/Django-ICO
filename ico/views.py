from django.shortcuts import render

# Create your views here.


def home(request):
    con = {}
    return render(request, 'ico/index.html', context=con)