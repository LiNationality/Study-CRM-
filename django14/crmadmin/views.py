from django.shortcuts import render,redirect
import importlib
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from crmadmin.utils import table_filter,table_search,table_short
# Create your views here.
from crmadmin import crmadmin
from crmEduction import models
from crmadmin.forms import create_model_form

def index(request):
    # for i in range(20):
    #     j=1
    #     models.Customers.objects.create(
    #         name=40015000+j,qq=165040900+j,qq_name="ahaid_"+str(j),
    #         phont=15939001000+j,source=1,status=0,referral_from=4251330000+j,
    #         consult_course=2,content="python自学",consultant=0,
    #         memo="python之路",tag=None
    #     )
    # print(crmadmin.enabled_admins["crmEduction"]["customers"].model)
    # print(crmadmin.enabled_admins)
    # for app_name,app_tables in crmadmin.enabled_admins.items():
    #     print(app_name)
    #     for table_name,admin in app_tables.items():
    #         print(table_name,admin)
    return render(request,'crmadmin/table_index.html',{'table_list':crmadmin.enabled_admins})

def display_table_objs(request,app_name,table_name):

    # print("-->",app_name,table_name)
    #models_module = importlib.import_module('%s.models'%(app_name))
    #model_obj = getattr(models_module,table_name)
    admin_class = crmadmin.enabled_admins[app_name][table_name]
    #admin_class = king_admin.enabled_admins[crm][userprofile]

    #object_list = admin_class.model.objects.all()
    object_list,filter_condtions = table_filter(request,admin_class) #过滤后的结果

    object_list = table_search(request,admin_class,object_list)


    object_list,orderby_key = table_short(request, admin_class, object_list) #排序后的结果
    print("orderby key ", orderby_key)
    paginator = Paginator(object_list, admin_class.list_per_page) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        query_sets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        query_sets = paginator.page(paginator.num_pages)

    return render(request,"crmadmin/table_objs.html",{"admin_class":admin_class,
                                                        "query_sets":query_sets,
                                                        "filter_condtions":filter_condtions,
                                                        "orderby_key":orderby_key,
                                                        "previous_orderby": request.GET.get("o",''),
                                                        "search_text":request.GET.get('_q','')})

def table_objs_change(request,app_name,table_name,obj_id):
    admin_class = crmadmin.enabled_admins[app_name][table_name]
    models_form_class=create_model_form(request,admin_class)
    print(admin_class.filter_horizontal)
    obj = admin_class.model.objects.get(id=obj_id)

    if request.method=="POST":
        form_obj=models_form_class(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()


    form_obj=models_form_class(instance=obj)

    return render(request,'crmadmin/table_objs_change.html',
                  {'form_obj':form_obj,
                   'admin_class':admin_class,
                   'app_name':app_name,
                   'table_name':table_name})

def table_objs_add(request,app_name,table_name):
    admin_class = crmadmin.enabled_admins[app_name][table_name]
    models_form_class = create_model_form(request, admin_class)

    # obj = admin_class.model.objects.get(id=obj_id)

    if request.method == "POST":
        form_obj = models_form_class(request.POST)
        if form_obj.is_valid():
            form_obj.save()

            return redirect(request.path.replace("/add/",'/'))
        else:
            form_obj=models_form_class()

    form_obj = models_form_class()

    return render(request, 'crmadmin/table_objs_add.html',
                  {'form_obj': form_obj,
                   'admin_class':admin_class})

def table_obj_delete(request,app_name,table_name,obj_id):
    admin_class = crmadmin.enabled_admins[app_name][table_name]

    obj = admin_class.model.objects.get(id=obj_id)
    if  admin_class.readonly_table:
        errors = {"readonly_table": "table is readonly ,obj [%s] cannot be deleted" % obj}
    else:
        errors = {}
    if request.method == "POST":
        if not admin_class.readonly_table:
            obj.delete()
            return redirect("/king_admin/%s/%s/" %(app_name,table_name))

    return render(request,"crmadmin/table_obj_delete.html",{"obj":obj,
                                                              "admin_class":admin_class,
                                                              "app_name": app_name,
                                                              "table_name": table_name,
                                                              "errors":errors
                                                              })