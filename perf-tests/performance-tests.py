import json
import random
from locust import HttpUser, task, between
from pyquery import PyQuery

"""Проект с другого сайта, потому запросы могут быть с другого проекта"""

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)
    data = None
    urls = None

    @task(2)
    def get_root(self):
        self.client.request_name = 'index'
        self.client.get("/")

    @task(2)
    def view_search(self):
        self.client.request_name = 'found'
        item_n = random.randrange(1,len(self.data))
        fio = self.data[item_n][2].split(" ")
        year = self.data[item_n][3]

        if "." in year:
            year = year.split(".")[-1]
        if "/" in year:
            year = year.split("/")[-1]
        if len(fio) >= 3:
            searchstring = "/search?surname={0}&forename={1}&patronym={2}&year_of_birth={3}".replace("{0}", fio[0]).\
                replace("{1}", fio[1]).replace("{2}",fio[2]).replace("{3}", year)
            r = self.client.get(searchstring)
            pq = PyQuery(r.content)
            if len(pq("table")("a")) is not 0:
                self.urls = [tr.attrib['href'] for tr in pq("table")("a")]

    @task(1)
    def view_detailed_search(self):
        self.client.request_name = 'view details'
        if self.urls is not None:
            if len(self.urls) >= 1:
                item_n = random.randrange(0, len(self.urls))
                self.client.get(self.urls[item_n])
            else:
                print('List is Null')

    @task(1)
    def view_bad_search(self):
        self.client.request_name = 'not found'
        fio = ["Сидоров","Карл","Фридрихович"]
        year = "1979"
        searchstring = "/search?surname={0}&forename={1}&patronym={2}&year_of_birth={3}".replace("{0}", fio[0]).\
                replace("{1}", fio[1]).replace("{2}",fio[2]).replace("{3}", year)
        self.client.get(searchstring)
        
"""Переименовать или создать rian-json с полезными данными"""

    def on_start(self):
        with open('rian.json') as json_file:
            self.data = json.load(json_file)

