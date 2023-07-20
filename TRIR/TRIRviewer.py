import tkinter as tk
from PIL import Image, ImageTk

import numpy as np
from scipy import optimize as opt
from scipy import signal
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap


from TRIR import pyTRIR
from TRIR import pyTRIRbgcorr
from TRIR import TRIRimporter





class TRIR_viewerstartup():
    def starter(parent):
        global jsondatasetviewer
        jsondatasetviewer = TRIRimporter.getjsonfile()
        TRIR_viewerstartup.toolframesetup(parent)
        TRIR_viewerstartup.plotframesetup(parent)

    def toolframesetup(parent):
        global statusbox,toolframe
        toolframe = tk.Frame(parent)
        toolframe.config(borderwidth=2, relief="ridge",bg='grey20', width=399)
        tk.Label(toolframe,text='Toolbar:',font=('Arial',11),fg='white',bg='grey25',width = 55).place(x=0,y=0)

        #statustask = tk.Label(self.toolframe ,text='root',font=('Courier',10),bg ='white',fg='black',width=60,height=2)
        #statustask.pack(anchor = "w", side = "bottom")
        commandf = tk.Frame(toolframe, borderwidth=2, relief="ridge", width=400)
        commandf.pack(anchor = "w", side = "bottom")
        statusbox = tk.Listbox(commandf,font=('Courier',10),bg ='white',fg='black',width=60,height=4)
                #listbox.pack(side = tk.LEFT, fill = tk.BOTH)
        statusbox.place(x=0,y=450)
        commandscroll = tk.Scrollbar(commandf)
        statusbox.insert(0, 'root')





    









        #############################   COMMANDS FOR WIDGETS   #############################
        class toolframe_widget_commands():
            def __init__():
                print('command widgets')

            def plotbutt():
                TRIR_viewerstartup.plotdata
            





        #############################   ALLWIDGETS PLACEMENT   #############################
        class toolframe_widget():
            def placewidgets():
                print('placing widgets in toolframe: starting <func toolframe_widgets>')
                plotbutton =tk.Button(toolframe,text='plot',bg="grey90", fg="darkred",font=('Arial',20) ,width= 15,borderwidth=1, command=toolframe_widget_commands.plotbutt)
                plotbutton.place(x=10,y=20)

                global logscalex
                tk.Label(toolframe,bg='grey25',fg='white',text='Logscale:',font=('Arial',10)).place(x=250,y=20)
                logscalex = tk.BooleanVar()
                tk.Checkbutton(toolframe,variable=logscalex,bg='grey20').place(x=330,y=20)
                global levelentry
                tk.Label(toolframe,bg='grey25',text='Levels:',font=('Arial',12),fg='white').place(x=250,y=50)
                levelentry = tk.Entry(toolframe,bg='black',fg='white',width=10,borderwidth=0,font=('Arial',12))
                levelentry.insert(0,'20')
                levelentry.place(x=290,y=50)
                global maxfacentry
                tk.Label(toolframe,bg='grey25',text='opacity:',font=('Arial',12),fg='white').place(x=250,y=80)
                maxfacentry = tk.Entry(toolframe,bg='black',fg='white',width=10,borderwidth=0,font=('Arial',12))
                maxfacentry.insert(0,'0.8')
                maxfacentry.place(x=290,y=80)
                
            
                print('class toolframe_widgets successfully loaded all widgets')

        toolframe_widget.placewidgets()
        #toolframe.pack(side= tk.LEFT, fill=tk.Y, expand=0, anchor= tk.S)
        toolframe.place(x=0,y=0,width=400,height=700)






















#%%PLOTFRAME setup


    def plotframesetup(parent):
        print('plotframe function: <starting plotframesetup>')
        global fig,canvas2d,main_ax,y_hist,x_hist
        canvaframe = tk.Frame(parent)
        canvaframe.config(background='grey25')
        
        fig = plt.figure(2,figsize=(10, 10))
        grid = fig.add_gridspec(6, 6, hspace=0.01, wspace=0.01,bottom=0.09,top=0.95,left=0.05,right=0.95)
        main_ax = fig.add_subplot(grid[1:, 1:])
        y_hist = fig.add_subplot(grid[1:, 0],sharey=main_ax)
        x_hist = fig.add_subplot(grid[0, 1:-1], sharex=main_ax)
       
        main_ax.set_xlabel('x')
        y_hist.set_ylabel('y')
        x_hist.xaxis.set_visible(False)

        canvas2d = FigureCanvasTkAgg(fig, master=parent)
        canvas2d.get_tk_widget().place(x=420,y=35,width=900,height=600)
        toolbar2d = NavigationToolbar2Tk(canvas2d,canvaframe)
        toolbar2d.pack(side=tk.TOP, fill=tk.BOTH) 

        canvaframe.place(x=420,y=0,width=900,height=35)

        TRIR_viewerstartup.plotdata


    def clearcanva():
        main_ax.cla()
        y_hist.cla()
        x_hist.cla()
        #plt.clf()
        #try:
            #cb.remove()
        #except:
            #print('cb not defined')

        canvas2d.draw()


    
























#%%PLOTFRAME setup
    def plotdata():
        print('plotting')
        levelnum = levelentry.get()
        colormap= 'RdBu_r'


        maxval,minval= pyTRIR.colormapsfor_TRIR.findmaxval(jsondatasetviewer['data'])
        main_ax.contourf(jsondatasetviewer['delays'],jsondatasetviewer['wn'],jsondatasetviewer['data'],levels=levelnum,cmap=colormap,vmin=minval,vmax=maxval,alpha=1)#,vmin=cmin,vmax=cmax)


        #map=main_ax.contourf(data,levels=20,cmap='RdBu_r')
        fig.colorbar(map, ax=main_ax)
        canvas2d.draw()
            












    

    