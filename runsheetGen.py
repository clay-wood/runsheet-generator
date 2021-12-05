"""
This project lets you try out Tkinter/Ttk and practice it!
Authors: Clay Wood, Raphael Affinito.
"""  # TODO: 1. PUT YOUR NAME IN THE ABOVE LINE.

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

import os
import datetime
from make_runsheet_v2 import write_runsheet
import webbrowser


def main():
    """ Constructs a GUI that will be used MUCH later to control EV3. """
    root = tk.Tk()
    root.title("Runsheet Generator")
    root.geometry("1200x900")

    # main_frame = ttk.Frame(root, padding=20)
    # main_frame.grid()  # only grid call that does NOT need a row and column

    main_frame = ttk.Notebook(root, padding=20)
    main_frame.grid()

    # PAGE 1 -- SAMPLE INFO
    page1 = ttk.Frame(main_frame)
    page1.grid()
    main_frame.add(page1, text='Sample Info')
    # PAGE 2 -- LOAD CELLS & DCDTS
    page2 = ttk.Frame(main_frame)
    page2.grid()    
    main_frame.add(page2, text='Load Cells & DCDTs')
    # PAGE 3 -- EXPERIMENT NOTES
    page3 = ttk.Frame(main_frame)
    page3.grid()    
    main_frame.add(page3, text='Exp. Notes')
    # PAGE 4 -- PID AND HYDRAULIC POWER SUPPLY  (HPS)
    page4 = ttk.Frame(main_frame)
    page4.grid()    
    main_frame.add(page4, text='PID & HPS')
    

    padding = {'padx': 5, 'pady': 3, 'sticky': 'new'}

    # ------------------------------------------------------------------
    # PREABMLE
    # ------------------------------------------------------------------
    
    for aa in range(4):
        title = ttk.Label([page1, page2, page3, page4][aa], text="Biax Experiment", font='Arial 18 bold')
        title.grid(row=0,column=0,columnspan=10,sticky='s')
        subtitle = ttk.Label([page1, page2, page3, page4][aa], text="Revised 30 Nov. 2021. For current calibrations: ~/gpfs/group/cjm38/default/Calibrations/", font='Arial 10 italic')
        subtitle.grid(row=1,column=0,columnspan=10,sticky='s')

    expName_label = ttk.Label(page1, text="Experiment Name:", font='Arial 14 bold')
    expName_label.grid(row=2,column=0, **padding)
    expName_entry = ttk.Entry(page1, width=4)
    expName_entry.insert(0, "p")
    expName_entry.grid(row=2,column=1, columnspan=2, **padding)
    expName_entry.focus()

    date_label = ttk.Label(page1, text="Date/Time:", font='Arial 14 bold')
    date_label.grid(row=2,column=3, **padding)
    date_entry = ttk.Entry(page1, width=8)
    x = datetime.datetime.now()
    date_entry.insert(0, x.strftime("%d/%m/%Y"))
    date_entry.grid(row=2,column=4)

    Name_label = ttk.Label(page1, text="Operator(s):", font='Arial 14 bold')
    Name_label.grid(row=3,column=0, **padding)
    Name_entry = ttk.Entry(page1)
    Name_entry.grid(row=3,column=1, columnspan=2, **padding)

    hydStart_label = ttk.Label(page1, text="Hydraulics start:", font='Arial 12 bold')
    hydStart_label.grid(row=3,column=3, **padding)
    hydStart_entry = ttk.Entry(page1, width=8)
    hydStart_entry.grid(row=3,column=4, **padding)

    hydEnd_label = ttk.Label(page1, text="Hydraulics end:", font='Arial 12 bold')
    hydEnd_label.grid(row=3,column=5, **padding)
    hydEnd_entry = ttk.Entry(page1, width=8)
    hydEnd_entry.grid(row=3,column=6, **padding)

    temp_label = ttk.Label(page1, text='Temperture (C)', font='Arial 12 bold')
    temp_label.grid(row=4,column=0)
    temp_entry = ttk.Entry(page1, width=8)
    temp_entry.grid(row=4,column=1)

    humid_label = ttk.Label(page1, text='Rel. Humid. (%)', font='Arial 12 bold')
    humid_label.grid(row=4,column=2)
    humid_entry = ttk.Entry(page1, width=8)
    humid_entry.grid(row=4,column=3)

    logger_optMenu = tk.StringVar(page1)
    logger_opts = [" ", "8-chan", "16-chan"]
    logger_label = ttk.Label(page1, text="Data Logger", font='Arial 12 bold')
    logger_label.grid(row=4, column=4, sticky=tk.W)
    logger = ttk.OptionMenu(page1, logger_optMenu, *logger_opts)
    logger.grid(row=4, column=5, sticky=tk.W, padx=1)

    ctrl_label = ttk.Label(page1, text='Control File', font='Arial 12 bold')
    ctrl_label.grid(row=4,column=6)
    ctrl_entry = ttk.Entry(page1)
    ctrl_entry.grid(row=4,column=7, columnspan=2)

    purpose_label = ttk.Label(page1, text="Purpose/Description", font='Arial 12 bold')
    purpose_label.grid(row=5, column=0, **padding)
    purpose = ScrolledText(page1, height=3)
    purpose.grid(row=5, column=1, columnspan=4, sticky='W', padx=1)

    # ------------------------------------------------------------------
    # SAMPLE BLOCKS
    # ------------------------------------------------------------------

    sideblk_optMenu = tk.StringVar(page1)
    sideblk_opts = ["", "Steel 5x5 cm", "Steel 10x10 cm", "SDS Vessel 5x5 cm", "AC DDS Vessel 5x5 cm", "Non-AC DDS Vessel 5x5 cm"]
    sideblk_label = ttk.Label(page1, text="Side Blocks", font='Arial 12 bold')
    sideblk_label.grid(row=6, column=0, sticky=tk.W)
    sideblk = ttk.OptionMenu(page1, sideblk_optMenu, *sideblk_opts)
    sideblk.grid(row=6, column=1, sticky=tk.W, padx=1)

    ACblk_label = ttk.Label(page1, text='Acoustic Blocks', font='Arial 12 bold')
    ACblk_label.grid(row=6,column=2)
    ACblk_entry = ttk.Entry(page1)
    ACblk_entry.grid(row=6,column=3, columnspan=2)

    # ------------------------------------------------------------------
    # SAMPLE MATERIAL
    # ------------------------------------------------------------------

    material_label = ttk.Label(page1, text="Material", font='Arial 12 bold')
    material_label.grid(row=7,column=0, **padding)
    material_entry = ttk.Entry(page1, width=8)
    material_entry.grid(row=7,column=1, columnspan=1, **padding)

    blk1_label = ttk.Label(page1, text="Block 1", font='Arial 12 bold')
    blk1_label.grid(row=7,column=4, **padding)
    blk2_label = ttk.Label(page1, text="Block 2", font='Arial 12 bold')
    blk2_label.grid(row=7,column=5, **padding)

    particle_label = ttk.Label(page1, text="Particle Size, Distribution", font='Arial 12 bold')
    particle_label.grid(row=8,column=0, **padding)
    particle_entry = ttk.Entry(page1, width=8)
    particle_entry.grid(row=8,column=1, columnspan=1, **padding)

    emptyBlk_label = ttk.Label(page1, text="Empty Block Weight (g)", font='Arial 12 bold')
    emptyBlk_label.grid(row=8,column=3, **padding)
    emptyBlk1_entry = ttk.Entry(page1, width=8)
    emptyBlk1_entry.grid(row=8,column=4, columnspan=1, **padding)
    emptyBlk2_entry = ttk.Entry(page1, width=8)
    emptyBlk2_entry.grid(row=8,column=5, columnspan=1, **padding)

    bench_label = ttk.Label(page1, text="Benchtop Sample Thickness (mm)", font='Arial 12 bold')
    bench_label.grid(row=9,column=0, **padding)
    bench_entry = ttk.Entry(page1, width=8)
    bench_entry.grid(row=9,column=1, columnspan=1, **padding)

    weight_label = ttk.Label(page1, text="Weight of Material (g)", font='Arial 12 bold')
    weight_label.grid(row=9,column=3, **padding)
    weightBlk1_entry = ttk.Entry(page1, width=8)
    weightBlk1_entry.grid(row=9,column=4, columnspan=1, **padding)
    weightBlk2_entry = ttk.Entry(page1, width=8)
    weightBlk2_entry.grid(row=9,column=5, columnspan=1, **padding)

    preComp_label = ttk.Label(page1, text="Pre-compaction Sample Thickness (mm)", font='Arial 12 bold')
    preComp_label.grid(row=10,column=0, **padding)
    preComp_entry = ttk.Entry(page1, width=8)
    preComp_entry.grid(row=10,column=1, columnspan=1, **padding)

    blkWeight_label = ttk.Label(page1, text="Sample Block Weight (g)", font='Arial 12 bold')
    blkWeight_label.grid(row=10,column=3, **padding)
    Blk1weight_entry = ttk.Entry(page1, width=8)
    Blk1weight_entry.grid(row=10,column=4, columnspan=1, **padding)
    Blk2weight_entry = ttk.Entry(page1, width=8)
    Blk2weight_entry.grid(row=10,column=5, columnspan=1, **padding)

    postComp_label = ttk.Label(page1, text="Post-compaction Sample Thickness (mm)", font='Arial 12 bold')
    postComp_label.grid(row=11,column=0, **padding)
    postComp_entry = ttk.Entry(page1, width=8)
    postComp_entry.grid(row=11,column=1, columnspan=1, **padding)

    gougeWeight_label = ttk.Label(page1, text="Gouge Weight (g)", font='Arial 12 bold')
    gougeWeight_label.grid(row=11,column=3, **padding)
    gougeWeight1_entry = ttk.Entry(page1, width=8)
    gougeWeight1_entry.grid(row=11,column=4, columnspan=1, **padding)
    gougeWeight2_entry = ttk.Entry(page1, width=8)
    gougeWeight2_entry.grid(row=11,column=5, columnspan=1, **padding)

    # ------------------------------------------------------------------
    # LOAD CELLS
    # ------------------------------------------------------------------

    area_label = ttk.Label(page2, text="Contact Area:", font='Arial 14 bold')
    area_label.grid(row=2, column=0, **padding)
    area_entry = ttk.Entry(page2, width=16)
    area_entry.grid(row=2, column=1, columnspan=1, **padding)
    
    LC_label = ttk.Label(page2, text="Load Cell Name", font='Arial 14 bold')
    LC_label.grid(row=3, column=0, **padding)

    Calib_label = ttk.Label(page2, text="Calibrations (mv/kN)", font='Arial 14 bold')
    Calib_label.grid(row=3, column=1, **padding)

    TarStr_label = ttk.Label(page2, text="Target stress (MPa)", font='Arial 14 bold')
    TarStr_label.grid(row=3, column=2, **padding)

    IniV_label = ttk.Label(page2, text="Init. Voltage", font='Arial 14 bold')
    IniV_label.grid(row=3, column=3, **padding)

    LoadV_label = ttk.Label(page2, text="Volt @ load", font='Arial 14 bold')
    LoadV_label.grid(row=3, column=4, **padding)

    horOpts = ["", "None","44mm Solid Horiz","44mm Solid Vert"]
    vertOpts = ["","None","44mm Solid Vert","44mm Solid Horiz"]

    HorLC_optMenu = tk.StringVar(page2)
    HorLC = ttk.OptionMenu(page2, HorLC_optMenu, *horOpts)
    HorLC.grid(row=4, column=0, **padding)

    HorCal_entry = ttk.Entry(page2, width=16)
    HorCal_entry.grid(row=4, column=1, columnspan=1, **padding)

    HorStress_entry = ttk.Entry(page2, width=16)
    HorStress_entry.grid(row=4, column=2, columnspan=1, **padding)

    HorIniV_entry = ttk.Entry(page2, width=16)
    HorIniV_entry.grid(row=4, column=3, columnspan=1, **padding)

    HorVolt_entry = ttk.Entry(page2, width=16)
    HorVolt_entry.grid(row=4, column=4, columnspan=1, **padding)

    VertLC_optMenu = tk.StringVar(page2)
    VertLC = ttk.OptionMenu(page2, VertLC_optMenu, *horOpts)
    VertLC.grid(row=5, column=0, **padding)

    VertCal_entry = ttk.Entry(page2, width=16)
    VertCal_entry.grid(row=5, column=1, columnspan=1, **padding)

    VertStress_entry = ttk.Entry(page2, width=16)
    VertStress_entry.grid(row=5, column=2, columnspan=1, **padding)

    VertIniV_entry = ttk.Entry(page2, width=16)
    VertIniV_entry.grid(row=5, column=3, columnspan=1, **padding)

    VertVolt_entry = ttk.Entry(page2, width=16)
    VertVolt_entry.grid(row=5, column=4, columnspan=1, **padding)

    # ------------------------------------------------------------------
    # VESSEL PRESSURES
    # ------------------------------------------------------------------

    useVessel_label = ttk.Label(page2, text="Use Vessel?", font='Arial 14 bold')
    useVessel_label.grid(row=6, column=0, **padding)
    vesselOpts = ["", "Yes","No"]
    vessel_optMenu = tk.StringVar(page2)
    vesselYN = ttk.OptionMenu(page2, vessel_optMenu, *vesselOpts)
    vesselYN.grid(row=6, column=1, **padding)

    fluid_label = ttk.Label(page2, text="Pore Fluid", font='Arial 14 bold')
    fluid_label.grid(row=6, column=2, **padding)
    fluid_entry = ttk.Entry(page2)
    fluid_entry.grid(row=6, column=3, columnspan=1, **padding)
    
    vessel_label = ttk.Label(page2, text="Vessel Pressures", font='Arial 14 bold')
    vessel_label.grid(row=7, column=0, **padding)

    vesCalib_label = ttk.Label(page2, text="Calibrations (V/MPa)", font='Arial 14 bold')
    vesCalib_label.grid(row=7, column=1, **padding)

    TarPres_label = ttk.Label(page2, text="Pressures (MPa)", font='Arial 14 bold')
    TarPres_label.grid(row=7, column=2, **padding)

    IniVpres_label = ttk.Label(page2, text="Init. Voltage", font='Arial 14 bold')
    IniVpres_label.grid(row=7, column=3, **padding)

    PressV_label = ttk.Label(page2, text="Volt @ load", font='Arial 14 bold')
    PressV_label.grid(row=7, column=4, **padding)

    pc_label = ttk.Label(page2, text="Confining", font='Arial 14 bold')
    pc_label.grid(row=8, column=0, **padding)

    pc_calib = ttk.Entry(page2, width=16)
    pc_calib.grid(row=8, column=1, columnspan=1, **padding)

    pcPress = ttk.Entry(page2, width=16)
    pcPress.grid(row=8, column=2, columnspan=1, **padding)

    pcIniV = ttk.Entry(page2, width=16)
    pcIniV.grid(row=8, column=3, columnspan=1, **padding)

    pcVolt = ttk.Entry(page2, width=16)
    pcVolt.grid(row=8, column=4, columnspan=1, **padding)

    ppa_label = ttk.Label(page2, text="PpA", font='Arial 14 bold')
    ppa_label.grid(row=9, column=0, **padding)

    ppa_calib = ttk.Entry(page2, width=16)
    ppa_calib.grid(row=9, column=1, columnspan=1, **padding)

    ppaPress = ttk.Entry(page2, width=16)
    ppaPress.grid(row=9, column=2, columnspan=1, **padding)

    ppaIniV = ttk.Entry(page2, width=16)
    ppaIniV.grid(row=9, column=3, columnspan=1, **padding)

    ppaVolt = ttk.Entry(page2, width=16)
    ppaVolt.grid(row=9, column=4, columnspan=1, **padding)

    ppb_label = ttk.Label(page2, text="PpB", font='Arial 14 bold')
    ppb_label.grid(row=10, column=0, **padding)

    ppb_calib = ttk.Entry(page2, width=16)
    ppb_calib.grid(row=10, column=1, columnspan=1, **padding)

    ppbPress = ttk.Entry(page2, width=16)
    ppbPress.grid(row=10, column=2, columnspan=1, **padding)

    ppbIniV = ttk.Entry(page2, width=16)
    ppbIniV.grid(row=10, column=3, columnspan=1, **padding)

    ppbVolt = ttk.Entry(page2, width=16)
    ppbVolt.grid(row=10, column=4, columnspan=1, **padding)

    # # ------------------------------------------------------------------
    # # DCDTS
    # # ------------------------------------------------------------------

    # valores = tk.StringVar()
    # valores.set("Carro Coche Moto Bici Triciclo Patineta Patin Patines Lancha Patrullas")

    # lstbox = tk.Listbox(page2, listvariable=valores, selectmode=tk.MULTIPLE, width=20, height=10)
    # lstbox.grid(row=19, column=0, columnspan=1)

    # def get_value():
    #     print(expName_entry.get()+'\n'+Name_entry.get()+'\n'+
    #     date_entry.get()+'\n'+logger_optMenu.get()+'\n'+ctrl_entry.get()+'\n'+
    #     purpose.get("1.0",'end-1c')+'\n'+sideblk_optMenu.get()+'\n'+ACblk_entry.get()+
    #     '\n'+material_entry.get()+'\n'+HorLC_optMenu.get()+'\n'+HorCal_entry.get()+
    #     '\n'+HorStress_entry.get()+'\n'+HorIniV_entry.get()+'\n'+HorVolt_entry.get())

    def printRunsheet():
        outputs = [expName_entry.get(), Name_entry.get(), date_entry.get(), hydStart_entry.get(), hydEnd_entry.get(), 
        temp_entry.get(), humid_entry.get(), logger_optMenu.get(), ctrl_entry.get(),
        purpose.get("1.0",'end-1c'), sideblk_optMenu.get(), ACblk_entry.get(), material_entry.get(), particle_entry.get(), bench_entry.get(), preComp_entry.get(), postComp_entry.get(), 
        emptyBlk1_entry.get(), emptyBlk2_entry.get(), weightBlk1_entry.get(), weightBlk2_entry.get(), Blk1weight_entry.get(), Blk2weight_entry.get(), gougeWeight1_entry.get(), gougeWeight2_entry.get(),  
        area_entry.get(), HorLC_optMenu.get(), HorCal_entry.get(), HorStress_entry.get(), HorIniV_entry.get(), 
        VertLC_optMenu.get(), VertCal_entry.get(), VertStress_entry.get(), VertIniV_entry.get(),
        vessel_optMenu.get(), fluid_entry.get(), pc_calib.get(), pcPress.get(), pcIniV.get(), 
        ppa_calib.get(), ppaPress.get(), ppaIniV.get(), ppb_calib.get(), ppbPress.get(), ppbIniV.get()]

        write_runsheet(outputs)
        webbrowser.open_new(r'file:'+os.getcwd()+'/'+outputs[0]+'_Runsheet.pdf')
        return 






    notes_label = ttk.Label(page3, text="Experiment Notes", font='Arial 15 bold')
    notes_label.grid(row=2, column=0, **padding)
    notes = ScrolledText(page3, height=50, width=150)
    notes.grid(row=2, column=0, **padding)




    # # Buttons for print and exit
    # # def get_value():
    # #     e_text=expName_entry.get()
    # #     f_text=date_entry.get()
    # #     g_text=purpose.get("1.0",'end-1c')
    # #     print(e_text+'\n'+f_text+'\n'+g_text)

    # print_button = ttk.Button(page3, text="Print Runsheet", command=get_value)
    print_button = ttk.Button(page3, text="Print Runsheet", command=printRunsheet)
    print_button.grid(**padding)

    exit_button = ttk.Button(page3, text="Exit")
    exit_button.grid(**padding)
    exit_button['command'] = lambda: exit()

    root.mainloop()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
