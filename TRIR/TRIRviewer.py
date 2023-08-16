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
                print('pl')
                TRIR_viewerstartup.plotdata()
            





        #############################   ALLWIDGETS PLACEMENT   #############################
        class toolframe_widget():
            def placewidgets():
                print('placing widgets in toolframe: starting <func toolframe_widgets>')
                plotbutton =tk.Button(toolframe,text='plot',bg="grey90", fg="darkred",font=('Arial',20) ,width= 15,borderwidth=1, command=toolframe_widget_commands.plotbutt)
                plotbutton.place(x=10,y=20)

                global logscalex
                tk.Label(toolframe,bg='grey25',fg='white',text='Logscale:',font=('Arial',10)).place(x=200,y=80)
                logscalex = tk.BooleanVar()
                tk.Checkbutton(toolframe,variable=logscalex,bg='grey20').place(x=300,y=80)
                global levelentry
                tk.Label(toolframe,bg='grey25',text='Levels:',font=('Arial',10),fg='white').place(x=200,y=110)
                levelentry = tk.Entry(toolframe,bg='black',fg='white',width=10,borderwidth=0,font=('Arial',10))
                levelentry.insert(0,'20')
                levelentry.place(x=300,y=110)
                global maxfacentry
                tk.Label(toolframe,bg='grey25',text='opacity:',font=('Arial',10),fg='white').place(x=200,y=140)
                maxfacentry = tk.Entry(toolframe,bg='black',fg='white',width=10,borderwidth=0,font=('Arial',10))
                maxfacentry.insert(0,'0.8')
                maxfacentry.place(x=300,y=140)

                global cutoffODvalue
                tk.Label(toolframe,bg='grey25',text='clip val:',font=('Arial',10),fg='white').place(x=200,y=170)
                cutoffODvalue = tk.Entry(toolframe,bg='black',fg='white',width=10,borderwidth=0,font=('Arial',10))
                cutoffODvalue.insert(0,'')
                cutoffODvalue.place(x=300,y=170)

                global gridbox2d
                tk.Label(toolframe,bg='grey25',fg='white',text='Grid:',font=('Arial',10)).place(x=200,y=200)
                gridbox2d = tk.BooleanVar()
                tk.Checkbutton(toolframe,variable=gridbox2d,bg='grey20').place(x=330,y=197)

                global colorm
                tk.Label(toolframe,bg='grey25',fg='white',text='colormap:',font=('Arial',10)).place(x=200,y=230)
                colorm = tk.StringVar()
                colormoptions = ['RdBu_r','seismic','custom','viridis', 'spring', 'PRGn', 'gnuplot']
                colorm.set(colormoptions[0])
                colormopt = tk.OptionMenu(toolframe, colorm, *colormoptions)
                colormopt.config(bg='grey25',fg='white',font=('Arial',10))
                colormopt.place(x=300,y=230,width=70)

                global xhist,yhist
                tk.Label(toolframe,bg='grey25',fg='white',text='xhist:',font=('Arial',10)).place(x=10,y=80)
                xhist = tk.Entry(toolframe,bg='black',fg='white',width=11,borderwidth=0,font=('Arial',10))
                xhist.insert(0,'0')
                xhist.place(x=50,y=80)
                #tk.Button(toolf,text='->',bg="grey90", fg="darkred",font=('Arial',10) ,width= 1,borderwidth=1, command=buttoncommands2d.platzhalter).place(x=130,y=299)
                    
                tk.Label(toolframe,bg='grey25',fg='white',text='yhist:',font=('Arial',10)).place(x=10,y=110)
                yhist = tk.Entry(toolframe,bg='black',fg='white',width=11,borderwidth=0,font=('Arial',10))
                yhist.insert(0,'0')
                yhist.place(x=50,y=110)
                tk.Button(toolframe,text='set histogram',bg="grey90", fg="darkred",font=('Arial',10) ,width= 12,borderwidth=1, command=TRIR_viewerstartup.setyhist).place(x=10,y=140)
                
            
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
    
    def setyhist():
                points = plt.ginput(n=1,timeout=30, show_clicks=True, mouse_add = plt.MouseButton.LEFT,mouse_pop= plt.MouseButton.RIGHT,mouse_stop = plt.MouseButton.MIDDLE)
                points = points[0]
                yhist.delete(0, 'end')
                yhist.insert(1,str(round(points[0],4)))
                xhist.delete(0, 'end')
                xhist.insert(1,str(round(points[1],4)))
                TRIR_viewerstartup.plotdata()


    
























