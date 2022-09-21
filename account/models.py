from django.db import models
from django.contrib.auth.models import User
# from hr.models import Personnel

# Create your models here.


class MenuTable(models.Model):
    menu_string = models.CharField(max_length=100)
    url_string = models.CharField(max_length=250)
    parent_id = models.ForeignKey("self", blank=True,null=True, on_delete=models.CASCADE)
    group_permission_id = models.CharField(max_length=50)
    has_child = models.BooleanField(null=True)
    isActive = models.BooleanField(null=True)
    isDelete = models.BooleanField(null=False)
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50, blank=True, null=True)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)


class EmployeeUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # employee = models.OneToOneField(Personnel, on_delete=models.CASCADE)
    permission = models.CharField(max_length=50)
    isActive = models.BooleanField(null=True)
    isDelete = models.BooleanField(null=False)
    insertUser = models.CharField(max_length=50, default='system')
    insertDate = models.DateField(blank=True, null=True, default=None)
    updateUser = models.CharField(max_length=50, default=None, blank=True, null=True)
    updateDate = models.DateField(blank=True, null=True, default=None)
    project = models.CharField(max_length=100,default='1')


class GroupTable(models.Model):
    group_name = models.CharField(max_length=200)
    isActive = models.BooleanField(null=True)
    isDelete = models.BooleanField(null=False)
    insertUser = models.CharField(max_length=50, default='system')
    insertDate = models.DateField(blank=True, null=True, default=None)
    updateUser = models.CharField(max_length=50, blank=True, null=True, default=None)
    updateDate = models.DateField(blank=True, null=True, default=None)
    project = models.CharField(max_length=100,default='1')

class UserGroupTable(models.Model):
    user_id = models.ForeignKey(EmployeeUser, on_delete=models.CASCADE)
    group_id = models.ForeignKey(GroupTable, on_delete=models.CASCADE)
    isActive = models.BooleanField(null=True)
    isDelete = models.BooleanField(null=False)
    insertUser = models.CharField(max_length=50, default='system')
    insertDate = models.DateField(blank=True, null=True, default=None)
    updateUser = models.CharField(max_length=50, blank=True, null=True, default=None)
    updateDate = models.DateField(blank=True, null=True, default=None)
    project = models.CharField(max_length=100,default='1')

class MenuGroupTable(models.Model):
    menu_id = models.ForeignKey(MenuTable, on_delete=models.CASCADE)
    menu_group_id = models.ForeignKey(GroupTable, on_delete=models.CASCADE)
    isActive = models.BooleanField(null=True)
    isDelete = models.BooleanField(null=False)
    insertUser = models.CharField(max_length=50, default='system')
    insertDate = models.DateField(blank=True, null=True, default=None)
    updateUser = models.CharField(max_length=50, blank=True, null=True, default=None)
    updateDate = models.DateField(blank=True, null=True, default=None)
    project = models.CharField(max_length=100,default='1')