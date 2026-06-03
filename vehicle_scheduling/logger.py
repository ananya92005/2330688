import logging
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(f"logs/vehicle_scheduling_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("VehicleScheduler")

def log_info(message): logger.info(message)
def log_error(message): logger.error(message)
def log_debug(message): logger.debug(message)
def log_request(method, url, status=None):
    if status: logger.info(f"HTTP {method} | URL: {url} | Status: {status}")
    else: logger.info(f"HTTP {method} | URL: {url} | Sending request...")
def log_response(depot_id, budget, selected_count, total_impact):
    logger.info(f"Depot {depot_id} | Budget: {budget}h | Tasks Selected: {selected_count} | Total Impact: {total_impact}")
