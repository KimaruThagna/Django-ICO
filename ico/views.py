from django.shortcuts import render

# Create your views here.


def bid_data(request):
    con = {}
    return render(request, 'ico/bid_data.html', context=con)


def user_data(request):
    con = {}
    return render(request, 'ico/user_data.html', context=con)