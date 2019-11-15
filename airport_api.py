from urllib2 import Request, urlopen
from urllib import urlencode, quote_plus

url = 'http://openapi.airport.kr/openapi/service/StatusOfPassengerFlights/getPassengerDepartures'
queryParams = '?' + urlencode({ quote_plus('ServiceKey') : '서비스키', quote_plus('to_time') : '2400', quote_plus('airport') : 'HKG', quote_plus('flight_id') : 'KE846', quote_plus('airline') : 'KE', quote_plus('lang') : 'K', quote_plus('from_time') : '0000' })

request = Request(url + queryParams)
request.get_method = lambda: 'GET'
response_body = urlopen(request).read()
print response_body
