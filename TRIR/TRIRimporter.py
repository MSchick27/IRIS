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


        
def getjsonfile():
    return jsondataset











class TRIR_import_top_window():
    def TRIR_window_import(parent):
        print('opening import window')

        TRIR_import_top_window.toolframesetup(parent)
        TRIR_import_top_window.plotframesetup(parent)


    



#%%TOOLFRAME setup
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
            def refresh(jsondata):
                TRIR_import_top_window.plotthejsondata(jsondata)
                print('function missing refresh plotting')
            def refreshbutton():
                TRIR_import_top_window.plotthejsondata(jsondataset)


            def removerfirstscan():
                newweighteddat = pyTRIR.modify_arrays.sub_delay1(jsondataset['data'])
                jsondataset['data']= newweighteddat


            def import_data_trir():
                global jsondataset
                scanentrystring = scanentry.get()
                delayentrystring = delayentry.get()
                funcoptstring = func.get()
                det_size = int(piximportentry.get())
                

                if funcoptstring == 's2s_signal':
                    #try function am ende addieren
                    jsondataset = pyTRIR.PYTRIR.importinitfunction(scanentrystring,delayentrystring,det_size)

                if funcoptstring == 'weights':
                    jsondataset = pyTRIR.weighted_import.init_weightedimport(scanentrystring,delayentrystring,det_size)

                
                wnlowlabel.config(text=str(round(float(jsondataset['wn'][0]),2)))
                wnhighlabel.config(text=str(round(float(jsondataset['wn'][-1]),2)))

                listbox.delete(0,tk.END)
                for delaytime in jsondataset['delays']:
                    listbox.insert(tk.END, str(round(float(delaytime),5)))
                listbox.select_set(0)

                scannumber.config(text=str(jsondataset['scannumber']))
                scanentry.delete(0,tk.END)
                scanentry.insert(0,str(jsondataset['scanslice']))
                delaynumber.config(text=str(jsondataset['delaynumber']))
                delayentry.delete(0,tk.END)
                delayentry.insert(0,str(jsondataset['delayslice']))


                toolframe_widget_commands.refresh(jsondataset)


            def generate_background():
                polynomial = int(polyentry.get())
                pixelslic = str(pixelentry.get())
                delayslice = str(fitdelayentry.get())
                jsondataset['bgdata'] = pyTRIRbgcorr.TRIRbgcorr(jsondataset,polynomial,delayslice,pixelslic)

            def export_data():
                pyTRIR.PYTRIR.exportdata(jsondataset)
                
                







        #############################   ALLWIDGETS PLACEMENT   #############################
        class toolframe_widget():
            def placewidgets():
                print('placing widgets in toolframe: starting <func toolframe_widgets>')
                plotbutton =tk.Button(toolframe,text='refresh',bg="grey90", fg="darkred",font=('Arial',20) ,width= 15,borderwidth=1, command=toolframe_widget_commands.refreshbutton)
                plotbutton.place(x=10,y=20)

                global logscalex
                tk.Label(toolframe,bg='grey25',fg='white',text='Logscale:',font=('Arial',10)).place(x=230,y=20)
                logscalex = tk.BooleanVar()
                tk.Checkbutton(toolframe,variable=logscalex,bg='grey20').place(x=300,y=20)
                global levelentry
                tk.Label(toolframe,bg='grey25',text='Levels:',font=('Arial',10),fg='white').place(x=230,y=50)
                levelentry = tk.Entry(toolframe,bg='black',fg='white',width=10,borderwidth=0,font=('Arial',12))
                levelentry.insert(0,'20')
                levelentry.place(x=290,y=50)
                global maxfacentry
                tk.Label(toolframe,bg='grey25',text='opacity:',font=('Arial',10),fg='white').place(x=230,y=80)
                maxfacentry = tk.Entry(toolframe,bg='black',fg='white',width=10,borderwidth=0,font=('Arial',12))
                maxfacentry.insert(0,'0.8')
                maxfacentry.place(x=290,y=80)
                removescanone = tk.Button(toolframe,text='subscan 1',bg="grey90", fg="darkred",font=('Arial',10) ,width= 10,borderwidth=1, command=toolframe_widget_commands.removerfirstscan)
                removescanone.place(x=250,y=110)
                



                global func
                func = tk.StringVar()
                funcoptions = ['s2s_signal','averaged','weights']
                func.set(funcoptions[0])
                funcopt = tk.OptionMenu(toolframe, func, *funcoptions)
                funcopt.config(bg='grey25',fg='white',font=('Arial',14))
                funcopt.place(x=10,y=55,width=120)
                importbutton =tk.Button(toolframe,text='import',bg="grey90", fg="darkred",font=('Arial',16) ,width= 13,borderwidth=1, command=toolframe_widget_commands.import_data_trir)
                importbutton.place(x=10,y=80)

                global piximportentry
                tk.Label(toolframe,bg='grey25',text='Detektor size:',font=('Arial',10),fg='white').place(x=10,y=120)
                piximportentry = tk.Entry(toolframe,bg='black',fg='white',width=10,borderwidth=0,font=('Arial',10))
                piximportentry.insert(0,'32')
                piximportentry.place(x=120,y=120)

                global wnlowlabel,wnhighlabel
                tk.Label(toolframe,bg='grey25',text='wavenumber low:',font=('Arial',10),fg='white').place(x=10,y=170)
                wnlowlabel = tk.Label(toolframe,bg='grey25',text='0',font=('Arial',10),fg='white')
                wnlowlabel.place(x=120,y=170)
                tk.Label(toolframe,bg='grey25',text='wavenumber high:',font=('Arial',10),fg='white').place(x=10,y=190)
                wnhighlabel = tk.Label(toolframe,bg='grey25',text='3000',font=('Arial',10),fg='white')
                wnhighlabel.place(x=120,y=190)

                global listbox
                tk.Label(toolframe,bg='grey25',text='Delays',font=('Arial',10),fg='white').place(x=10,y=230)
                listboxframe = tk.Frame(toolframe, borderwidth=1, relief="ridge")
                listboxframe.place(x= 10,y=250,width=100,height=100)
                listbox = tk.Listbox(listboxframe)
                listbox.place(x=0,y=0,width = 100,height= 99)
                scrollbar = tk.Scrollbar(listboxframe)
                #for i in range(43):
                 #   listbox.insert(tk.END, str(i))

                listbox.config(yscrollcommand = scrollbar.set)
                #listbox.bind("<<ListboxSelect>>",scrollframe.listboxchange)
                scrollbar.config(command = listbox.yview)

                global scanentry,scannumber
                tk.Label(toolframe,bg='grey25',text='Scannumber:',font=('Arial',10),fg='white').place(x=140,y=230)
                scannumber = tk.Label(toolframe,bg='grey25',text='67',font=('Arial',10),fg='white')
                scannumber.place(x=230,y=230)
                tk.Label(toolframe,bg='grey25',text='Slice:',font=('Arial',10),fg='white').place(x=260,y=230)
                scanentry = tk.Entry(toolframe,bg='black',fg='white',width=10,borderwidth=0,font=('Arial',10))
                scanentry.insert(0,':')
                scanentry.place(x=300,y=230)


                global delayentry,delaynumber
                tk.Label(toolframe,bg='grey25',text='Delaynumber:',font=('Arial',10),fg='white').place(x=140,y=260)
                delaynumber = tk.Label(toolframe,bg='grey25',text='43',font=('Arial',10),fg='white')
                delaynumber.place(x=230,y=260)
                tk.Label(toolframe,bg='grey25',text='Slice:',font=('Arial',10),fg='white').place(x=260,y=260)
                delayentry = tk.Entry(toolframe,bg='black',fg='white',width=10,borderwidth=0,font=('Arial',12))
                delayentry.insert(0,':')
                delayentry.place(x=300,y=260)




                #Backgroundsubtraction part
                global polyentry,pixelentry,fitdelayentry
                tk.Label(toolframe,bg='grey25',text='Background subtraction:',font=('Arial',14),fg='white').place(x=30,y=400)
                tk.Label(toolframe,bg='grey25',text='Polynomial Order:',font=('Arial',10),fg='white').place(x=10,y=440)
                polyentry = tk.Entry(toolframe,bg='black',fg='white',width=10,borderwidth=0,font=('Arial',12))
                polyentry.insert(0,'5')
                polyentry.place(x=170,y=440)
                tk.Label(toolframe,bg='grey25',text='Pixels to Fit:',font=('Arial',10),fg='white').place(x=10,y=470)
                pixelentry = tk.Entry(toolframe,bg='black',fg='white',width=10,borderwidth=0,font=('Arial',12))
                pixelentry.insert(0,':')
                pixelentry.place(x=170,y=470)
                tk.Label(toolframe,bg='grey25',text='Fit to delay:',font=('Arial',10),fg='white').place(x=10,y=500)
                fitdelayentry = tk.Entry(toolframe,bg='black',fg='white',width=10,borderwidth=0,font=('Arial',12))
                fitdelayentry.insert(0,':')
                fitdelayentry.place(x=170,y=500)



                jsonbutton =tk.Button(toolframe,text='generate Background',bg="grey90", fg="darkred",font=('Arial',10) ,width= 15,borderwidth=1, command=toolframe_widget_commands.generate_background)
                jsonbutton.place(x=10,y=540)
                savejsonbutton =tk.Button(toolframe,text='Save json',bg="grey90", fg="darkred",font=('Arial',10) ,width= 15,borderwidth=1)#, command=)
                savejsonbutton.place(x=10,y=580)

                exportdataopus = tk.Button(toolframe,text='export data',bg="grey90", fg="darkred",font=('Arial',12) ,width= 15,borderwidth=1, command=toolframe_widget_commands.export_data)
                exportdataopus.place(x=10,y=620)


                print('class toolframe_widgets successfully loaded all widgets')

        toolframe_widget.placewidgets()
        #toolframe.pack(side= tk.LEFT, fill=tk.Y, expand=0, anchor= tk.S)
        toolframe.place(x=0,y=0,width=400,height=700)






















