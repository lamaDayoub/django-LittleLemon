from rest_framework.throttling import UserRateThrottle

class TenCallsPerMinute(UserRateThrottle):
    # scope='hundred'
    x = 3