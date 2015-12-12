#!/usr/bin/python
# -*- coding: utf-8 -*-

import ast
import json
import os
import sys

from pyspark.sql import Row
from pyspark import SparkContext

CONTRACT_TYPES = [u'Contrato Definitivo', u'Prorrogacao', u'Contrato Rescindido', u'Prorrogação e Alteração Salarial', u'Rescisão', u'Renovação', u'Contrato encerrado']

def parse_player_data(d):
    try:
        parsed_d = json.loads(d)
        return Row(name=parsed_d['name'],
#               picture=parsed_d['picture'],
               birthdate=parsed_d['birthdate'],
               team=parsed_d['team'],
#               badge=parsed_d['badge'],
               reg_id=parsed_d['reg_id'],
               contract_type=parsed_d['contract-type'],
               contract_number=parsed_d['contract-number'],
               contract_begin=parsed_d.get('contract-begin',None),
               contract_end=parsed_d.get('contract-end', None),
               contract_pub_date=parsed_d['contract-pub-date'],
               )
    except:
        print d
        raise

def clean_contracts(d):
    return d.filter(lambda x: x.contract_type in CONTRACT_TYPES)

def load_data(path):
    sc = SparkContext()
    data = sc.textFile(path).map(parse_player_data)
    return clean_contracts(data)

if __name__ == '__main__':
#    print 'Contract types: ======================================'
#    print data.map(lambda x: x.contract_type).distinct().collect()
#    print '======================================================'
    pass



