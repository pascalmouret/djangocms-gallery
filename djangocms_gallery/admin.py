# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from djangocms_gallery.models import Slide


class SlideAdmin(admin.StackedInline):
    model = Slide
    fields = ('ordering', 'image', ('page', 'url',),)