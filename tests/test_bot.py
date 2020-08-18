from bot.bot import Bot
import pytest


@pytest.fixture(scope='module')
def bot():
    return Bot()

def test_no_message(bot):
    assert bool(bot.message) == False

def test_no_user_name(bot):
    assert bool(bot.username) == False

def test_invalid_command(bot):
    assert bot.valid_command == False

def test_stock_code_is_None(bot):
    assert bot.stock_code == None

def test_has_no_code(bot):
    assert bot.has_code == False

def test_username(bot):
    bot.username = 'test_usert'
    assert bool(bot.username) == True

def test_valid_stock_commmand(bot):
    bot.message = '/stock=aapl.us'
    assert bot.valid_command == True

def test_has_code(bot):
    assert bot.has_code == True

def test_stock_code_is_correct(bot):
    assert bot.stock_code == 'aapl.us'

def test_get_stock_data(bot):
    bot.get_stock_data()
    assert bot.stock_data != None

def test_stock_data_complete(bot):
    assert bot.is_stock_data_complete == True


def test_complete_stock_message(bot):
    my_message =  f'Hi {bot.username}, {bot.stock_data["Symbol"]} Open price is {bot.stock_data["Open"]} per share, have a nice day'
    bot_message = bot.reply_message()
    assert my_message == bot_message

def test_data_not_found_for_stock_code():
    bot = Bot('/stock=aaaaaap.us')
    my_message =  f'Hi {bot.username}, it seems we don\'t have any information for symbol: "{bot.stock_code}",are you sure the symbol is correct?'
    bot_message = bot.reply_message()
    assert my_message == bot_message

def test_user_not_entered_a_stock_code():
    bot = Bot('/stock=')
    my_message =  f'Hi {bot.username}, it seems you typed the right command but forgot to include a stock symbol'
    bot_message = bot.reply_message()
    assert my_message == bot_message


