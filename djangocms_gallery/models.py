# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from cms.models.fields import PageField

from filer.fields.image import FilerImageField
from djangocms_gallery import settings

import math


class Gallery(CMSPlugin):
    title = models.CharField(_('title'), max_length=100, blank=True, null=True)
    template = models.CharField(_('template'), max_length=255, default=settings.GALLERY_TEMPLATES[0][0],
        choices=settings.GALLERY_TEMPLATES)
    autoplay = models.PositiveIntegerField(_('autoplay'), default=0, blank=True,
        help_text=_('Time in seconds each slide is displayed. Zero means no autoplay.'))

    # Advanced
    duration = models.PositiveIntegerField(_('duration'), default=0, blank=True,
        help_text=_('Duration of the animation in seconds. Zero means no animation.'))

    def __unicode__(self):
        if self.title:
            return self.title
        return super(Gallery, self).__unicode__()

    def __init__(self, *args, **kwargs):
        super(Gallery, self).__init__(*args, **kwargs)
        self.reload()

    def copy_relations(self, old_instance):
        for slide in old_instance.slides.all():
            slide.pk = None
            slide.gallery = self.pk
            slide.save()

    def save(self, *args, **kwargs):
        super(Gallery, self).save(*args, **kwargs)
        self.reload()

    def reload(self):
        if self.slides.all().count() > 0:
            self._automatic_ratios()
            for minmax in ['min', 'max']:
                for atr in ['width', 'height']:
                    current = '%s_%s' % (minmax, atr)
                    setattr(self, current, getattr(self._minmax(minmax, atr).image, atr))
                    setattr(self, '%s_ratio' % current, self._ratio(atr, getattr(self, current)))
            default = settings.DEFAULT_RATIO.lower()
            self.size = self._ratio(default.split('_')[1], getattr(self, default))

    def _ratio(self, dimension, value):
        ratio = self.high_ratio
        if dimension == 'height':
            ratio = self.wide_ratio
        new_size = math.ceil(value*ratio)
        if dimension == 'width':
            return value, new_size
        return new_size, value

    def _automatic_ratios(self):
        first = self.slides.all()[0]
        wide = float(first.image.width)/float(first.image.height)
        high = float(first.image.height)/float(first.image.width)
        for slide in self.slides.all()[1:]:
            slide_wide = float(slide.image.width)/float(slide.image.height)
            slide_high = float(slide.image.height)/float(slide.image.width)
            if slide_wide > wide:
                wide = slide_wide
            if slide_high > high:
                high = slide_high
        self.wide_ratio = wide
        self.high_ratio = high

    def _minmax(self, minmax, atr):
        ret = self.slides.all()[0]
        for slide in self.slides.all()[1:]:
            res = getattr(ret.image, atr) - getattr(slide.image, atr)
            if minmax == 'max' and res < 0:
                ret = slide
            if minmax == 'min' and res > 0:
                ret = slide
        return ret


class Slide(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='slides')
    ordering = models.IntegerField(_('ordering'), default=100)
    image = FilerImageField(verbose_name=_('image'))

    title = models.CharField(_('title'), max_length=100, blank=True, null=True)
    page = PageField(verbose_name=_('page'), blank=True, null=True)
    url = models.URLField(_('url'), blank=True, null=True)

    class Meta:
        ordering = ['ordering', 'pk',]

    def __unicode__(self):
        return self.get_title

    @property
    def get_title(self):
        if self.title:
            return self.title
        return self.image.label

    @property
    def link(self):
        if self.page:
            return self.page.get_absolute_url()
        if self.url:
            return self.url
        return '#'

    @property
    def has_link(self):
        if self.page or self.url:
            return True
        return False

    def save(self, *args, **kwargs):
        super(Slide, self).save(*args, **kwargs)
        self.gallery.reload()