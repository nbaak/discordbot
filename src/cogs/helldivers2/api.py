import cogs.helldivers2.httpclient as httpclient


class Endpoints:
    war = 'https://helldiverstrainingmanual.com/api/v1/war/status'
    news = 'https://helldiverstrainingmanual.com/api/v1/war/news'
    campaign = 'https://helldiverstrainingmanual.com/api/v1/war/campaign'
    planet_index = 'https://helldiverstrainingmanual.com/api/v1/war/history'
    major_order = 'https://helldiverstrainingmanual.com/api/v1/war/major-orders'
    planets = 'https://helldiverstrainingmanual.com/api/v1/planets'


def get_major_order():
    return httpclient.get(Endpoints.major_order)


def get_war():
    return httpclient.get(Endpoints.war)


def get_news():
    return httpclient.get(Endpoints.news)


def get_campaign():
    return httpclient.get(Endpoints.campaign)


def get_planet(index:int):
    return httpclient.get(f"{Endpoints.planet_index}/{index}")


def planets():
    return httpclient.get(Endpoints.planets)


def test():
    print(get_news()[0])
    print(get_major_order())
    print(planets()['126'])


if __name__ == '__main__':
    test()
