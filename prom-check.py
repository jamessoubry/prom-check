#!/usr/local/bin/python3

import requests
import sys
import time
from datetime import datetime, timezone, timedelta

interval = 60
prometheus = sys.argv[1]
alertmanager = sys.argv[2]


def send_alert(prometheus, alertmanager):
    """Send alert to alertmanager."""

    start_time = datetime.now(timezone.utc).astimezone()
    end_time = start_time + timedelta(minutes=interval)

    print("[{}] Sending alert to {}.".format(
            start_time,
            alertmanager
    ))

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
        print("[{}] Alert sent OK.".format(
            datetime.now(timezone.utc).astimezone()
        ))
        return True
    else:
        print("[{}] Alert failed to send.".format(
            datetime.now(timezone.utc).astimezone()
        ))
        return False


def check_prom(prometheus):
    """Test Prometheus endpoint."""

    try:
        r = requests.get(
            "http://{}/metrics".format(prometheus),
            timeout=(30, 30)
        )

        print("[{}] Status Code: {}".format(
            datetime.now(timezone.utc).astimezone(),
            r.status_code
        ))

        if r.status_code == 200:
            return True
        else:
            print("[{}] {} is down.".format(
                datetime.now(timezone.utc).astimezone(),
                prometheus
            ))
            return False

    except:
        print("[{}] Failed to get prometheus endpoint in 30 seconds".format(
            datetime.now(timezone.utc).astimezone()
        ))
        return False


print(
    "Starting prom-check with prometheus: {} and alertmanager: {}".format(
        prometheus,
        alertmanager
    )
)

while True:

    print("[{}] Testing Prometheus..".format(
        datetime.now(timezone.utc).astimezone()
    ))

    if not check_prom(prometheus):
        send_alert(prometheus, alertmanager)

    print("[{}] Waiting for {} seconds..".format(
        datetime.now(timezone.utc).astimezone(),
        interval
    ))

    time.sleep(interval)
