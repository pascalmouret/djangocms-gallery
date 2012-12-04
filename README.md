# djangocms-gallery

Gallery plugin for django-cms. Still in development.

## Installation
You can easily install it via pip:

* `pip install djangocms-gallery`
* add `djangocms_gallery` to your `INSTALLED_APPS`
* run `syncdb` and `migrate`

## Requirements
* django-filer
* easy-thumbnails

## Settings
### GALLERY_TEMPLATES
A Tuple of Tuples containing the available Templates:

`(('djangocms_gallery/default.html', _('default'),)`

### ADVANCED_OPTIONS
Default is False. If True, additional options will be available in the admin.

## People
This plugin uses cl.gallery.js out of the classjs-plugins-library:
* https://github.com/FinalAngel/classjs-plugins