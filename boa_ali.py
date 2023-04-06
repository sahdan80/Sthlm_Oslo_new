#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Sahlgren 2022, WSP

import emme_functions.emme as emme
import emme_functions.emme_functions
import emme_functions.emme_functions as ef
import emme_functions.auxiliary_functions as aux
import pandas as pd
import inro
import os
import pickle
from emme_functions.emme_functions import line_link_list as link_list
import inro.modeller as _m
from inro.emme.desktop import app as _app
import inro.emme.database.emmebank as _emmebank

# R:/7055/10350700/5_Berakningar/Sampers/Rigg/Person2017_255_Nulage_230223
name_of_project = "BP_2017_boa_ali_230406"
# project = 'D:/10350700_255_AE_DS/Person2040_255_JA_230302/E444bank//%s//%s//'
project = 'R:/7055/10350700/5_Berakningar/Sampers/Rigg/Person2017_255_Nulage_230223_Resultatriggning/E443bank/%s/%s/'
regional_bases =["Palt", "Samm", "Skane", "Sydost", "Vast"]
# regional_bases =["Samm"]
# regional_bases =["Palt"]
# my_desktop = _app.start_dedicated(project='R:/7055/10350700/5_Berakningar/Sampers/Rigg/Person2017_255_Nulage_230223_Resultatriggning/E443bank/UA/NB/Jvg/Jvg.emp', visible=False, user_initials="ds")
my_desktop = _app.start_dedicated(project='R:/7055/10350700/5_Berakningar/Sampers/Rigg/Person2017_255_Nulage_230223_Resultatriggning/E443bank/UA/NB/Jvg/Jvg.emp', visible=False, user_initials="ds")
my_modeller = _m.Modeller(my_desktop)
print(my_desktop.version)
# scenarios = [1001]

scen_id = 1101
# decide if UA and/or JA sjould be analyzed
# scenario_ja_ua = ["JA", "UA"]
# scenario_ja_ua = ["UA"]
scenario_ja_ua = ["UA"]


nodes = {"JA": {}, "UA": {}}
# year_factor = 365
year_factor = 1

modes = ["i","j","k"]
#loop over regional models


