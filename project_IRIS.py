import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkPDFViewer import tkPDFViewer as pdf
import matplotlib.pyplot as plt
from time import strftime

from TRIR import TRIRimporter,TRIRviewer,pyTRIR
from FTIR import FTIRviewer


class mMenubar():
    def initmenu(parent):
        def donothing():
            print('useless button for now')
 
        menubar = tk.Menu(parent)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Re-open", command=donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Close", command=root.quit)
        menubar.add_cascade(label="IRIS", menu=filemenu)

        IRmenu = tk.Menu(menubar, tearoff=0)
        IRmenu.add_command(label="FTIR viewer", command=menubarfunctions.open_FTIR_viewer)
        #IRmenu.add_command(label="import FTIR data", command=donothing)
        menubar.add_cascade(label="IR", menu=IRmenu)

        TRIRmenu = tk.Menu(menubar, tearoff=0)
        TRIRmenu.add_command(label="import TRIR data", command=menubarfunctions.open_TRIR_import)
        TRIRmenu.add_command(label="TRIR viewer", command=menubarfunctions.open_TRIR_viewer)
        TRIRmenu.add_separator()
        TRIRmenu.add_command(label="Lissajou", command=menubarfunctions.open_TRIR_viewer)
        menubar.add_cascade(label="TRIR", menu=TRIRmenu)

        D2IRmenu = tk.Menu(menubar, tearoff=0)
        D2IRmenu.add_command(label="import 2D-IR data", command=donothing)
        D2IRmenu.add_command(label="2D-IR viewer", command=donothing)
        D2IRmenu.add_separator()
        D2IRmenu.add_command(label="construction!", command=donothing) 
        menubar.add_cascade(label="2D-IR", menu=D2IRmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=donothing)
        helpmenu.add_command(label="Documentation.", command=menubarfunctions.opendocumentation)
        menubar.add_cascade(label="Help", menu=helpmenu)
        return menubar





class menubarfunctions():
    def destroy_currentwindow():
        for widget in frame.winfo_children():
            widget.destroy()
        #frame.destroy()

    def open_TRIR_viewer():
        print('...')
        menubarfunctions.destroy_currentwindow()
        TRIRviewer.TRIR_viewerstartup.starter(frame)

    def open_TRIR_import():
        print('import window...')
        menubarfunctions.destroy_currentwindow()
        TRIRimporter.TRIR_import_top_window.TRIR_window_import(frame)

    def open_FTIR_viewer():
        print('opening FTIR viewer')
        menubarfunctions.destroy_currentwindow()
        FTIRviewer.dataconstruct.init_dict()
        FTIRviewer.FTIR_viewerstartup.starter(frame)

    def open_2dir_viewer():
        print('opening module for 2D-IR analysis')
        menubarfunctions.destroy_currentwindow()
        
        

    
    def opendocumentation():
        print('open topwindorw for doc')
        top = tk.Toplevel()
        top.geometry('700x900')
        top.title('IRIS-documentation')
        viewer = pdf.ShowPdf()
        pdfframe = viewer.pdf_view(top,pdf_location = r"IRIS/SETUP/Fehlerrechnung.pdf", width = 200, height = 200)
        pdfframe.pack()

        



   

class startup:
    def __init__(self):
        global root
        root = tk.Tk()
        root.title('IRIS"')
        root.geometry('1300x700')
        root.configure(background='grey25')

        try:
            timer.frame_timer(root)
        except:
            print('Timer not available')

        def on_closing():
            if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
                plt.close()
                root.destroy()

        root.config(menu=mMenubar.initmenu(root))
        root.protocol("WM_DELETE_WINDOW", on_closing) 
        root.mainloop()

class timer():

    def frame_timer(parent):
        def update_time():
            string = strftime("%H:%M:%S %A %d %Y")
            lbl1.config(text=string)
            lbl1.update()
            lbl1.after(1000, update_time)

        string = strftime("%H:%M:%S %A %d %Y")
        global frame 
        frame = tk.Frame(parent, width = 1300, height = 700, bg = 'grey25')
        frame.place(x = 0, y = 0)
        tk.Label(frame, text = 'IRIS', width = 32, height =2, font = ('Helvetica', 30)).place(x=380,y=220)
        tk.Label(frame, text = 'AKB Dataanalysis-Tool copyright by M.Schick', width = 92, height =2, font = ('Helvetica', 10)).place(x=380,y=300)
        lbl1 = tk.Label(frame, text = list, width = 39, height = 10, font = ('Arial', 25))
        lbl1.place(x = 380, y = 350)
        lbl1.config(text=string)
        lbl1.after(1000, update_time)

        

startup()


