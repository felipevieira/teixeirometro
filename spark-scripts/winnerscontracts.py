#!/usr/bin/python
# -*- coding: utf-8 -*-

CONTRACT_TYPES = [u'Contrato Definitivo', u'Prorrogacao', u'Contrato Rescindido', 
					u'Prorrogação e Alteração Salarial', u'Rescisão', u'Renovação', u'Contrato encerrado']

def get_date(c):
	try:
		return c.contract_begin_date or c.contract_pub_date
	except AttributeError:
		return c.contract_pub_date

def get_statistics(data, s, year):
	winners_statistics = {}
	for team in s:
		print team
		team_id = data.filter(lambda contract: contract.team==team).first().team_id
		statistics = {}
		for contract_type in CONTRACT_TYPES:			
			statistics[contract_type] = data.filter(lambda contract: contract.team_id == team_id and
				contract.contract_type == contract_type and get_date(contract).year == year).count()
			winners_statistics[team] = statistics

	return winners_statistics
