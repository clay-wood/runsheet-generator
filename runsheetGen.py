"""
This project lets you try out Tkinter/Ttk and practice it!
Authors: Clay Wood, Raphael Affinito.
"""  # TODO: 1. PUT YOUR NAME IN THE ABOVE LINE.

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import datetime


def main():
    """ Constructs a GUI that will be used MUCH later to control EV3. """
    # ------------------------------------------------------------------
    # TODO: 2. Follow along with the video to make a remote control GUI
    # For every grid() method call you will add a row and a column argument
    # ------------------------------------------------------------------

    root = tk.Tk()
    root.title("Runsheet Generator")
    root.geometry("1200x900")

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()  # only grid call that does NOT need a row and column

    padding = {'padx': 5, 'pady': 3, 'sticky': 'new'}

    # ------------------------------------------------------------------
    # PREABMLE
    # ------------------------------------------------------------------

    title = ttk.Label(main_frame, text="Biax Experiment", font='Arial 18 bold')
    title.grid(row=0,column=0,columnspan=10,sticky='s')
    subtitle = ttk.Label(main_frame, text="Revised 30 Nov. 2021. For current calibrations: ~/gpfs/group/cjm38/default/Calibrations/", font='Arial 10 italic')
    subtitle.grid(row=1,column=0,columnspan=10,sticky='s')

    expName_label = ttk.Label(main_frame, text="Experiment Name:", font='Arial 12 bold')
    expName_label.grid(row=2,column=0, **padding)
    expName_entry = ttk.Entry(main_frame, width=4)
    expName_entry.insert(0, "p")
    expName_entry.grid(row=2,column=1, columnspan=2, **padding)
    expName_entry.focus()

    date_label = ttk.Label(main_frame, text="Date/Time:", font='Arial 12 bold')
    date_label.grid(row=2,column=3, **padding)
    date_entry = ttk.Entry(main_frame, width=8)
    x = datetime.datetime.now()
    date_entry.insert(0, x.strftime("%d/%m/%Y"))
    date_entry.grid(row=2,column=4)

    Name_label = ttk.Label(main_frame, text="Operator(s):", font='Arial 12 bold')
    Name_label.grid(row=3,column=0, **padding)
    Name_entry = ttk.Entry(main_frame)
    Name_entry.insert(0, " ")
    Name_entry.grid(row=3,column=1, columnspan=2, **padding)

    hydStart_label = ttk.Label(main_frame, text="Hydraulics start:", font='Arial 12 bold')
    hydStart_label.grid(row=3,column=3, **padding)
    hydStart_entry = ttk.Entry(main_frame, width=8)
    hydStart_entry.grid(row=3,column=4, **padding)

    hydEnd_label = ttk.Label(main_frame, text="Hydraulics end:", font='Arial 12 bold')
    hydEnd_label.grid(row=3,column=5, **padding)
    hydEnd_entry = ttk.Entry(main_frame, width=8)
    hydEnd_entry.grid(row=3,column=6, **padding)

    temp_label = ttk.Label(main_frame, text='Temperture (C)', font='Arial 12 bold')
    temp_label.grid(row=4,column=0)
    temp_entry = ttk.Entry(main_frame, width=8)
    temp_entry.grid(row=4,column=1)

    humid_label = ttk.Label(main_frame, text='Rel. Humid. (%)', font='Arial 12 bold')
    humid_label.grid(row=4,column=2)
    humid_entry = ttk.Entry(main_frame, width=8)
    humid_entry.grid(row=4,column=3)

    logger_optMenu = tk.StringVar(main_frame)
    logger_opts = ["", "8-chan", "16-chan"]
    logger_label = ttk.Label(main_frame, text="Data Logger", font='Arial 12 bold')
    logger_label.grid(row=4, column=4, sticky=tk.W)
    logger = ttk.OptionMenu(main_frame, logger_optMenu, *logger_opts)
    logger.grid(row=4, column=5, sticky=tk.W, padx=1)

    ctrl_label = ttk.Label(main_frame, text='Control File', font='Arial 12 bold')
    ctrl_label.grid(row=4,column=6)
    ctrl_entry = ttk.Entry(main_frame)
    ctrl_entry.grid(row=4,column=7, columnspan=2)

    purpose_label = ttk.Label(main_frame, text="Purpose/Description", font='Arial 12 bold')
    purpose_label.grid(row=5, column=0, **padding)
    purpose = ScrolledText(main_frame, height=3)
    purpose.grid(row=5, column=1, columnspan=5)

    # ------------------------------------------------------------------
    # SAMPLE BLOCKS
    # ------------------------------------------------------------------

    sideblk_optMenu = tk.StringVar(main_frame)
    sideblk_opts = ["", "Steel 5x5 cm", "Steel 10x10 cm", "SDS Vessel 5x5 cm", "AC DDS Vessel 5x5 cm", "Non-AC DDS Vessel 5x5 cm"]
    sideblk_label = ttk.Label(main_frame, text="Side Blocks", font='Arial 12 bold')
    sideblk_label.grid(row=6, column=0, sticky=tk.W)
    sideblk = ttk.OptionMenu(main_frame, sideblk_optMenu, *sideblk_opts)
    sideblk.grid(row=6, column=1, sticky=tk.W, padx=1)

    ACblk_label = ttk.Label(main_frame, text='Acoustic Blocks', font='Arial 12 bold')
    ACblk_label.grid(row=6,column=6)
    ACblk_entry = ttk.Entry(main_frame)
    ACblk_entry.grid(row=6,column=7, columnspan=2)

    def get_value():
        print(expName_entry.get()+'\n'+Name_entry.get()+'\n'+
        date_entry.get()+'\n'+logger_optMenu.get()+'\n'+ctrl_entry.get()+'\n'+
        purpose.get("1.0",'end-1c')+'\n'+sideblk_optMenu.get())
    #
    # sampBlk_label = ttk.Label(main_frame, text="Sample Block Thickness w/o gouge:")
    # sampBlk_label.grid(row=3,column=0, **padding)
    # sampBlk_entry = ttk.Entry(main_frame, width=35)
    # sampBlk_entry.insert(0, " ")
    # sampBlk_entry.grid(row=3,column=1, columnspan=1, **padding)
    #
    # placeholder = ttk.Label(main_frame, text="Under Load (mm):")
    # placeholder.grid(row=3,column=3, **padding)
    # placeholder = ttk.Entry(main_frame, width=35)
    # placeholder.insert(0, " ")
    # placeholder.grid(row=3,column=4, columnspan=1, **padding)
    #
    # placeholder = ttk.Label(main_frame, text="Material:")
    # placeholder.grid(row=5,column=0, **padding)
    # placeholder = ttk.Entry(main_frame, width=35)
    # placeholder.insert(0, " ")
    # placeholder.grid(row=5,column=1, columnspan=1, **padding)
    #
    # placeholder = ttk.Label(main_frame, text="Particle Size, Size Distribution:")
    # placeholder.grid(row=5,column=3, **padding)
    # placeholder = ttk.Entry(main_frame, width=35)
    # placeholder.insert(0, " ")
    # placeholder.grid(row=5,column=4, columnspan=1, **padding)

