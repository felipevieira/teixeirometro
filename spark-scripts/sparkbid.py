#!/usr/bin/python
# -*- coding: utf-8 -*-

import ast
import json
import os
import sys
import csv

from pyspark.sql import Row
from pyspark import SparkContext

from datetime import datetime

from winnerscontracts import *
from absolutevalues import *

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
               contract_type=parsed_d['contract-type'].encode("utf-8"),
               contract_number=parsed_d['contract-number'],
               contract_begin=get_date(parsed_d.get('contract-begin', None)),
               contract_end=get_date(parsed_d.get('contract-end', None)),
               contract_pub_date=get_date(parsed_d['contract-pub-date']),
               )
    except:
        print d
        raise

def to_csv(outputfile, data, fields):
    with open(outputfile, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(fields)
        for x in data:
            writer.writerow([getattr(x, f) for f in fields])

def get_date(value):
  if value:
    return datetime.strptime(value, '%d/%m/%Y')

def clean_contracts(d):
    return d.filter(lambda x: x.contract_type in CONTRACT_TYPES).filter(lambda x: x.contract_end >= x.contract_begin)

def load_data(path):
    sc = SparkContext()
    return sc.textFile(path).map(parse_player_data)

def write_dict_to_csv(my_dict, filename):  
  writer = csv.writer(open(filename, 'wb'))
  for key, value in my_dict.items():
     writer.writerow([key, value])

WINNERS = ["Corinthians / SP", "Atlético / MG", "São Paulo / SP", "Santos/ SP"]
LOOSERS = ["Joinville / SC", "Vasco da Gama", "Avaí / SC", "Goiás / GO", "Figueirense / SC"]

if __name__ == '__main__':
    data = load_data("../dataset-cleaned.json").cache()

    #write_dict_to_csv(get_absolute_statistics(data), "csvs/absolutevalues.csv")
    #write_dict_to_csv(get_fun_facts(data), "csvs/funfacts.csv")
    #write_dict_to_csv(get_statistics(data, WINNERS, 2013), "csvs/winners2013.csv")
    #write_dict_to_csv(get_statistics(data, WINNERS, 2014), "csvs/winners2014.csv")
    write_dict_to_csv(get_statistics(data, WINNERS, 2015), "csvs/winners2015.csv")
    #write_dict_to_csv(get_statistics(data, LOOSERS, 2013), "csvs/loosers2013.csv")
    #write_dict_to_csv(get_statistics(data, LOOSERS, 2014), "csvs/loosers2014.csv")
    #write_dict_to_csv(get_statistics(data, LOOSERS, 2015), "csvs/loosers2015.csv")


    #print get_statistics(data, LOOSERS, 2014)
    #print 'Contract types: ======================================'
    #print data.map(lambda x: x.contract_type).distinct().collect()
    #print '======================================================'
    #pass





