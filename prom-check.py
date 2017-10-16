#!/usr/local/bin/python3

import requests
import sys
import time

prometheus = sys.argv[1]
alertmanager = sys.argv[2]

print("Starting prom-check with prometheus: {} and alertmanager: {}".format(prometheus, alertmanager))


while True:
	up = False
	try:
		print("testing Prometheus..")
		r = requests.get("http://{}/metrics".format(prometheus), timeout=30)
		if r.status_code == 200:
			up = True
		print(r.status_code)
	except:
		print("Failed to get prometheus endpoint in 30 seconds")
		pass

	if not up:

		print("{} is down. Sending alert to {}".format(prometheus, alertmanager))
		body = [{"labels": {"Alertname": "Prometheus Down", "severity": "critical"}}]

		a = requests.post('http://{}/api/v1/alerts'.format(alertmanager), json=body)

		print(a.status_code)
		print(a.json())

	print("waiting for 60 seconds")
	time.sleep(60)
