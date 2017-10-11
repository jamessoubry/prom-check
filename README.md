# PROM-CHECK
## Who Watches the Watchmen?

This Docker container will monitor Prometheus and send an alert directly to an alertmanager if down. It is useful if you don't want to run multiple Prometheis. The other option would be to run a micro instance of prometheus that only monitors your big prometheus but this should be alot simpler to set up.

```
docker run -d jamessoubry/prom-check prometheus1:9090 alertmanager1:9093
```

