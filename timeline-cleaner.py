import tweepy
import config


class TweetCleaner:

    def __init__(self, context=None):
        self.api = self.set_api()

    def set_api(self):
        auth = tweepy.OAuthHandler(
            config.CONSUMER_KEY,
            config.CONSUMER_SECRET
        )
        auth.set_access_token(config.ACCESS_KEY, config.ACCESS_SECRET)
        print('[+] Tweet API Connected')
        return tweepy.API(auth, timeout=120)

    def wipe_timeline(self):
        for status in tweepy.Cursor(self.api.user_timeline).items():
            self.api.destroy_status(status.id)
            print('[+] Del Tweet ID: {}'.format(status.id))


if __name__ == "__main__":
    print('[-] Test connection')
    try:
        tc = TweetCleaner()
        if tc:
            print('[+] Success')
    except:
        print('[!] FAILED TO CONNECT')

    print('Wipe Timeline?')

    consent = input('[y/n]==> ')

    if consent[0].lower() == 'y':
        tc.wipe_timeline()
    else:
        print('[!] You did not press y')
        print('[!] No action taken')