#%%PLOTFRAME setup
    def plotdata():
        print('plotting')
        TRIR_viewerstartup.clearplot()
        levelnum = int(levelentry.get())
        colormap= str(colorm.get())
        if colorm.get() == 'custom':
            colormap = pyTRIR.colormapsfor_TRIR.create_custom_colormap('#0056AC', '#AC0000')


        databgsub = pyTRIR.modify_arrays.subtract_bg(jsondatasetviewer)

        if cutoffODvalue.get()=='':
            maxval,minval= pyTRIR.colormapsfor_TRIR.findmaxval(databgsub,maxfacentry.get())
        else:
            maxval,minval= float(cutoffODvalue.get()),-float(cutoffODvalue.get())

        clipped_databgsub = np.clip(databgsub,a_min=minval,a_max = maxval)
        main_ax.contourf(jsondatasetviewer['delays'],jsondatasetviewer['wn'],clipped_databgsub,levels=levelnum,cmap=colormap,vmin=minval,vmax=maxval,alpha=1)#'RdBu_r''seismic'
        print('Max '+str(maxval) + ' & min '+str(minval))

        global cb
        map=main_ax.contourf(clipped_databgsub,levels=20,cmap=colormap)
        cb = fig.colorbar(map, ax=main_ax)

        yhistdelay = float(yhist.get())
        yhistdelayindex = np.argmin(abs(jsondatasetviewer['delays']-yhistdelay))
        yhistdelay = jsondatasetviewer['delays'][yhistdelayindex]
        yhist.delete(0, 'end')
        yhist.insert(1,str(round(yhistdelay,2)))
        yhisto = clipped_databgsub[:,yhistdelayindex]
                
        xhistwn = float(xhist.get())
        xhistwnindex = np.argmin(abs(jsondatasetviewer['wn']-xhistwn))
        xhistwn = jsondatasetviewer['wn'][xhistwnindex]
        xhist.delete(0, 'end')
        xhist.insert(1,str(round(xhistwn,4)))
        xhisto = clipped_databgsub[xhistwnindex,:]


        #plot setup axis
        main_ax.set_xlabel('time [ps]')
        main_ax.set_ylabel(r'wavenumber $cm^{-1}$')
        main_ax.set_ylim(np.min(jsondatasetviewer['wn']),np.max(jsondatasetviewer['wn']))
        main_ax.set_xlim(np.min(jsondatasetviewer['delays']),np.max(jsondatasetviewer['delays']))
        if logscalex.get()== True:
            main_ax.set_xscale('log')
            xaxislow,xaxishigh = pyTRIR.modify_arrays.getlogaxis(jsondatasetviewer)
            main_ax.set_xlim(xaxislow,xaxishigh)

        main_ax.grid(gridbox2d.get())

        cb.set_label(r'∆OD', rotation=270)   

        y_hist.plot(yhisto,jsondatasetviewer['wn'])
        y_hist.invert_xaxis()
        y_hist.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        y_hist.set_xlabel('∆OD')

        x_hist.plot(jsondatasetviewer['delays'],xhisto)
        x_hist.ticklabel_format(style='sci', axis='y', scilimits=(2,0))
        x_hist.set_ylabel('∆OD')


            


        y_hist.set_ylabel(r'wavenumber $cm^{-1}$')

        canvas2d.draw()
    
    def clearplot():
        main_ax.cla()
        y_hist.cla()
        x_hist.cla()
        #plt.clf()
        try:
            cb.remove()
        except:
            print('colorbar not defined')
            












    

    