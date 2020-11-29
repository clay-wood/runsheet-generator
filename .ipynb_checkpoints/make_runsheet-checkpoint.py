import os
import numpy as np
import pandas as pd

calibration_file_path = './calibrations.csv'
df = pd.read_csv(calibration_file_path)



def calc_stress(gain, area, targ_stress, init_volt):
    
    calibration = np.fromstring(gain, dtype=float, sep=',') * np.fromstring(area, dtype=float, sep=',')
    
    targ_volt = (calibration * np.fromstring(targ_stress, dtype=float, sep=',')) + np.fromstring(init_volt, dtype=float, sep=',')

    calibration = np.array2string(calibration, precision = 5)[1:-1]
    targ_volt = np.array2string(targ_volt, precision = 5, separator=', ')[1:-1]
    
    return calibration, targ_volt


def calc_press(gain, targ_stress, init_volt):
    
    targ_volt = (np.fromstring(gain, dtype=float, sep=',') * np.fromstring(targ_stress, dtype=float, sep=',')) + np.fromstring(init_volt, dtype=float, sep=',')
    targ_volt = np.array2string(targ_volt, precision = 5, separator=', ')[1:-1]
    
    return targ_volt


def get_gain(load, hilo):
    gain = df[df['Type'].str.contains(load, case=False) & 
       df['Gain'].str.contains(hilo, case=False)].values[0,4]
    
    return gain


def get_dcdt_gain(HV,rodLen,hilo):
    gain = df[df['Type'].str.contains(HV, case=False) & 
              df['Rod Length'].str.contains(rodLen, case=False) & 
              df['Gain'].str.contains(hilo, case=False)].values[0,4]
    
    return gain


def sec1(Preamble):

    section1 = '''\n\n\\renewcommand{\\arraystretch}{1}
\\begin{tabular}{ p{11cm} p{10cm} }
    \\textbf{Exp. Name: }'''+Preamble['ExpName']+''' & \\textbf{Date/Time: }'''+Preamble['Date']+''' \\\\
    \\textbf{Operator(s): }'''+Preamble['Operator']+''' & \\textbf{Hydraulics start: }'''+Preamble['HydStart']+''' \\\\
    & \\textbf{Hydraulics end: }'''+Preamble['HydEnd']+'''
\\end{tabular}
    \\bigskip \n\n'''
    
    return section1


def sec2(Block_material):
    
    section2 = '''\\textit{Sample Block Thickness w/ no gouge: } 
\\bigskip

\\textit{Layer Thickness (total on bench):} mm @sample

\\textit{Under Load: mm}

\\textit{Material (Qtz, Granite, ?): }'''+Block_material['Material']+'''

\\textit{Particle Size, Size Distribution :}
\\bigskip \n\n'''
    
    return section2


def sec3(Load_Cells,Block_material):    
    
    if Load_Cells['HorizLC'] != None:
        
        H_gain = get_gain(Load_Cells['HorizLC'], Load_Cells['H_gain'])
        
        calibration, targ_volt = calc_stress(str(H_gain), Block_material['Area'], Load_Cells['H_Stress'],Load_Cells['H_init_V'])
        
        section3_H = '''
\\begin{tabular}{ |p{2.75cm}|p{4cm}|p{3.5cm}|p{2.5cm}| p{3cm}| }
    \\hline
    \\textbf{Load cell name} & \\textbf{Calibrations (mV/kN)} & \\textbf{Target stress (MPa)} & \\textbf{Init. Voltage} & \\textbf{Volt. @ load}\\\\
    \\hline
    '''+Load_Cells['HorizLC']+''' & \\begin{tabular}[c]{@{}l@{}}'''+str(round(H_gain,4))+'''\\\\ (V/MPa): '''+calibration+'''\\end{tabular} & '''+Load_Cells['H_Stress']+''' & '''+Load_Cells['H_init_V']+''' & '''+targ_volt+'''\\\\ 
    \\hline
\\end{tabular}'''
    else:
        section3_H = '\n'

    if Load_Cells['VertLC'] != None:
        
        V_gain = get_gain(Load_Cells['VertLC'], Load_Cells['V_gain'])
        
        calibration, targ_volt = calc_stress(str(V_gain), Block_material['Area'], Load_Cells['V_Stress'],Load_Cells['V_init_V'])
        
        section3_V = '''
\\begin{tabular}{ |p{2.75cm}|p{4cm}|p{3.5cm}|p{2.5cm}| p{3cm}| }
    \\hline
    \\textbf{Load cell name} & \\textbf{Calibrations (mV/kN)} & \\textbf{Target stress (MPa)} & \\textbf{Init. Voltage} & \\textbf{Volt. @ load}\\\\
    \\hline
    '''+Load_Cells['VertLC']+''' & \\begin{tabular}[c]{@{}l@{}}'''+str(round(V_gain,4))+'''\\\\ (V/MPa): '''+calibration+'''\\end{tabular} & '''+Load_Cells['V_Stress']+''' & '''+Load_Cells['V_init_V']+''' & '''+targ_volt+'''\\\\ 
    \\hline
\\end{tabular}'''
    else:
        section3_V = ''

    section3 = '''\\renewcommand{\\arraystretch}{1}
\\begin{tabular}{ p{11cm} p{10cm} }
    \\textbf{\\textit{Load Cells:}} & Contact Area: '''+Block_material['Area']+''' $ m^2 $ \\\\
\\end{tabular}\n

\\renewcommand{\\arraystretch}{1.5}'''+section3_H+section3_V+'''
\\bigskip \n'''
    
    return section3


