import os
import numpy as np
import pandas as pd

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

def sec1(exp_name, operators, date, hyd_start, hyd_end):

    section1 = '''\n\n\\renewcommand{\\arraystretch}{1}
\\begin{tabular}{ p{11cm} p{10cm} }
    \\textbf{Exp. Name: }'''+exp_name.value+''' & \\textbf{Date/Time: }'''+str(date.value)+''' \\\\
    \\textbf{Operator(s): }'''+operators.value+''' & \\textbf{Hydraulics start: }'''+hyd_start.value+''' \\\\
    & \\textbf{Hydraulics end: }'''+hyd_end.value+'''
\\end{tabular}
    \\bigskip \n\n'''
    
    return section1

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def sec2(block_thck, layer_thck, block_thck_ld, material, part_size):
    
    section2 = '''\\textit{Sample Block Thickness w/ no gouge: }'''+block_thck.value+''' 
\\bigskip

\\textit{Layer Thickness (total on bench): }'''+layer_thck.value+''' mm

\\textit{Under Load: }'''+block_thck_ld.value+''' mm

\\textit{Material (Qtz, Granite, ?): }'''+material.value+'''

\\textit{Particle Size, Size Distribution : }'''+part_size.value+'''
\\bigskip \n\n'''
    
    return section2

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def sec3(area, h_lc_picker, h_lc_calib, h_lc_stress, h_lc_ini_V, v_lc_picker, v_lc_calib, v_lc_stress, v_lc_ini_V):
    
    table_hdr = '''
\\begin{tabular}{ |p{2.75cm}|p{4cm}|p{3.5cm}|p{2.5cm}| p{3cm}| }
    \\hline
    \\textbf{Load cell name} & \\textbf{Calibrations (mV/kN)} & \\textbf{Target stress (MPa)} & \\textbf{Init. Voltage} & \\textbf{Volt. @ load}\\\\
    \\hline
    '''
    
    if h_lc_picker.value != 'None':
                
        calibration, targ_volt = calc_stress(h_lc_calib, area, h_lc_stress, h_lc_ini_V)
        
        section3_H = h_lc_picker.value+''' & \\begin{tabular}[c]{@{}l@{}}'''+str(round(float(h_lc_calib.value),4))+'''\\\\ (V/MPa): '''+str(round(float(calibration),4))+'''\\end{tabular} & '''+h_lc_stress.value+''' & '''+h_lc_ini_V.value+''' & '''+targ_volt+'''\\\\ 
    \\hline'''
    else:
        section3_H = '\n'

    if v_lc_picker.value != 'None':
                
        v_calibration, v_targ_volt = calc_stress(v_lc_calib, area, v_lc_stress, v_lc_ini_V)
        
        section3_V = v_lc_picker.value+''' & \\begin{tabular}[c]{@{}l@{}}'''+str(round(float(v_lc_calib.value),4))+'''\\\\ (V/MPa): '''+str(round(float(v_calibration),4))+'''\\end{tabular} & '''+v_lc_stress.value+''' & '''+v_lc_ini_V.value+''' & '''+v_targ_volt+'''\\\\ 
    \\hline'''
    else:
        section3_V = '\n'

    section3 = '''\\renewcommand{\\arraystretch}{1}
\\begin{tabular}{ p{11cm} p{10cm} }
    \\textbf{\\textit{Load Cells:}} & Contact Area: '''+area.value+''' $ m^2 $ \\\\
\\end{tabular}\n

\\renewcommand{\\arraystretch}{1.5}'''+table_hdr+section3_H+section3_V+'''
\\end{tabular}
\\bigskip \n'''
    
    return section3

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def sec4(use_vessel, pore_fluid, pc_gain, pc_press, pc_ini_V, pc_load_v, ppa_gain, ppa_press, ppa_ini_V, ppa_load_v, ppb_gain, ppb_press, ppb_ini_V, ppb_load_v):
    if use_vessel.value.lower() != 'no':
            
        if pc_gain.value != 'None':
            pc_targ_volt = calc_press(pc_gain, pc_press, pc_ini_V)
            section4_Pc = '''\\multicolumn{1}{ |c| } {\\textbf{Pc}} & Gain: '''+str(round(float(pc_gain.value),4))+''' & '''+pc_press.value+''' & '''+pc_ini_V.value+''' & '''+pc_targ_volt+'''\\\\ 
            \\hline'''
        else:
            section4_Pc = ' '

        if ppa_gain.value != 'None':
            ppa_targ_volt = calc_press(ppa_gain, ppa_press, ppa_ini_V)
            section4_Pa = '''\\multicolumn{1}{ |c| } {\\textbf{PpA}} & '''+str(round(float(ppa_gain.value),4))+''' & '''+ppa_press.value+''' & '''+ppa_ini_V.value+''' & '''+ppa_targ_volt.value+'''\\\\ 
            \\hline'''
        else: 
            section4_Pa = ' '

        if ppb_gain.value != 'None':
            ppb_targ_volt = calc_press(ppb_gain, ppb_press, ppb_ini_V)
            section4_Pb = '''\\multicolumn{1}{ |c| } {\\textbf{PpB}} & '''+str(round(float(ppb_gain.value),4))+''' & '''+ppb_press.value+''' & '''+ppb_ini_V.value+''' & '''+ppb_targ_volt+'''\\\\ 
            \\hline'''
        else: 
            section4_Pb = ' '

        section4 = '''
        \\renewcommand{\\arraystretch}{1}
    \\begin{tabular}{ p{11cm} p{10cm} }
        \\textbf{\\textit{Vessel Pressures:}} & Pore Fluid: '''+pore_fluid.value+''' \\
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

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def sec5(data_logger, h_dcdt, h_dcdt_calib, v_dcdt, v_dcdt_calib):
    section5 = '''\\renewcommand{\\arraystretch}{1}
