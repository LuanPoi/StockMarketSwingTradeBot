from Scripts.DataManager import Interface_APIHandler


class YahooAPIHandler(Interface_APIHandler):
    API_KEY = ""

    def __init__(self, api_key):
        if not str(api_key).isspace() and str(api_key) != "":
            self.API_KEY = str(api_key)
        return

    def connect(self, ticker):
        return

    def historical(self, start_date, end_date):
        return
