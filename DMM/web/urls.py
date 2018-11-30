from django.urls import re_path, path
# add , name after index
from web.views import index

urlpatterns = [
    # use this for more sites path('name', name)
    re_path('', index),
]
