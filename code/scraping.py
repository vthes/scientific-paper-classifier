import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, url):
        self.url = url
        self.category_data = {}
        self.ids = {}
        self.names = {}
        self.idlist = []
        self.namelist = []

    def fetch_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        head_h2s = soup.findAll('h2', class_='accordion-head')
        body_divs = soup.findAll(class_='accordion-body')

        for i in range(len(head_h2s)):
            self.category_data[f'{head_h2s[i].text}'] = \
                [tag.text.replace(')', '').split('(') for tag in body_divs[i].
                    findAll('h4')]

        self.ids = dict.fromkeys(self.category_data)
        for key in self.ids.keys():
            self.ids[key] = [v[0].strip() for v in self.category_data[key]]

        self.idlist = [x for v in [*self.ids.values()] for x in v]

        self.names = dict.fromkeys(self.category_data)
        for key in self.names.keys():
            self.names[key] = [v[1] for v in self.category_data[key]]

        self.namelist = [x for v in [*self.names.values()] for x in v]

    def get_data(self):
        return [self.ids, self.names]

    def get_groups(self):
        return [*self.category_data.keys()]

    def get_ids(self, group=None):
        return self.idlist if group is None else self.ids[group]

    def get_names(self, group=None):
        return self.namelist if group is None else self.names[group]

    def get_name_by_id(self, id_):
        return self.namelist[self.idlist.index(id_)]

    def get_id_by_name(self, name):
        return self.idlist[self.namelist.index(name)]
