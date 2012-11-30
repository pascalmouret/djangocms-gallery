# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


DEFAULT_GALLERY_TEMPLATES = (
    ('djangocms_gallery/default.html', _('default')),
)

GALLERY_TEMPLATES = getattr(settings, 'DJANGOCMS_GALLERY_TEMPLATES', DEFAULT_GALLERY_TEMPLATES)