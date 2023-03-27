# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Sahlgren, WSP 2023
import emme_functions.emme as emme
import emme_functions.emme_functions as ef
import emme_functions.auxiliary_functions as aux
import pandas as pd

nbb_project = 'D://10350700_Oslo_Sthlm/Jvg/Jvg.emp'



my_emme = emme.Emme(nbb_project)
emmebank = my_emme.my_emmebank
UA1 = emmebank.scenario(3)
my_network = UA1.get_network()



def transit_lines(network):
    _transit_lines = []
    for _line in network.transit_lines():
        if ef.is_transit(_line):
            _transit_lines.append(_line)
    return _transit_lines


for line in transit_lines(my_network):
    print(line)
    name = ef.get_line_name(line)
    print(line)
    line.description = name




UA1.publish_network(my_network)

print("done")