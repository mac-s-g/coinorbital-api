import os
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USER_TABLE'])

class User:

  #public user attributes
  user_id = None
  investments = {}
  watchlist = {}
  __record = {}

  #default attributes
  __default_investments = {
    "Bitcoin": {
      "name": "Bitcoin",
      "symbol": "BTC",
      "transactions": []
    },
    "Ethereum": {
      "name": "Ethereum",
      "symbol": "ETH",
      "transactions": []
    },
    "Litecoin": {
      "name": "Litecoin",
      "symbol": "LTC",
      "transactions": []
    }
  }
  __default_watchlist = ["BTC", "ETH", "LTC", "BCH"]

  def __init__(self, event):

    self.user_id = event['requestContext']['authorizer']['principalId']

    record = table.get_item(
      Key={
          'user_id': self.user_id
      }
    )

    if "Item" in record:
      for key in record:
        self.__record[key] = record[key]
      self.__initializeFromRecord(record["Item"])
    else:
      self.__initializeNewUser()


  def get(self):
    user = self.__record
    user.user_id = self.user_id
    user.investments = self.investments
    user.watchlist = self.watchlist
    return user

  def __initializeFromRecord(self, record):
    self.investments = {}
    self.watchlist = []
    if "investments" in record:
      for inv_name in record["investments"]:
        investment = record["investments"][inv_name]
        if self.validInvestment(investment):
          self.investments[investment["name"]] = investment
    if "watchlist" in record:
      self.watchlist = record["watchlist"]


  def validInvestment(self, investment):
    valid = True

    try:
      if "name" not in investment or "symbol" not in investment:
        raise
      if "transactions" in investment:
        for tx in investment["transactions"]:
          if self.validTransaction(tx) is False:
            raise
      else:
        #this is a little dirty
        investment.transactions = []
    except:
      valid = False

    return valid


  def validTransaction(self, tx):
    valid = True
    required_keys = [
      "cost_per_coin_usd",
      "quantity",
      "type",
      "time_recorded"
    ]
    try:
      for key in required_keys:
        if key not in tx:
          raise
    except:
      valid = False

    return valid


  def __initializeNewUser(self):
    self.investments = self.__default_investments
    self.watchlist = self.__default_watchlist
