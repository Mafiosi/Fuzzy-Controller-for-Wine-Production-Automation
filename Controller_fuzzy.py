##############################
##        LIBRARIES         ##
##############################

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import skfuzzy as fuzz
import skfuzzy.control as control
from queue import Queue
import time
import array as arr
import datetime
import threading


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
    special_inout_3 = ['BAD', 'MEDIUM', 'GOOD']
    temp_in_3 = ['NEG', 'OK', 'POS']
    standard_in_5 = ['BIG LOW', 'LOW', 'MEDIUM', 'HIGH', 'BIG HIGH']
    standard_out_3 = ['BAD', 'MEDIUM', 'GOOD']

    ##############################
    ####  DENSITY

    # MEMBERSHIPS
    time_var = control.Antecedent(np.arange(0, 1.01, 0.01), 'time_var')
    density_error = control.Antecedent(np.arange(0, 1.01, 0.01), 'density_error')
    density_out = control.Consequent(np.arange(0, 1.01, 0.01), 'density_out')

    # MEMBERSHIP SHAPE
    time_var['BIG LOW'] = fuzz.trapmf(time_var.universe, [0, 0, 0.1, 0.3])
    time_var['LOW'] = fuzz.trimf(time_var.universe, [0.1, 0.3, 0.5])
    time_var['MEDIUM'] = fuzz.trimf(time_var.universe, [0.3, 0.5, 0.7])
    time_var['HIGH'] = fuzz.trimf(time_var.universe, [0.5, 0.7, 0.9])
    time_var['BIG HIGH'] = fuzz.trapmf(time_var.universe, [0.7, 0.9, 1, 1])

    density_error['LOW'] = fuzz.trapmf(density_error.universe, [0, 0, 0.2, 0.5])
    density_error['MEDIUM'] = fuzz.trimf(density_error.universe, [0.2, 0.5, 0.8])
    density_error['HIGH'] = fuzz.trapmf(density_error.universe, [0.5, 0.8, 1, 1])

    density_out['BAD'] = fuzz.trapmf(density_out.universe, [0, 0, 0.2, 0.5])
    density_out['MEDIUM'] = fuzz.trimf(density_out.universe, [0.2, 0.5, 0.8])
    density_out['GOOD'] = fuzz.trapmf(density_out.universe, [0.5, 0.8, 1, 1])


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
    color_error['BIG LOW'] = fuzz.trapmf(color_error.universe, [0, 0, 0.1, 0.3])
    color_error['LOW'] = fuzz.trimf(color_error.universe, [0.1, 0.3, 0.5])
    color_error['MEDIUM'] = fuzz.trapmf(color_error.universe, [0.3, 0.5, 0.6, 0.8])
    color_error['HIGH'] = fuzz.trapmf(color_error.universe, [0.6, 0.8, 1, 1])

    color_out['BAD'] = fuzz.trapmf(color_out.universe, [0, 0, 0.2, 0.5])
    color_out['MEDIUM'] = fuzz.trimf(color_out.universe, [0.2, 0.5, 0.8])
    color_out['GOOD'] = fuzz.trapmf(color_out.universe, [0.5, 0.8, 1, 1])


    # RULES
    rule_color_1 = control.Rule(time_var['BIG LOW'], color_out['GOOD'])
    rule_color_2 = control.Rule(time_var['LOW'], color_out['GOOD'])
    rule_color_3 = control.Rule(time_var['MEDIUM'] & color_error['HIGH'], color_out['MEDIUM'])
    rule_color_4 = control.Rule(time_var['MEDIUM'] & (color_error['MEDIUM'] | color_error['LOW'] | color_error['BIG LOW']), color_out['GOOD'])
    rule_color_5 = control.Rule(time_var['HIGH'] & color_error['HIGH'], color_out['BAD'])
    rule_color_6 = control.Rule(time_var['HIGH'] & color_error['MEDIUM'], color_out['MEDIUM'])
    rule_color_7 = control.Rule(time_var['HIGH'] & color_error['LOW'], color_out['GOOD'])
    rule_color_8 = control.Rule(time_var['BIG HIGH'] & (color_error['HIGH'] | color_error['MEDIUM']), color_out['BAD'])
    rule_color_9 = control.Rule(time_var['BIG HIGH'] & color_error['LOW'], color_out['MEDIUM'])
    rule_color_10 = control.Rule(time_var['HIGH'] & color_error['BIG LOW'], color_out['GOOD'])
    rule_color_11 = control.Rule(color_error['BIG LOW'], color_out['GOOD'])


    # CONTROL SYSTEM
    color_control = control.ControlSystem([rule_color_1, rule_color_2, rule_color_3, rule_color_4,
                                           rule_color_5, rule_color_6, rule_color_7, rule_color_8,
                                           rule_color_9, rule_color_10, rule_color_11])

    color = control.ControlSystemSimulation(color_control)

    ##############################
    ####  TANINS
    # MEMBERSHIPS
    # TIME_VAR ALREADY CREATED BEFORE IN DENSITY
    tanins_error = control.Antecedent(np.arange(0, 1.01, 0.01), 'tanins_error')
    tanins_out = control.Consequent(np.arange(0, 1.01, 0.01), 'tanins_out')

    # MEMBERSHIP SHAPE
    # TIME_VAR ALREADY DEFINED BEFORE IN DENSITY
    tanins_error['BIG LOW'] = fuzz.trapmf(tanins_error.universe, [0, 0, 0.1, 0.3])
    tanins_error['LOW'] = fuzz.trimf(tanins_error.universe, [0.1, 0.3, 0.5])
    tanins_error['MEDIUM'] = fuzz.trapmf(tanins_error.universe, [0.3, 0.5, 0.6, 0.8])
    tanins_error['HIGH'] = fuzz.trapmf(tanins_error.universe, [0.6, 0.8, 1, 1])

    tanins_out['BAD'] = fuzz.trapmf(tanins_out.universe, [0, 0, 0.2, 0.5])
    tanins_out['MEDIUM'] = fuzz.trimf(tanins_out.universe, [0.2, 0.5, 0.8])
    tanins_out['GOOD'] = fuzz.trapmf(tanins_out.universe, [0.5, 0.8, 1, 1])

    # RULES
    rule_tanins_1 = control.Rule(time_var['BIG LOW'], tanins_out['GOOD'])
    rule_tanins_2 = control.Rule(time_var['LOW'], tanins_out['GOOD'])
    rule_tanins_3 = control.Rule(time_var['MEDIUM'] & tanins_error['HIGH'], tanins_out['MEDIUM'])
    rule_tanins_4 = control.Rule(time_var['MEDIUM'] & (tanins_error['MEDIUM'] | tanins_error['LOW'] | tanins_error['BIG LOW']), tanins_out['GOOD'])
    rule_tanins_5 = control.Rule(time_var['HIGH'] & tanins_error['HIGH'], tanins_out['BAD'])
    rule_tanins_6 = control.Rule(time_var['HIGH'] & tanins_error['MEDIUM'], tanins_out['MEDIUM'])
    rule_tanins_7 = control.Rule(time_var['HIGH'] & tanins_error['LOW'], tanins_out['GOOD'])
    rule_tanins_8 = control.Rule(time_var['BIG HIGH'] & (tanins_error['HIGH'] | tanins_error['MEDIUM']), tanins_out['BAD'])
    rule_tanins_9 = control.Rule(time_var['BIG HIGH'] & tanins_error['LOW'], tanins_out['MEDIUM'])
    rule_tanins_10 = control.Rule(tanins_error['BIG LOW'], tanins_out['GOOD'])
    rule_tanins_11 = control.Rule(time_var['HIGH'] & tanins_error['BIG LOW'], tanins_out['GOOD'])

    # CONTROL SYSTEM
    tanins_control = control.ControlSystem([rule_tanins_1, rule_tanins_2, rule_tanins_3, rule_tanins_4,
                                            rule_tanins_5, rule_tanins_6, rule_tanins_7, rule_tanins_8,
                                            rule_tanins_9, rule_tanins_10, rule_tanins_11])

    tanins = control.ControlSystemSimulation(tanins_control)

    ##############################
    ####  REMONTAGEM

    # MEMBERSHIPS
    color_in = control.Antecedent(np.arange(0, 1.01, 0.01), 'color_in')
    tanins_in = control.Antecedent(np.arange(0, 1.01, 0.01), 'tanins_in')
    remontagem_out = control.Consequent(np.arange(0, 1.01, 0.01), 'remontagem_out')

    # MEMBERSHIP SHAPE (TANINS NAME DEPEND ON TABLE USE)
    color_in['BAD'] = fuzz.trapmf(color_in.universe, [0, 0, 0.2, 0.5])
    color_in['MEDIUM'] = fuzz.trimf(color_in.universe, [0.2, 0.5, 0.8])
    color_in['GOOD'] = fuzz.trapmf(color_in.universe, [0.5, 0.8, 1, 1])

    tanins_in['LOW'] = fuzz.trapmf(tanins_in.universe, [0, 0, 0.2, 0.5])
    tanins_in['OK'] = fuzz.trimf(tanins_in.universe, [0.2, 0.5, 0.8])
    tanins_in['HIGH'] = fuzz.trapmf(tanins_in.universe, [0.5, 0.8, 1, 1])

    remontagem_out['NAO'] = fuzz.trapmf(remontagem_out.universe, [0, 0, 0.2, 0.2])
    remontagem_out['SIM'] = fuzz.trapmf(remontagem_out.universe, [0.8, 0.8, 1, 1])

    # RULES (TANINS NAME DEPEND ON TABLE USE)
    rule_remontagem_1 = control.Rule(color_in['GOOD'], remontagem_out['NAO'])
    rule_remontagem_2 = control.Rule(color_in['BAD'], remontagem_out['SIM'])
    rule_remontagem_3 = control.Rule(color_in['MEDIUM'] & tanins_in['HIGH'], remontagem_out['NAO'])
    rule_remontagem_4 = control.Rule(color_in['MEDIUM'] & (tanins_in['OK'] | tanins_in['LOW']), remontagem_out['SIM'])

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

    temp_in['NEG'] = fuzz.trapmf(temp_in.universe, [0, 0, 0.4, 0.5])
    temp_in['OK'] = fuzz.trimf(temp_in.universe, [0.4, 0.5, 0.6])
    temp_in['POS'] = fuzz.trapmf(temp_in.universe, [0.5, 0.6, 1, 1])

    density_in['BAD'] = fuzz.trapmf(density_in.universe, [0, 0, 0.2, 0.5])
    density_in['MEDIUM'] = fuzz.trimf(density_in.universe, [0.2, 0.5, 0.8])
    density_in['GOOD'] = fuzz.trapmf(density_in.universe, [0.5, 0.8, 1, 1])

    chiller_out['NAO'] = fuzz.trapmf(chiller_out.universe, [0, 0, 0.2, 0.2])
    chiller_out['SIM'] = fuzz.trapmf(chiller_out.universe, [0.8, 0.8, 1, 1])

    # RULES
    rule_chiller_1 = control.Rule(temp_in['NEG'], chiller_out['NAO'])
    rule_chiller_2 = control.Rule(temp_in['POS'], chiller_out['SIM'])
    rule_chiller_3 = control.Rule(temp_in['OK'] & color_in['BAD'] & density_in['BAD'], chiller_out['NAO'])
    rule_chiller_4 = control.Rule(temp_in['OK'] & color_in['BAD'] & (density_in['MEDIUM'] | density_in['GOOD']), chiller_out['SIM'])
    rule_chiller_5 = control.Rule(temp_in['OK'] & color_in['MEDIUM'] & density_in['GOOD'], chiller_out['SIM'])
    rule_chiller_6 = control.Rule(temp_in['OK'] & color_in['GOOD'], chiller_out['NAO'])
    rule_chiller_7 = control.Rule(temp_in['OK'] & color_in['MEDIUM'] & (density_in['BAD'] | density_in['MEDIUM']), chiller_out['NAO'])

    # CONTROL SYSTEM
    chiller_control = control.ControlSystem([rule_chiller_1, rule_chiller_2, rule_chiller_3, rule_chiller_4,
                                             rule_chiller_5, rule_chiller_6, rule_chiller_7])

    chiller = control.ControlSystemSimulation(chiller_control)

    ##############################
    ##   EOF FUZZY DEFINITION   ##
    ##############################

    return time_var, density_error, density_out, density_control, density, \
           color_error, color_out, color_control, color, \
           tanins_error, tanins_out, tanins_control, tanins, \
           color_in, tanins_in, remontagem_out, remontagem_control, remontagem, \
           temp_in, density_in, chiller_out, chiller_control, chiller


