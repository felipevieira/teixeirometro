#!/usr/bin/python
# -*- coding: utf-8 -*-

import sparkbid
import sys
import operator

def rank_teams_most_contracts(d):
    x = d.filter(lambda x: x.contract_type == 'Contrato Definitivo').map(lambda x: x.team).countByValue()
    x = sorted(x.iteritems(), key=operator.itemgetter(1))
    return x

def rank_teams_most_rescision(d):
    x = d.filter(lambda x: x.contract_type in sparkbid.CONTRACT_RECISION_TYPES).map(lambda x: x.team).countByValue()
    x = sorted(x.iteritems(), key=operator.itemgetter(1))
    return x

def list_contratos(d, t):
    x = d.filter(lambda x: x.contract_type == 'Contrato Definitivo').filter(lambda x: x.team == t).collect()
    for i in x:
        print i

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: %s <dataset.json>' % sys.argv[0]

    d = sparkbid.load_data(sys.argv[1])
    print 'Times que mais contrataram:=========='
    most_contracts = rank_teams_most_contracts(d)
    for x in most_contracts:
        print x[0].encode('utf-8'), x[1]
    print

    print 'Rescisões: =========================='
    for x in rank_teams_most_rescision(d):
        print x[0].encode('utf-8'), x[1]