def sec4(Vessel):
    if Vessel['UseVessel'].lower() != 'no':
            
        if Vessel['Pc_press'] != None:
            
            pc_gain = df[df['Type'].str.contains("pc", case=False) & 
                         df['Device'].str.contains('ptrdx', case=False)].values[0,4]
            Pc_targ_volt = calc_press(str(pc_gain), Vessel['Pc_press'], Vessel['Pc_init_V'])
            
            section4_Pc = '''\\multicolumn{1}{ |c| } {\\textbf{Pc}} & Gain: '''+str(round(pc_gain,4))+''' & '''+Vessel['Pc_press']+''' & '''+Vessel['Pc_init_V']+''' & '''+Pc_targ_volt+'''\\\\ 
            \\hline'''
        else:
            section4_Pc = ''

        if Vessel['PpA_gain'].lower() != 'no':
            
            ppa_gain = get_gain('ppa', Vessel['PpA_gain'])
            PpA_targ_volt = calc_press(str(ppa_gain), Vessel['PpA_press'], Vessel['PpA_init_V'])
            
            section4_Pa = '''\\multicolumn{1}{ |c| } {\\textbf{PpA}} & '''+str(round(ppa_gain,4))+''' & '''+Vessel['PpA_press']+''' & '''+Vessel['PpA_init_V']+''' & '''+PpA_targ_volt+'''\\\\ 
            \\hline'''
        else: 
            section4_Pa = ''

        if Vessel['PpB_gain'].lower() != 'no':
            
            ppb_gain = get_gain('ppb', Vessel['PpB_gain'])
            PpB_targ_volt = calc_press(str(ppb_gain), Vessel['PpB_press'], Vessel['PpB_init_V'])
            
            section4_Pb = '''\\multicolumn{1}{ |c| } {\\textbf{PpB}} & '''+str(round(ppb_gain,4))+''' & '''+Vessel['PpB_press']+''' & '''+Vessel['PpB_init_V']+''' & '''+PpB_targ_volt+'''\\\\ 
            \\hline'''
        else: 
            section4_Pb = ''

        section4 = '''
        \\renewcommand{\\arraystretch}{1}
    \\begin{tabular}{ p{11cm} p{10cm} }
        \\textbf{\\textit{Vessel Pressure:}} & Pore Fluid: '''+Vessel['PoreFluid']+''' \\
    \\end{tabular}\n
    \\renewcommand{\\arraystretch}{1.5}
    \\begin{tabular}{ p{1cm}|p{4cm}|p{4.75cm}|p{2.5cm}| p{3.5cm}| }
        \\cline{2-5}
        & \\textbf{Calibrations $ (V/MPa) $} & \\textbf{Pressures (MPa)} & \\textbf{Init. Voltage} & \\textbf{Volt. @ load}\\\\
        \\cline{1-5}'''+section4_Pc+section4_Pa+section4_Pb+'''
    \\end{tabular}
        \\medskip \n\n'''
    else: 
        section4 = '\\medskip \n\n'
        
    return section4
    
    
def sec5(DCDTs):

    Hdcdt = get_dcdt_gain('horizontal dcdt', DCDTs['H_DCDT_rod'], DCDTs['H_DCDT_gain'])
    Vdcdt = get_gain(DCDTs['V_DCDT'], DCDTs['V_DCDT_gain'])
    
    section5 = '''\\renewcommand{\\arraystretch}{1}
\\begin{tabular}{ p{11cm} p{10cm} }
	\\textbf{Data Logger Used: }'''+DCDTs['DataLogger']+''' channel &\\textbf{Control File: }'''+DCDTs['CtrlFile']+'''  \\\\
\end{tabular}
\medskip 

\\begin{tabular}{ p{11cm} p{10cm} }
	\\textbf{Horiz. DCDT:} \\textit{'''+DCDTs['H_DCDT_rod']+''' rod} & \\textbf{Vert. DCDT: }'''+DCDTs['V_DCDT']+''' \\\\
	'''+str(round(Hdcdt,4))+''' mm/V &'''+str(round(Vdcdt,4))+ ''' mm/V
\\end{tabular}
\\medskip \n'''
    
    return section5


def sec6(ExpInfo):
    
    section6 = '''
\\textit{Purpose/Description: }'''+ExpInfo['Purpose']+'''\\\\ \n 
\\textit{Acoustics Blocks used: }'''+ExpInfo['AcBlocks']+'''\n'''
    
    return section6


def sec7(notes):
    
    w = [x.split('\n') for x in notes][0]
    w4 = [x for x in w if x]
    updated_notes = list(map(lambda x: '\t \\item ' + x +'\n ', w4))
    updated_notes = ''.join(updated_notes)
    
    section7 = '''\\newpage \n \\textbf{Experiment Notes}\n \\medskip\n {\\small \\begin{itemize}[label=\\#]\n \setlength\itemsep{0.25em}\n '''+updated_notes+'''\\end{itemize}} \n\n \\end{document}'''
    
    return section7



def write_runsheet(Preamble, Block_material, Load_Cells, Vessel, DCDTs, ExpInfo, notes):
    FileName = Preamble['ExpName'][0:5]
    runsheet_header = open('runsheet.hdr','r')

    outfile = open(FileName+'_Runsheet.tex', 'w')
    pageAry = []

    def a_tex_file(title):
    #     global pageAry
        pageAry.append(runsheet_header)
        pageAry.append(sec1(Preamble))
        pageAry.append(sec2(Block_material))
        pageAry.append(sec3(Load_Cells, Block_material))
        pageAry.append(sec4(Vessel))
        pageAry.append(sec5(DCDTs))
        pageAry.append(sec6(ExpInfo))
        pageAry.append(sec7(notes))
#         pageAry.append('\n\n\\end{document}')
        return

    a_tex_file(FileName)

    for i in pageAry:
        outfile.writelines(i)
    outfile.close()
    os.system("pdflatex " + FileName+'_Runsheet');