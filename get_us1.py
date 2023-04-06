

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
# project_file = 'D://10339171_NBB//5_Ber//NBB_Ue-Le_Huvudalternativ//E444bank//JA//NB//Jvg//Jvg.emp'
project_file = 'D:/10350700_255_AE_DS/Jvg_temp//Jvg.emp'
my_emme = emme.Emme(project_file)
my_emmebank = my_emme.my_emmebank
my_emme.my_desktop.version
scenario_id = 1001
# scen_ids = {"JA": 3, "UA": 1}




scenario = my_emmebank.scenario(scenario_id)

my_network = scenario.get_network()
rail_modes = ["i","j", "k"]

for link in my_network.links():
    if ef.check_link_mode(my_network, link, rail_modes) and link["#bana"]!= "":

        us1 = {"speed": {"i": [], "j":[], "k":[]}, "local":{"i":[], "j":[], "k":[]}, "other": {"i":[], "j":[], "k":[]}} # collect run times for ecah line on link based on train type
        lines_on_link = []
        for segment in link.segments():
            if ef.is_transit(segment.line):
                lines_on_link.append(segment.line.id)
                us1[segment.line["#train_type"]][segment.line.mode.id].append(segment.data1)
        # min_run_times = {"speed": min(us1["speed"]), "local": min(us1["local"]), "other": min(us1["other"])}
        if ef.is_transit(segment.line):
            min_run_times= {}
            for train_type, modes in us1.items():
                min_run_times[train_type] = {}
                for mode, us1_list in modes.items():
                    try:
                        min_run_times[train_type][mode] = min(us1_list)
                    except ValueError: # skip empty lists
                        pass

            for segment in link.segments():
                segment.data1 = min_run_times[segment.line["#train_type"]][segment.line.mode.id]