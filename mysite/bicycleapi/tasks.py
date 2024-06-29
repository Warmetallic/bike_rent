# Import necessary modules
from celery import shared_task
from celery.utils.log import get_task_logger
from .models import Bicycle
import logging

# Configure logging
logger = get_task_logger(__name__)
file_handler = logging.FileHandler("celery_log.txt")  # Log file path
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


@shared_task
def calculate_rental_cost(bicycle_id, hours_rented):
    logger.info(
        f"Calculating rental cost for bicycle {bicycle_id} for {hours_rented} hours."
    )
    bicycle = Bicycle.objects.get(id=bicycle_id)
    cost_per_hour = 10
    total_cost = hours_rented * cost_per_hour
    logger.info(f"Total cost for bicycle {bicycle_id}: {total_cost}")
    return total_cost
