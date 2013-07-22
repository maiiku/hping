# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import models
from datetime import datetime as dt
from django.utils.timezone import utc
from settings.common import LOGFILE


class BaseModel(models.Model):
    '''
    Model with common fields for all models
    All models should inherit this class
    '''
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.modified = dt.utcnow()
        super(BaseModel, self).save(*args, **kwargs)


class Haystack(BaseModel):
    '''
    Model holding urls to be checked
    '''
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=False, null=False)
    search_phrase = models.CharField(max_length=255, blank=True, null=True)
    last_checked = models.DateTimeField(null=True)
    last_ok = models.DateTimeField(null=True)
    last_error = models.DateTimeField(null=True)
    last_time_ms = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.url)

    class Meta:
        unique_together = ("url", "search_phrase")

    def get_absolute_url(self):
        return reverse('hay_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('hay_delete', kwargs={'pk': self.pk})

class PingHistory(BaseModel):
    '''
    Model holding health check history
    '''
    haystack = models.ForeignKey('Haystack')
    http_code=models.IntegerField(default=0)
    time_ms = models.IntegerField(default=0)
    phrase_found = models.BooleanField(default=True)

    @property
    def is_error(self):
        '''
        Everything else then 200 OK is not ok
        '''
        return True if (self.http_code != 200) or not self.phrase_found else False

    def save(self, *args, **kwargs):
        super(PingHistory, self).save(*args, **kwargs)
        self.haystack.last_time_ms = self.time_ms
        self.haystack.last_checked = self.created
        if not self.is_error:
            self.haystack.last_ok = dt.utcnow().replace(tzinfo=utc)
        else:
            self.haystack.last_error = dt.utcnow().replace(tzinfo=utc)
        self.haystack.save()

        #append to log file
        line =  '[{status}] {url} @ {check_time}: got {code} response in {ms}ms and requirement {phrase_found}\n'.format(
            status='FAILED' if self.is_error else 'SUCCESS',
            url=self.haystack.url,
            check_time=self.created,
            code=self.http_code,
            ms=self.time_ms,
            phrase_found='FAILED' if not self.phrase_found else 'SUCCESS' )
        with open(LOGFILE, 'a+') as f:
            f.write(line)