#!/usr/local/bin/python3

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import sys
import time
from datetime import datetime, timezone, timedelta

interval = 30
prometheus = sys.argv[1]
alertmanager = sys.argv[2]


def requests_session(
    retries=5,
    backoff_factor=1,
    status_forcelist=( 500, 502, 503, 504 ),
):


    s = requests.Session()

    retries = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist
    )
    adapter = HTTPAdapter(max_retries=retries)
    s.mount('http://', adapter)
    s.mount('https://', adapter)
    return s


def send_alert(prometheus, alertmanager):
    """Send alert to alertmanager."""

    start_time = datetime.now(timezone.utc).astimezone()
    end_time = start_time + timedelta(seconds=interval)

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

    try:
        a = requests_session().post(
            'http://{}/api/v1/alerts'.format(alertmanager),
            json=body
        )

        if a.status_code == 200:
            print("[{}] Alert sent OK.".format(
                datetime.now(timezone.utc).astimezone()
            ))
            return True

    except:
        pass
    print("[{}] Alert failed to send.".format(
        datetime.now(timezone.utc).astimezone()
    ))
    return False


def check_prom(prometheus):
    """Test Prometheus endpoint."""

    try:


        r = requests_session().get(
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
