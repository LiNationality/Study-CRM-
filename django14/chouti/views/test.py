from django.shortcuts import render,redirect,HttpResponse


def Test(request):

    return render(request,'test.html')