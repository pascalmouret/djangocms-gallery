# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


DEFAULT_GALLERY_TEMPLATES = (
    ('djangocms_gallery/default.html', _('default')),
)

DEFAULT_ADVANCED_OPTIONS = False

# 'MIN_WIDTH', 'MIN_HEIGHT', 'MAX_WIDTH', 'MAX_HEIGHT'
DEFAULT_DEFAULT_RATIO = 'MIN_WIDTH'


GALLERY_TEMPLATES = getattr(settings, 'DJANGOCMS_GALLERY_TEMPLATES', DEFAULT_GALLERY_TEMPLATES)
ADVANCED_OPTIONS = getattr(settings, 'DJANGOCMS_GALLERY_ADVANCED_OPTIONS', DEFAULT_ADVANCED_OPTIONS)
DEFAULT_RATIO = getattr(settings, 'DJANGOCMS_GALLERY_DEFAULT_RATIO', DEFAULT_DEFAULT_RATIO)