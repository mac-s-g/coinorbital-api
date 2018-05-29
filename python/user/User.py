import os
import boto3
import time
import json
from decimal import *

class User:
  __debug = False

  #public user attributes
  user_id = None
  investments = {}
  watchlist = []
  __record = {}
  __table = False

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

  """
  user class construct

  attempt to pull a user from dynamo or fallback to default user object
  """
  def __init__(self, event, debug=False):
    self.__debug = debug
    record = {}

    if debug is True:
        record = {
            "user_id": 1,
            "investments": self.__default_investments,
            "watchlist": self.__default_watchlist
        }
    else:
      try:
        self.user_id = event['requestContext']['authorizer']['principalId']
        dynamodb = boto3.resource('dynamodb')
        self.__table = dynamodb.Table(os.environ['USER_TABLE'])
      except:
        raise Exception('malformatted User input: {}'.format(json.dumps(event)))

      record = self.__table.get_item(
        Key={
            'user_id': self.user_id
        }
      )


    if "Item" in record:
      self.__initializeFromRecord(record["Item"])
    else:
      self.__initializeNewUser()


  def __initializeNewUser(self):
    self.setItem("investments", self.__default_investments)
    self.setItem("watchlist", self.__default_watchlist)


  def __initializeFromRecord(self, record):
    for (key, value) in record.items():
      self.setItem(key, value)


  def get(self):
    user = self.__record
    user['user_id'] = self.user_id
    user['investments'] = self.investments
    user['watchlist'] = self.watchlist
    return user


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
        investment['transactions'] = []
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
      # tx["cost_per_coin_usd"] = Decimal(tx["cost_per_coin_usd"])
      # tx["quantity"] = Decimal(tx["quantity"])
    except:
      valid = False

    return valid


  def validWatchlist(self, watchlist):
    valid = True

    try:
      for coin in watchlist:
        if type(coin) is not str:
          raise
    except:
      valid = False

    return valid


  def setItem(self, key, value):
    if key == "investments":
      try:
        for (name, investment) in value.items():
          self.setInvestment(investment)
      except:
        raise Exception('set investments failed: {}'.format(json.dumps(value)))
    elif key == "watchlist":
      self.setWatchlist(value)
    elif key == "user_id":
      pass #this value is protected
    else:
      self.__record[key] = value


  def setInvestment(self, investment):
    try:
      if self.validInvestment(investment):
        if investment["name"] in self.investments:
          self.investments[investment["name"]] = {
            **self.investments[investment["name"]],
            **investment
          }
        else:
          self.investments[investment['name']] = investment
    except:
      raise Exception('set investment failed: {}'.format(json.dumps(investment)))


  def setTransactions(self, investment_name, transactions):
    try:
      self.investments[investment_name]['transactions'] = []
      for tx in transactions:
        self.addTransaction(investment_name, tx)
    except:
      raise Exception('set transactions failed: {}, {}'.format(
        investment_name, json.dumps(transaction)
      ))


  def addTransaction(self, investment_name, tx):
    if self.validTransaction(tx):
      self.investments[investment_name]['transactions'].append(tx)
    else:
      raise Exception('add transaction failed: {}, {}'.format(
        investment_name, json.dumps(tx)
      ))


  def setWatchlist(self, watchlist):
    if self.validWatchlist(watchlist):
      self.watchlist = watchlist
    else:
      raise Exception('set watchlist failed: {}'.format(json.dumps(watchlist)))


  def deleteInvestment(self, name):
    self.investments.pop(name, None)


  def save(self):
    user = self.get()
    user['last_modified'] = int(time.time())
    if not self.__debug:
      self.__table.put_item(Item=user)
