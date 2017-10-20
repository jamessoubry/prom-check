#!/usr/local/bin/python3

import requests
import sys
import time
from datetime import datetime, timezone, timedelta

interval = 60
prometheus = sys.argv[1]
alertmanager = sys.argv[2]

print(
    "Starting prom-check with prometheus: {} and alertmanager: {}".format(
        prometheus,
        alertmanager
    )
)


while True:
    up = False

    print("[{}] Testing Prometheus..".format(
        datetime.now(timezone.utc).astimezone()
    ))

    try:
        r = requests.get(
            "http://{}/metrics".format(prometheus),
            timeout=30
        )

        if r.status_code == 200:
            up = True

        print("[{}] Status Code: {}".format(
            datetime.now(timezone.utc).astimezone(),
            r.status_code
        ))
    except:
        print("[{}] Failed to get prometheus endpoint in 30 seconds".format(
            datetime.now(timezone.utc).astimezone()
        ))
        pass

    if not up:

        print(
            "[{}] {} is down. Sending alert to {}.".format(
                datetime.now(timezone.utc).astimezone(),
                prometheus,
                alertmanager
            )
        )

        start_time = datetime.now(timezone.utc).astimezone()
        end_time = start_time + timedelta(minutes=interval)

        body = [
            {
                "labels": {
                    "severity": "critical",
                    "instance": prometheus,
                    "alertname": "prometheus_down"
                },
                "annotations": {
                    "summary": "Prometheus Down",
                    "description": "Prometheus Instance Is Down"
                },
                "startsAt": start_time.isoformat(),
                "endsAt": end_time.isoformat()
            }
        ]

        a = requests.post(
            'http://{}/api/v1/alerts'.format(alertmanager),
            json=body
        )

        if a.status_code == 200:
            print("[{}] Alert sent OK.".format(datetime.now(timezone.utc).astimezone()))
        else:
            print("[{}] Alert failed to send.".format(datetime.now(timezone.utc).astimezone()))

    print("[{}] Waiting for {} seconds..".format(datetime.now(timezone.utc).astimezone(), interval))
    time.sleep(interval)
