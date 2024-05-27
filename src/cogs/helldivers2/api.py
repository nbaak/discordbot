import cogs.helldivers2.httpclient as httpclient

class Endpoints:
    war_status = 'https://helldiverstrainingmanual.com/api/v1/war/status'
    war_info = 'https://helldiverstrainingmanual.com/api/v1/war/info'
    news = 'https://helldiverstrainingmanual.com/api/v1/war/news'
    campaign = 'https://helldiverstrainingmanual.com/api/v1/war/campaign'
    # planet_index = 'https://helldiverstrainingmanual.com/api/v1/war/history/[planetIndex]'
    major_order = 'https://helldiverstrainingmanual.com/api/v1/war/major-orders'
    planets = 'https://helldiverstrainingmanual.com/api/v1/planets'


def get_major_order():
    return httpclient.get(Endpoints.major_order)


def get_war_status():
    return httpclient.get(Endpoints.war_status)


def get_war_info():
    return  httpclient.get(Endpoints.war_info)


def get_news():
    return httpclient.get(Endpoints.news)


def get_campaign():
    return httpclient.get(Endpoints.campaign)


def planets():
    return httpclient.get(Endpoints.planets)


def test():
    print(get_news()[0])


if __name__ == '__main__':
    test()
