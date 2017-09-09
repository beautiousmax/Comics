# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Comics(models.Model):
    image_link = models.CharField(max_length=250)
    saved_date = models.DateField(auto_now_add=True)
    comic_title = models.CharField(max_length=250, default='')
    alt_text = models.CharField(max_length=250, default='')
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.image_link)