for ja_ua in scenario_ja_ua:

    with _emmebank.Emmebank(project %(ja_ua,"NB") + "/Jvg/emmebank") as eb:
        node_names = {}

        scen = eb.scenario(scen_id)
        my_network = scen.get_network()

        my_network.create_attribute("NODE", "transfers_boa", default_value=0)
        my_network.create_attribute("NODE", "transfers_ali", default_value=0)
        my_network.create_attribute("NODE", "transit_boardings", default_value=0)
        my_network.create_attribute("TRANSIT_SEGMENT", "transit_alightings", default_value=0)
        my_network.create_attribute("NODE", "transit_alightings", default_value=0)

        # nodes[ja_ua] = {"nationell": {}}


        for line in my_network.transit_lines():
            if line.mode.id in modes:
                segments = line.segments(True)
                seg = next(segments)
                for next_seg in segments:
                    next_seg.transit_alightings = seg.transit_volume - next_seg.transit_volume + next_seg.transit_boardings
                    seg = next_seg

        for node in my_network.nodes():
            if node.is_centroid == False:

                ca_ali_i = 0

                for seg in node.outgoing_segments(include_hidden=True):
                    if seg.line.mode.id in modes:
                        ca_ali_i += seg.transit_alightings

                node.transfers_ali = ca_ali_i - node.final_alightings
                node.transit_alightings = ca_ali_i

                ca_board_i = 0
                for seg in node.outgoing_segments():
                    if seg.line.mode.id in modes:
                        ca_board_i += seg.transit_boardings

                node.transfers_boa = ca_board_i - node.initial_boardings
                node.transit_boardings = ca_board_i

                nodes[ja_ua][node.id] = {}
                # # nodes[ja_ua][node.id]["base"] = "nationell"


                # nodes[ja_ua][node.id]["boa_tot"] = 0
                nodes[ja_ua][node.id]["boa_tot"] = ca_board_i #TODO set back to this
                nodes[ja_ua][node.id]["boa_transfers"] = node.transfers_boa
                nodes[ja_ua][node.id]["boa_initial"] = node.initial_boardings
                nodes[ja_ua][node.id]["ali_tot"] = ca_ali_i
                nodes[ja_ua][node.id]["ali_transfers"] = node.transfers_ali
                nodes[ja_ua][node.id]["ali_final"] = node.final_alightings
                nodes[ja_ua][node.id]["ali_boa_tot"] = ca_board_i + ca_ali_i
                nodes[ja_ua][node.id]["station"] = node["#station"]
                # if any(node["#station"] == item for item in stations_sel):
                #     nodes[ja_ua][node.id]["station_selection"] = True


            # if ja_ua=="UA": # get station names from UA (needs to be one of JA or UA in national base (stations not imported to regional bases)
            #     node_names[node.id] = node["#station"]

    for regional_base in regional_bases:
        # project_file = project %(ja_ua, "RB") + regional_base + "//Koll//Koll.emp"

        with _emmebank.Emmebank(project %(ja_ua,"RB")  + regional_base + "//Koll/emmebank") as eb:

            scen = eb.scenario(scen_id)
            my_network = scen.get_network()
            my_network.create_attribute("NODE", "transfers_boa", default_value=0)
            my_network.create_attribute("NODE", "transfers_ali", default_value=0)
            my_network.create_attribute("NODE", "transit_boardings", default_value=0)
            my_network.create_attribute("TRANSIT_SEGMENT", "transit_alightings", default_value=0)
            my_network.create_attribute("NODE", "transit_alightings", default_value=0)

            for line in my_network.transit_lines():
                if line.mode.id in modes:
                    segments = line.segments(True)
                    seg = next(segments)
                    for next_seg in segments:
                        next_seg.transit_alightings = seg.transit_volume - next_seg.transit_volume + next_seg.transit_boardings
                        seg = next_seg

            for node in my_network.nodes():
                if node.is_centroid == False:
                    # calculate total alightings and transfer alightings
                    ca_ali_i = 0
                    for seg in node.outgoing_segments(include_hidden=True):
                        if seg.line.mode.id in modes:
                            ca_ali_i += seg.transit_alightings
                    node.transfers_ali = ca_ali_i - node.final_alightings
                    node.transit_alightings = ca_ali_i
                    # calculate total boardings and transfer boardings

                    ca_board_i = 0
                    for seg in node.outgoing_segments():
                        if seg.line.mode.id in modes:
                            ca_board_i += seg.transit_boardings
                    node.transfers_boa = ca_board_i - node.initial_boardings
                    node.transit_boardings = ca_board_i

            # for node in my_network.nodes():
            #     if node.id in nodes[ja_ua]: # check if node is in dictionary. If not this means that the node does not exist in national base and thus should be skipped
                    if node.id in nodes[ja_ua]: #there are more nodes in regional base than in national base
                        # nodes[ja_ua][node.id]["base"] = regional_base
                        nodes[ja_ua][node.id]["boa_tot"] += ca_board_i
                        nodes[ja_ua][node.id]["boa_transfers"] += node.transfers_boa
                        nodes[ja_ua][node.id]["boa_initial"] += node.initial_boardings
                        nodes[ja_ua][node.id]["ali_tot"] += ca_ali_i
                        nodes[ja_ua][node.id]["ali_transfers"] += node.transfers_ali
                        nodes[ja_ua][node.id]["ali_final"] += node.final_alightings
                        nodes[ja_ua][node.id]["ali_boa_tot"] += (ca_board_i + ca_ali_i)

                else:
                # except KeyError: # there are nodes in regional bases that dont exist in national. skip these
                    pass


        # convert to year numbers

    for node in nodes[ja_ua]:
        for key_, val_ in nodes[ja_ua][node].items():

            if key_ in ["station", "station_selection"]:
                # print("passed")
                pass

            else:
                nodes[ja_ua][node][key_] *= year_factor

summary_ja = pd.DataFrame.from_dict(nodes["JA"], orient="index")
summary_ja["scenario"] = "JA"

summary_ua = pd.DataFrame.from_dict(nodes["UA"], orient="index")
summary_ua["scenario"] = "UA"

# summarize_nodes = {"JA", "UA"}
# for node, station in node_names.items():
#     if station !="":
#         summarize_nodes[station] = {"boa": 0, "ali": 0}
#         summarize_nodes[station] +=


summary = pd.concat([summary_ja, summary_ua])
summary.index.name='node_id'
csv_name = "boa_ali_%s.csv" % name_of_project
summary.to_csv(csv_name, sep=";", encoding="utf-8")

emme_functions.auxiliary_functions.addUTF8Bom(csv_name)

print("done")


