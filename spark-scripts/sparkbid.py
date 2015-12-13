#!/usr/bin/python
# -*- coding: utf-8 -*-

import ast
import json
import os
import sys

from pyspark.sql import Row
from pyspark import SparkContext

from datetime import datetime

from winners_contracts import *

CONTRACT_TYPES = [u'Contrato Definitivo', u'Prorrogacao', u'Contrato Rescindido', u'Prorrogação e Alteração Salarial', u'Rescisão', u'Renovação', u'Contrato encerrado']
CONTRACT_RECISION_TYPES = [u'Contrato Rescindido', u'Rescisão']

def parse_player_data(d):
    try:
        parsed_d = json.loads(d)
        return Row(name=parsed_d['name'].encode("utf-8"),
               picture=parsed_d['picture'],
               birthdate=get_date(parsed_d['birthdate']),
               team=parsed_d['team'].encode("utf-8"),
               team_id=parsed_d['team_id'],
               badge=parsed_d['badge'],
               reg_id=parsed_d['reg_id'],
               contract_type=parsed_d['contract-type'],
               contract_number=parsed_d['contract-number'],
               contract_begin=get_date(parsed_d.get('contract-begin',None)),
               contract_end=get_date(parsed_d.get('contract-end', None)),
               contract_pub_date=get_date(parsed_d['contract-pub-date']),
               )
    except:
        print d
        raise

def get_date(value):
  if value:
    return datetime.strptime(value, '%d/%m/%Y')

def clean_contracts(d):
    return d.filter(lambda x: x.contract_type in CONTRACT_TYPES)

def load_data(path):
    sc = SparkContext()
    data = sc.textFile(path).map(parse_player_data)
    return clean_contracts(data)

WINNERS = ["Corinthians", "Internacional", "São Paulo / SP", "Atlético / MG", "Santos / SP"]
LOOSERS = ["Joinville / SC", "Vasco da Gama", "Avaí / SC", "Goiás / GO", "Figueirense / SC"]

if __name__ == '__main__':
    data = load_data("../dataset.json")
    print get_statistics(data, LOOSERS, 2015)
    #print 'Contract types: ======================================'
    #print data.map(lambda x: x.contract_type).distinct().collect()
    #print '======================================================'
    #pass



