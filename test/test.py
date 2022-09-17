import requests
website = "https://creditsuissecompetition.herokuapp.com/tickerStreamPart1"
payload = {'stream': [
      '00:01,A,5,5.5',
      '02:04,A,5,5.6',
      '02:03,B,5,5.5',
      '00:02,B,5,5.6',
  ]}
#r = requests.get(website)
r = requests.post(website, data=payload)
print(r)
'''
r = requests.delete('https://httpbin.org/delete')
r = requests.head('https://httpbin.org/get')
r = requests.options('https://httpbin.org/get')
'''