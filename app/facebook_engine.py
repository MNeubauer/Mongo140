import facebook


class fb():
    def __init__(self):
        self.FB_SECRET = app.config['FB_SECRET']
        self.FB_APP_ID = app.config['FB_APP_ID']
        self.FB_PAGE_ID = app.config'FB_PAGE_ID']

    def fb_init(self):
        graph = facebook.GraphAPI(***ACCESS TOKEN***)
        page = graph.get_object('skunkworks140')