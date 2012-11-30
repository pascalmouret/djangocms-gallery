# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from djangocms_gallery.models import Gallery
from djangocms_gallery.admin import SlideAdmin


class GalleryPlugin(CMSPluginBase):
    model = Gallery
    name = _('Gallery')
    render_template = 'djangocms_gallery/gallery_base.html'

    inlines = [SlideAdmin,]

plugin_pool.register_plugin(GalleryPlugin)