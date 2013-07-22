# -*- coding: utf-8 -*-
import urllib2
from apps.pinger.models import Haystack, PingHistory


class SendPing(object):
    CHUNK = 16 * 1024

    def __init__(self):
        self.haystack = Haystack.objects.all()

    def stream_data_from_url(self, url):
        '''
        streams data from given url
        '''
        url_data = ''
        req = urllib2.urlopen(url)
        code = req.getcode()
        encoding=req.headers['content-type'].split('charset=')[-1]
        for chunk in iter(lambda: req.read(self.CHUNK), ''):
            if not chunk:
                break
            url_data += unicode(chunk, encoding)

        return url_data, code

    def check_phrase(self, phrase, urldata):
        if phrase in urldata:
            return True
        else:
            return False


    def ping_straw(self, straw):
        import time
        error = False
        code = 0

        tstart = time.time()

        try:
            url_data, code = self.stream_data_from_url(straw.url)
        except:
            error = True

        tend = time.time()
        ms = tend-tstart

        if not error:
            error = self.check_phrase(straw.search_phrase, url_data)

        ping = PingHistory(
            haystack=straw,
            time_ms=ms,
            phrase_found=error,
            http_code=code,
        )
        ping.save()

    def run(self):
        for straw in self.haystack:
            self.ping_straw(straw)