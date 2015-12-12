#!/usr/bin/python
# -*- coding: utf-8 -*-

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
            parsed_data = bid_get_data_for_date(origin.date()).json()
	    html_data = parsed_data["dados"]

	    parse_html_data(html_data)

	    origin += timedelta(days=1)

def parse_html_data(html_data):
	players = []

	soup = BeautifulSoup(html_data, 'html.parser')
	player_entries = soup.find_all("div", class_="modal-content")
	for player_entry in player_entries:
                player = {}
		body = player_entry.find("div", class_="modal-body")
		for p in body.find_all("p"):
			if u'Inscrição:' in p.text:
				player['reg_id'] = int(p.text[len('Inscrição')])
			elif u'Tipo Contrato:' in p.text:
				tokens = p.text.split(':')
				player['contract-type'] = tokens[1][:-2].strip()
				player['contract-number'] = tokens[2].strip()
			elif u'Data inicio:' in p.text:
				tokens = p.text.split(':')
				dt_begin = tokens[1][:-len('Data termino:')].strip()
				dt_end = tokens[2].strip()
				if dt_begin:
					player['contract-begin'] = datetime.strptime(dt_begin, '%d/%m/%Y')
				if dt_end:
					player['contract-end'] = datetime.strptime(dt_end, '%d/%m/%Y')
			elif u'Nascimento:' in p.text:
				player['birthdate'] = datetime.strptime(p.text.split(':')[-1].strip(), '%d/%m/%Y')
			elif u'Data de Publicação:' in p.text:
				player['contract-pub-date'] = datetime.strptime(p.text.split(u': ')[-1].strip(), '%d/%m/%Y %H:%M:%S')
		team = body.find('p', class_='boxPlus')
		player['team'] = team.text.strip()
		players.append(player)

get_bid_data_since(datetime(2015,12,1))
