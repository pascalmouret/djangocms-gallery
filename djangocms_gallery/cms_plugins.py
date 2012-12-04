# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from djangocms_gallery.models import Gallery
from djangocms_gallery.admin import SlideAdmin
from djangocms_gallery import settings


class GalleryPlugin(CMSPluginBase):
    model = Gallery
    name = _('Gallery')
    render_template = 'djangocms_gallery/gallery_base.html'

    inlines = [SlideAdmin,]
    fields = ('title', 'template', 'autoplay',)
    advanced_fields = ('duration', 'navigation_style',)

    @property
    def declared_fieldsets(self):
        self.fieldsets = ((None, {'fields': self.fields}))
        if settings.ADVANCED_OPTIONS:
            self.fieldsets = (self.fieldsets, (_('Advanced'), {'fields': self.advanced_fields, 'classes': ['collapse',]}))
        return super(GalleryPlugin, self)._declared_fieldsets()

plugin_pool.register_plugin(GalleryPlugin)