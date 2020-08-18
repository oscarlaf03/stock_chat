
# import re  # TODO
import requests

class Bot:
    def __init__(self, message='', username=''):
        self.message = message
        self.username = username
        self.bot_name = 'The Stock Bot Master'
        self.stock_data = None

    @property
    def valid_command(self):
        return self.message.lower().startswith('/stock=')

    @property
    def has_code(self):
        return self.valid_command and len(self.message.split('=')) > 1

    @property
    def stock_code(self):
        return self.message.split('=')[1].strip() if self.has_code else None

    def csv_to_dict(self,csv, delimeter=','):
        csv = csv.split()
        keys = csv[0].split(delimeter)
        return {k: v for k, v in zip(keys, csv[1].split(delimeter))}
    
    def get_stock_data(self):
        url = f'https://stooq.com/q/l/?s={self.stock_code}&f=sd2t2ohlcv&h&e=csv'
        r = requests.get(url)
        if r.status_code == 200:
            data = self.csv_to_dict(r.text)
            data['got_response'] = True
            self.stock_data = data
        else:
            self.stock_data = {'got_response': False}

    @property
    def is_stock_data_complete(self):
        if self.stock_data and self.stock_data['got_response']:
            missing_values = list(self.stock_data.values()).count('N/D')
            return not (missing_values >= 7)
        else:
            return False

    
    def reply_message(self):
        if self.valid_command:
            if self.stock_code:
                self.get_stock_data()
                if self.stock_data['got_response']:
                    if self.is_stock_data_complete:
                        return f'Hi {self.username}, {self.stock_data["Symbol"]} Open price is {self.stock_data["Open"]} per share, have a nice day'
                    else:
                        return f'Hi {self.username}, it seems we don\'t have any information for symbol: "{self.stock_code}",are you sure the symbol is correct?'
                else:
                    return  f'Sorry {self.username}, We had some issues contacting the stock market, please try again later'
            else:
                return  f'Hi {self.username}, it seems you typed the right command but forgot to include a stock symbol'
        else:
             return f'Sorry {self.username} I cannot understand: "{self.message}", but I can understand "/stock=" followed by valid stock symbol'