# GET INPUTS FROM MAIN PROGRAM
def get_input(communication_queue, values, interval, first_run):

    # WAIT FOR MESSAGE FROM MAIN PROGRAM
    # -1 - SENSOR INPUT
    # -2 - CHANGE OF REFERENCE VALUES

    while True:

        rule = communication_queue.get(True, 5)

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
                temp = communication_queue.get()
                if temp != -1:
                    values[i] = temp
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

    if first_run:
        interval[0] = values[5] - values[0]         # DENSITY       INTERVAL
        interval[1] = values[1] - values[6]         # COLOR         INTERVAL
        interval[2] = 20                            # TEMPERATURE   INTERVAL
        interval[3] = values[4] - values[8]         # TANINS        INTERVAL

    return values, interval


# NORMALIZE VALUES
def norm_and_error(communication_queue, values, results_in, initial_date, interval):

    # NORMALIZE DENSITY
    error = (values[5] - values[0])/interval[0]
    if error > 1:
        communication_queue.put(-2)
        results_in[0] = 1
    elif error < -1:
        communication_queue.put(-2)
        results_in[0] = 1
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
        results_in[1] = 0
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
        results_in[2] = 1
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
        results_in[4] = 0
    elif error < 0:
        communication_queue.put(-9)
        results_in[4] = abs(error)
    else:
        results_in[4] = error

    return results_in


