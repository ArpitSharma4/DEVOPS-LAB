# delivery_metrics.py
from prometheus_client import start_http_server, Gauge, Summary
import random, time, logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

total_deliveries = Gauge("total_deliveries", "Total number of deliveries")
pending_deliveries = Gauge("pending_deliveries", "Number of pending deliveries")
on_the_way_deliveries = Gauge("on_the_way_deliveries", "Number of deliveries on the way")
average_delivery_time = Summary("average_delivery_time_seconds", "Average delivery time in seconds")

def simulate_delivery(high_pending=False):
    if high_pending:
        pending = random.randint(50, 100)
    else:
        pending = random.randint(10, 20)
    on_the_way = random.randint(5, 20)
    delivered = random.randint(30, 70)
    avg_time = random.uniform(15, 45)

    total = pending + on_the_way + delivered

    logging.info(f"Pending:{pending} On-the-way:{on_the_way} AvgTime:{avg_time:.2f}s Total:{total}")

    total_deliveries.set(total)
    pending_deliveries.set(pending)
    on_the_way_deliveries.set(on_the_way)
    average_delivery_time.observe(avg_time)

if __name__ == "__main__":
    start_http_server(8000, addr="0.0.0.0")
    while True:
        simulate_delivery(high_pending=False)
        time.sleep(1)
