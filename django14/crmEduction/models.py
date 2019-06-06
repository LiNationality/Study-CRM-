from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customers(models.Model):
    """客户信息表"""
    name=models.CharField(max_length=32,blank=True,null=True)
    qq=models.CharField(max_length=64,unique=True)
    qq_name=models.CharField(max_length=64,blank=True,null=True)
    phont=models.CharField(max_length=64,blank=True,null=True)
    source_choices=(
        (0,'转介绍'),
        (1,'qq群'),
        (2,'官网'),
        (3,'百度推广'),
        (4,'51CTO'),
        (5,'知乎'),
        (6,'市场推广'),
    )
    source=models.SmallIntegerField(choices=source_choices)
    status_choices=(
        (0,'已报名'),
        (1,'未报名'),
    )
    status=models.SmallIntegerField(choices=source_choices,default=1)
    referral_from=models.CharField(verbose_name='转介绍人QQ',max_length=64,blank=True,null=True)

    consult_course=models.ForeignKey("Courses",verbose_name="咨询课程",on_delete=True)
    content=models.TextField(verbose_name="详细咨询")

    consultant=models.ForeignKey("UserProfiles",on_delete=True)

    date=models.DateTimeField(auto_now_add=True)
    memo=models.TextField(blank=True,null=True)

    tags=models.ManyToManyField("Tag",blank=True,null=True)
    def __str__(self):
        return self.qq
    class Meta:
        verbose_name="客户表"
        verbose_name_plural="客户表"
    pass

class Tag(models.Model):
    name=models.CharField(unique=True,max_length=32)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name='标签'
        verbose_name_plural='标签'
    pass

class CustomersFollowUp(models.Model):
    """客户跟进表"""
    customer=models.ForeignKey("Customers",on_delete=True)
    content=models.TextField(verbose_name="跟进内容")
    consultant=models.ForeignKey("UserProfiles",on_delete=True)
    date=models.DateTimeField(auto_now_add=True)
    intention_choices=(
        (0,'两周内报名'),
        (1,'一月内报名'),
        (2,'近期无报名计划'),
        (3,'已在其它机构报名'),
        (4,'已报名'),
        (5,'已拉黑'),
    )
    intention=models.SmallIntegerField(choices=intention_choices)
    # date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "<%s : %s>" % (self.customer.qq,self.intention)
    class Meta:
        verbose_name='客户跟进表'
        verbose_name_plural='客户跟进表'
    pass

class Courses(models.Model):
    """课程表"""
    name=models.CharField(max_length=64,unique=True)
    price=models.PositiveSmallIntegerField()
    period=models.PositiveSmallIntegerField(verbose_name="周期(月)")
    outline=models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='课程表'
        verbose_name='课程表'
    pass

class Branch(models.Model):
    """校区"""
    name=models.CharField(max_length=128,unique=True)
    addr=models.CharField(max_length=128)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name='校区'
        verbose_name_plural='校区'
    pass

class ClassTable(models.Model):
    """班级表"""
    branch=models.ForeignKey("Branch",verbose_name="分校",on_delete=True)
    course=models.ForeignKey("Courses",on_delete=True)
    semester=models.PositiveSmallIntegerField(verbose_name="学期")
    teacher=models.ManyToManyField("UserProfiles")
    class_type_choice=(
        (0,'面授(全周)'),
        (1,'面授(周末)'),
        (2,'网络班'),
    )
    class_type=models.SmallIntegerField(choices=class_type_choice,verbose_name="班级类型")
    start_date=models.DateTimeField(verbose_name="开班日期")
    end_date=models.DateTimeField(verbose_name="结业日期",blank=True,null=True)

    def __str__(self):
        return "%s %s %s" % (self.branch,self.course,self.semester)
    class Meta:
        verbose_name='班级表'
        verbose_name_plural='班级表'
    pass

class CoursesRecord(models.Model):
    """上课记录表"""
    from_class=models.ForeignKey("ClassTable",on_delete=True)
    day_num=models.PositiveSmallIntegerField(verbose_name="第几天")
    teacher=models.ForeignKey("UserProfiles",on_delete=True)
    has_homework=models.BooleanField(default=True)
    homework_content=models.TextField(blank=True,null=True)
    outline=models.TextField(verbose_name="本节课大纲")
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.from_class,self.day_num)

    class Meta:
        unique_together=("from_class","day_num")
        verbose_name='上课记录表'
        verbose_name_plural='上课记录表'
    pass

class StudyRecord(models.Model):
    """学习记录表"""
    student=models.ForeignKey("Enrollment",on_delete=True)
    coursr_record=models.ForeignKey("CoursesRecord",on_delete=True)
    attendance_choices=(
        (0,'已签到'),
        (1,'迟到'),
        (2,'缺勤'),
        (3,'早退'),
    )
    attendance=models.SmallIntegerField(choices=attendance_choices,default=0)
    score_choices=(
        (100,"A+"),
        (90,"A"),
        (85,"B+"),
        (80,"B"),
        (75,"B-"),
        (70,"C+"),
        (60,"C"),
        (40,"C-"),
        (-50,"D"),
        (-100,"COPY"),
        (0,"N/A"),
    )
    score=models.SmallIntegerField(choices=score_choices)
    memo=models.TextField(blank=True,null=True)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s %s %s"%(self.student,self.coursr_record,self.score)

    class Meta:
        unique_together=('student','coursr_record')
        verbose_name="学习记录表"
        verbose_name_plural="学习记录表"
    pass

class Enrollment(models.Model):
    """报名表"""
    customer=models.ForeignKey("Customers",on_delete=True)
    enrolled_class=models.ForeignKey("ClassTable",verbose_name="所在班级",on_delete=True)
    consultant=models.ForeignKey("UserProfiles",verbose_name="课程顾问",on_delete=True)
    contract_agreed=models.BooleanField(default=False,verbose_name="学员已同意合同")
    contract_approved=models.BooleanField(default=False,verbose_name="合同已审核")
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s"%(self.customer,self.enrolled_class)

    class Meta:
        unique_together=("customer","enrolled_class")
        verbose_name='报名表'
        verbose_name_plural='报名表'
    pass

class Payment(models.Model):
    """缴费记录"""
    customer=models.ForeignKey("Customers",on_delete=True)
    course=models.ForeignKey("Courses",verbose_name="所报课程",on_delete=True)
    amount=models.PositiveSmallIntegerField(verbose_name="数额",default=500)
    consultant=models.ForeignKey("UserProfiles",on_delete=True)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s"%(self.customer,self.amount)
    class Meta:
        verbose_name='缴费记录'
        verbose_name_plural='缴费记录'
    pass

class UserProfiles(models.Model):
    """账户表"""
    user=models.OneToOneField(User,on_delete=True)
    name=models.CharField(max_length=32)
    roles=models.ManyToManyField("Roles",blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='账户表'
        verbose_name_plural='账户表'
    pass

class Roles(models.Model):
    """角色表"""
    name=models.CharField(max_length=32,unique=True)
    memus=models.ManyToManyField("Menu",blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name='角色表'
        verbose_name_plural='角色表'
    pass

class Menu(models.Model):
    """菜单"""
    name=models.CharField(max_length=32)
    url_name=models.CharField(max_length=64)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name='菜单'
        verbose_name_plural='菜单'
    pass