# SIMULATE FUZZY USING NORMALIZED VALUES
def fuzzy_work(results_in, density, color, tanins, remontagem, chiller):

    # DENSITY MEMBERSHIP
    density.input['time_var'] = results_in[3]
    density.input['density_error'] = results_in[0]
    # COLOR MEMBERSHIP
    color.input['time_var'] = results_in[3]
    color.input['color_error'] = results_in[1]
    # TANINS MEMBERSHIP
    tanins.input['time_var'] = results_in[3]
    tanins.input['tanins_error'] = results_in[4]

    # COMPUTE FIRST INPUTS
    density.compute()
    color.compute()
    tanins.compute()

    # REMONTAGEM MEMBERSHIP
    remontagem.input['color_in'] = color.output['color_out']
    remontagem.input['tanins_in'] = tanins.output['tanins_out']
    # CHILLER MEMBERSHIP
    chiller.input['density_in'] = density.output['density_out']
    chiller.input['color_in'] = color.output['color_out']
    chiller.input['temperature_in'] = results_in[2]

    # COMPUTE FINAL INPUTS
    remontagem.compute()
    chiller.compute()

    return density, color, tanins, remontagem, chiller


# PROCESS FINALS RESULT INTERPRETATION
def process_results(communication_queue, remontagem, chiller, remontagem_threshold, chiller_threshold):

    # NOTIFY OF GOOD RESULT
    communication_queue.put(1)

    # VERIFY IF REMONTAGEM RESULT IS ABOVE THRESHOLD
    if remontagem.output['remontagem_out'] > remontagem_threshold:
        communication_queue.put(1)
    else:
        communication_queue.put(0)

    # VERIFY IF CHILLER RESULT IS ABOVE THRESHOLD
    if chiller.output['chiller_out'] > chiller_threshold:
        communication_queue.put(1)
    else:
        communication_queue.put(0)


