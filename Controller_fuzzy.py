##############################
##        LIBRARIES         ##
##############################

import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import skfuzzy.control as control

##############################
##     EOF  LIBRARIES       ##
##############################
##############################
##     INPUT VARIABLES      ##
##############################

#HOW MUCH TIME WE HAVE
time_end = 15 + 1


##############################
##  EOF INPUT VARIABLES     ##
##############################
##############################
##    FUZZY DEFINITION      ##
##############################
#NAME LIST

standard_in_3 = ['LOW', 'MEDIUM', 'HIGH']
special_in_3 = ['BAD', 'MEDIUM', 'GOOD']
standard_in_5 = ['BIG LOW', 'LOW', 'MEDIUM', 'HIGH', 'BIG HIGH']
standard_out_2 = ['NAO', 'SIM']
standard_out_3 = ['BAD', 'MEDIUM', 'GOOD']


####  DENSITY

#MENBERSHIPS
time_var = control.Antecedent(np.arange(0, time_end, 0.01), 'time_var')
density_error = control.Antecedent(np.arange(0, 1, 0.01), 'density_error')
density_out = control.Consequent(np.arange(0, 1, 0.01), 'density')

#MENBERSHIP SHAPE
time_var.automf(5, 'quant', standard_in_5)
density_error.automf(3, 'quant', standard_in_3)
density_out.automf(3, 'quant', standard_out_3)

#RULES
rule_density_1 = control.Rule(time_var['BIG LOW'], density_out['GOOD'])
rule_density_2 = control.Rule(time_var['LOW'], density_out['GOOD'])
rule_density_3 = control.Rule(time_var['MEDIUM'] & density_error['HIGH'], density_out['MEDIUM'])
rule_density_4 = control.Rule(time_var['MEDIUM'] & (density_error['MEDIUM'] | density_error['LOW']), density_out['GOOD'])
rule_density_5 = control.Rule(time_var['HIGH'] & density_error['HIGH'], density_out['BAD'])
rule_density_6 = control.Rule(time_var['HIGH'] & density_error['MEDIUM'], density_out['MEDIUM'])
rule_density_7 = control.Rule(time_var['HIGH'] & density_error['LOW'], density_out['GOOD'])
rule_density_8 = control.Rule(time_var['BIG HIGH'] & (density_error['HIGH'] | density_error['MEDIUM']), density_out['BAD'])
rule_density_9 = control.Rule(time_var['BIG HIGH'] & density_error['LOW'], density_out['MEDIUM'])

#CONTROL SYSTEM
density_control = control.ControlSystem([rule_density_1, rule_density_2, rule_density_3, rule_density_4,
                                         rule_density_5, rule_density_6, rule_density_7, rule_density_8,
                                         rule_density_9])

density = control.ControlSystemSimulation(density_control)

####  DENSITY

#MENBERSHIPS
time_var = control.Antecedent(np.arange(0, time_end, 0.01), 'time_var')
density_error = control.Antecedent(np.arange(0, 1, 0.01), 'density_error')
density_out = control.Consequent(np.arange(0, 1, 0.01), 'density')

#MENBERSHIP SHAPE
time_var.automf(5, 'quant', standard_in_5)
density_error.automf(3, 'quant', standard_in_3)
density_out.automf(3, 'quant', standard_out_3)

#RULES
rule_density_1 = control.Rule(time_var['BIG LOW'], density_out['GOOD'])
rule_density_2 = control.Rule(time_var['LOW'], density_out['GOOD'])
rule_density_3 = control.Rule(time_var['MEDIUM'] & density_error['HIGH'], density_out['MEDIUM'])
rule_density_4 = control.Rule(time_var['MEDIUM'] & (density_error['MEDIUM'] | density_error['LOW']), density_out['GOOD'])
rule_density_5 = control.Rule(time_var['HIGH'] & density_error['HIGH'], density_out['BAD'])
rule_density_6 = control.Rule(time_var['HIGH'] & density_error['MEDIUM'], density_out['MEDIUM'])
rule_density_7 = control.Rule(time_var['HIGH'] & density_error['LOW'], density_out['GOOD'])
rule_density_8 = control.Rule(time_var['BIG HIGH'] & (density_error['HIGH'] | density_error['MEDIUM']), density_out['BAD'])
rule_density_9 = control.Rule(time_var['BIG HIGH'] & density_error['LOW'], density_out['MEDIUM'])

#CONTROL SYSTEM
density_control = control.ControlSystem([rule_density_1, rule_density_2, rule_density_3, rule_density_4,
                                         rule_density_5, rule_density_6, rule_density_7, rule_density_8,
                                         rule_density_9])

density = control.ControlSystemSimulation(density_control)

#EXAMPLE SIMULATION

density.input['time_var'] = 8
density.input['density_error'] = 0.2
density.compute()

print(density.output['density'])
density_out.view(sim=density)

##############################
##   EOF FUZZY DEFINITION   ##
##############################

