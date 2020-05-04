def rowcreate():
    ToolsAndInnovations.objects.all().delete()
    with open('Tools.csv') as f:
        reader = csv.reader(f)
        index = 0
        for row in reader:
            print(row)
            if index <= 2:
                index += 1
                continue
            else:
                tools, created = ToolsAndInnovations.objects.get_or_create(
                    name=row[1],
                    url=row[2],
                    web_launchyear=row[4],
                    prime_phase_alpha=row[5],
                    prime_phase_number=row[6],
                    function_free=row[7],
                    ui_functionfree=row[8],
                    function_controlled=row[9],
                    geo_category=row[10],
                    ui_geo_category=row[11],
                    twitter=row[12],
                    twitter_follow_latest=row[14],
                    active_pre=row[15],
                    active_dis=row[16],
                    active_ana=row[17],
                    active_wri=row[18],
                    active_pub=row[19],
                    active_out=row[20],
                    active_ass=row[21],
                )
            index += 1

import pandas as pd
import datetime
import os
import glob
def create_tweets():
    Tweets.objects.all().delete()
    os.chdir('/home/mikhail/PycharmProjects/tools/tweets_full/')
    for file in glob.glob("*.csv"):
        print(file)
        f = pd.read_csv(file)
        for index, row in f.iterrows():
            tweets = Tweets.objects.create(
                tweet_dt=datetime.datetime.strptime(row['tweet_dt'], "%Y-%m-%d").date(),
                topic=row['topic'],
                username=row['username'],
                name=row['name'],
                tweet=row['tweet'],
                like_count=row['like_count'],
                reply_count=row['reply_count'],
                retweet=row['retweet_count'],
                retweeted=row['retweeted']
            )