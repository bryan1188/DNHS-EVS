from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from registration.forms import UploadStudentsForm
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse,reverse_lazy
from django.conf.urls.static import static
from django.conf import settings
from registration.management.helpers.XlsUploader import XlsUploader
from registration import models
import os

# Create your views here.
# go to viewsF/cbv folder for the views.py files
