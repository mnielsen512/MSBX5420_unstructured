import time
import requests
import json
from retrying import retry
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer


admin = AdminClient({'bootstrap.servers': 'kafka-1:9092'})
admin.create_topics([NewTopic("citibike.station.update.1", num_partitions=3, replication_factor=1)])
p = Producer({'bootstrap.servers': 'kafka-1:9092','api.version.request': True})

@retry(wait_exponential_multiplier=1000)
def scrape_station_status():
	print("trying again!")
	r = requests.get("https://gbfs.citibikenyc.com/gbfs/en/station_status.json")
	if r.status_code != 200:
		raise IOError("Station status fetch failed!")
	return r.json()

while True:
	data = scrape_station_status()  # data is a dictionary
	n = 0
#	print(len(data['data']['stations']))  #for testing length it OK
	while n < len(data['data']['stations']):
#		print(data['data']['stations'][n])
		my_b = json.dumps(data['data']['stations'][n])
		my_bytes = str.encode(my_b)
		p.produce('citibike.station.update.1', my_bytes) 
		n += 1
	p.flush()
	time.sleep(10)
