"""
@todo:用于动态生成类
"""
from django.forms import forms,ModelForm
from crmEduction import models


class CustomerModelForm(ModelForm):
    class Meta:
        model=models.Customers
        fields="__all__"


def create_model_form(request,admin_class):
    """
    @todo:动态生成ModelForm
    :param request:
    :param admin_class:
    :return:
    """
    def __new__(cls,*args,**kwargs):
        # print("base fields",cls.base_fields)
        for field_name,field_obj in cls.base_fields.items():
            # print(field_name,dir(field_obj))
            field_obj.widget.attrs['class']='form-control'
        return ModelForm.__new__(cls)
    class Meta:
        model=models.Customers
        fields="__all__"
    attrs={'Meta':Meta}
    _model_form_class=type("DynamicModelForm",(ModelForm,),attrs)
    setattr(_model_form_class,'__new__',__new__)

    # print("model form",_model_form_class.Meta.model)
    # setattr(_model_form_class,)

    return _model_form_class