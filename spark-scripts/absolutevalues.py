#!/usr/bin/python
# -*- coding: utf-8 -*-

def get_absolute_statistics(dataset):
	absolute_statistics = {}

	absolute_statistics["total_contracts"] = dataset.count()

	absolute_statistics["total_new_contracts"] = dataset.filter(
		lambda x: x.contract_type == "Contrato Definitivo").count()

	absolute_statistics["total_rescissions"] = dataset.filter(
		lambda x: x.contract_type == "Contrato Rescindido" or x.contract_type == "Rescisão" or
		x.contract_type == "Contrato encerrado").count()

	absolute_statistics["total_renewals"] = dataset.filter(
		lambda x: x.contract_type == "Prorrogacao" or x.contract_type == "Prorrogação e Alteração Salarial" or
		x.contract_type == "Renovação").count()

	absolute_statistics["distinct_teams"] = dataset.map(lambda x: x.team_id).distinct().count()

	absolute_statistics["distinct_players"] = dataset.map(lambda x: x.name).distinct().count()

	return absolute_statistics

def get_fun_facts(dataset):
	fun_facts = {}

	fun_facts["first_entry"] = dataset.takeOrdered(1, lambda x: x.contract_pub_date)

	return fun_facts		
