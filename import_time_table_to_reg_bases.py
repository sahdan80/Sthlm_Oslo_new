#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Sahlgren 2022, WSP

import emme_functions.emme as emme
import emme_functions.emme_functions
import emme_functions.emme_functions as ef
import emme_functions.auxiliary_functions as aux
import pandas as pd8
import inro
import os
import pickle
from emme_functions.emme_functions import line_link_list as link_list
import inro.modeller as _m
from inro.emme.desktop import app as _app

import inro.emme.database.emmebank as _emmebank

# file_path_regional_bases = 'D:/10350700_255_AE_DS/UA1/E444bank/UA/RB/'
file_path_regional_bases = 'D:/10350700_255_AE_DS/UA2/E444bank/UA/RB/'
# transit_line_file_ = "D:/10350700_255_AE_DS/UA1/E444bank/UA/NB/Jvg/transit_lines_UA1.txt"
transit_line_file_ = "D:/10350700_255_AE_DS/UA2/E444bank/UA/NB/Jvg/transit_lines_UA2.txt"
regional_bases = ["Palt", "Samm", "Skane", "Sydost", "Vast"]
build = False # set to true if build file is to be imported
# build_file_path = "D:/10350700_255_AE_DS/Person2040_255_JA_230302/E444bank/UA/RB/Palt/Koll/"
# build_file = "build_reg_bases_sthlm_oslo_UA.ems"
# project_file_path = 'D:/10350700_255_AE_DS/UA1/E444bank/UA/NB/Jvg'
project_file_path = 'D:/10350700_255_AE_DS/UA2/E444bank/UA/NB/Jvg'
my_desktop = _app.start_dedicated(project=project_file_path + "/Jvg.emp", visible=False, user_initials="ds")
my_modeller = _m.Modeller(my_desktop)
print(my_desktop.version)
scenarios = [1001, 1002]
delete_modes ="jk"
# delete_modes ="ijk"
import_time_table = True
import_build_file = False

#
# #THIS PART IMPORTS TRANSIT LINE TRANSACTION FILE TO NATIONAL BASE.
# with _emmebank.Emmebank(project_file_path  + "//emmebank") as eb:
#     NAMESPACE = "inro.emme.data.network.transit.delete_transit_lines"
#     delete_lines = my_modeller.tool(NAMESPACE)
#
#
#     try:
#         delete_lines(selection="mode=ijk",
#                      scenario=eb.scenario(1001))
#         print("transit lines deleted")
#     except inro.emme.core.exception.ArgumentError: # if no lines exist accordning to selection
#         print("not transit lines deleted")
#         pass
#
#     NAMESPACE = "inro.emme.data.network.transit.transit_line_transaction"
#     process = my_modeller.tool(NAMESPACE)
#
#     try:
#         process(transaction_file=transit_line_file_,
#                 revert_on_error=False,
#                 scenario=eb.scenario(1001))
#     except inro.emme.core.exception.Error:
#         print(" no transaction file could be read")


# regional bases
for regional_base in regional_bases:
    project_file = file_path_regional_bases + regional_base + "//Koll//Koll.emp"
    print(project_file)

    with _emmebank.Emmebank(file_path_regional_bases + regional_base + "//Koll//emmebank") as eb:

        for scenario_nr in scenarios:
            print(scenario_nr)
            # NAMESPACE = "inro.emme.data.scenario.change_primary_scenario"
            # change_scenario = _m.Modeller().tool(NAMESPACE)
            # change_scenario(scenario=scenario_nr)

            NAMESPACE = "inro.emme.data.network.transit.delete_transit_lines"
            delete_lines = my_modeller.tool(NAMESPACE)
            try:
                delete_lines(selection="mode=" + delete_modes,
                             scenario=eb.scenario(scenario_nr))
                print("transit lines with mode=%s deleted" %delete_modes)
            except inro.emme.core.exception.ArgumentError:  # if no lines exist accordning to selection
                print("no transit lines deleted")
                pass
            # revert_on_error = False

            ## THIS SECTION IS FOR IMPORTING A BUILD FILE###
            if build:
                import os
                if import_build_file:
                    # proecess network builds
                    _m = inro.modeller
                    NAMESPACE = "inro.emme.data.network.process_network_build"
                    process = _m.Modeller().tool(NAMESPACE)
                    # project_path = os.path.dirname(_m.Modeller().desktop.project.path)
                    network_build = os.path.join(build_file_path, "Network_builds", build_file)
                    print(network_build)
                    # network_build_links = os.path.join(project_path, "Network_builds", "edit_links.ems")
                    try:
                        process(network_builds=[network_build],
                                revert_on_error=True,
                                scenarios=eb.scenario(scenario_nr))
                        print("build processed")
                    except inro.emme.core.exception.Error:
                        print("build not processed")
                        print(inro.emme.core.exception.Error)

            # process network transit line transaction file
            NAMESPACE = "inro.emme.data.network.transit.transit_line_transaction"
            process = my_modeller.tool(NAMESPACE)
            # default_path = os.path.dirname(modeller.emmebank.path).replace("\\", "/")
            # transit_line_file = os.path.join(default_path, "d221.in").replace("\\", "/")
            # process(transaction_file=transit_line_file_,
            #                 revert_on_error=True,
            #                 scenario=eb.scenario(scenario_nr))
            try:
                process(transaction_file=transit_line_file_,
                        revert_on_error=False,
                        scenario=eb.scenario(scenario_nr))
                print("transit transaction file imported")
            except inro.emme.core.exception.Error:
                print("no transaction file could be read")

            # print("transit line transaction file imported")

    print("done")
