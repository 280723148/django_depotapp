from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.conf import settings
import os


dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_roles_path = os.path.join(dir_path, 'roles')


def var_dir(instance, filename):
    return os.path.join(_roles_path, instance.name, 'vars', filename)


def task_dir(instance, filename):
    return os.path.join(_roles_path, instance.name, 'tasks', filename)


class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    creator = models.ForeignKey(User)
    createDatetime = models.DateTimeField(auto_now_add=True)
    directory = models.FilePathField(path=_roles_path, match='*.yml', recursive=True, max_length=200)
    tasks = models.FileField(upload_to=task_dir, blank=False)
    vars = models.FileField(upload_to=var_dir)

    def __unicode__(self):
        return u'%s' % self.name

