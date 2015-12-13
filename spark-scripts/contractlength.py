#!/usr/bin/python
# -*- coding: utf-8 -*-

import sparkbid
import sys
import operator
from datetime import datetime

def rank_contracts_nominal_length(d):
    x = d.filter(lambda x: x.contract_type == 'Contrato Definitivo').filter(lambda x: x.contract_begin and \
                 x.contract_end).map(lambda x: (x, datetime.strptime(x.contract_end, '%d/%m/%Y') -
                 datetime.strptime(x.contract_begin, '%d/%m/%Y'))).collect()
    x = sorted(x, key=operator.itemgetter(1))
    return x

#def rank_contracts_real_length(d):
#    x = d.filter(lambda x: x.contract_type == 'Contrato Definitivo').filter(lambda x: x.contract_begin and \
#                 x.contract_end).map(lambda x: (x, datetime.strptime(x.contract_end, '%d/%m/%Y') -
#                 datetime.strptime(x.contract_begin, '%d/%m/%Y'))).collect()
#    x = sorted(x, key=operator.itemgetter(1))
#    return x

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: %s <dataset.json>' % sys.argv[0]

    d = sparkbid.load_data(sys.argv[1])
    print 'Contratos mais longos:=========='
    most_contracts = rank_contracts_nominal_length(d)
    for x in most_contracts:
        print x[0].team.encode('utf-8'), x[0].name.encode('utf-8'), x[1]
    print

