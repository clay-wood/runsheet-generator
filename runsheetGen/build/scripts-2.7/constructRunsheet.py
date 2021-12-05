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

        section4 = table_hdr+section4_Pc+section4_Pa+section4_Pb+''' \\end{tabular}
        \\end{table} \\vspace{-0.5cm} \n\n'''

    else:
        section4 = '\n\n'
        
    return section4

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def sec5(dcdt1, dcdt1_calib, dcdt2, dcdt2_calib, dcdt3, dcdt3_calib, dcdt4, dcdt4_calib):
    table_hdr = '''\\begin{table}[ht!]
    \\small
    \\renewcommand{\\arraystretch}{1.2}
    \\begin{tabular}{ l l } 
        \\multicolumn{2}{c}{\\textbf{\\textit{Displacement Transducers}}} \\\\
        \\textbf{\\textit{Name}} & \\textbf{\\textit{Gain (mm/V)}} \\\\ \\hline '''

    table_body = ''
    if dcdt1_calib != '':
        table_body += dcdt1+''' &  '''+dcdt1_calib+''' \\\\ \\hline '''
    if dcdt2_calib != '':
        table_body += dcdt2+''' &  '''+dcdt2_calib+''' \\\\ \\hline '''
    if dcdt3_calib != '':
        table_body += dcdt3+''' &  '''+dcdt3_calib+''' \\\\ \\hline '''
    if dcdt4_calib != '':
        table_body += dcdt4+''' &  '''+dcdt4_calib+''' \\\\ \\hline '''

    section5 = table_hdr + table_body + ''' \\end{tabular}
    \\end{table} \\vspace{-0.5cm} \n\n'''
    
    return section5

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def sec6(servo, hps):
    table_hdr = '''\\begin{table}[!ht]
        \\footnotesize
        \\renewcommand{\\arraystretch}{1.1}
        \\begin{tabular}{ p{1cm}|p{2cm} } \\rowcolor[HTML]{EFEFEF}
            \\multicolumn{2}{c}{\\textit{Horizontal Servo Settings} \\cellcolor[HTML]{EFEFEF}} \\\\ \\hline '''

    part1_body = '''P: '''+servo[0]+''' & D$_{atten}$: '''+servo[1]+''' \\\\ \\hline
        I: '''+servo[2]+''' & Feedback: '''+servo[3]+''' \\\\ \\hline 
        D: '''+servo[4]+''' & E-gain: '''+servo[5]+''' \\\\ \\hline 
        \\multicolumn{2}{c}{\\textit{Vertical Servo Settings} \\cellcolor[HTML]{EFEFEF}} \\\\ \\hline 
        P: '''+servo[6]+''' & D$_{atten}$  '''+servo[7]+''' \\\\ \\hline 
        I: '''+servo[8]+''' & Feedback: '''+servo[9]+''' \\\\ \\hline
        D: '''+servo[10]+''' & E-gain: '''+servo[11]+''' \\\\ \\hline 
    \\end{tabular} '''
    part1 = table_hdr + part1_body

    table2_hdr = '''\\hfill 
        \\renewcommand{\\arraystretch}{1.1}
        \\begin{tabular}{ l|l|l } \\rowcolor[HTML]{EFEFEF}
        \\textit{Chilled water at HPS} & \\textit{Chiller Unit} & \\textit{Proc. water @ Chiller} \\\\ \\hline '''

    part2_body = '''1. Temp In ($\\degree$F): '''+hps[0]+''' & 6. Panel Temp ($\\degree$F): '''+hps[5]+''' & 10. Temp In ($\\degree$F): '''+hps[9]+''' \\\\ \\hline 
    2. Pres. In (psi): '''+hps[1]+''' & 7. Panel Pres. (psi): '''+hps[6]+''' & 11. Pres. In (psi): '''+hps[10]+''' \\\\ \\hline 
    3. Temp Out ($\\degree$F): '''+hps[2]+''' & 8. Near Pres. In (psi): '''+hps[7]+'''& 12. Temp Out ($\\degree$F): '''+hps[11]+''' \\\\ \\hline 
    4. Pres. Out (psi): '''+hps[3]+'''& 9. Near Pres. Out (psi): '''+hps[8]+'''& 13. Pres. Out (psi): '''+hps[12]+''' \\\\ \\hline 
    5. Flow (lpm): '''+hps[4]+''' \\\\ \\hline 
    \\multicolumn{3}{c}{\\textit{Hyd. Power Supply (HPS)} \\cellcolor[HTML]{EFEFEF}} \\\\ \\hline 
    14. Tank Temp ($\\degree$C): '''+hps[13]+''' & 15. Temp. Out ($\\degree$C): '''+hps[4]+''' & 16. Pres. Out (psi): '''+hps[15]+''' \\\\ \\hline 
    \\end{tabular} 
    \\end{table} \\vspace{-0.5cm} \n\n'''
    part2 = table2_hdr + part2_body

    section6 = part1 + part2

    return section6

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

