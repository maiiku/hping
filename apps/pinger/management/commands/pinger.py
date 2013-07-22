from django.core.management.base import BaseCommand, CommandError
from apps.pinger.ping import SendPing

class Command(BaseCommand):
    '''
    Manage script to run with cron
    for corn to work with venv, cd to project, choose right pyhon, eun command
    cd /home/my/project && /home/my/virtual/bin/python /home/my/project/manage.py pinger > /var/log/pinger_cron.log 2>&1
    '''
    help = 'Checks urls added to database. intended to use with cron'

    def handle(self, *args, **options):

        pinger = SendPing()
        try:
            pinger.run()
        except Exception, e:
            raise CommandError('Exception caught: %s, %s' % (e.__doc__, e.message))

        self.stdout.write('Successfully run pinger!')