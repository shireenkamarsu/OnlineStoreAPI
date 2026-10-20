from datetime import datetime

def validate_cart_dates_within_range(cart_dates,start,end):
    fmt = "%Y-%m-%d"
    start = datetime.strptime(start,fmt)
    end = datetime.strptime(end, fmt)
    for d in cart_dates:
        dt = datetime.strptime(d[:10], fmt)
        if not (start <= dt <= end):
            return False
    return True