\\begin{tabular}{ p{11cm} p{10cm} }
\\small
    \\textbf{Data Logger Used: }'''+data_logger.value+''' channel &\\textbf{Control File: }+ CTRL File  \\\\
\\end{tabular}


\\begin{tabular}{ p{11cm} p{10cm} }
\\small
    \\textbf{Horiz. DCDT:} \\textit{'''+h_dcdt.value+'''} & \\textbf{Vert. DCDT: }'''+v_dcdt.value+''' \\\\
    '''+str(round(float(h_dcdt_calib.value),4))+''' mm/V &'''+str(round(float(v_dcdt_calib.value),4))+ ''' mm/V
\\end{tabular}
 \\smallskip \n'''
    
    return section5

def sec6(purpose, ac_blocks, temp, humid):
    section6 = '''
\\small
\\textit{Purpose/Description: }'''+purpose.value+'''\\\\ \n 
\\textit{Acoustics Blocks used: }'''+ac_blocks.value+'''\n
\\textbf{Temperature: }'''+temp.value+'''\t'''+humid.value+'''\n'''
    
    return section6

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def sec7(PID_hyd):
    
    section7 = '''\n\n \\renewcommand{\\arraystretch}{1}
\\begin{table}[h]
\\scriptsize
\\centering
\\begin{tabular}{llll|llll}
\\multicolumn{4}{c|}{Horiz. Servo Settings} & \\multicolumn{4}{c}{Vert. Servo Settings} \\\\ \\hline
\\textbf{P} & '''+PID_hyd['H_P']+''' & \\textbf{D\\textsubscript{atten}} & '''+PID_hyd['H_Datten']+''' & \\textbf{P} & '''+PID_hyd['V_P']+''' & \\textbf{D\\textsubscript{atten}} & '''+PID_hyd['V_Datten']+''' \\\\
\\textbf{I} & '''+PID_hyd['H_I']+''' & \\textbf{Feedback} & '''+PID_hyd['H_Feedbk']+''' & \\textbf{I} & '''+PID_hyd['V_I']+''' & \\textbf{Feedback} & '''+PID_hyd['V_Feedbk']+''' \\\\
\\textbf{D} & '''+PID_hyd['H_D']+''' & \\textbf{E-gain} & '''+PID_hyd['H_Egain']+''' & \\textbf{D} & '''+PID_hyd['V_D']+''' & \\textbf{E-gain} & '''+PID_hyd['V_Egain']+''' \\\\
\\end{tabular}
\\end{table}

\n\n

\\begin{table}[h]
\\scriptsize
\\centering
\\begin{tabular}{ll|ll|ll|ll}
\\multicolumn{2}{c}{@ Hyd. Power Supply (HPS)} & \\multicolumn{2}{c}{Chilled water at HPS} & \\multicolumn{2}{c}{Chiller Unit} & \\multicolumn{2}{c}{Process water at Chiller} \\\\ \\hline
14. Tank Temp. (C)  & '''+PID_hyd['HPS_tank_temp']+''' & 1. Temp. In (F)    & '''+PID_hyd['HPSchill_temp_in']+''' & 6. Panel Temp. (F)      & '''+PID_hyd['Chill_panel_temp']+''' & 10. Temp. In (F) & '''+PID_hyd['Process_temp_in']+''' \\\\
15. Temp. Out (C)   & '''+PID_hyd['HPS_temp_out']+''' & 2. Pres. In (psi)  & '''+PID_hyd['HPSchill_pres_in']+''' & 7. Panel Pres. (psi)    & '''+PID_hyd['Chill_panel_pres']+''' & 11. Pres. In (psi) & '''+PID_hyd['Process_pres_in']+''' \\\\
16. Pres. Out (psi) & '''+PID_hyd['HPS_pres_out']+''' & 3. Temp. Out (F)   & '''+PID_hyd['HPSchill_temp_out']+''' & 8. Near Pres. In (psi)  & '''+PID_hyd['Chill_pres_in']+''' & 12. Temp. Out (F) & '''+PID_hyd['Process_temp_out']+''' \\\\
                    &  & 4. Pres. Out (psi) & '''+PID_hyd['HPSchill_pres_out']+''' & 9. Near Pres. Out (psi) & '''+PID_hyd['Chill_pres_out']+''' & 13. Pres. Out (psi) & '''+PID_hyd['Process_pres_out']+''' \\\\
                    &  & 5. Flow (lpm)      & '''+PID_hyd['HPSchill_flow']+''' &                         &  &                     & 
