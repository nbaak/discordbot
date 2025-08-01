import cogs.helldivers2.httpclient as httpclient

X_SUPER_CLIENT = "Discord-Bot"
X_SUPER_CONTACT = ""


class Endpoints:
    all = "https://api.diveharder.com/v1/all"
    war_statistics = "https://api.helldivers2.dev/api/v1/war"
    # dispatch = "https://api.helldivers2.dev/a/pi/v1/dispatches?maxEntries=1024"
    dispatch = "https://api.live.prod.thehelldiversgame.com/api/NewsFeed/801"
    campaign = "https://api.helldivers2.dev/api/v1/campaigns"
    planets = "https://api.helldivers2.dev/api/v1/planets"
    major_order = "https://api.helldivers2.dev/api/v1/assignments"


def get_all():
    headers = {"X-Super-Client": X_SUPER_CLIENT, "X-Super-Contact": X_SUPER_CONTACT}
    return httpclient.get(Endpoints.all, headers)


def get_major_order():
    headers = {"X-Super-Client": X_SUPER_CLIENT, "X-Super-Contact": X_SUPER_CONTACT}
    return httpclient.get(Endpoints.major_order, headers)


def get_war_statistics():
    headers = {"X-Super-Client": X_SUPER_CLIENT, "X-Super-Contact": X_SUPER_CONTACT}
    return httpclient.get(Endpoints.war_statistics, headers)


def get_campaign():
    headers = {"X-Super-Client": X_SUPER_CLIENT, "X-Super-Contact": X_SUPER_CONTACT}
    return httpclient.get(Endpoints.campaign, headers)


def get_planet(index:int):
    headers = {"X-Super-Client": X_SUPER_CLIENT, "X-Super-Contact": X_SUPER_CONTACT}
    return httpclient.get(f"{Endpoints.planet_index}/{index}", headers)


def planets():
    headers = {"X-Super-Client": X_SUPER_CLIENT, "X-Super-Contact": X_SUPER_CONTACT}
    return httpclient.get(Endpoints.planets, headers)


def dispatch():
    headers = {"X-Super-Client": X_SUPER_CLIENT,
               "X-Super-Contact": X_SUPER_CONTACT,
               "Accept-Language": "de,en-US;",
               }
    parameters = {"maxEntries": 1024}
    return httpclient.get(Endpoints.dispatch, headers, parameters)


def test():
    print(get_major_order())
    print(planets()[126])
    print(get_campaign())
    print(dispatch()[-1])


if __name__ == "__main__":
    test()
