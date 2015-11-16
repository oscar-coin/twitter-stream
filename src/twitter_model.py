class TwitterData(dict):
    def __init__(self, parsed, **kwargs):
        super(TwitterData, self).__init__(**kwargs)
        set_if(self, "id", parsed.id)
        set_if(self, "created_at", parsed.created_at)
        set_if(self, "text", parsed.text)
        set_if(self, "lang", parsed.lang)
        set_if(self, "retweet_count", parsed.retweet_count)
        set_if(self, "favorite_count", parsed.favorite_count)
        if parsed.place:
            set_if(self, "place", TwitterPlace(parsed.place))
        if parsed.user:
            set_if(self, "user", TwitterUser(parsed.user))


class TwitterPlace(dict):
    def __init__(self, parsed, **kwargs):
        super(TwitterPlace, self).__init__(**kwargs)
        set_if(self, "country", parsed.country)
        set_if(self, "name", parsed.full_name)
        set_if(self, "type", parsed.place_type)


class TwitterUser(dict):
    def __init__(self, parsed, **kwargs):
        super(TwitterUser, self).__init__(**kwargs)
        set_if(self, "id", parsed.id)
        set_if(self, "name", parsed.name)
        set_if(self, "description", parsed.description)
        set_if(self, "screen_name", parsed.screen_name)
        set_if(self, "location", parsed.location)


def set_if(obj, prop, val):
    if not val or (hasattr(val, "__len__") and not len(val) > 0):
        return
    obj[prop] = val

