from ipywidgets import interact
from ipywidgets import interactive
from IPython.display import clear_output
import ipywidgets as widgets
from make_runsheet import write_runsheet

import numpy as np
import pandas as pd

import os
import webbrowser

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def calc_stress(gain, area, targ_stress, init_volt):
    calibration = float(gain.value) * float(area.value)
    targ_volt = (calibration * np.fromstring(targ_stress.value, dtype=float, sep=',')) + float(init_volt.value)
    
    calibration = str(calibration)
    targ_volt = np.array2string(targ_volt, precision=5, separator=', ')[1:-1]
    
    return calibration, targ_volt

def calc_press(gain, targ_stress, init_volt):
    
    targ_volt = (np.fromstring(gain.value, dtype=float, sep=',') * np.fromstring(targ_stress.value, dtype=float, sep=',')) + np.fromstring(init_volt.value, dtype=float, sep=',')
    targ_volt = np.array2string(targ_volt, precision = 5, separator=', ')[1:-1]
    
    return targ_volt

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def entry_gui():
    
    style = {'description_width': 'initial'}
    sm_layout = widgets.Layout(flex='1 1 1%', width='auto')

    exp_name = widgets.Text(
        placeholder='pxxxx',
        description='Exp. Name:',
        continuous_update = True,
        disabled=False, 
        style=style)

    op_name = widgets.Text(
        placeholder='Name(s)',
        description='Operator Name(s):',
        continuous_update = True,
        disabled=False, 
        style=style)

    hyd_start = widgets.Text(
        placeholder='xxx.x',
        description='Hyd. Start:',
        continuous_update = True,
        disabled=False, 
        style=style)

    hyd_end = widgets.Text(
        placeholder='xxx.x',
        description='Hyd. End:',
        continuous_update = True,
        disabled=False, 
        style=style)

    pick_date = widgets.DatePicker(
        description='Exp. Date:',
        disabled=False, 
        style=style)

    names = widgets.VBox(children=[exp_name, op_name], layout=sm_layout)
    dates = widgets.VBox(children=[pick_date, hyd_start, hyd_end], layout=sm_layout)

    pre_layout = widgets.Layout(display='flex',
             flex_flow='row',
             align_items='stretch',
             border='2px solid grey',
             padding='10px',
             width='75%',
             grid_gap = '60px 60px')

    preamble = widgets.GridBox(children=[names, dates], layout=pre_layout)

    area = widgets.Text(
        placeholder='m^2',
        description='Contact Area (m^2)',
        value='', 
        continuous_update = True,
        disabled=False, 
        style=style)

    block_thck = widgets.Text(
        placeholder='mm',
        description='Sample Block Thickness (no gouge)',
        continuous_update = True,
        disabled=False, 
        style=style)

    layer_thck = widgets.Text(
        placeholder='mm',
        description='Layer Thickness',
        continuous_update = True,
        disabled=False, 
        style=style)

    layer_thck_ld = widgets.Text(
        placeholder='mm',
        description='Under Load',
        continuous_update = True,
        disabled=False, 
        style=style)

    material = widgets.Text(
        placeholder='Anhydrite, Westerly Granite',
        description='Material',
        continuous_update = True,
        disabled=False, 
        style=style)

    part_size = widgets.Text(
        placeholder='Size Distribution',
        description='Particle Size, Distribution',
        continuous_update = True,
        disabled=False, 
        style=style)

    mat_layout = widgets.Layout(display='flex',
             flex_flow='row',
             align_items='stretch',
             border='2px solid grey',
             padding='10px',
             width='75%',
             grid_gap = '60px 60px')

    mat_col1 = widgets.VBox(children=[area, block_thck, layer_thck], layout=widgets.Layout(flex='1 1 1%', width='auto'))
    mat_col2 = widgets.VBox(children = [material, part_size], layout=widgets.Layout(flex='1 1 1%', width='auto'))
    material_block = widgets.GridBox(children=[mat_col1, mat_col2], layout=mat_layout)

    h_lc_title = widgets.Label('Horizontal Load Cell')

    h_lc_picker = widgets.Dropdown(
        options=['44mm Solid Horiz', '44mm Solid Vert', 'None'],
        value='44mm Solid Horiz',
        description='Horiz. Load Cell:',
        disabled=False, 
        style=style)

    h_lc_calib = widgets.Text(
        placeholder='mV/kN',
        description='Calibration (mV/kN):',
        continuous_update = True,
        disabled=False, 
        style=style)

    h_lc_stress = widgets.Text(
        placeholder='MPa',
        description='Target Stress(es) (MPa):',
        continuous_update = True,
        disabled=False, 
        style=style)

    h_lc_ini_V = widgets.Text(
        placeholder='Volt',
        description='H. Init. Volt.:',
        continuous_update = True,
        disabled=False, 
        style=style)
    
    h_load_v =  widgets.Label(value='Volt. @ Load = ')
    
    def hor_handle_change(change):
        if str(change.new) == '' or str(change.new) == '--' or str(change.new) == '-':
            h_load_v.value = 'Volt. @ Load = N/A'
        else:
            _, targ_volt = calc_stress(h_lc_calib, area, h_lc_stress, h_lc_ini_V)
            h_load_v.value = 'Volt. @ Load = '+ targ_volt
    
    h_lc_ini_V.observe(hor_handle_change, names='value')

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

    v_lc_title = widgets.Label('Vertical Load Cell')

    v_lc_picker = widgets.Dropdown(
        options=['44mm Solid Vert', '44mm Solid Vert', 'None'],
        value='44mm Solid Vert',
        description='Vert. Load Cell:',
        disabled=False, 
        style=style)

    v_lc_calib = widgets.Text(
        placeholder='mV/kN',
        description='Calibration (mV/kN):',
        continuous_update = True,
        disabled=False, 
        style=style)

    v_lc_stress = widgets.Text(
        placeholder='MPa',
        description='Target Stress(es) (MPa):',
        continuous_update = True,
        disabled=False, 
        style=style)

    v_lc_ini_V = widgets.Text(
        placeholder='Volt',
        description='V. Init. Volt.:',
        continuous_update = True,
        disabled=False, 
        style=style)
    
    v_load_v =  widgets.Label(value='Volt. @ Load = ')
    
    def ver_handle_change(change):
        if str(change.new) == '' or str(change.new) == '--' or str(change.new) == '-':
            v_load_v.value = 'Volt. @ Load = N/A'
        else:
            _, targ_volt = calc_stress(v_lc_calib, area, v_lc_stress, v_lc_ini_V)
            v_load_v.value = 'Volt. @ Load = '+ targ_volt
            
    v_lc_ini_V.observe(ver_handle_change, names='value')

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

    pore_fluid = widgets.Text(
        value='DI H2O', 
        placeholder='DI H2O', 
        description='Pore Fluid', 
        continuous_update=True, 
        disabled=False, 
        style=style)

    vessel_title = widgets.Label('Confining Pressure')

    pc_gain = widgets.Text(
        value='0.1456',
        placeholder='0.1456 V/MPa',
        description='Pc Gain (V/MPa):',
        continuous_update = True,
        disabled=False, 
        style=style)

    pc_press = widgets.Text(
        placeholder='MPa',
        description='Target Stress(es) (MPa):',
        continuous_update = True,
        disabled=False, 
        style=style)

    pc_ini_V = widgets.Text(
        placeholder='Volt',
        description='V. Init. Volt.:',
        continuous_update = True,
        disabled=False, 
        style=style)
    
    pc_load_v =  widgets.Label(value='Volt. @ Load = ')
    
    def pc_handle_change(change):
        if str(change.new) == '' or str(change.new) == '--' or str(change.new) == '-':
            pc_load_v.value = 'Volt. @ Load = N/A'
        else:
            targ_volt = calc_press(pc_gain, pc_press, pc_ini_V)
            pc_load_v.value = 'Volt. @ Load = '+ targ_volt
            
    pc_ini_V.observe(pc_handle_change, names='value')

    pc_items = widgets.VBox(children=[vessel_title, pc_gain, pc_press, pc_ini_V, pc_load_v])

    ppa_gain = widgets.Text(
        placeholder='Ppa Gain (V/MPa)',
        description='Ppa Gain (V/MPa):',
        continuous_update = True,
        disabled=False, 
        style=style)

    ppa_press = widgets.Text(
        placeholder='MPa',
        description='PpA Press. (MPa)',
        continuous_update = True,
        disabled=False, 
        style=style)

    ppa_ini_V = widgets.Text(
        placeholder='Volt',
        description='V. Init. Volt.:',
        continuous_update = True,
        disabled=False, 
        style=style)

    ppa_load_v =  widgets.Label(value='Volt. @ Load = ')
    
    def ppa_handle_change(change):
        if str(change.new) == '' or str(change.new) == '--' or str(change.new) == '-':
            ppa_load_v.value = 'Volt. @ Load = N/A'
        else:
            targ_volt = calc_press(ppa_gain, ppa_press, ppa_ini_V)
            ppa_load_v.value = 'Volt. @ Load = '+ targ_volt
            
    ppa_ini_V.observe(ppa_handle_change, names='value')

    ppa_items = widgets.VBox(children=[vessel_title, ppa_gain, ppa_press, ppa_ini_V, ppa_load_v])

    ppb_gain = widgets.Text(
        placeholder='PpB Gain (V/MPa)',
        description='PpB Gain (V/MPa):',
        continuous_update = True,
        disabled=False, 
        style=style)

    ppb_press = widgets.Text(
        placeholder='MPa',
        description='PpB Press. (MPa)',
        continuous_update = True,
        disabled=False, 
        style=style)

    ppb_ini_V = widgets.Text(
        placeholder='Volt',
        description='V. Init. Volt.:',
        continuous_update = True,
        disabled=False, 
        style=style)

    ppb_load_v =  widgets.Label(value='Volt. @ Load = ')
    
    def ppb_handle_change(change):
        if str(change.new) == '' or str(change.new) == '--' or str(change.new) == '-':
            ppb_load_v.value = 'Volt. @ Load = N/A'
        else:
            targ_volt = calc_press(ppb_gain, ppb_press, ppb_ini_V)
            ppb_load_v.value = 'Volt. @ Load = '+ targ_volt
            
    ppb_ini_V.observe(ppb_handle_change, names='value')

    ppb_items = widgets.VBox(children=[pore_fluid, vessel_title, ppb_gain, ppb_press, ppb_ini_V, ppb_load_v])

    layout_args = {'flex_flow':'row',
         'padding':'10px',
         'width':'75%',
         'grid_gap':'60px'}
    
    layout2 = widgets.Layout(display='flex', **layout_args, border='2px solid royalblue')


    horizontal = widgets.VBox(children=[h_lc_title, h_lc_picker, h_lc_calib, h_lc_stress, h_lc_ini_V, h_load_v], layout=widgets.Layout(flex='1 1 0%', width='auto'))
    vertical = widgets.VBox(children=[v_lc_title, v_lc_picker, v_lc_calib, v_lc_stress, v_lc_ini_V, v_load_v], layout=widgets.Layout(flex='1 1 0%', width='auto'))

    layout = widgets.Layout(display='flex',
             flex_flow='row',
             align_items='stretch',
             border='2px solid grey',
             padding='10px',
             width='75%')

    hor_vert = widgets.GridBox(children=[horizontal, vertical], layout=layout)

    use_vessel = widgets.RadioButtons(
        options=['yes', 'no'],
        description='Use Vessel?',
        value='no',
        disabled=False)

    def vessel_input(a):
        pore_press=widgets.Label('')
        if a == 'yes':
            pore_press = widgets.GridBox(children=[pc_items, ppa_items, ppb_items], layout=layout2)
        return display(pore_press)

    vessel_params = widgets.interactive_output(vessel_input, {'a': use_vessel})

    data_logger = widgets.Dropdown(
        options=['8 channel', '16 channel'],
        value='8 channel',
        description='Data Logger Used:',
        disabled=False, 
        style=style)

    h_dcdt = widgets.Combobox(
        options=['short rod', 'long rod', 'None'],
        placeholder='Horiz. DCDT',
        ensure_option=True,
        description='Horiz. DCDT:',
        disabled=False, 
        style=style)

    h_dcdt_calib = widgets.Text(
        placeholder='mm/V',
        description='Horiz. DCDT calib.:',
        continuous_update = True,
        disabled=False, 
        style=style)

    v_dcdt = widgets.Combobox(
        options=['Trans-Tek2', 'None'],
        placeholder='Vert. DCDT',
        ensure_option=True,
        description='Vert. DCDT:',
        disabled=False, 
        style=style)

    v_dcdt_calib = widgets.Text(
        placeholder='mm/V',
        description='Vert. DCDT calib.:',
        continuous_update = True,
        disabled=False, 
        style=style)

    layout = widgets.Layout(display='flex',
             flex_flow='row',
             border='2px solid grey',
             padding='10px',
             grid_gap='5px 100px',
             width='75%')

    hdcdt = widgets.VBox(children=[h_dcdt, h_dcdt_calib], layout=widgets.Layout(flex='1 1 1%', width='auto'))
    vdcdt = widgets.VBox(children=[v_dcdt, v_dcdt_calib], layout=widgets.Layout(flex='1 1 1%', width='auto'))
    dcdts = widgets.GridBox(children=[data_logger, hdcdt, vdcdt], layout=layout)

    style2 = {'width': 'initial'}
    purpose = widgets.Textarea(
        placeholder='Purpose/Description',
        description='Purpose/Description',
        continuous_update = True,
        disabled=False, 
        style=style, 
        layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    ac_blocks = widgets.Text(
        placeholder='', 
        description='Acoustics blocks used', 
        continuous_update=True, 
        disabled=False, 
        style=style, 
        layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    temp = widgets.Text(
        placeholder='Temperature (C)', 
        description='Temperture', 
        continuous_update=True, 
        disabled=False, 
        style=style, 
        layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    humid = widgets.Text(
        placeholder='Rel. Humid. (%)', 
        description='Relative Humidity', 
        continuous_update=True, 
        disabled=False, 
        style=style, 
        layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    temp_humid = widgets.HBox([ac_blocks, temp, humid])
    
    notes = widgets.Textarea(
        placeholder='Experiment Notes',
        description='Experiment Notes',
        continuous_update = True,
        disabled=False, 
        style=style, 
        layout=widgets.Layout(flex='1 1 1%', width='auto')
    )
    layout = widgets.Layout(display='flex',
             flex_flow='column',
             align_items='stretch',
             border='2px solid grey',
             padding='10px',
             width='75%')
    exp_info = widgets.GridBox(children=[purpose, temp_humid, notes], layout=layout)

    vessel_params = widgets.interactive_output(vessel_input, {'a': use_vessel})
    
    
    
    use_pid = widgets.RadioButtons(
        options=['yes', 'no'],
        description='Record PID?',
        value='no',
        disabled=False)
    
    h_servo_label = widgets.Label('Hor. Servo Settings', layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    h_servo_p = widgets.Text(
        placeholder='',
        description='P',
        continuous_update = True,
        disabled=False, layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    h_servo_i = widgets.Text(
        placeholder='',
        description='I',
        continuous_update = True,
        disabled=False, layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    h_servo_d = widgets.Text(
        placeholder='',
        description='D',
        continuous_update = True,
        disabled=False, layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    h_servo_dAt = widgets.Text(
        placeholder='',
        description='Datten',
        continuous_update = True,
        disabled=False, layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    h_servo_f = widgets.Text(
        placeholder='',
        description='Feedback',
        continuous_update = True,
        disabled=False, layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    h_servo_e = widgets.Text(
        placeholder='',
        description='E-gain',
        continuous_update = True,
        disabled=False, layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    v_servo_label = widgets.Label('Vert. Servo Settings', layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    v_servo_p = widgets.Text(
        placeholder='',
        description='P',
        continuous_update = True,
        disabled=False, layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    v_servo_i = widgets.Text(
        placeholder='',
        description='I',
        continuous_update = True,
        disabled=False, layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    v_servo_d = widgets.Text(
        placeholder='',
        description='D',
        continuous_update = True,
        disabled=False, layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    v_servo_dAt = widgets.Text(
        placeholder='',
        description='Datten',
        continuous_update = True,
        disabled=False, layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    v_servo_f = widgets.Text(
        placeholder='',
        description='Feedback',
        continuous_update = True,
        disabled=False, layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    v_servo_e = widgets.Text(
        placeholder='',
        description='E-gain',
        continuous_update = True,
        disabled=False, layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    filler_label = widgets.Label('', layout=widgets.Layout(flex='1 1 1%', width='auto'))
    
    layout = widgets.Layout(display='flex',
         flex_flow='row',
         align_items='stretch',
         border='2px solid grey',
         padding='10px',
         width='75%')
    
    col1 = widgets.VBox([h_servo_label, h_servo_p, h_servo_i, h_servo_d])
    col2 = widgets.VBox([filler_label, h_servo_dAt, h_servo_f, h_servo_e])
    col12 = widgets.HBox([col1,col2])
    
    col3 = widgets.VBox([v_servo_label, v_servo_p, v_servo_i, v_servo_d])
    col4 = widgets.VBox([filler_label, v_servo_dAt, v_servo_f, v_servo_e])
    col34 = widgets.HBox([col3, col4])
#     pid_set = widgets.GridBox(children=[col12, col34], layout=layout)
    
    def pid_input(a):
        pid_set=widgets.Label('')
        if a == 'yes':
            pid_set = widgets.GridBox(children=[col12, col34], layout=layout)
        return display(pid_set)
    
    pid_params = widgets.interactive_output(pid_input, {'a': use_pid})

    outputs = [exp_name, op_name, hyd_start, hyd_end, pick_date, area, 
               block_thck, layer_thck, layer_thck_ld, material, part_size, 
               h_lc_picker, h_lc_calib, h_lc_stress, h_lc_ini_V, v_lc_picker, 
               v_lc_calib, v_lc_stress, v_lc_ini_V, pore_fluid, ppa_gain, ppa_press, 
               ppa_ini_V, ppa_load_v, ppb_gain, ppb_press, ppb_ini_V, ppb_load_v, 
               pc_gain, pc_press, pc_ini_V, pc_load_v, use_vessel, vessel_params, 
               data_logger, h_dcdt, h_dcdt_calib, v_dcdt, v_dcdt_calib, 
               layout, purpose, ac_blocks, temp, humid, notes, layout]

    gui = display(preamble, material_block, hor_vert, use_vessel, vessel_params, dcdts, exp_info, use_pid, pid_params)
    
    return gui, outputs

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def print_btn(outputs):
    
    button = widgets.Button(description="Make Runsheet")
    output = widgets.Output()

    display(button, output)

    def click(b):
        with output:
            clear_output(wait=True)
            if outputs[0].value != '':
                print('printing runsheet...')
                write_runsheet(outputs)
                webbrowser.open_new(r'file:'+os.getcwd()+'/'+outputs[0].value+'_Runsheet.pdf')
            else:
                print('Please complete form before generating runsheet.')

    return button.on_click(click)