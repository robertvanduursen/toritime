class IntentionCacheMissError(Exception):
    """
    this intentional search-and-not-found will tell you what you need to work on next

    """

    def __init__(self):
        super().__init__()
        print("YO")
