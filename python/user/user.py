#make this a class
def getId(event):
  return event['requestContext']['authorizer']['principalId']

def getWatchListTemplate():
  return {}