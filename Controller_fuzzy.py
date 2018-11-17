##############################
##        LIBRARIES         ##
##############################

import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import skfuzzy.control as control
from queue import Queue
import time
import array as arr
import datetime

##############################
##     EOF  LIBRARIES       ##
##############################


# INITIALIZATION OF CONTROLLER
def fuzzy_initialization():

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
    tanins_in.automf(3, 'quant', special_inout_3)
    remontagem_out['NAO'] = fuzz.trapmf(remontagem_out.universe, [0, 0, 0.2, 0.2])
    remontagem_out['SIM'] = fuzz.trapmf(remontagem_out.universe, [0.8, 0.8, 1, 1])


    # RULES (TANINS NAME DEPEND ON TABLE USE)
    rule_remontagem_1 = control.Rule(color_in['GOOD'], remontagem_out['NAO'])
    rule_remontagem_2 = control.Rule(color_in['BAD'], remontagem_out['SIM'])
    rule_remontagem_3 = control.Rule(color_in['MEDIUM'] & tanins_in['GOOD'], remontagem_out['NAO'])
    rule_remontagem_4 = control.Rule(color_in['MEDIUM'] & (tanins_in['MEDIUM'] | tanins_in['BAD']), remontagem_out['SIM'])

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

    return density, color, tanins, remontagem, chiller


# GET INPUTS FROM MAIN PROGRAM
def get_input(communication_queue, values):

    # WAIT FOR MESSAGE FROM MAIN PROGRAM
    # -1 - SENSOR INPUT
    # -2 - CHANGE OF REFERENCE VALUES

    while True:

        rule = communication_queue.get()

        # WILL RECEIVE SENSOR VALUE
        if rule == -1:
            for i in range(4):
                values[i+5] = communication_queue.get()
            break

            # values[5] --->  DENSITY       SENSOR
            # values[6] --->  COLOR         SENSOR
            # values[7] --->  TEMPERATURE   SENSOR
            # values[8] --->  TANINS        SENSOR

        # WILL RECEIVE REFERENCE VALUE
        if rule == -2:
            for i in range(5):
                values[i] = communication_queue.get()
            break

            # values[0] --->  DENSITY       REFERENCE
            # values[1] --->  COLOR         REFERENCE
            # values[2] --->  TEMPERATURE   REFERENCE
            # values[3] --->  TANINS        REFERENCE
            # values[4] --->  TIME          REFERENCE

        # RETURNS ERROR MESSAGE
        else:
            communication_queue.put(-1)
            time.sleep(2)

    return values


# NORMALIZE VALUES
def norm_and_error(communication_queue, values, results_in, initial_date, interval):

    # NORMALIZE DENSITY
    error = (values[5] - values[0])/interval[0]
    if error > 1:
        communication_queue.put(-2)
        results_in[0] = 1
    elif error < -1:
        communication_queue.put(-2)
        results_in[0] = -1
    elif error < 0:
        communication_queue.put(-3)
        results_in[0] = abs(error)
    else:
        results_in[0] = error

    # NORMALIZE COLOR
    error = (values[1] - values[6])/interval[1]
    if error > 1:
        communication_queue.put(-4)
        results_in[1] = 1
    elif error < -1:
        communication_queue.put(-4)
        results_in[1] = -1
    elif error < 0:
        communication_queue.put(-5)
        results_in[1] = abs(error)
    else:
        results_in[1] = error

    # NORMALIZE TEMPERATURE
    error = ((values[7] - values[2])/interval[2]) + 0.5
    if error > 1:
        communication_queue.put(-6)
        results_in[2] = 1
    elif error < -1:
        communication_queue.put(-6)
        results_in[2] = -1
    else:
        results_in[2] = abs(error)

    # NORMALIZE TIME
    elapsed_time = datetime.datetime.now() - initial_date
    normalized_elapsed = (elapsed_time.total_seconds()/(60*60*values[3]*24))
    if normalized_elapsed > 1:
        communication_queue.put(-7)
        results_in[3] = 1
    else:
        results_in[3] = normalized_elapsed

    # NORMALIZE TANINS
    error = (values[4] - values[8])/interval[3]
    if error > 1:
        communication_queue.put(-8)
        results_in[4] = 1
    elif error < -1:
        communication_queue.put(-8)
        results_in[4] = -1
    elif error < 0:
        communication_queue.put(-9)
        results_in[4] = abs(error)
    else:
        results_in[4] = error

    return results_in


