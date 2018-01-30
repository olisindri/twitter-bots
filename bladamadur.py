# coding=utf-8
import markovify
import os
import re
import sys
import tweepy

DATA_DIRECTORY = os.path.join(sys.path[0], 'data/visir_is')


def post_to_twitter(tweet):
    """
    Initialises the Twitter API with credentials from environmental variables
    and uses that authenticated API access to post `tweet` on Twitter
    """
    auth = tweepy.OAuthHandler(
        os.environ['BLADAMADUR_CONSUMER_KEY'],
        os.environ['BLADAMADUR_CONSUMER_SECRET'])
    auth.set_access_token(
        os.environ['BLADAMADUR_ACCESS_TOKEN'],
        os.environ['BLADAMADUR_ACCESS_TOKEN_SECRET'])
    api = tweepy.API(auth)

    api.update_status(tweet)


def get_corpus():
    """
    Reads all files in the data directory and returns a Markovify model
    that can be used to build sentences
    """
    all_text = []

    for _, _, files in os.walk(DATA_DIRECTORY):
        for f in files:
            with open(os.path.join(DATA_DIRECTORY, f), 'r') as article:
                # Quotation marks rarely come out as pairs in finished chains.
                # So we remove them before adding the article text:
                all_text.append(re.sub(r'[„“]', '', article.read()))

    return markovify.Text("".join(all_text), state_size=2)


def create_tweet(model):
    """
    Returns a short sentence (maximum 140 characters) from a given model
    """
    return model.make_short_sentence(140, init_state=None)


post_to_twitter(create_tweet(get_corpus()))
