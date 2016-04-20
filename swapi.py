#!/usr/bin/env python3

"""
Kuali Coding Exercise

We would like you to write a script which pulls from the Star Wars API and
reports a list of starships and previous owners. Which language you use, how it
is done and the rest are up to you. The exercise constraints:

    * The script should be able to run from CentOS-7.
    * It reports the output to stdout in a readable manner (a list of starships
      and previous owners)
    * Create a new public repo in github and submit the code there.
    * When you are done in your email back to HR include the link to the public
      repo.
    * Your end result should be something we can run, so please include
      instructions for running it that a smart engineer who might not be
      familiar with your tech stack could follow.
    * Only submit your own work. You can use libraries and frameworks, but make
      sure you wrote the script itself.

The project is deliberately open-ended because we want to see how you build
it--there is not any preferred way to get to the end result.
"""

import sys
import urllib.parse

import requests


class Starship:
    URL = "http://swapi.co/api/starships/"

    def __init__(self, name, model, pilot_urls):
        self.name = name
        self.model = model
        self.pilot_urls = pilot_urls

    @classmethod
    def make_from_json(cls, d):
        starship = cls(d['name'], d['model'], d['pilots'])
        starship._all_data = d
        return starship

    @classmethod
    def fetch_list(cls):
        page = 1
        params = {}
        l = []
        while page is not None:
            if page > 1:
                params['page'] = page
            resp = requests.get(cls.URL, params=params).json()
            nxt = resp['next']
            if nxt is None:
                page = None
            else:
                qs = urllib.parse.urlparse(nxt).query
                page = urllib.parse.parse_qs(qs).get('page', [0])[0]
                page = int(page)
            l += [cls.make_from_json(d) for d in resp['results']]
        return l

    def fetch_pilots(self):
        self.pilots = [Pilot.fetch_url(url) for url in self.pilot_urls]


class Pilot:
    URL = 'http://swapi.co/api/people/'

    def __init__(self, name):
        self.name = name

    @classmethod
    def make_from_json(cls, d):
        pilot = cls(d['name'])
        pilot._all_data = d
        return pilot

    @classmethod
    def fetch_url(cls, url):
        if not url.startswith(cls.URL):
            raise TypeError("Invalid URL")
        resp = requests.get(url).json()
        return cls.make_from_json(resp)


def main():
    starships = Starship.fetch_list()
    for s in starships:
        if not s.pilot_urls:
            continue
        s.fetch_pilots()

        sys.stdout.write(s.name+": ")
        sys.stdout.write(", ".join([p.name for p in s.pilots]))
        sys.stdout.write("\n")


if __name__ == '__main__':
    main()
