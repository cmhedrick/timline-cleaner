import sys
import logging

from timeline_cleaner import TweetCleaner

logging.basicConfig(
    filename='wiper.log',
    filemode='w',
    format=(
        '%(levelname)s:%(asctime)s - %(process)d - %(message)s'
    )
)

logging.info('Preparing for cleaning...')
try:
    tc = TweetCleaner()
except:
    logging.critical('FAILED TO CREAT TweetCleaner INSTANCE')
    sys.exit('See wiper.log!')

logging.info('Begin wiping tweets...')
try:
    tc.wipe_timeline()
except:
    logging.critical('Failed to wipe tweets...')
    sys.exit('See wiper.log!')

logging.info('Hating on everything...')
try:
    tc.unlike()
except:
    logging.critical('Failed to unlike all tweets')
    sys.exit('See wiper.log!')

logging.info('All clean!')
