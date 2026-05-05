
import re

def extract_tracker_count(text):
    numbers = re.findall(r'\d+', text)
    return int(numbers[0]) if numbers else 0
