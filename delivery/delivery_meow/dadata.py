from dadata import Dadata


class gDadata:
    token = '8ecc6963af3bb50bb5c43dd2272475d4b5dc5cd8'
    secret = "47d3e9e948fd7100cbbfb9ff8434b0b376fef181"

    def __init__(self):
        self.dadata = Dadata(self.token, self.secret)

    def get_geo(self, address):
        result = self.dadata.clean("address", f"{address}")
        geo = {'geo_lat': result['geo_lat'], 'geo_lon': result['geo_lon']}

        return geo

    def get_address(self, query):
        return self.dadata.suggest('address', query)