#%%PLOTFRAME setup


    def plotframesetup(parent):
        print('plotframe function: <starting plotframesetup>')
        global fig,canvas2d,data_ax,bg_ax,rms_bg_ax,noise_ax,noiseall_ax,diff_ax
        canvaframe = tk.Frame(parent)
        canvaframe.config(background='grey25')
        
        fig = plt.figure(0,figsize=(10, 10))
        grid = fig.add_gridspec(11, 11, hspace=0.01, wspace=0.01,bottom=0.09,top=0.95,left=0.05,right=0.95)
        data_ax = fig.add_subplot(grid[0:3, 0:3])
        data_ax.set_xlabel('time [ps]')
        data_ax.set_title('raw')
        bg_ax = fig.add_subplot(grid[0:3, 4:7],sharey=data_ax,sharex=data_ax)
        bg_ax.set_title('background')
        rms_bg_ax = fig.add_subplot(grid[0:3, 8:11])
        rms_bg_ax.set_title('std deviation')
        rms_bg_ax.set_xlabel('scans')
        rms_bg_ax.set_ylabel('pixels')
        noise_ax = fig.add_subplot(grid[4:7, 0:3])
        noise_ax.set_title('noise')
        noise_ax.set_xlabel('scans')
        noise_ax.set_ylabel('pixels')
        noiseall_ax = fig.add_subplot(grid[8:11, 0:3])
        noiseall_ax.set_title('trace of all scans')
        noiseall_ax.set_xlabel('scans')
        noiseall_ax.set_ylabel('Pixels')
        diff_ax = fig.add_subplot(grid[4:11, 4:11],sharey=data_ax,sharex=data_ax)
        diff_ax.set_title('Diff Signal')
        diff_ax.set_xlabel('time')
        diff_ax.set_ylabel('wn')

       
        

        canvas2d = FigureCanvasTkAgg(fig, master=parent)
        canvas2d.get_tk_widget().place(x=420,y=35,width=900,height=600)
        toolbar2d = NavigationToolbar2Tk(canvas2d,canvaframe)
        toolbar2d.pack(side=tk.TOP, fill=tk.BOTH) 

        canvaframe.place(x=420,y=0,width=900,height=35)

    def clearcanva():
        data_ax.cla()
        bg_ax.cla()
        rms_bg_ax.cla()
        diff_ax.cla()
        noise_ax.cla()
        noiseall_ax.cla()
        rms_bg_ax.cla()

        data_ax.set_xlabel('time [ps]')
        bg_ax.set_title('background')
        rms_bg_ax.set_title('std deviation')
        rms_bg_ax.set_xlabel('delays')
        rms_bg_ax.set_ylabel('pixels')
        noise_ax.set_title('noise')
        noise_ax.set_xlabel('scans in delay x')
        noise_ax.set_ylabel('pixels')
        noiseall_ax.set_title('trace of all scans')
        noiseall_ax.set_xlabel('scans')
        noiseall_ax.set_ylabel('Pixels')
        diff_ax.set_title('Diff Signal')
        diff_ax.set_xlabel('time')
        diff_ax.set_ylabel('wn')

        canvas2d.draw()
























