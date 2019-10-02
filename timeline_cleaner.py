import csv
import time
import datetime

import tweepy
import ijson

import config


class TweetCleaner:

    def __init__(self, context=None):
        self.api = self.set_api()
        self.count = 0

    def set_api(self):
        auth = tweepy.OAuthHandler(
            config.CONSUMER_KEY,
            config.CONSUMER_SECRET
        )
        auth.set_access_token(config.ACCESS_KEY, config.ACCESS_SECRET)
        print('[+] Tweet API Connected')
        return tweepy.API(auth, timeout=120)

    def wipe_timeline(self):
        self.count = 0
        for status in tweepy.Cursor(self.api.user_timeline).items():
            self.api.destroy_status(status.id)
            self.count += 1
            print('[+] Del Tweet ID: {}'.format(status.id))
        return self.count

    def wipe_by_date_range(self, start, end):
        self.count = 0
        statuses = tweepy.Cursor(self.api.user_timeline).items()
        while True:
            try:
                status = statuses.next()
                if status.created_at < end and status.created_at > start:
                    self.api.destroy_status(status.id)
                    self.count += 1
                    print('[+] Del Tweet ID: {}'.format(status.id))
            except tweepy.TweepError:
                time.sleep(60 * 15)
                continue
            except StopIteration:
                break
        return self.count

    def wipe_by_archive(self):
        with open('tweetdir/tweet.json', 'rb') as f:
            print('[-] Breaking down json')
            objects = ijson.items(f, 'item')
            statuses = list(objects)
            print('[+] Json complete')
            self.count = 0
            for status in statuses:
                try:
                    print('[-] Attempting Del on {0}'.format(status['id']))
                    self.api.destroy_status(status['id'])
                    self.count += 1
                    print('[+] Del Tweet ID: {0}'.format(status['id']))
                except tweepy.TweepError as e:
                    print(
                        '[!] Error Response: {0}'.format(
                            e.response.status_code
                        )
                    )
                    if e.response.status_code not in [404, 403]:
                        print('[!] Starting Sleep')
                        time.sleep(60 * 15)
                        print('[-] Sleep done!')
                    continue
                except StopIteration:
                    print('[!] Iter error, fucking off')
                    break
            print('[+] Done')

    def unlike(self):
        self.count = 0
        for status in tweepy.Cursor(self.api.favorites).items():
            self.api.destroy_favorite(status.id)
            self.count += 1
            print('[+] Unliked ID: {}'.format(status.id))
        return self.count


if __name__ == "__main__":
    tc = TweetCleaner()
    cmds = """
    Please choose from the commands below:
    q = quit
    w = wipe timeline
    d = wipe by date range
    a = wipe by archive.json
    u = unlike everything
    """
    cmd = ''
    while cmd.lower() != 'q':
        print(cmds)
        cmd = input("==> ")
        if cmd.lower() == 'w':
            print('[-] Wiping Timeline...')
            count = tc.wipe_timeline()
            print('[+] Deleted: {0} Tweets'.format(count))

        if cmd.lower() == 'a':
            tc.wipe_by_archive()

        if cmd.lower() == 'd':
            start = ''
            print('[-] Please provide start date or q to quit.')
            while start != 'q':
                start = input('[yyyy-mm-dd]==> ')
                try:
                    start = start.split('-')
                    start = datetime.datetime(
                        int(start[0]), int(start[1]), int(start[2])
                    )
                    break
                except:
                    print('[!] Bad format try again')

            end = ''
            flag = False
            print('[-] Please provide end date or q to quit.')
            while end != 'q':
                end = input('[yyyy-mm-dd]==> ')
                try:
                    end = end.split('-')
                    end = datetime.datetime(
                        int(end[0]), int(end[1]), int(end[2])
                    )
                    break
                except:
                    print('[!] Bad format try again')
            print(
                '[+] Starting wipe of tweets {0} - {1}...'.format(
                    start.strftime('%Y-%m-%d'),
                    end.strftime('%Y-%m-%d')
                )
            )
            count = tc.wipe_by_date_range(start, end)
            print('[+] Wipe complete!')
            print('[+] Deleted: {0} Tweets'.format(count))

        if cmd.lower() == 'u':
            print('[-] Unliking everything...')
            count = tc.unlike()
            print('[+] Unliked: {0} Tweets'.format(count))
