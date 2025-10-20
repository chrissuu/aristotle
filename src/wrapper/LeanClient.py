from kimina_client import KiminaClient

class LeanClient:
    def __init__(self, api_url):
        client = KiminaClient(api_url=api_url)

    def check(self, snippet):
        success, errors = None, None
        return success, errors