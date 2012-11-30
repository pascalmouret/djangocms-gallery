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
    autoplay = models.BooleanField(_('autoplay'), default=True)

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return super(Gallery, self).__unicode__()

    def __init__(self, *args, **kwargs):
        super(Gallery, self).__init__(*args, **kwargs)
        self.reload()

    def reload(self):
        self.ratio = self._automatic_ratio()
        for minmax in ['min', 'max']:
            for atr in ['width', 'height']:
                setattr(self, '_%s_%s' % (minmax, atr), self._minmax(minmax, atr))
                setattr(self, '%s_%s' % (minmax, atr), getattr(getattr(self, '_%s_%s' % (minmax, atr)).image, atr))
        for minmax in ['min', 'max']:
            for atr in ['width', 'height']:
                setattr(self, '%s_%s_ratio' % (minmax, atr), self._ratio(atr, getattr(self, '%s_%s' % (minmax, atr))))

        print self.min_width_ratio

    def copy_relations(self, old_instance):
        for slide in old_instance.slides.all():
            slide.pk = None
            slide.gallery = self.pk
            slide.save()

    def _ratio(self, dimension, value):
        print '%s %s' % (self.wide_ratio, self.high_ratio)
        ratio = self.high_ratio
        if dimension == 'height':
            ratio = self.wide_ratio
        new_size = math.ceil(value*ratio)
        if dimension == 'width':
            return value, new_size
        return new_size, value

    def _automatic_ratio(self):
        if self.slides.all().count == 0:
            wide = high = 0
        elif self.slides.all().count == 1:
            wide = high = float(self.slides.all()[0].image.width)/float(self.slides.all()[0].image.height)
        else:
            wide = float(self.slides.all()[0].image.width)/float(self.slides.all()[0].image.height)
            high = float(self.slides.all()[0].image.height)/float(self.slides.all()[0].image.width)
            print(wide, high)
            for slide in self.slides.all():
                slide_wide = float(slide.image.width)/float(slide.image.height)
                slide_high = float(slide.image.height)/float(slide.image.width)
                if slide_wide > wide:
                    wide = slide_wide
                if slide_high > high:
                    high = slide_high
        self.wide_ratio = wide
        self.high_ratio = high

    def _minmax(self, minmax, atr):
        slides = self.slides.all()
        if slides.count == 0:
            return 0
        ret = slides[0]
        if slides.count > 1:
            for slide in slides:
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

    page = PageField(verbose_name=_('page'), blank=True, null=True)
    url = models.URLField(_('url'), blank=True, null=True)

    class Meta:
        ordering = ['ordering', 'pk',]

    def __unicode__(self):
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