# PRINT RESULTS
def print_results(time_var, density_error, density_out, density_control, density, color_error, color_out, color_control,
                  color, tanins_error, tanins_out, tanins_control, tanins, color_in, tanins_in, remontagem_out,
                  remontagem_control, remontagem, temp_in, density_in, chiller_out, chiller_control, chiller):

    # GENERIC FUNCTIONS EXAMPLES
    if False:
        time_var.view()
        density_error.view()
        density_out.view()
        chiller_out.view()

    # INPUTS SIMULATION

    # DENSITY
    if False:
        time_var.view(sim=density)
        density_error.view(sim=density)
        density_out.view(sim=density)
        density_control.view()

        # DENSITY SAMPLING
        space = np.linspace(0, 1.1, 21)
        x, y = np.meshgrid(space, space)
        z = np.zeros_like(x)

        # Loop through the system 21*21 times to collect the control surface
        for i in range(21):
            for j in range(21):
                density.input['time_var'] = x[i, j]
                density.input['density_error'] = y[i, j]
                density.compute()
                z[i, j] = density.output['density_out']

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis',
                        linewidth=0.4, antialiased=True)
        ax.contourf(x, y, z, zdir='z', offset=3, cmap='viridis', alpha=0.5)
        ax.contourf(x, y, z, zdir='x', offset=3, cmap='viridis', alpha=0.5)
        ax.contourf(x, y, z, zdir='y', offset=3, cmap='viridis', alpha=0.5)
        ax.set_zlim(0, 1)
        ax.view_init(30, 60)
        plt.show()


    # COLOR
    if False:
        time_var.view(sim=color)
        color_error.view(sim=color)
        color_out.view(sim=color)
        color_control.view()

    # TANINS
    if False:
        time_var.view(sim=tanins)
        tanins_error.view(sim=tanins)
        tanins_out.view(sim=tanins)
        tanins_control.view()

    # REMONTAGEM
    if True:
        color_in.view(sim=remontagem)
        tanins_in.view(sim=remontagem)
        remontagem_out.view(sim=remontagem)
        remontagem_control.view()

    # CHILLER
    if True:
        temp_in.view(sim=chiller)
        density_in.view(sim=chiller)
        color_in.view(sim=chiller)
        chiller_out.view(sim=chiller)
        chiller_control.view()

        # CHILLER SAMPLING
        space = np.linspace(0, 1.1, 21)
        x, y = np.meshgrid(space, space)
        z = np.zeros_like(x)

        # Loop through the system 21*21 times to collect the control surface
        for i in range(21):
            for j in range(21):
                chiller.input['temperature_in'] = x[i, j]
                chiller.input['color_in'] = (1*0.7)
                chiller.input['density_in'] = y[i, j]
                chiller.compute()
                z[i, j] = chiller.output['chiller_out']

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x, y, z,label='something', rstride=1, cstride=1, cmap='viridis',
                        linewidth=0.4, antialiased=True)
        # ax.contourf(x, y, z, zdir='z', offset=3, cmap='viridis', alpha=0.5)
        # ax.contourf(x, y, z, zdir='x', offset=3, cmap='viridis', alpha=0.5)
        # ax.contourf(x, y, z, zdir='y', offset=3, cmap='viridis', alpha=0.5)
        ax.view_init(30, 200)
        ax.set_zlim(0, 1)
        ax.set_xlabel("Temperature", fontsize=18)
        ax.set_ylabel("Density", fontsize=18)
        ax.set_zlabel("Chiller", fontsize=18)
        plt.show()


