##############################
##        LIBRARIES         ##
##############################

import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import skfuzzy.control as control
from queue import Queue

##############################
##     EOF  LIBRARIES       ##
##############################


# INITIALIZATION OF CONTROLLER
def fuzzy_initialization(use_tanins):

    ##############################
    ##    FUZZY DEFINITION      ##
    ##############################
    # MEMBERSHIPS NAME LIST

    standard_in_3 = ['LOW', 'MEDIUM', 'HIGH']
    special_in_3 = ['LOW', 'OK', 'HIGH']
    special_inout_3 = ['BAD', 'MEDIUM', 'GOOD']
    temp_in_3 = ['NEG', 'OK', 'POS']
    standard_in_5 = ['BIG LOW', 'LOW', 'MEDIUM', 'HIGH', 'BIG HIGH']

    standard_out_3 = ['BAD', 'MEDIUM', 'GOOD']

    ##############################
    ####  DENSITY

    # MEMBERSHIPS
    time_var = control.Antecedent(np.arange(0, 1.01, 0.01), 'time_var')
    density_error = control.Antecedent(np.arange(0, 1.01, 0.01), 'density_error')
    density_out = control.Consequent(np.arange(0, 1.01, 0.01), 'density')

    # MEMBERSHIP SHAPE
    time_var.automf(5, 'quant', standard_in_5)
    density_error.automf(3, 'quant', standard_in_3)
    density_out.automf(3, 'quant', standard_out_3)

    # RULES
    rule_density_1 = control.Rule(time_var['BIG LOW'], density_out['GOOD'])
    rule_density_2 = control.Rule(time_var['LOW'], density_out['GOOD'])
    rule_density_3 = control.Rule(time_var['MEDIUM'] & density_error['HIGH'], density_out['MEDIUM'])
    rule_density_4 = control.Rule(time_var['MEDIUM'] & (density_error['MEDIUM'] | density_error['LOW']), density_out['GOOD'])
    rule_density_5 = control.Rule(time_var['HIGH'] & density_error['HIGH'], density_out['BAD'])
    rule_density_6 = control.Rule(time_var['HIGH'] & density_error['MEDIUM'], density_out['MEDIUM'])
    rule_density_7 = control.Rule(time_var['HIGH'] & density_error['LOW'], density_out['GOOD'])
    rule_density_8 = control.Rule(time_var['BIG HIGH'] & (density_error['HIGH'] | density_error['MEDIUM']), density_out['BAD'])
    rule_density_9 = control.Rule(time_var['BIG HIGH'] & density_error['LOW'], density_out['MEDIUM'])

    # CONTROL SYSTEM
    density_control = control.ControlSystem([rule_density_1, rule_density_2, rule_density_3, rule_density_4,
                                             rule_density_5, rule_density_6, rule_density_7, rule_density_8,
                                             rule_density_9])

    density = control.ControlSystemSimulation(density_control)

    ##############################
    ####  COLOR

    # MEMBERSHIPS
    # TIME_VAR ALREADY CREATED BEFORE IN DENSITY
    color_error = control.Antecedent(np.arange(0, 1.01, 0.01), 'color_error')
    color_out = control.Consequent(np.arange(0, 1.01, 0.01), 'color_out')

    # MEMBERSHIP SHAPE
    # TIME_VAR ALREADY DEFINED BEFORE IN DENSITY
    color_error.automf(3, 'quant', standard_in_3)
    color_out.automf(3, 'quant', standard_out_3)

    # RULES
    rule_color_1 = control.Rule(time_var['BIG LOW'], color_out['GOOD'])
    rule_color_2 = control.Rule(time_var['LOW'], color_out['GOOD'])
    rule_color_3 = control.Rule(time_var['MEDIUM'] & color_error['HIGH'], color_out['MEDIUM'])
    rule_color_4 = control.Rule(time_var['MEDIUM'] & (color_error['MEDIUM'] | color_error['LOW']), color_out['GOOD'])
    rule_color_5 = control.Rule(time_var['HIGH'] & color_error['HIGH'], color_out['BAD'])
    rule_color_6 = control.Rule(time_var['HIGH'] & color_error['MEDIUM'], color_out['MEDIUM'])
    rule_color_7 = control.Rule(time_var['HIGH'] & color_error['LOW'], color_out['GOOD'])
    rule_color_8 = control.Rule(time_var['BIG HIGH'] & (color_error['HIGH'] | color_error['MEDIUM']), color_out['BAD'])
    rule_color_9 = control.Rule(time_var['BIG HIGH'] & color_error['LOW'], color_out['MEDIUM'])

    # CONTROL SYSTEM
    color_control = control.ControlSystem([rule_color_1, rule_color_2, rule_color_3, rule_color_4,
                                           rule_color_5, rule_color_6, rule_color_7, rule_color_8,
                                           rule_color_9])

    color = control.ControlSystemSimulation(color_control)

    ##############################
    ####  TANINS
    if use_tanins:
        # MEMBERSHIPS
        # TIME_VAR ALREADY CREATED BEFORE IN DENSITY
        tanins_error = control.Antecedent(np.arange(0, 1.01, 0.01), 'tanins_error')
        tanins_out = control.Consequent(np.arange(0, 1.01, 0.01), 'tanins_out')

        # MEMBERSHIP SHAPE
        # TIME_VAR ALREADY DEFINED BEFORE IN DENSITY
        tanins_error.automf(3, 'quant', standard_in_3)
        tanins_out.automf(3, 'quant', standard_out_3)

        # RULES
        rule_tanins_1 = control.Rule(time_var['BIG LOW'], tanins_out['GOOD'])
        rule_tanins_2 = control.Rule(time_var['LOW'], tanins_out['GOOD'])
        rule_tanins_3 = control.Rule(time_var['MEDIUM'] & tanins_error['HIGH'], tanins_out['MEDIUM'])
        rule_tanins_4 = control.Rule(time_var['MEDIUM'] & (tanins_error['MEDIUM'] | tanins_error['LOW']), tanins_out['GOOD'])
        rule_tanins_5 = control.Rule(time_var['HIGH'] & tanins_error['HIGH'], tanins_out['BAD'])
        rule_tanins_6 = control.Rule(time_var['HIGH'] & tanins_error['MEDIUM'], tanins_out['MEDIUM'])
        rule_tanins_7 = control.Rule(time_var['HIGH'] & tanins_error['LOW'], tanins_out['GOOD'])
        rule_tanins_8 = control.Rule(time_var['BIG HIGH'] & (tanins_error['HIGH'] | tanins_error['MEDIUM']), tanins_out['BAD'])
        rule_tanins_9 = control.Rule(time_var['BIG HIGH'] & tanins_error['LOW'], tanins_out['MEDIUM'])

        # CONTROL SYSTEM
        tanins_control = control.ControlSystem([rule_tanins_1, rule_tanins_2, rule_tanins_3, rule_tanins_4,
                                                rule_tanins_5, rule_tanins_6, rule_tanins_7, rule_tanins_8,
                                                rule_tanins_9])

        tanins = control.ControlSystemSimulation(tanins_control)

    ##############################
    ####  REMONTAGEM

    # MEMBERSHIPS
    color_in = control.Antecedent(np.arange(0, 1.01, 0.01), 'color_in')
    tanins_in = control.Antecedent(np.arange(0, 1.01, 0.01), 'tanins_in')
    remontagem_out = control.Consequent(np.arange(0, 1.01, 0.01), 'remontagem_out')

    # MEMBERSHIP SHAPE (TANINS NAME DEPEND ON TABLE USE)
    color_in.automf(3, 'quant', special_inout_3)
    if use_tanins:
        tanins_in.automf(3, 'quant', special_inout_3)
    else:
        tanins_in.automf(3, 'quant', special_in_3)
    remontagem_out['NAO'] = fuzz.trapmf(remontagem_out.universe, [0, 0, 0.2, 0.2])
    remontagem_out['SIM'] = fuzz.trapmf(remontagem_out.universe, [0.8, 0.8, 1, 1])


    # RULES (TANINS NAME DEPEND ON TABLE USE)
    rule_remontagem_1 = control.Rule(color_in['GOOD'], remontagem_out['NAO'])
    rule_remontagem_2 = control.Rule(color_in['BAD'], remontagem_out['SIM'])
    if use_tanins:
        rule_remontagem_3 = control.Rule(color_in['MEDIUM'] & tanins_in['GOOD'], remontagem_out['NAO'])
        rule_remontagem_4 = control.Rule(color_in['MEDIUM'] & (tanins_in['MEDIUM'] | tanins_in['BAD']), remontagem_out['SIM'])
    else:
        rule_remontagem_3 = control.Rule(color_in['MEDIUM'] & tanins_in['HIGH'], remontagem_out['NAO'])
        rule_remontagem_4 = control.Rule(color_in['MEDIUM'] & (tanins_in['LOW'] | tanins_in['OK']), remontagem_out['SIM'])


    # CONTROL SYSTEM
    remontagem_control = control.ControlSystem([rule_remontagem_1, rule_remontagem_2, rule_remontagem_3, rule_remontagem_4])

    remontagem = control.ControlSystemSimulation(remontagem_control)

    ##############################
    ####  CHILL (DUDE)

    # MEMBERSHIPS
    # COLOR_IN ALREADY CREATED BEFORE IN REMONTAGEM
    temp_in = control.Antecedent(np.arange(0, 1.01, 0.01), 'temperature_in')
    density_in = control.Antecedent(np.arange(0, 1.01, 0.01), 'density_in')
    chiller_out = control.Consequent(np.arange(0, 1.01, 0.01), 'chiller_out')

    # MEMBERSHIP SHAPE
    # COLOR_IN ALREADY CREATED BEFORE IN REMONTAGEM
    temp_in.automf(3, 'quant', temp_in_3)
    density_in.automf(3, 'quant', special_inout_3)
    chiller_out['NAO'] = fuzz.trapmf(remontagem_out.universe, [0, 0, 0.2, 0.2])
    chiller_out['SIM'] = fuzz.trapmf(remontagem_out.universe, [0.8, 0.8, 1, 1])

    # RULES
    rule_chiller_1 = control.Rule(temp_in['NEG'], chiller_out['NAO'])
    rule_chiller_2 = control.Rule(temp_in['POS'], chiller_out['SIM'])
    rule_chiller_3 = control.Rule(temp_in['OK'] & color_in['BAD'] & density_in['BAD'], chiller_out['NAO'])
    rule_chiller_4 = control.Rule(temp_in['OK'] & color_in['BAD'] & (density_in['MEDIUM'] | density_in['GOOD']), chiller_out['SIM'])
    rule_chiller_5 = control.Rule(temp_in['OK'] & color_in['MEDIUM'] & density_in['GOOD'], chiller_out['SIM'])
    rule_chiller_6 = control.Rule(temp_in['OK'] & color_in['GOOD'], chiller_out['NAO'])

    # CONTROL SYSTEM
    chiller_control = control.ControlSystem([rule_chiller_1, rule_chiller_2, rule_chiller_3, rule_chiller_4,
                                             rule_chiller_5, rule_chiller_6])

    chiller = control.ControlSystemSimulation(chiller_control)

    ##############################
    ##   EOF FUZZY DEFINITION   ##
    ##############################

    if use_tanins:
        return density, color, tanins, remontagem, chiller
    else:
        return density, color, remontagem, chiller

