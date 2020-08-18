
# import re  # TODO
import requests

class Bot:
    def __init__(self, message, username):
        self.message = message
        self.username = username
        self.bot_name = 'The Stock Bot Master'

    def valid_command(self):
        return self.message.lower().startswith('/stock=')

    def stock_code(self):
        return self.message.split('=')[1].strip()

    def csv_to_dict(self,csv, delimeter=','):
        csv = csv.split()
        keys = csv[0].split(delimeter)
        return {k: v for k, v in zip(keys, csv[1].split(delimeter))}

    def stock_data(self):
        url = f'https://stooq.com/q/l/?s={self.stock_code()}&f=sd2t2ohlcv&h&e=csv'
        r = requests.get(url)
        if r.status_code == 200:
            data = self.csv_to_dict(r.text)
            data['got_response'] = True
            return data
        else:
            return {'got_response': False}

    def reply_message(self):
        if self.valid_command():
            if self.stock_data()['got_response']:
                return f'Hi {self.username}, {self.stock_data()["Symbol"]} Open price is {self.stock_data()["Open"]} per share, have a nice day'
            else:
                return  f'Sorry {self.username}, We had some issues contacting the stock market, please try again later'
        else:
             return f'Sorry {self.username} I cannot understand: "{self.message}", but I can understand "/stock=" followed by valid stock symbol'



