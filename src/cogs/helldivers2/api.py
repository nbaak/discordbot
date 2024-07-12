import cogs.helldivers2.httpclient as httpclient


class Endpoints:
    war_statistics = "https://api.helldivers2.dev/api/v1/war"
    dispatch = "https://api.helldivers2.dev/api/v1/dispatches"
    campaign = "https://api.helldivers2.dev/api/v1/campaigns"
    planets = "https://api.helldivers2.dev/api/v1/planets"
    major_order = "https://api.helldivers2.dev/api/v1/assignments"


def get_major_order():
    return httpclient.get(Endpoints.major_order)


def get_war_statistics():
    return httpclient.get(Endpoints.war_statistics)


def get_campaign():
    return httpclient.get(Endpoints.campaign)


def get_planet(index:int):
    return httpclient.get(f"{Endpoints.planet_index}/{index}")


def planets():
    return httpclient.get(Endpoints.planets)


def dispatch():
    return httpclient.get(Endpoints.dispatch)


def test():
    print(get_major_order())
    print(planets()[126])
    print(get_campaign())
    

if __name__ == "__main__":
    test()