# NORMALIZE VALUES
def normalize(density_ref, density_sensor, color_ref, color_sensor, temperature_ref, temperature_sensor,
              tanins_ref, tanins_sensor, time_ref):

    # NORMALIZE DENSITY




# THIS IS THE MAIN CONTROL ROUTINE
def control_routine(communication_queue):

    ##############################
    ##     INPUT VARIABLES      ##
    ##############################
    # VARIABLES TO BE RECEIVED BY INITIAL CALL OF FUNCTION BY MAIN THREAD

    # q          - Queue Variable Create One and pass values as such
    #                       from queue import Queue
    #                       q = Queue()
    #                       q.put(density_from_sensor)
    #                       q.put(color_from_sensor) and so forth (4 times)
    #                       use this order: density/color/temperature/tanins


    ##############################
    ##     CONTROL VARIABLES    ##
    ##############################
    # VARIABLES TO CONTROL IMPLEMENTATION OF FUZZY

    use_tanins = False      # USE TANINS TABLE OR NOT
    use_sensor = False      # SIMULATE USING SENSORS OR NOT


    ##############################
    ##     GENERIC VARIABLES    ##
    ##############################
    # GENERIC VALUE TO BE USED BY MAIN FUNCTION




    ##############################
    ##  REFERENCE DEFINITION    ##
    ##############################
    # DEFINE A REFERENCE FOR EACH VALUE

    if use_sensor:

        density_ref = communication_queue.get()
        color_ref = communication_queue.get()
        temperature_ref = communication_queue.get()
        tanins_ref = communication_queue.get()
        time_ref = communication_queue.get()

    # USE THIS TO SET INITIAL SIMULATION REFERENCES
    else:
        density_ref = 0.995     # FINAL VALUE FOR DENSITY in kg/L
        color_ref = 400         # FINAL VALUE FOR COLOR in NTU
        temperature_ref = 25    # CONSTANT VALUE FOR TEMPERATURE in ºC
        tanins_ref = 15         # VALUE FOR TANINS in percentage% / Volume
        time_ref = 15           # FINAL VALUE FOR TIME in days

    ##############################
    ##    INPUT DEFINITION      ##
    ##############################
    # DEFINES VALUES FROM SENSORS

    # WAIT FOR SENSOR INPUT
    if use_sensor:

        density_sensor = communication_queue.get()
        color_sensor = communication_queue.get()
        temperature_sensor = communication_queue.get()
        tanins_sensor = communication_queue.get()

    # USE THIS TO SET INITIAL SIMULATION VALUES
    else:

        density_sensor = 0.2
        color_sensor = 0.4
        temperature_sensor = 0.3
        tanins_sensor = 0.7

    # NORMALIZATION OF VALUES
    normalize(density_ref, density_sensor, color_ref, color_sensor, temperature_ref, temperature_sensor,
              tanins_ref, tanins_sensor, time_ref)

    ##############################
    ##   FUZZY INITIALIZATION   ##
    ##############################
    # INITIALIZE FUZZY CONTROL VARIABLES

    if use_tanins:
        density, color, tanins, remontagem, chiller = fuzzy_initialization(use_tanins)
    else:
        density, color, remontagem, chiller = fuzzy_initialization(use_tanins)

    while True:

        # WAIT FOR SENSOR INPUT
        if use_sensor:
            density_sensor = communication_queue.get()
            color_sensor = communication_queue.get()
            temperature_sensor = communication_queue.get()
            tanins_sensor = communication_queue.get()

        # USE THIS TO SIMULATE VALUES
        else:
            density_sensor = 0.2
            color_sensor = 0.4
            temperature_sensor = 0.3
            tanins_sensor = 0.7

        calculate_error()


