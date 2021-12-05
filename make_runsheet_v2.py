import os
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def calc_stress(gain, area, targ_stress, init_volt):
    calibration = float(gain) * float(area)
    targ_volt = (calibration * np.fromstring(targ_stress, dtype=float, sep=',')) + float(init_volt)
    
    calibration = str(calibration)
    targ_volt = np.array2string(targ_volt, precision=5, separator=', ')[1:-1]
    
    return calibration, targ_volt

def calc_press(gain, targ_stress, init_volt):
    
    targ_volt = (np.fromstring(gain, dtype=float, sep=',') * np.fromstring(targ_stress, dtype=float, sep=',')) + np.fromstring(init_volt, dtype=float, sep=',')
    targ_volt = np.array2string(targ_volt, precision = 5, separator=', ')[1:-1]
    
    return targ_volt

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def sec1(exp_name, operators, date, hyd_start, hyd_end, temp, humid, data_logger, ctrlFile):
    section1 = '''\n\n\\begin{table}[!ht]
	\\renewcommand{\\arraystretch}{1.1}
	\\begin{tabular}{p{10cm} p{10cm} }
	    \\textbf{Exp. Name: }'''+exp_name+''' & \\textbf{Date/Time: }'''+date+'''\\\\
	    \\textbf{Operator(s): }'''+operators+''' & Hydraulics start: '''+hyd_start+''' \\\\
	    Temperature ($\\degree$C): '''+temp+''' & Hydraulics end: '''+hyd_end+''' \\\\
	    Relative Humidity ($\\%$): '''+humid+''' & Data Logger/Control File: '''+data_logger+''' '''+ctrlFile+'''\\\\
	\\end{tabular}
\\end{table} 
\\vspace{-0.5cm} \n\n'''
    
    return section1

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def sec2(purpose, sample_blk, ac_blk, material, part_size, bench_thk, preCom_thk, postCom_thk, empty1, empty2, matWeight1, matWeight2, sampleBlk_weight1, sampleBlk_weight2, gougeWeight1, gougeWeight2):
    
    part1_hdr = '''\\begin{table}[!ht]
	\\renewcommand{\\arraystretch}{1.1}
	\\begin{tabular}{p{20cm}}'''
    purpose2 = '''\\textbf{Purpose/Description:} '''+purpose+''' \\\\'''

    if sample_blk != '':
	    sec2_samp = '''Sample Block Used and Thickness with \\textbf{no} Sample: '''+sample_blk+''' \\\\'''
    else:
        sec2_samp = '''Sample Block Used and Thickness with \\textbf{no} Sample: '''+ac_blk+''' \\\\'''

    part1 = part1_hdr+sec2_samp+'''
	\\end{tabular}
    \\end{table} \\vspace{-0.5cm} \n\n'''

    part2_hdr = '''\\begin{table}[!ht]
        \\small
        \\renewcommand{\\arraystretch}{1.2}
        \\begin{tabular}{ |p{7cm}| } \\hline \n'''
    
    part2_body = ''
    if material != '':
        part2_body += 'Material: '+material+' \\\\'
    if part_size != '':
        part2_body += 'Particle Size, Distribution: '+part_size+' \\\\'
    if bench_thk != '':
        part2_body += 'Benchtop Sample Thickness (mm): '+bench_thk+' \\\\'
    if preCom_thk != '':
        part2_body += 'Pre-Compaction Sample Thickness (mm): '+preCom_thk+' \\\\'
    if postCom_thk != '':
        part2_body += 'Post-Compaction Sample Thickness (mm): '+postCom_thk+' \\\\'

    part2 = part2_hdr + part2_body + ''' \\hline \\end{tabular}'''

    if (empty1 and empty2 and matWeight1 and matWeight2 and sampleBlk_weight1 and sampleBlk_weight2 and gougeWeight1 and gougeWeight2) != '':
        part3_hdr = '''\\hfill
        \\begin{tabular}{ |l|c|c| } \\hline
            & Block 1 & Block 2 \\\\ \\hline \n'''
        part3_body = '''Empty Block Weight (g) & '''+empty1+'''  & '''+empty2+'''\\\\ \\hline
	    Weight of Material Used (g) & '''+matWeight1+''' & '''+matWeight2+''' \\\\ \\hline
	    Sample Block Weight (g) & '''+sampleBlk_weight1+''' & '''+sampleBlk_weight2+''' \\\\ \\hline
	    Weight of Gouge (g) & '''+gougeWeight1+''' & '''+gougeWeight2+''' \\\\ \\hline'''
        part3 =  part3_hdr + part3_body + '''\\end{tabular}'''
    else:
        part3 = ' '
    
    section2 = part1 + part2 + part3 + '\\end{table} \\vspace{-0.5cm} \n\n'

    return section2

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def sec3(area, h_lc_picker, h_lc_calib, h_lc_stress, h_lc_ini_V, v_lc_picker, v_lc_calib, v_lc_stress, v_lc_ini_V):

    table_hdr = '''\\begin{table}[ht!]
        \\renewcommand{\\arraystretch}{1.5}
        \\begin{tabular}{ |p{2.75cm}|p{4cm}|p{3.5cm}|p{2.5cm}| p{3cm}| }
            \\multicolumn{3}{l}{\\textbf{\\textit{Load Cells:}}} & \\multicolumn{2}{l}{Contact Area: '''+area+''' $ m^2 $}\\\\ \\hline
            \\textbf{Load cell name} & \\textbf{Calibrations (mV/kN)} & \\textbf{Target stress (MPa)} & \\textbf{Init. Voltage} & \\textbf{Volt. @ load}\\\\
            \\hline
            '''
    if h_lc_picker != 'None':
                    
            calibration, targ_volt = calc_stress(h_lc_calib, area, h_lc_stress, h_lc_ini_V)
            
            section3_H = h_lc_picker+''' & \\begin{tabular}[c]{@{}l@{}}'''+str(round(float(h_lc_calib),4))+'''\\\\ (V/MPa): '''+str(round(float(calibration),4))+'''\\end{tabular} & '''+h_lc_stress+''' & '''+h_lc_ini_V+''' & '''+targ_volt+'''\\\\ \\hline'''
    else:
            section3_H = '\n'

    if v_lc_picker != 'None':
                
        v_calibration, v_targ_volt = calc_stress(v_lc_calib, area, v_lc_stress, v_lc_ini_V)
        
        section3_V = v_lc_picker+''' & \\begin{tabular}[c]{@{}l@{}}'''+str(round(float(v_lc_calib),4))+'''\\\\ (V/MPa): '''+str(round(float(v_calibration),4))+'''\\end{tabular} & '''+v_lc_stress+''' & '''+v_lc_ini_V+''' & '''+v_targ_volt+'''\\\\ \\hline'''
    else:
        section3_V = '\n'
        
    section3 = table_hdr+section3_H+section3_V+'''
    \\end{tabular}
    \\end{table} \\vspace{-0.5cm} \n\n'''
    
    return section3

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def sec4(use_vessel, pore_fluid, pc_gain, pc_press, pc_ini_V, ppa_gain, ppa_press, ppa_ini_V, ppb_gain, ppb_press, ppb_ini_V):
    if use_vessel != 'No':
        table_hdr = '''\\begin{table}[ht!]
            \\renewcommand{\\arraystretch}{1.5}
            \\begin{tabular}{ |p{4cm}|p{5cm}|p{2.5cm}| p{4.75cm}| }
            \\multicolumn{2}{l}{\\textbf{\\textit{Vessel Pressures:}}} & \\multicolumn{2}{l}{Pore Fluid:'''+pore_fluid+'''} \\\\ \\hline
            \\textbf{Calibrations (V/MPa)} & \\textbf{Pressures (MPa)} & \\textbf{Init. Voltage} & \\textbf{Volt. @ load} \\\\ \\hline'''
            
        if pc_gain != '':
            pc_targ_volt = calc_press(pc_gain, pc_press, pc_ini_V)
            section4_Pc = '''\\textit{\\small Pc:} '''+str(round(float(pc_gain),4))+''' & '''+pc_press+''' & '''+pc_ini_V+''' & '''+pc_targ_volt+'''\\\\ \\hline'''
        else:
            section4_Pc = ' '
        
        if ppa_gain != '':
                ppa_targ_volt = calc_press(ppa_gain, ppa_press, ppa_ini_V)
                section4_Pa = '''\\textit{\\small PpA:} '''+str(round(float(ppa_gain),4))+''' & '''+ppa_press+''' & '''+ppa_ini_V+''' & '''+ppa_targ_volt+'''\\\\ \\hline'''
        else: 
            section4_Pa = ' '

        if ppb_gain != '':
                ppb_targ_volt = calc_press(ppb_gain, ppb_press, ppb_ini_V)
                section4_Pb = '''\\textit{\\small PpA:} '''+str(round(float(ppb_gain),4))+''' & '''+ppb_press+''' & '''+ppb_ini_V+''' & '''+ppb_targ_volt+'''\\\\ \\hline'''
        else: 
            section4_Pb = ' '

        section4 = table_hdr+section4_Pc+section4_Pa+section4_Pb+'''\\end{tabular}
        \\end{table} \\vspace{-0.5cm} \n\n'''

    else:
        section4 = '\n\n'
        
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