# SIMULATE FUZZY USING NORMALIZED VALUES
def fuzzy_work(communication_queue, results_in, results_out, density, color, tanins, remontagem, chiller):


    return results_out


# THIS IS THE MAIN CONTROL ROUTINE
def control_routine(communication_queue):

    ##############################
    ##     INPUT VARIABLES      ##
    ##############################
    # VARIABLES TO BE RECEIVED BY INITIAL CALL OF FUNCTION BY MAIN THREAD

    # communication_queue - Queue Variable
    # HOW TO CREATE       - from queue import Queue
    #                       q = Queue()
    #                       q.put(density_from_sensor)
    #                       q.put(color_from_sensor) and so forth (4 times)
    #                       use this order: density/color/temperature/tanins


    ##############################
    ##     CONTROL VARIABLES    ##
    ##############################
    # VARIABLES TO CONTROL THE BEHAVIOUR OF THE PROGRAM

    use_sensor = False     # USING SENSORS OR NOT - IF SIMULATING CHOOSE FALSE
    all_good   = True      # GUARANTEES NO ERRORS ARE BEING MADE IN MIDDLE STAGES - NO TOUCH
    first_run  = True      # WARNS PROGRAM IT'S RUNNING FOR FIRST TIME


    ##############################
    ##     GENERIC VARIABLES    ##
    ##############################
    # GENERIC VALUE TO BE USED BY MAIN FUNCTION
    values = arr.array('i', [0, 0, 0, 0, 0, 0, 0, 0, 0])
    interval = arr.array('i', [0, 0, 0, 0])
    results_in = arr.array('i', [0, 0, 0, 0, 0])
    results_out = arr.array('B', [0, 0])
    initial_date = datetime.date.today()


    ##############################
    ##   FUZZY INITIALIZATION   ##
    ##############################
    # INITIALIZE FUZZY CONTROL VARIABLES

    density, color, tanins, remontagem, chiller = fuzzy_initialization()


    ##############################
    ##  REFERENCE DEFINITION    ##
    ##############################
    # DEFINE AN INITIAL REFERENCE FOR EACH VALUE

    if use_sensor:

        values[0] = communication_queue.get()       # DENSITY       REFERENCE
        values[1] = communication_queue.get()       # COLOR         REFERENCE
        values[2] = communication_queue.get()       # TEMPERATURE   REFERENCE
        values[3] = communication_queue.get()       # TIME          REFERENCE
        values[4] = communication_queue.get()       # TANINS        REFERENCE

    # USE THIS TO SET INITIAL SIMULATION REFERENCES
    else:
        values[0] = 995                         # DENSITY       REFERENCE - FINAL VALUE FOR DENSITY in kg/L
        values[1] = 400                         # COLOR         REFERENCE - FINAL VALUE FOR COLOR in NTU
        values[2] = 25                          # TEMPERATURE   REFERENCE - CONSTANT VALUE FOR TEMPERATURE in ºC
        values[3] = 15                          # TIME          REFERENCE - FINAL VALUE FOR TIME in days
        values[4] = 400                         # TANINS        REFERENCE - VALUE FOR TANINS in percentage% / Volume
        values[5] = 1080                        # DENSITY       SENSOR
        values[6] = 300                         # COLOR         SENSOR
        values[7] = 22                          # TEMPERATURE   SENSOR
        values[8] = 100                         # TANINS        SENSOR

    ##############################
    ##    MAIN CONTROL CYCLE    ##
    ##############################
    # WAITS FOR INPUTS, NORMALIZES, CALCULATES, SENDS DATA

    while True:

        ##############################
        ##    INPUT DEFINITION      ##
        ##############################

        # DEFINES VALUES FROM SENSORS
        if use_sensor:
            values = get_input(communication_queue, values)

        # DEFINES INTERVALS FOR ERROR REFERENCE
        if first_run:
            interval[0] = values[5] - values[0]  # DENSITY      INTERVAL
            interval[1] = values[1] - values[6]  # COLOR        INTERVAL
            interval[2] = 20                     # TEMPERATURE  INTERVAL
            interval[3] = values[4] - values[8]  # TANINS       INTERVAL
            first_run = False

        # NORMALIZATION OF VALUES
        results_in = norm_and_error(communication_queue, values, results_in, initial_date, interval)

        # SET FUZZY TO SIMULATE
        results_out = fuzzy_work(communication_queue, results_in, results_out, density, color, tanins,
                                 remontagem, chiller)