\\end{tabular}
\\end{table}
'''
    
    return section7

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def sec8(notes):
    
    if notes.value != None:
        w4 = notes.value.split('\n\n')
        updated_notes = list(map(lambda x: '\t \\item ' + x +'\n ', w4))
        updated_notes = ''.join(updated_notes)

        section8 = '''\\newpage \n \\textbf{Experiment Notes}\n \\medskip\n {\\small \\begin{itemize}[label=\\#]\n \setlength\itemsep{0.25em}\n '''+updated_notes+'''\\end{itemize}} \n\n \\end{document}'''
        
    else: 
        section8 = '''\\newpage \n \\textbf{Experiment Notes} \n\n \\end{document}'''
        
    return section8

runsheet_header = '''\\documentclass[letterpaper,10pt]{article}
\\usepackage{blindtext}
\\usepackage{authblk}
\\usepackage{tabularx} % extra features for tabular environment
\\usepackage{textcomp}
\\usepackage{gensymb}
\\usepackage{amsmath}  % improve math presentation
\\usepackage{xcolor}
\\usepackage{rotating}
\\usepackage[margin=0.75in,letterpaper]{geometry} % decreases margins
\\usepackage{setspace}
\\usepackage{multirow}
\\usepackage{enumitem}
\\setlength{\\arrayrulewidth}{0.25mm}
\\renewcommand{\\arraystretch}{1.5}
%++++++++++++++++++++++++++++++++++++++++

\\begin{document}

\\begin{center}
\t{\Large \\textbf{Biax Experiment}}
\\end{center}
\\bigskip'''

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def write_runsheet(outputs, tex='no'):
    
    [exp_name, op_name, hyd_start, hyd_end, pick_date, area, block_thck, layer_thck, layer_thck_ld, material, part_size, 
    h_lc_picker, h_lc_calib, h_lc_stress, h_lc_ini_V, v_lc_picker, v_lc_calib, v_lc_stress, v_lc_ini_V, pore_fluid, ppa_gain, ppa_press, 
    ppa_ini_V, ppa_load_v, ppb_gain, ppb_press, ppb_ini_V, ppb_load_v, pc_gain, pc_press, pc_ini_V, pc_load_v, use_vessel, 
    vessel_params, data_logger, h_dcdt, h_dcdt_calib, v_dcdt, v_dcdt_calib, layout, purpose, ac_blocks, temp, humid, notes, layout] = list(map(lambda xx: outputs[xx], np.arange(len(outputs))))
    
    FileName = exp_name.value

    outfile = open(FileName+'_Runsheet.tex', 'w')
    pageAry = []

    def a_tex_file(title):
        pageAry.append(runsheet_header)
        pageAry.append(sec1(exp_name, op_name, pick_date, hyd_start, hyd_end))
        pageAry.append(sec2(block_thck, layer_thck, layer_thck_ld, material, part_size))
        pageAry.append(sec3(area, h_lc_picker, h_lc_calib, h_lc_stress, h_lc_ini_V, v_lc_picker, v_lc_calib, v_lc_stress, v_lc_ini_V))
        pageAry.append(sec4(use_vessel, pore_fluid, pc_gain, pc_press, pc_ini_V, pc_load_v, ppa_gain, ppa_press, ppa_ini_V, ppa_load_v, ppb_gain, ppb_press, ppb_ini_V, ppb_load_v))
        pageAry.append(sec5(data_logger, h_dcdt, h_dcdt_calib, v_dcdt, v_dcdt_calib))
        pageAry.append(sec6(purpose, ac_blocks, temp, humid))
#         pageAry.append(sec7(PID_hyd))
        pageAry.append(sec8(notes))
#         pageAry.append('\n\n\\end{document}')
        return

    a_tex_file(FileName)

    for i in pageAry:
        outfile.writelines(i)
        
    outfile.close()
    os.system("pdflatex " + FileName+'_Runsheet');
    
    # remove .aux and .log files -- comment out if necessary
    if FileName+'_Runsheet'+'.aux' in os.listdir(): os.remove(FileName+'_Runsheet'+'.aux')
    if FileName+'_Runsheet'+'.log' in os.listdir(): os.remove(FileName+'_Runsheet'+'.log')
    
    # if tex.lower() == 'no':
    #     os.remove(FileName+'_Runsheet'+'.tex')