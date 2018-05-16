#make this a class
def getId(event):
  return event['requestContext']['authorizer']['principalId']

def getWatchListTemplate():
  return {}

def getInvestmentTemplate():
  return {}

def getTransactionTemplate():
  return {}

def getInvestments(user_record):
  if "investments" in user_record:
    return user_record['investments']
  else:
    return {}

def getTransactions(investment):
  if "transactions" in investment:
    return investment['transactions']
  else:
    return []