runsheet_header = '''\\documentclass[letterpaper, 10pt]{article}
\\usepackage[table,xcdraw]{xcolor}
\\usepackage{textcomp}
\\usepackage{gensymb}
\\usepackage{amsmath}  % improve math presentation
\\usepackage[left=0.75in,top=0.75in,bottom=0.2in,letterpaper]{geometry} % decreases margins
\\usepackage{setspace}
\\usepackage{enumitem}\n

%----------------------------------------------\n

\\begin{document}

\\begin{center}
    {\\Large \\textbf{Biax Experiment}}\\\\
    {\\small For current calibrations -- \\texttt{gpfs/group/cjm38/default/Calibrations/}}\\\\
    {\\footnotesize \\textit{Revised: 30 Nov. 2021}}
\\end{center}\n\n'''

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def write_runsheet(outputs, tex='no'):
    
    [exp_name, pick_date, op_name, hyd_start, hyd_end, temp, humid, data_logger, ctrl, 
    purpose, sample_blk, ac_blk, material, part_size, bench_thk, preCom_thk, postCom_thk, empty1, empty2, matWeight1, matWeight2, sampleBlk_weight1, sampleBlk_weight2, gougeWeight1, gougeWeight2,
    area, h_lc_picker, h_lc_calib, h_lc_stress, h_lc_ini_V, v_lc_picker, v_lc_calib, v_lc_stress, v_lc_ini_V, 
    use_vessel, pore_fluid, pc_gain, pc_press, pc_ini_V, ppa_gain, ppa_press, ppa_ini_V, ppb_gain, ppb_press, ppb_ini_V] = list(map(lambda xx: outputs[xx], np.arange(len(outputs))))
    
    FileName = exp_name

    outfile = open(FileName+'_Runsheet.tex', 'w')
    pageAry = []

    def a_tex_file(title):
        pageAry.append(runsheet_header)
        pageAry.append(sec1(exp_name, op_name, pick_date, hyd_start, hyd_end, temp, humid, data_logger, ctrl))
        pageAry.append(sec2(purpose, sample_blk, ac_blk, material, part_size, bench_thk, preCom_thk, postCom_thk, empty1, empty2, matWeight1, matWeight2, sampleBlk_weight1, sampleBlk_weight2, gougeWeight1, gougeWeight2))
        pageAry.append(sec3(area, h_lc_picker, h_lc_calib, h_lc_stress, h_lc_ini_V, v_lc_picker, v_lc_calib, v_lc_stress, v_lc_ini_V))
        pageAry.append(sec4(use_vessel, pore_fluid, pc_gain, pc_press, pc_ini_V, ppa_gain, ppa_press, ppa_ini_V, ppb_gain, ppb_press, ppb_ini_V))
        # pageAry.append(sec5(data_logger, h_dcdt, h_dcdt_calib, v_dcdt, v_dcdt_calib))
        # pageAry.append(sec6(purpose, ac_blocks, temp, humid))
#         pageAry.append(sec7(PID_hyd))
        # pageAry.append(sec8(notes))
        pageAry.append('\n\n\\end{document}')
        return

    a_tex_file(FileName)

    for i in pageAry:
        outfile.writelines(i)
        
    outfile.close()
    os.system("pdflatex " + FileName+'_Runsheet.tex')
    
    # remove .aux and .log files -- comment out if necessary
    if FileName+'_Runsheet'+'.aux' in os.listdir(): os.remove(FileName+'_Runsheet'+'.aux')
    if FileName+'_Runsheet'+'.log' in os.listdir(): os.remove(FileName+'_Runsheet'+'.log')
    
    # if tex.lower() == 'no':
    #     os.remove(FileName+'_Runsheet'+'.tex')