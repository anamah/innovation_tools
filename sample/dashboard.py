from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncDay
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from innovation.models import ToolsAndInnovations, Metadata, Tweets
import dashboard


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

def most_tweets_service(request):
    phase = get_params(request)
    if phase is not None:
        tools = ToolsAndInnovations.objects.filter(prime_phase_number=phase).values()
        twitter_accounts = [tool['twitter'].split('/')[-1] for tool in tools if tool['twitter'].startswith('https')]
        tweets = []
        for account in twitter_accounts:
            tw = Tweets.objects.filter(topic__contains=account).values('topic').annotate(dcount=Count('topic'))
            for t in tw:
                tweets.append({'topic': t['topic'], 'dcount': t['dcount']})
    else:
        tweets = Tweets.objects.values('topic').annotate(dcount=Count('topic'))

    tweets = sorted(tweets, key=lambda tup: int(tup['dcount']))
    tweets = tweets[-20:]
    return render_to_string('dashboard/stats.html', {
        'title': 'Tweets statistics',
        'stats': [
            {'label': tweet['topic'],
             'count': tweet['dcount']}
            for tweet in tweets
        ]
    })

def most_popular_service(request):
    phase = get_params(request)
    if phase is not None:
        tools = ToolsAndInnovations.objects.filter(prime_phase_number=phase).values()
        twitter_accounts = [tool['twitter'].split('/')[-1] for tool in tools if tool['twitter'].startswith('https')]
        tweets = []
        for account in twitter_accounts:
            tw = Tweets.objects.filter(topic__contains=account).values('topic').annotate(sum=Sum('like_count'))
            for t in tw:
                tweets.append({'topic': t['topic'], 'sum': t['sum']})
    else:
        tweets = Tweets.objects.values('topic').annotate(sum=Sum('like_count'))
    tweets = sorted(tweets, key=lambda tup: int(tup['sum']))
    tweets = tweets[-20:]
    return render_to_string('dashboard/stats.html', {
        'title': 'Tweets Likes statistics',
        'stats': [
            {'label': tweet['topic'],
             'count': tweet['sum']}
            for tweet in tweets
        ]
    })

def get_params(request):
    request = request.dicts[1]['request']
    phase = request.GET.get('phase')
    return phase

def most_retweet_service(request):
    phase = get_params(request)
    if phase is not None:
        tools = ToolsAndInnovations.objects.filter(prime_phase_number=phase).values()
        twitter_accounts = [tool['twitter'].split('/')[-1] for tool in tools if tool['twitter'].startswith('https')]
        tweets = []
        for account in twitter_accounts:
            tw = Tweets.objects.filter(topic__contains=account).values('topic').annotate(sum=Sum('retweet'))
            for t in tw:
                tweets.append({'topic': t['topic'], 'sum': t['sum']})
    else:
        tweets = Tweets.objects.values('topic').annotate(sum=Sum('retweet'))
    tweets = sorted(tweets, key=lambda tup: int(tup['sum']))
    tweets = tweets[-20:]

    return render_to_string('dashboard/stats.html', {
        'title': 'Tweets Retweet statistics',
        'stats': [
            {'label': tweet['topic'],
             'count': tweet['sum']}
            for tweet in tweets
        ]
    })

def word_cloud(request):
    return render_to_string('dashboard/stats2.html')

def twitters_count(request):
    return render_to_string('dashboard/counter.html', {
        'title': 'Tweets Counts',
        'count': Tweets.objects.count(),
        'icon': '<i class="material-icons">message</i>'
    })



def twitters_username_count(request):
    username_counts = len(Tweets.objects.values('username').annotate(dcount=Count('username')))
    return render_to_string('dashboard/counter.html', {
        'title': 'Twitter Username Counts',
        'count': username_counts,
        'icon': '<i class="material-icons">account_circle</i>'
    })

def twitters_topic_count(request):
    topic_counts = len(Tweets.objects.values('topic').annotate(dcount=Count('topic')))
    return render_to_string('dashboard/counter.html', {
        'title': 'Topic Counts',
        'count': topic_counts,
        'icon': '<i class="material-icons">assessment</i>'
    })

dashboard.register('Welcome', [
    [users_count, groups_count, staff_count],
    [registration_stats, login_stats],
    [word_cloud]
])


dashboard.register('Tweets', [
    [twitters_count, twitters_username_count, twitters_topic_count],
    [most_tweets_service, most_popular_service],
    [most_retweet_service],
    [word_cloud]]
)
