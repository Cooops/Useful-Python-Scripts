import pytz
from datetime import datetime, timedelta

def get_timezones(period_length):
    """
    (int) -> datetime date
    
    Takes in a predefined integer as a length (ie 90, which would be 90 days) and returns the oldest date (based on CST).
    Used for creating date values for any given timeseries (used when making charts, etc).
    """
    try:
        CST = pytz.timezone('US/Central')
        oldestDate = (datetime.now(CST) + timedelta(days=1)) - timedelta(days=period_length)
        return oldestDate
