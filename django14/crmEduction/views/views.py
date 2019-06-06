from django.shortcuts import render

# Create your views here.

def index(request):
    roles = request.user.userprofiles.roles.all()
    menu_list = []
    for role in request.user.userprofiles.roles.all():
        for menu in role.memus.all():
            print(menu.name)
            print(menu.url_name)
            menu_list.append(menu)
    return render(request,'index.html',{'roles':roles,'menu_list':menu_list,})
def customer_list(request):
    roles=request.user.userprofiles.roles.all()
    menu_list=[]
    for role in request.user.userprofiles.roles.all():
        for menu in role.memus.all():
            print(menu.name)
            print(menu.url_name)
            menu_list.append(menu)
    # print(request.user.userprofiles.roles.all())
    return render(request, 'sales/customer.html',{'roles':roles,'menu_list':menu_list,})