from django.contrib import admin
from django.urls import path, include
from .views import home, cron_job_call_handler
from dotenv import load_dotenv
import os

load_dotenv()

urlpatterns = [
    path('', home),
    path(os.getenv('CRON_URL'), cron_job_call_handler),
]