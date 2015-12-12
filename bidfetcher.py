import requests
import time
import ast
import sys
import re

from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup

BID_URL = 'http://bid.cbf.com.br'
BID_REQ_URL = 'http://bid.cbf.com.br/a/bid/carregar/json/'

def bid_get_data_for_date(d):
   s = requests.Session()
   s.get(BID_URL)
   r = s.post(BID_REQ_URL, data={'uf':'',
                                        'dt_pesquisa':d.strftime('%d/%m/%Y'),
                                        'tp_contrato':'TODOS',
                                        'n_atleta':''})

   return r

def get_bid_data_since(origin):
	while origin <= datetime.today() :
	    parsed_data = ast.literal_eval(bid_get_data_for_date(origin.date()).content)
	    html_data = parsed_data["dados"]

	    parse_html_data(html_data)

	    origin += timedelta(days=1)

def parse_html_data(html_data):
	soup = BeautifulSoup(html_data, 'html.parser')
	player_entries = soup.find_all("div", class_="modal-content")
	for player_entry in player_entries:
		print player_entry.prettify()	

get_bid_data_since(datetime(2015,12,12))
