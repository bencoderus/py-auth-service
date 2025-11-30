def rate_limit(limit: int = 10, time_window: int = 60):
    def rate_limiter():
        print("Rate limit", limit, time_window)

    return rate_limiter