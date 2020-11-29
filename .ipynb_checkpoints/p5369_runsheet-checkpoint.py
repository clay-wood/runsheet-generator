import make_runsheet as mr

Preamble= {

'ExpName': 'p5369WGFracNSPPOsc',

'Date': '10/30/2019',

'Operator': 'Wood/Manogharan',

'HydStart': '',

'HydEnd': ''}


Block_material = {

'Material': 'WG, Fracture outside vessel.', 
'Area': '0.002233036'
    
}


Load_Cells = {
    
'HorizLC': '44',
'H_gain': 'HG: 123.9', 
'H_Stress': '1, 5, 10, 15, 20', 
'H_init_V': '0.70478', 
# 'H_load_volt': '0.9815, 2.088, 3.472, 4.855', 

'VertLC': None, 
'V_gain': None, 
'V_stress': None, 
'V_init_V': None, 
'V_load_volt': None
}


Vessel = {

'UseVessel': 'yes',

'Pc_press': '3.5',
'Pc_init_V': '-0.089760',
'Pc_press_volt': '0.4198',

'PpA_gain': 'HG: 1.52',
'PpA_press': '2.2',
'PpA_init_V': '-0.088558',
'PpA_press_volt': '3.255',

'PpB_gain': 'HG: 1.48',
'PpB_press': '1',
'PpB_init_V': '-0.046551',
'PpB_press_volt': '1.433',
}


DCDTs = {

'DataLogger': '16',
'CtrlFile': 'No',

'H_DCDT_rod': 'Short',
'H_DCDT_gain': 'HG: 0.64 mm/V',

'V_DCDT': 'TT2',
'V_DCDT_gain': '',
}


ExpInfo = {

'Purpose': '''
DAET and fluid flow of WG L-block sample. \n
Other Details
''',

'AcBlocks': '''
SDS L-block v2
'''
}


mr.write_runsheet(Preamble, Block_material, Load_Cells, Vessel, DCDTs, ExpInfo)