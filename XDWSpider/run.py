# -*- coding:utf-8 -*-
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PythonServer.settings")# project_name 项目名称
django.setup()

from scrapy import cmdline
cmdline.execute("scrapy crawl xiaodiao".split(" "))