#     options = [
#     "",
#     "None",
#     "44mm Solid Horiz",
#     "44mm Solid Vert"
# ]
#
#     options2 = [
#     "",
#     "None",
#     "44mm Solid Vert",
#     "44mm Solid Horiz"
# ]
#
#     clicked = tk.StringVar()
#     clicked2 = tk.StringVar()
#
#     LC_label = ttk.Label(main_frame, text="Load Cell Name", font='Arial 14 bold')
#     LC_label.grid(row=7, column=0, **padding)
#
#     Calib_label = ttk.Label(main_frame, text="Calibrations (mv/kN)", font='Arial 14 bold')
#     Calib_label.grid(row=7, column=1, **padding)
#
#     TarStr_label = ttk.Label(main_frame, text="Target stress (MPa)", font='Arial 14 bold')
#     TarStr_label.grid(row=7, column=2, **padding)
#
#     IniV_label = ttk.Label(main_frame, text="Init. Voltage", font='Arial 14 bold')
#     IniV_label.grid(row=7, column=3, **padding)
#
#     LoadV_label = ttk.Label(main_frame, text="Volt @ load", font='Arial 14 bold')
#     LoadV_label.grid(row=7, column=4, **padding)
#
#     # ------------------------------------------------------------------
#
#     opt = ttk.OptionMenu(main_frame, clicked, *options)
#     opt.grid(row=8, column=0, **padding)
#
#     placeholder = ttk.Entry(main_frame, width=16)
#     placeholder.insert(0, " ")
#     placeholder.grid(row=8, column=1, columnspan=1, **padding)
#
#     placeholder = ttk.Entry(main_frame, width=16)
#     placeholder.insert(0, " ")
#     placeholder.grid(row=8, column=2, columnspan=1, **padding)
#
#     placeholder = ttk.Entry(main_frame, width=16)
#     placeholder.insert(0, " ")
#     placeholder.grid(row=8, column=3, columnspan=1, **padding)
#
#     placeholder = ttk.Entry(main_frame, width=16)
#     placeholder.insert(0, " ")
#     placeholder.grid(row=8, column=4, columnspan=1, **padding)
#
#
#     opt2 = ttk.OptionMenu(main_frame, clicked2, *options2)
#     opt2.grid(row=9, column=0, **padding)
#
#     placeholder = ttk.Entry(main_frame, width=16)
#     placeholder.insert(0, " ")
#     placeholder.grid(row=9, column=1, columnspan=1, **padding)
#
#     placeholder = ttk.Entry(main_frame, width=16)
#     placeholder.insert(0, " ")
#     placeholder.grid(row=9, column=2, columnspan=1, **padding)
#
#     placeholder = ttk.Entry(main_frame, width=16)
#     placeholder.insert(0, " ")
#     placeholder.grid(row=9, column=3, columnspan=1, **padding)
#
#     placeholder = ttk.Entry(main_frame, width=16)
#     placeholder.insert(0, " ")
#     placeholder.grid(row=9, column=4, columnspan=1, **padding)
#
#     # ------------------------------------------------------------------
#
#     # separator = ttk.Separator(main_frame, orient='horizontal')
#     # separator.place(relx=0, rely=0.425, relwidth=1, relheight=0.005)
#     # separator2 = ttk.Separator(main_frame, orient='horizontal')
#     # separator2.place(relx=0, rely=0.6, relwidth=1, relheight=0.005)
#     # separator3 = ttk.Separator(main_frame, orient='horizontal')
#     # separator3.place(relx=0, rely=0.855, relwidth=1, relheight=0.005)
#
#     # separator.grid(row=10, column=0, columnspan=1, **padding)
#
# #     v = tk.StringVar(main_frame, "1")
# #     choiceY = ttk.Radiobutton(main_frame, text="yes", variable=v, value='yes')
# #     choiceY.grid(row=10, column=0, columnspan=1, **padding)
# #     choiceN = ttk.Radiobutton(main_frame, text="no", variable=v, value='no')
# #     choiceN.grid(row=11, column=0, columnspan=1, **padding)
#
#     vessel_label = ttk.Label(main_frame, text="Vessel Pressures", font='Arial 14 bold')
#     vessel_label.grid(row=13, column=0, **padding)
#
#     pc_label = ttk.Label(main_frame, text="Confining", font='Arial 14 bold')
#     pc_label.grid(row=15, column=0, **padding)
#
#     ppa_label = ttk.Label(main_frame, text="PpB", font='Arial 14 bold')
#     ppa_label.grid(row=16, column=0, **padding)
#
#     ppb_label = ttk.Label(main_frame, text="PpB", font='Arial 14 bold')
#     ppb_label.grid(row=17, column=0, **padding)
#
#     vesCalib_label = ttk.Label(main_frame, text="Calibrations (V/MPa)", font='Arial 14 bold')
#     vesCalib_label.grid(row=14, column=1, **padding)
#
#     TarPres_label = ttk.Label(main_frame, text="Pressures (MPa)", font='Arial 14 bold')
#     TarPres_label.grid(row=14, column=2, **padding)
#
#     IniVpres_label = ttk.Label(main_frame, text="Init. Voltage", font='Arial 14 bold')
#     IniVpres_label.grid(row=14, column=3, **padding)
#
#     PressV_label = ttk.Label(main_frame, text="Volt @ load", font='Arial 14 bold')
#     PressV_label.grid(row=14, column=4, **padding)
#
#     # ------------------------------------------------------------------
#
#     placeholder5 = ttk.Entry(main_frame, width=16)
#     placeholder5.grid(row=15, column=1, columnspan=1, **padding)
#
#     placeholder6 = ttk.Entry(main_frame, width=16)
#     placeholder6.grid(row=15, column=2, columnspan=1, **padding)
#
#     placeholder7 = ttk.Entry(main_frame, width=16)
#     placeholder7.grid(row=15, column=3, columnspan=1, **padding)
#
#     placeholder8 = ttk.Entry(main_frame, width=16)
#     placeholder8.grid(row=15, column=4, columnspan=1, **padding)
#
#     # ------------------------------------------------------------------
#
#     placeholder5 = ttk.Entry(main_frame, width=16)
#     placeholder5.grid(row=16, column=1, columnspan=1, **padding)
#
#     placeholder6 = ttk.Entry(main_frame, width=16)
#     placeholder6.grid(row=16, column=2, columnspan=1, **padding)
#
#     placeholder7 = ttk.Entry(main_frame, width=16)
#     placeholder7.grid(row=16, column=3, columnspan=1, **padding)
#
#     placeholder8 = ttk.Entry(main_frame, width=16)
#     placeholder8.grid(row=16, column=4, columnspan=1, **padding)
#
#     # ------------------------------------------------------------------
#
#     placeholder5 = ttk.Entry(main_frame, width=16)
#     placeholder5.grid(row=17, column=1, columnspan=1, **padding)
#
#     placeholder6 = ttk.Entry(main_frame, width=16)
#     placeholder6.grid(row=17, column=2, columnspan=1, **padding)
#
#     placeholder7 = ttk.Entry(main_frame, width=16)
#     placeholder7.grid(row=17, column=3, columnspan=1, **padding)
#
#     placeholder8 = ttk.Entry(main_frame, width=16)
#     placeholder8.grid(row=17, column=4, columnspan=1, **padding)
#
#     # ------------------------------------------------------------------
#

#
#     notes_label = ttk.Label(main_frame, text="Experiment Notes", font='Arial 15 bold')
#     notes_label.grid(row=22, column=0, **padding)
#     notes = ScrolledText(main_frame, height=7)
#     notes.grid(row=23, column=0, columnspan=3, **padding)




    # Buttons for print and exit
    # def get_value():
    #     e_text=expName_entry.get()
    #     f_text=date_entry.get()
    #     g_text=purpose.get("1.0",'end-1c')
    #     print(e_text+'\n'+f_text+'\n'+g_text)

    print_button = ttk.Button(main_frame, text="Print Results", command=get_value)
    print_button.grid(**padding)

    exit_button = ttk.Button(main_frame, text="Exit")
    exit_button.grid(**padding)
    exit_button['command'] = lambda: exit()

    root.mainloop()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
