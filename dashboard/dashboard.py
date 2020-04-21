from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncDay
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from innovation.models import ToolsAndInnovations, Metadata
from .base import Dashboard

User = get_user_model()


def users_count(request):
    return render_to_string('dashboard/counter.html', {
        'title': 'Tools And Innovations Resources',
        'count': ToolsAndInnovations.objects.count(),
        'icon': '<i class="material-icons">account_circle</i>'
    })


def groups_count(request):
    return render_to_string('dashboard/counter.html', {
        'title': 'Users',
        'count': User.objects.count(),
        'icon': '<i class="material-icons">perm_identity</i>'
    })


def staff_count(request):
    User = get_user_model()

    return render_to_string('dashboard/counter.html', {
        'title': 'Staff',
        'count': User.objects.filter(is_staff=True).count(),
        'icon': '<i class="material-icons">supervisor_account</i>'
    })


def registration_stats(request):
    stats = ToolsAndInnovations.objects.values('prime_phase_number').annotate(dcount=Count('prime_phase_number'))
    stats = [stage for stage in stats if stage['prime_phase_number'].isdigit()]
    stats = sorted(stats, key=lambda tup: int(tup['prime_phase_number']))
    # stats = (
    #     User.objects
    #     .annotate(label=TruncMonth('date_joined'))
    #     .values('label')
    #     .annotate(count=Count('id'))
    # )
    return render_to_string('dashboard/stats.html', {
        'title': 'Prime Phase Number statistics',
        'stats': [
            {'label': int(stage['prime_phase_number']),
             'count': stage['dcount']}
            for stage in stats if stage['prime_phase_number'].isdigit()
        ]
    })


def login_stats(request):
    stats = ToolsAndInnovations.objects.values('prime_phase_number').annotate(dcount=Count('prime_phase_number'))
    statsWithPhase = [stage for stage in stats if stage['prime_phase_number'].isdigit()]
    stats = [stage for stage in stats if not stage['prime_phase_number'].isdigit()]
    statswithphase = sorted(statsWithPhase, key=lambda tup: int(tup['prime_phase_number']))
    statsDict = {}
    for st in statswithphase:
        try:
            metadata = Metadata.objects.get(research_phase_number=st['prime_phase_number'])
            statsDict[metadata.research_phases7] =statsDict.get(metadata.research_phases7, 0)  + st['dcount']
        except Metadata.DoesNotExist:
            statsDict['NoInformation'] =statsDict.get('NoInformation', 0)  + st['dcount']
    for st in stats:
        statsDict['NoInformation'] = statsDict.get('NoInformation', 0) + st['dcount']
    # for st in statswithphase:
    return render_to_string('dashboard/stats.html', {
        'title': 'Research Phase Stages statistics',
        'stats': [
            {'label': phase,
             'count': count}
            for phase, count in statsDict.items()
        ]
    })


default_dashboard = Dashboard('Welcome', [
    [users_count, groups_count, staff_count],
    [registration_stats, login_stats]
])
