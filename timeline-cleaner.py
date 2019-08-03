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


if __name__ == "__main__":
    print('[-] Test connection')
    try:
        tc = TweetCleaner()
        if tc:
            print('[+] Success')
    except:
        print('[!] FAILED TO CONNECT')