#%%PLOTFRAME setup
    def plotthejsondata(jsondataset):
        plt.figure(0,figsize=(10, 10))
        levelnum = int(levelentry.get())
        TRIR_import_top_window.clearcanva()

        maxval,minval= pyTRIR.colormapsfor_TRIR.findmaxval(jsondataset['data'],0.8)
        data_ax.contourf(jsondataset['delays'],jsondataset['wn'],jsondataset['data'],levels=levelnum,cmap='RdBu_r',vmin=minval,vmax=maxval,alpha=1)#,vmin=cmin,vmax=cmax)
        maxval,minval= pyTRIR.colormapsfor_TRIR.findmaxval(jsondataset['bgdata'],0.8)
        bg_ax.contourf(jsondataset['delays'],jsondataset['wn'],jsondataset['bgdata'],levels=levelnum,cmap='RdBu_r',vmin=minval,vmax=maxval,alpha=1)
        
        #rmsdata = pyTRIR.modify_arrays.subtract_bg_rms(jsondataset)
        maxval,minval= pyTRIR.colormapsfor_TRIR.findmaxval(jsondataset['std_deviation'],maxfacentry.get())
        clipped_stddev = np.clip(jsondataset['std_deviation'],a_min=minval,a_max = maxval)
        rms_bg_ax.pcolormesh(jsondataset['delays'],np.arange(len(jsondataset['wn'])),clipped_stddev,cmap='magma')

        
        databgsub = pyTRIR.modify_arrays.subtract_bg(jsondataset)
        maxval,minval= pyTRIR.colormapsfor_TRIR.findmaxval(databgsub,maxfacentry.get())
        clipped_databgsub = np.clip(databgsub,a_min=minval,a_max = maxval)
        diff_ax.contourf(jsondataset['delays'],jsondataset['wn'],clipped_databgsub,levels=levelnum,cmap='RdBu_r',vmin=minval,vmax=maxval,alpha=1)#'RdBu_r''seismic'
        print('Max '+str(maxval) + ' & min '+str(minval))
        
        try:
            for item in listbox.curselection():
                noisedelayindex = item
            noise_ax.pcolormesh(np.arange(np.shape(jsondataset['noise'])[1]),np.arange(np.shape(jsondataset['noise'])[2]),np.transpose(jsondataset['noise'][noisedelayindex]),cmap='viridis')
        except:
            print('SCANPLOT: Select delay to display scans')
            print(str(listbox.curselection()))
            noise_ax.pcolormesh(np.arange(np.shape(jsondataset['noise'])[1]),np.arange(np.shape(jsondataset['noise'])[2]),np.transpose(jsondataset['noise'][0]),cmap='viridis')

        noisealldata= pyTRIR.modify_arrays.noiseallscans(jsondataset)
        maxval,minval= pyTRIR.colormapsfor_TRIR.findmaxval(jsondataset['noise'],maxfacentry.get())
        noiseall_ax.pcolormesh(np.arange(np.shape(noisealldata)[0]),np.arange(np.shape(noisealldata)[1]),noisealldata.transpose(),cmap='viridis')





        if logscalex.get()== True:
            data_ax.set_xscale('log')
            xaxislow,xaxishigh = pyTRIR.modify_arrays.getlogaxis(jsondataset)
            data_ax.set_xlim(xaxislow,xaxishigh)
            rms_bg_ax.set_xscale('log')
            rms_bg_ax.set_xlim(xaxislow,xaxishigh)

        if func.get() == 'weights':
            noise_ax.set_title('wheights')
        
        if func.get() == 's2s_signal':
            noise_ax.set_title('s2s_signal')

        canvas2d.draw()
        print('plotted')

        plt.close()











