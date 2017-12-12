import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question
import load_data
import crypto_model
import article_summerizer
import json

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def welcome():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent("CurrentPriceIntent", convert={'currency': str})
def current_price(currency):
    return statement('The current price of '+currency+' is '+load_data.get_current_price(currency)+' dollars.')


@ask.intent("PredictIntent", convert={'currency': str})
def predict(currency):
    prediction, accuracy = crypto_model.predict(currency, load_data.get_current_price(currency), load_data.load_historical(currency))
    return statement('I predict that the price of '+currency+' will go '+prediction+' but I am only '+accuracy+' percent sure.')


@ask.intent("SentimentIntent", convert={'currency': str})
def sentiment(currency):
    source, url, description, title = load_data.get_news_articles(currency)
    #summary = article_summerizer.summerize(currency, url)
    return statement('According to '+source+', '+description+' I sent the link to the full article on your Alexa app.').simple_card(title=title, content=url)


@ask.intent("HelpIntent")
def help():
    return statement(render_template('help'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)