def sec7(notes):
    
    if notes != '':
        w4 = notes.split('\n\n')
        updated_notes = list(map(lambda x: '\t \\item ' + x +'\n ', w4))
        updated_notes = ''.join(updated_notes)

        section7 = '''\\newpage \n \\textbf{Experiment Notes}\n \\medskip\n {\\small \\begin{itemize}[label=\\#]\n \setlength\itemsep{0.25em}\n '''+updated_notes+'''\\end{itemize}} \n\n \\end{document}'''
        
    else: 
        section7 = '''\\newpage \n \\textbf{Experiment Notes} \n\n'''
        
    return section7

runsheet_header = '''\\documentclass[letterpaper, 10pt]{article}
\\usepackage[table,xcdraw]{xcolor}
\\usepackage{textcomp}
\\usepackage{gensymb}
\\usepackage{amsmath}  % improve math presentation
\\usepackage[left=0.75in,top=0.75in,bottom=0.2in,letterpaper]{geometry}
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
    use_vessel, pore_fluid, pc_gain, pc_press, pc_ini_V, ppa_gain, ppa_press, ppa_ini_V, ppb_gain, ppb_press, ppb_ini_V, 
    dcdt1, dcdt1_calib, dcdt2, dcdt2_calib, dcdt3, dcdt3_calib, dcdt4, dcdt4_calib, 
    servo, hps, notes] = list(map(lambda xx: outputs[xx], np.arange(len(outputs))))
    
    FileName = exp_name

    outfile = open(FileName+'_Runsheet.tex', 'w')
    pageAry = []

    def a_tex_file(title):
        pageAry.append(runsheet_header)
        pageAry.append(sec1(exp_name, op_name, pick_date, hyd_start, hyd_end, temp, humid, data_logger, ctrl))
        pageAry.append(sec2(purpose, sample_blk, ac_blk, material, part_size, bench_thk, preCom_thk, postCom_thk, empty1, empty2, matWeight1, matWeight2, sampleBlk_weight1, sampleBlk_weight2, gougeWeight1, gougeWeight2))
        pageAry.append(sec3(area, h_lc_picker, h_lc_calib, h_lc_stress, h_lc_ini_V, v_lc_picker, v_lc_calib, v_lc_stress, v_lc_ini_V))
        pageAry.append(sec4(use_vessel, pore_fluid, pc_gain, pc_press, pc_ini_V, ppa_gain, ppa_press, ppa_ini_V, ppb_gain, ppb_press, ppb_ini_V))
        pageAry.append(sec5(dcdt1, dcdt1_calib, dcdt2, dcdt2_calib, dcdt3, dcdt3_calib, dcdt4, dcdt4_calib))
        pageAry.append(sec6(servo, hps))
        pageAry.append(sec7(notes))
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