# THIS IS THE MAIN CONTROL ROUTINE
def control_routine(communication_queue):

    ##############################
    ##     INPUT VARIABLES      ##
    ##############################
    # VARIABLES TO BE RECEIVED BY INITIAL CALL OF FUNCTION BY MAIN THREAD

    # communication_queue - Queue Variable


    ##############################
    ##     CONTROL VARIABLES    ##
    ##############################
    # VARIABLES TO CONTROL THE BEHAVIOUR OF THE PROGRAM

    use_sensor   = False    # USING SENSORS OR NOT - IF SIMULATING CHOOSE FALSE
    print_graphs = True     # PRINT GRAPHS FOR PRESENTATION
    first_run    = True        # WARNS OF FIRST RUN TRIALS - DO NOT CHANGE


    ##############################
    ##     GENERIC VARIABLES    ##
    ##############################
    # GENERIC VALUE TO BE USED BY MAIN FUNCTION

    values = arr.array('i', [0, 0, 0, 0, 0, 0, 0, 0, 0])
    interval = arr.array('i', [0, 0, 0, 0])
    results_in = arr.array('f', [0, 0, 0, 0, 0])
    initial_date = datetime.datetime.now()          # INITIAL DATE  REFERENCE


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
        values[2] = 26                          # TEMPERATURE   REFERENCE - CONSTANT VALUE FOR TEMPERATURE in ºC
        values[3] = 15                          # TIME          REFERENCE - FINAL VALUE FOR TIME in days
        values[4] = 2                           # TANINS        REFERENCE - VALUE FOR TANINS in percentage% / Volume
        values[5] = 1015                        # DENSITY       SENSOR
        values[6] = 300                         # COLOR         SENSOR
        values[7] = 28                          # TEMPERATURE   SENSOR
        values[8] = 1                           # TANINS        SENSOR
        interval[0] = 1085 - 995                #values[5] - values[0]     # DENSITY       INTERVAL
        interval[1] = 400                       #values[1] - values[6]     # COLOR         INTERVAL
        interval[2] = 10                        # TEMPERATURE   INTERVAL
        interval[3] = 2                         # values[4] - values[8]     # TANINS        INTERVAL

    # DEFINES THRESHOLD FOR FINAL EVALUATION
    remontagem_threshold = 0.7                  # REMONTAGEM    THRESHOLD FOR END VALUE
    chiller_threshold = 0.7                     # CHILLER       THRESHOLD FOR END VALUE


    ##############################
    ##   FUZZY INITIALIZATION   ##
    ##############################
    # INITIALIZE FUZZY CONTROL VARIABLES

    time_var, density_error, density_out, density_control, density, \
    color_error, color_out, color_control, color, \
    tanins_error, tanins_out, tanins_control, tanins, \
    color_in, tanins_in, remontagem_out, remontagem_control, remontagem, \
    temp_in, density_in, chiller_out, chiller_control, chiller = fuzzy_initialization()


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
            values, interval = get_input(communication_queue, values, interval, first_run)
            first_run = False


        # NORMALIZATION OF VALUES
        results_in = norm_and_error(communication_queue, values, results_in, initial_date, interval)

        # SET FUZZY TO SIMULATE
        density, color, tanins, remontagem, chiller = fuzzy_work(results_in, density, color, tanins,
                                                                 remontagem, chiller)

        process_results(communication_queue, remontagem, chiller, remontagem_threshold, chiller_threshold)

        if print_graphs:
            print_results(time_var, density_error, density_out, density_control, density,
                          color_error, color_out, color_control, color,
                          tanins_error, tanins_out, tanins_control, tanins,
                          color_in, tanins_in, remontagem_out, remontagem_control, remontagem,
                          temp_in, density_in, chiller_out, chiller_control, chiller)

        # EXITS PROGRAM IF ONLY A SIMULATION
        if not use_sensor:
            break


# DELETE WHEN INTEGRATING WITH CODE
if __name__ == "__main__":

    communication_queue = Queue()

    control_thread = threading.Thread(name='Control_Cycle', target=control_routine, args=(communication_queue,))
    control_thread.start()

    # PRINT RESULTS
    while True:

        results = []
        temp = communication_queue.get()

        print("ERROR LIST")
        # FINAL RESULTS
        if temp == 1:
            print("\nEOF ERROR LIST")
            temp = communication_queue.get()
            results.append(temp)
            print("REMONTAGEM WILL WORK = " + str(temp))
            temp = communication_queue.get()
            results.append(temp)
            print("CHILLER    WILL WORK = " + str(temp))
            break

        # ERROR RESULT
        else:
            temp = communication_queue.get()
            results.append(temp)
            print(temp)

    control_thread.join()
    print("FINISH")

