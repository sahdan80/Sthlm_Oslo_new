# -*- coding: utf-8 -*-
# Author: Daniel Sahlgren 2022, WSP

import emme_functions.emme as emme
import emme_functions.emme_functions
import emme_functions.emme_functions as ef
import emme_functions.auxiliary_functions as aux
import pandas as pd
# import inro
import os
import pickle
from emme_functions.emme_functions import line_link_list as link_list



strackor_file = "indata/banor_strackning_enligt_TRV.csv"
strackor = pd.read_csv(strackor_file, encoding="UTF-8", sep=";")

strackor = [{"start":x, "end": y, "bana": z} for x, y,z in zip(strackor['start'], strackor['end'], strackor['bana'])]


print(strackor)
nodes = {} # key: station, val: node.id

project_file = 'D:/10350700_255_AE_DS/Jvg_temp//Jvg.emp'
my_emme = emme.Emme(project_file)
my_emmebank = my_emme.my_emmebank
my_modeller = my_emme.my_modeller
my_emme.my_desktop.version
scenario_id = 1002
# scenario_with_stations_id = 3
# scen_ids = {"JA": 3, "UA": 1}


scenario = my_emmebank.scenario(scenario_id)
network = scenario.get_network()
my_excluded_links = [("681141","681131"), ("681131","681101"), ("628022","681071")] # links in i, j form
my_excluded_links =[network.link(link_id[0], link_id[1]) for link_id in my_excluded_links] # get link objects
my_excluded_links_rev = [link.reverse_link for link in my_excluded_links] # get reverse links
my_excluded_links = my_excluded_links + my_excluded_links_rev
print(my_excluded_links)
"""paths_file: csv file with paths where column "start" is first node and "end is end node""
Link_modes: list with modes that links may have eg ["i","j", "k"]"""
# names_scenario = my_emmebank.scenario(scenario_with_stations_id)
# names_network =  names_scenario.get_network()

# ef.check_field(scenario=scenario,_id="bana",atype="STRING",type="LINK", initialize=True)

NAMESPACE = "inro.emme.data.network_field.create_network_field"
create_netfield = my_modeller.tool(NAMESPACE)

new_field = create_netfield(
    network_field_type="LINK",
    network_field_atype="STRING",
    network_field_name="bana",
    network_field_description="",
    overwrite=True,
    scenario=scenario)


for node in network.nodes():
    station = node["#station"]

    if station != "":
        nodes[station] = node.id

nodes_name = {}

paths_to_csv = []
my_paths = {}
excluded_links = []

for link in network.links():
    if not ef.check_link_mode(network=network, link=link, _modes=["i", "j", "k"]):
        excluded_links.append(link)

for node in network.nodes():
    station = node["#station"]

    if station != "":
        nodes["station"] = node.id

for stracka in strackor: # check that station has been named correct and that it is in the network
    start = stracka["start"]
    stop = stracka["end"]
    bana = stracka["bana"]
    try:
        nodes[start]
    except KeyError:
        print(stracka)
        print(start + " start not found")

    try:
        nodes[stop]
    except KeyError:
        print(stracka)
        print(stop + " stop not found")

for stracka in strackor:

    start = nodes[stracka["start"]]
    stop = nodes[stracka["end"]]
    bana = stracka["bana"]

    sp = network.shortest_path_tree(
        origin_node_id=start,
        link_costs='length',
        excluded_links=excluded_links + my_excluded_links,
        consider_turns=False,
        turn_costs=None,
        max_cost=None
    )

    # sp.reachable_nodes()
    path = sp.path_to_node(stop)

    for link in path:
        link["#bana"] = bana
        link.reverse_link["#bana"] = bana


scenario.publish_network(network)