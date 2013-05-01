"""
sentry.management.commands.get_user_events
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse

from sentry.models import Event, Group


class Command(BaseCommand):
    help = "Helps find all events pertaining to specified user"

    option_list = BaseCommand.option_list + (
        make_option('--username', type=str, default=None,
                    help="GetGlue username of user"),
        make_option('--ip', type=str, default=None,
                    help="IP address of user"),
        make_option('--group', default=None, type=int,
                    help="Get events belonging to a specific group"),
        make_option('--event', default=None, type=int,
                    help="Choose a specific event"),
    )

    def handle(self, **options):
        if options['username']:
            user_ident = "id:%s" % options['username']
        elif options['ip']:
            user_ident = "ip:%s" % options['ip']
        else:
            print "Either `username` or `ip` option is required"
            return

        events = Event.objects.all()

        group_id = options['group']
        if group_id:
            group = Group.objects.get(pk=group_id)
            events = events.filter(group=group)

        event_id = options['event']
        if event_id:
            events = events.filter(id=event_id)

        events = events.order_by('-datetime')

        print "Results matching user_ident %s:" % user_ident
        for event in events:
            if event.user_ident == user_ident:
                url = reverse('sentry-group-event', kwargs={
                    'project_id': event.project.slug,
                    'team_slug': event.team.slug,
                    'group_id': event.group.id,
                    'event_id': event.id,
                })
                print "%s (%s)" % (url, event.datetime)
