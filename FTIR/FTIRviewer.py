import tkinter as tk
from tkinter import filedialog
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
import os
import json
import random
import pandas as pd


from FTIR import pyFTIR,pyFTIR_dicts,pyFTIR_FITS

dirpath = os.path.dirname(os.path.dirname(__file__))
jsondict = {}

class dataconstruct():
    def init_dict():
        global init_dict
        init_dict = pyFTIR_dicts.init()

    def j_son(x,y,bg,bgkey,bgscale,show,col,lwidth,lstyle,lab,subpl):
        dataset = pyFTIR_dicts.j_son_spectrum(x,y,bg,bgkey,bgscale,show,col,lwidth,lstyle,lab,subpl)
        return dataset
    













class FTIR_viewerstartup():
    def starter(parent):
        FTIR_viewerstartup.toolframesetup(parent)
        FTIR_viewerstartup.plotframesetupIR(parent)














        
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% SETTING THE UPPER TOOLBOX #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
        statusbox.place(x=0,y=0)
        commandscroll = tk.Scrollbar(commandf)
        statusbox.insert(0, 'root')

        def imageset():
                global PLOTT
                PLOTT = Image.open(str(dirpath)+'/FTIR/pics/Plotbut.png')
                PLOTT = PLOTT.resize((150, 30), Image.ANTIALIAS)
                PLOTT = ImageTk.PhotoImage(PLOTT)
                global CLEAR
                CLEAR = Image.open(str(dirpath)+'/FTIR/pics/clearbut.png')
                CLEAR = CLEAR.resize((100, 20), Image.ANTIALIAS)
                CLEAR = ImageTk.PhotoImage(CLEAR)
                global arrow
                arrow_g = Image.open(str(dirpath)+'/FTIR/pics/arrow.jpeg')
                arrow_g = arrow_g.resize((18, 18), Image.ANTIALIAS)
                arrow = ImageTk.PhotoImage(arrow_g)
                global washer
                washer = Image.open(str(dirpath)+'/FTIR/pics/backg.png')
                washer = washer.resize((18, 18), Image.ANTIALIAS)
                washer = ImageTk.PhotoImage(washer)
                global export
                export = Image.open(str(dirpath)+'/FTIR/pics/export.jpg')
                export = export.resize((18, 18), Image.ANTIALIAS)
                export = ImageTk.PhotoImage(export)

        imageset()

















        class buttoncommands:
            def test():
                print('test')

            def import_data_():
                print('select your dpt data files')
                global jsondict
                jsondict = pyFTIR.import_and_export_functions.import_files(statusbox,delimitervar,jsondict,listbox)
                print(jsondict)
                print('JSON generated')

            def import_data_JSON():
                print('select your json FILE')
                global jsondict
                jsondict = pyFTIR.import_and_export_functions.import_JSON_project(statusbox,listbox)

            def export_data_JSON():
                a = filedialog.asksaveasfilename(initialdir = str(dirpath),title = "Save Project")
                newjsonfile = open(str(str(a) + '.json'),'w')
                json.dump(jsondict, newjsonfile)
                newjsonfile.close()
                print('Project saved at: '+str(str(a) + '.json'))


            def delete_data():
                listbox.delete(tk.ANCHOR)
                jsondict.pop(str(datalistbox), None)
                print('file deleted')
            

            def plotplot():
                scrollframe.update_json(datalistbox)
                FTIR_viewerstartup.plot()
                #statustask.configure(text='Plotting',fg='black')
                statusbox.insert(0, 'Plotting...')

            
            def set_ax():
                points = plt.ginput(n=3,timeout=30, show_clicks=True, mouse_add = plt.MouseButton.LEFT,mouse_pop= plt.MouseButton.RIGHT,mouse_stop = plt.MouseButton.MIDDLE)
                print(points)
                x_margin = [round(float(points[0][0]),6),round(float(points[1][0]),6)]
                x_margin.sort()
                y_margin = [round(float(points[0][1]),6),round(float(points[1][1]),6)]
                y_margin.sort()
                #print(x_margin)
                xlow.delete(0,tk.END)
                xhigh.delete(0,tk.END)
                ylow.delete(0,tk.END)
                yhigh.delete(0,tk.END)
                xlow.insert(0,str(x_margin[0]))
                xhigh.insert(0,str(x_margin[1]))
                ylow.insert(0,str(y_margin[0]))
                yhigh.insert(0,str(y_margin[1]))
                buttoncommands.plotplot()




        
        class buttons:
             def mainbuttons():
                plotbutton =tk.Button(toolframe,image=PLOTT,borderwidth=0 ,fg='skyblue',bg='grey25',command=buttoncommands.plotplot).place(x=10,y=20)
                clearbutton=tk.Button(toolframe,bg='grey25',fg='white',borderwidth=0,image=CLEAR, command=buttoncommands.test).place(x=180,y=25)
                axisbutton = tk.Button(toolframe,bg='grey90',fg='darkred',borderwidth=1,text='axis', command=buttoncommands.set_ax).place(x=290,y=95)
                loadjson = tk.Button(toolframe,bg='grey90',fg='darkred',font=('Arial',10),borderwidth=1,text='json', command=buttoncommands.import_data_JSON).place(x=280,y=230)
                loaddata = tk.Button(toolframe,image=arrow, bg='grey25',fg='white',borderwidth=0, command=buttoncommands.import_data_).place(x=280,y=270)
                deldata = tk.Button(toolframe,image=washer, bg='grey25',fg='white',borderwidth=0, command=buttoncommands.delete_data).place(x=305,y=270)
                exjson = tk.Button(toolframe,image=export, bg='grey25',fg='white',borderwidth=0, command=buttoncommands.export_data_JSON).place(x=330,y=270)
                
                global xlow,xhigh,ylow,yhigh
                global xlabel,ylabel,titleentry, ymulti
                global gridbox,delimiteropt,delimitervar,labelbox

                tk.Label(toolframe,bg='grey25',text='x:',font=('Arial',10),fg='white').place(x=10,y=100)
                xlow = tk.Entry(toolframe,bg='black',fg='white',width=12,borderwidth=0,font=('Arial',10))
                xlow.insert(0,float(init_dict['xlow']))
                xlow.place(x=25,y=110)
                xhigh = tk.Entry(toolframe,bg='black',fg='white',width=12,borderwidth=0,font=('Arial',10))
                xhigh.insert(0,float(init_dict['xhigh']))
                xhigh.place(x=25,y=90)

                xlabel = tk.Entry(toolframe,bg='black',fg='white',width=20,borderwidth=0,font=('Arial',10))
                xlabel.insert(1,str(init_dict['xlabel']))
                xlabel.place(x=10,y=130)


                tk.Label(toolframe,bg='grey25',text='y:',font=('Arial',10),fg='white').place(x=160,y=100)
                ylow = tk.Entry(toolframe,bg='black',fg='white',width=12,borderwidth=0,font=('Arial',10))
                ylow.insert(0,float(init_dict['ylow']))
                ylow.place(x=200,y=110)
                yhigh = tk.Entry(toolframe,bg='black',fg='white',width=12,borderwidth=0,font=('Arial',10))
                yhigh.insert(0,float(init_dict['yhigh']))
                yhigh.place(x=200,y=90)

                ylabel = tk.Entry(toolframe,bg='black',fg='white',width=20,borderwidth=0,font=('Arial',10))
                ylabel.insert(-1,str(init_dict['ylabel']))
                ylabel.place(x=200,y=130)

                tk.Label(toolframe,bg='grey25',text='y_fac:',font=('Arial',10),fg='white').place(x=160,y=150)
                ymulti = tk.Entry(toolframe,bg='black',fg='white',width=12,borderwidth=0,font=('Arial',10))
                ymulti.insert(-1,str(init_dict['ymulti']))
                ymulti.place(x=200,y=150)

                titleentry = tk.Entry(toolframe,bg='black',fg='white',width=20,borderwidth=0,font=('Arial',10))
                titleentry.insert(0,'Title')
                titleentry.place(x=10,y=65)


                tk.Label(toolframe,bg='grey25',fg='white',text='Grid:',font=('Arial',10)).place(x=10,y=160)
                gridbox = tk.BooleanVar()
                tk.Checkbutton(toolframe,variable=gridbox,bg='grey20').place(x=50,y=157)

                tk.Label(toolframe,bg='grey25',fg='white',text='Legend:',font=('Arial',10)).place(x=10,y=180)
                labelbox = tk.BooleanVar()
                tk.Checkbutton(toolframe,variable=labelbox,bg='grey20').place(x=50,y=177)

                delimitervar = tk.StringVar()
                delimiteroptions = ['tab','space',',',';']
                delimitervar.set(delimiteroptions[0])
                delimiteropt = tk.OptionMenu(toolframe, delimitervar, *delimiteroptions)
                delimiteropt.config(width=3,font=('Arial',10),bg='grey25',fg='white')
                delimiteropt.place(x=280,y=295)



        buttons.mainbuttons()



























        class scrollframe:
            def start_switchableframe():
                global listbox
                listboxframe = tk.Frame(toolframe, borderwidth=1, relief="ridge")
                listboxframe.place(x= 25,y=230,width=240,height=100)
                listbox = tk.Listbox(listboxframe)
                #listbox.pack(side = tk.LEFT, fill = tk.BOTH)
                listbox.place(x=0,y=0,width = 230,height= 99)
                scrollbar = tk.Scrollbar(listboxframe)
                listbox.insert(tk.END, 'no files')

                listbox.config(yscrollcommand = scrollbar.set)
                listbox.bind("<<ListboxSelect>>",scrollframe.listboxchange)
                scrollbar.config(command = listbox.yview)

                global container
                container = tk.Frame(toolframe, borderwidth=2,bg='grey25', relief="ridge")
                container.place(x= 25,y=330,width=340,height=350)
                print('container placed')

            def listboxchange(event):
                global datalistbox
                selection = event.widget.curselection()

                if selection:
                        index = selection[0]
                        datalistbox = event.widget.get(index)
                        scrollframe.rebuild_optionmenu(datalistbox)
                        print('selected: '+str(datalistbox))

                else:
                        print('Please select a data key')

            
            def rebuild_optionmenu(selectedkey):
                for widget in container.winfo_children():
                    widget.destroy()

                global showbox              #SETUP für SHOW checkbox
                tk.Label(container,text='Show:',font=('Arial',10),bg='grey25',fg='white').place(x=5,y=10)
                showbox = tk.BooleanVar()
                showcheckbutton = tk.Checkbutton(container,onvalue=True,offvalue=False,variable=showbox,bg='grey25',command=lambda:scrollframe.update_json(selectedkey))
                showcheckbutton.place(x=40,y=8)

                if jsondict[str(selectedkey)]['show'] == True:
                    showbox.set(True)
                    showcheckbutton.select()
                else:
                    showbox.set(False)
                    showcheckbutton.deselect()

                
                global datalabelentry       #Setup für den LABEL ENTRY
                tk.Label(container,bg='grey25',text='Label:',font=('Arial',10),fg='white').place(x=70,y=10)
                datalabelentry = tk.Entry(container,bg='black',font=('Arial',10),fg='white',width=20,borderwidth=0)
                datalabelentry.insert(0,str(jsondict[str(selectedkey)]['label']))
                datalabelentry.place(x=110,y=10)

                labelchangebutton = tk.Button(container,text='->', bg='grey90',fg='darkred',font=('Arial',10),borderwidth=1, command=lambda:scrollframe.change_key(selectedkey)).place(x=270,y=7)


                #ROW 2 #############################################
                global subplotnum
                tk.Label(container,bg='grey25',text='Plot:',font=('Arial',10),fg='white').place(x=5,y=30)
                subplotnum = tk.IntVar()
                subplotnumoptions = [0,1]
                subplotnum.set(subplotnumoptions[int(jsondict[str(selectedkey)]['subplot'])])
                subplotopt = tk.OptionMenu(container, subplotnum, *subplotnumoptions)
                #subplotopt.config(width=1)
                subplotopt.config(font=('Arial',10),bg='grey25',fg='white')
                subplotopt.place(x=40,y=30,width=40)

                global col
                col = tk.StringVar()
                col.set(str(jsondict[selectedkey]['color']))
                coloptions = ['black','red','lightcoral','blue','skyblue','green','cyan','magenta','darkorange','grey','chocolate'] 
                colopt = tk.OptionMenu(container, col, *coloptions)#,command=lambda:scrollframe.change_json(dataname))
                colopt.config(font=('Arial',10),bg='grey25',fg='white')
                colopt.place(x=100,y=30,width=70)

                global line
                line = tk.StringVar()
                line.set(str(jsondict[selectedkey]['linestyle']))
                lineoptions = ['solid','dashed','dotted','dashdot'] 
                lineopt = tk.OptionMenu(container, line, *lineoptions)#,command=lambda:scrollframe.change_json(dataname))
                lineopt["menu"].config(fg="RED")
                lineopt.config(bg="grey25", fg="white",font=('Arial',10))
                lineopt.place(x=180,y=30,width=70)



                #ROW 3 #############################################
                global bgbox,bgkeyentry, scales
                #SETUP für BG checkbox
                tk.Label(container,bg='grey25',text='Bg:',font=('Arial',10),fg='white').place(x=5,y=60)
                bgbox = tk.BooleanVar()
                bgcheckbutton = tk.Checkbutton(container,onvalue=True,offvalue=False,variable=bgbox,bg='grey25',command=lambda:scrollframe.update_json(selectedkey))
                bgcheckbutton.place(x=40,y=60)
                if jsondict[str(selectedkey)]['bg'] == True:
                    bgbox.set(True)
                    bgcheckbutton.select()
                else:
                    bgbox.set(False)
                    bgcheckbutton.deselect()

                tk.Label(container,bg='grey25',text='Bg key:',font=('Arial',10),fg='white').place(x=70,y=60)
                bgkeyentry = tk.Entry(container,bg='black',width=15,borderwidth=0,font=('Arial',10),fg='white')
                bgkeyentry.insert(0,str(jsondict[str(selectedkey)]['bgkey']))
                bgkeyentry.place(x=115,y=60)

                scales = tk.Scale(container,orient='horizontal',bg="grey25",font=('Arial',10),from_= -0.5, to=1.6,resolution=0.001,length =90,width=10,sliderlength=20,fg='sky blue')
                scales.set(float(jsondict[str(selectedkey)]['bgscale']))
                scales.bind("<ButtonRelease-1>",scrollframe.lambda_update)
                scales.place(x=220,y=50)


                #ROW 4 #############################################
                exportdata = tk.Button(container,text='export', bg="grey90", fg="darkred",font=('Arial',10),borderwidth=1, command=lambda:scrollframe.export_data(selectedkey)).place(x=250,y=90)

                #ROW 5 #############################################
                global promentry
                tk.Label(container,bg='grey25',text='Prominence:',font=('Arial',10),fg='white').place(x=5,y=120)
                promentry = tk.Entry(container,bg='black',fg='white',width=8,borderwidth=0,font=('Arial',10))
                promentry.insert(0, '0.0005')
                promentry.place(x=60,y=120)
                peakbutton = tk.Button(container,text='Peaks',bg="grey90", fg="darkred",font=('Arial',10),width= 6,borderwidth=1, command=lambda:scrollframe.findpeaks(selectedkey,jsondict)).place(x=160,y=120)

                invert = tk.Button(container,text='invt.',bg="grey90", fg="darkred",font=('Arial',10),width= 6,borderwidth=1, command=lambda:scrollframe.invertdata(selectedkey)).place(x=240,y=120)


                #ROW 5 #############################################
                global wavecutentry
                secdev = tk.Button(container,text='2.dev',bg="grey90", fg="darkred",font=('Arial',10) ,width= 4,borderwidth=1, command=lambda:scrollframe.sec_dev(selectedkey)).place(x=180,y=150)
                cut_out = tk.Button(container,text='Cut',bg="grey90", fg="darkred",font=('Arial',10) ,width= 4,borderwidth=1, command=lambda:scrollframe.cut(selectedkey)).place(x=130,y=150)
                wavecutentry = tk.Entry(container,bg='black',fg='white',width=18,borderwidth=0,font=('Arial',10))
                wavecutentry.insert(0, '')
                wavecutentry.place(x=5,y=150)

                ignorebut = tk.Button(container,text='ign',bg="grey90", fg="darkred",font=('Arial',10) ,width= 4,borderwidth=1, command=lambda:scrollframe.ignore(selectedkey)).place(x=250,y=150)
                
                trapzdata = tk.Button(container,text='TRAPZ', bg="grey90", fg="darkred",font=('Arial',10),width= 4,borderwidth=1, command=lambda:scrollframe.show_trapz(selectedkey)).place(x=130,y=170)



                # ROW 6 #############################################
                global polyentry,waveentry
                polyfitdata = tk.Button(container,text='polyFIT', bg="grey90", fg="darkred",font=('Arial',10),width= 6,borderwidth=1, command=lambda:scrollframe.polyfit_data(selectedkey)).place(x=120,y=200)
                tk.Label(container,bg="black", fg="white",font=('Arial',10),text='Polyfit deg:').place(x=10,y=200)
                polyentry = tk.Entry(container,bg='black',fg='white',width=3,borderwidth=0,font=('Arial',10))
                polyentry.insert(0, '5')
                polyentry.place(x=80,y=200)

                waveentry = tk.Entry(container,bg='black',fg='white',width=18,borderwidth=0,font=('Arial',10))
                waveentry.insert(0, '')
                waveentry.place(x=200,y=200)

                # ROW 7 #############################################
                fitband = tk.Button(container,text='Fit', bg="grey90", fg="darkred",font=('Arial',10),width= 6,borderwidth=1, command=lambda:scrollframe.fitbands(selectedkey)).place(x=120,y=230)
                tk.Label(container,bg="black", fg="white",font=('Arial',10),text='Fitting:').place(x=10,y=230)
                fitentry = tk.Entry(container,bg='black',fg='white',width=18,borderwidth=0,font=('Arial',10))
                fitentry.insert(0, '')
                fitentry.place(x=200,y=230)
                global fitmode
                fitmode = tk.StringVar()
                fitmodeoptions = ['lorentz','gauss','adv_multi-lrnz'] 
                fitmode.set(fitmodeoptions[0])
                fitmodeopt = tk.OptionMenu(container, fitmode, *fitmodeoptions)
                fitmodeopt["menu"].config(fg="RED")
                fitmodeopt.config(bg="grey25", fg="white",font=('Arial',10))
                fitmodeopt.place(x=50,y=230,width=65)

                # ROW 8 #############################################
                global fourierentry
                fourierfitdata = tk.Button(container,text='FFT smooth', bg="grey90", fg="darkred",font=('Arial',10),width= 6,borderwidth=1, command=lambda:scrollframe.fouriersmooth(selectedkey)).place(x=120,y=260)
                tk.Label(container,bg="black", fg="white",font=('Arial',10),text='Sm cutoff:').place(x=10,y=260)
                fourierentry = tk.Entry(container,bg='black',fg='white',width=3,borderwidth=0,font=('Arial',10))
                fourierentry.insert(0, '6')
                fourierentry.place(x=80,y=260)

                smoothstar = tk.Button(container,text='advanced sm', bg="grey90", fg="darkred",font=('Arial',10),width= 8,borderwidth=1, command=lambda:scrollframe.fouriersmooth(selectedkey)).place(x=200,y=260)
                
                

                


                # ROW 9 #############################################










# FUNCTIONS SCROLLFRAME FUNCTIONS SCROLLFRAME FUNCTIONS SCROLLFRAME #############################################
            def lambda_update(eff):
                print('bg rearranged')
                selectedkey = datalistbox
                scrollframe.update_json(selectedkey)
                FTIR_viewerstartup.plot()
                #statustask.configure(text='Plotting',fg='black')
                #statusbox.insert(0, 'Plotting...')


            def update_json(key):
                #print('update functin, einlesen aller widget values')
                jsondict[key]['show']= bool(showbox.get())
                jsondict[key]['label']= str(datalabelentry.get())
                jsondict[key]['subplot']= str(subplotnum.get())
                jsondict[key]['bg']= bool(bgbox.get())
                jsondict[key]['bgkey']= str(bgkeyentry.get())
                jsondict[key]['bgscale']= float(scales.get())
                jsondict[key]['color']= str(col.get())
                jsondict[key]['linestyle']= str(line.get())


            def getxy(data):
                x = list(jsondict[data]['xdata'])
                y = list(jsondict[data]['ydata'])
                bgdatakey = jsondict[data]['bgkey']
                if jsondict[data]['bg'] == True:
                    xbg= list(jsondict[bgdatakey]['xdata'])
                    ybg= list(jsondict[bgdatakey]['ydata'])
                    scale = float(jsondict[data]['bgscale'])
                    x,y = pyFTIR.manipulate_data.subtract_bg(x,y,xbg,ybg,scale)
                return x,y
            
            def dont_double_date(name,dataset): #nutzfunltiomn um platz zu sparen, name muss häufiger gecheckt werden
                counter=0
                while name in jsondict:
                        counter = counter+1
                        name = str(name + str(counter))

                jsondict[name] = dataset
                listbox.insert(tk.END, name)

            
            def change_key(key):
                print('changed '+str(jsondict[str(key)]['label'])+' to '+str(datalabelentry.get()))
                new_key = str(datalabelentry.get())
                jsondict[new_key] = jsondict[key]
                del jsondict[key]
                listbox.delete(tk.ANCHOR)
                listbox.insert(tk.ANCHOR , str(new_key))
                #scrollframe.update_json(key)

            def export_data(key):
                a = filedialog.asksaveasfilename(initialdir = dirpath,title = "Save file")#,filetypes = (("textfiles", "*.txt*"))) 
                x,y = scrollframe.getxy(key) 
                x,y = [format(item,'.9f') for item in x],[format(item,'.9f') for item in y]
                df = pd.DataFrame({'wavenumber': x,'OD':y})
                df = df.set_index('wavenumber')

                df.to_csv(str(a), sep ='\t')
                print(str('data exported to: '+str(a)))

            
            def findpeaks(key,jsondict):
                num = int(jsondict[key]['subplot'])
                xpeaks,ypeaks = pyFTIR.extract_data.peaker(key,jsondict,promentry)
                print(ypeaks)
                for c in range(len(xpeaks)):
                    ax[num].text(xpeaks[c],ypeaks[c],s=str(round(xpeaks[c],4))+'\n',size=10)
                ax[num].scatter(xpeaks,ypeaks,marker='x',color='r')
                canvas.draw()
            
            def invertdata(key):
                x,y = scrollframe.getxy(key)
                nx,ny = x,[item*(-1) for item in y]
                jsondict[key]['xdata']= nx
                jsondict[key]['ydata']= ny
                buttoncommands.plotplot()
                print('inverted: '+str(key)+'data *(-1)')

            def sec_dev(key):
                print('function to calculate the second derivative of the given spectrum')
                x,y = scrollframe.getxy(key)
                y = np.array(y)
                dy = np.gradient(y)
                ddy = list(np.gradient(dy))
                ddydump = dataconstruct.j_son(x,ddy,False,'',0,True,'green',0.9,'solid',str('Second dev of:'+str(key)),1)

                datadump = str(key+'_sec dev')
                counter=0
                while datadump in jsondict:
                    counter = counter+1
                    datadump = str(datadump + str(counter))
                jsondict[datadump] = ddydump
                listbox.insert(tk.END, datadump)

            def cut(key):
                print('function to cut out a specific region of the spectrum')
                x,y = scrollframe.getxy(key)
                wavecut = wavecutentry.get()
                xcut = list(wavecut.split(','))
                if wavecut == '':
                    statusbox.insert(0, 'Press 2 times on the plot')
                    polypoints = plt.ginput(n=2,timeout=30, show_clicks=True, mouse_add = plt.MouseButton.LEFT,mouse_pop= plt.MouseButton.RIGHT,mouse_stop = plt.MouseButton.MIDDLE)
                    xcut = [polypoints[0][0],polypoints[1][0]]
                
                xcut = [float(item) for item in xcut]
                xcut.sort()
                statusbox.insert(0, str(xcut))

                xredcut,yredcut = pyFTIR.manipulate_data.data_reduce(x,y,xcut[0],xcut[1])
                cutteddata =  dataconstruct.j_son(xredcut,yredcut,False,'',0,True,'magenta',0.9,'solid',str('Data cut out'),1)
                datadump = str(key+'_cut')
                counter=0
                while datadump in jsondict:
                        counter = counter+1
                        datadump = str(datadump + str(counter))

                jsondict[datadump] = cutteddata
                listbox.insert(tk.END, datadump)

            def ignore(key):
                print('not sure for now')

            def show_trapz(key):
                x,y = scrollframe.getxy(key)
                wavecut = wavecutentry.get()
                xint = list(wavecut.split(','))
                if wavecut == '':
                    print('tap 2 times on the Plot to define the intgration area !!!')
                    polypoints = plt.ginput(n=2,timeout=30, show_clicks=True, mouse_add = plt.MouseButton.LEFT,mouse_pop= plt.MouseButton.RIGHT,mouse_stop = plt.MouseButton.MIDDLE)
                    xint = [polypoints[0][0],polypoints[1][0]]

                xint = [float(item) for item in xint]
                xint.sort()
                statusbox.insert(0, str(xint))

                xredint,yredint = pyFTIR.manipulate_data.data_reduce(x,y,xint[0],xint[1])
                trapzvalue = np.abs(np.trapz(yredint,x=xredint))
                print('Integral value: '+str(trapzvalue))
                trapzval_formatted = "%.3g" %trapzvalue

                xint_formatted = [ round(item,2) for item in xint ]
                datadump = str(key+'_trapz :'+str(trapzval_formatted)+' over '+str(xint_formatted))
                integrationarea = dataconstruct.j_son(xredint,yredint,False,'',0,True,'skyblue',0.9,'solid',str(datadump),1)
                counter=0
                while datadump in jsondict:
                        counter = counter+1
                        datadump = str(datadump + str(counter))

                jsondict[datadump] = integrationarea
                listbox.insert(tk.END, datadump)



            def polyfit_data(key):
                    print('tap 4 times on the Plot to define the fitting areas !!!')
                    polydeg = int(polyentry.get())
                    print('manuelle eingabe des grades')
                    waveval = waveentry.get()
                    xpoly = list(waveval.split(','))
                    if waveval =='':
                        statusbox.insert(0, 'Press 4 times on the plot')
                        polypoints = plt.ginput(n=5,timeout=30, show_clicks=True, mouse_add = plt.MouseButton.LEFT,mouse_pop= plt.MouseButton.RIGHT,mouse_stop = plt.MouseButton.MIDDLE)
                        xpoly = [polypoints[0][0],polypoints[1][0],polypoints[2][0],polypoints[3][0]]

                    xpoly = [float(item) for item in xpoly]
                    xpoly.sort()
                    statusbox.insert(0, str(xpoly))
                    waveentry.insert(0,str(xpoly))
                    print(xpoly)


                    x = list(jsondict[key]['xdata'])
                    y = list(jsondict[key]['ydata'])
                    bgdatakey = jsondict[key]['bgkey']
                    if jsondict[key]['bg'] == True:
                        xbg= list(jsondict[bgdatakey]['xdata'])
                        ybg= list(jsondict[bgdatakey]['ydata'])
                        scale = float(jsondict[key]['bgscale'])
                        x,y = pyFTIR.manipulate_data.subtract_bg(x,y,xbg,ybg,scale)

                    xred,yred = pyFTIR.manipulate_data.data_reduce(x,y,xpoly[0],xpoly[1])
                    xred2, yred2 = pyFTIR.manipulate_data.data_reduce(x,y,xpoly[2],xpoly[3])

                    for c in range(len(xred2)):
                        xred.append(xred2[c])
                        yred.append(yred2[c])
                    
                    polypar = np.polyfit(xred,yred,polydeg)
                    polyfunk = np.poly1d(polypar)
                    statusbox.insert(0, str(polyfunk))
                    xdatapoly,ydatad = pyFTIR.manipulate_data.data_reduce(x,y,xpoly[0],xpoly[3])
                    ydatapoly = []
                    for i in range(len(xdatapoly)):
                        yval = polyfunk(xdatapoly[i])
                        ydatapoly.append(yval)

                    polyset =  dataconstruct.j_son(xdatapoly,list(polyfunk(xdatapoly)),False,'',0,True,'grey',0.9,'dashed',str('Polyfit'),0)
                    datapol = str(key+'_polyfit')
                    scrollframe.dont_double_date(name=datapol,dataset=polyset)
                    
                    doubledset =  dataconstruct.j_son(xdatapoly,ydatad,True,str(str(key)+'_polyfit'),1,True,'darkorange',0.9,'solid',str('Data for substraktion'),1)
                    datadub = str(key+'_data')
                    scrollframe.dont_double_date(name=datadub,dataset=doubledset)

                
            def autofit_bg():
                print('fit bg')

            def fouriersmooth(key):
                print('fourier smoothing fuction satrt')
                x,y= scrollframe.getxy(key)

                smoothfak = int(fourierentry.get())
                y_smoothed = pyFTIR_FITS.advanced.fouriersmooth(y,smoothfak)
                newkey =str(str(key)+'_FFT_'+str(smoothfak))
                fourierset =  dataconstruct.j_son(x[:int(len(y_smoothed))],y_smoothed,False,'',0,True,'magenta',0.9,'solid',newkey,1)
                jsondict[newkey] = fourierset
                listbox.insert(tk.END, newkey)

            def fit_bands(key):
                print('bandfitting func running..')
                fitfunc = str(fitmode.get())
                print(fitfunc)
                x,y= scrollframe.getxy(key)

                tpoints = plt.ginput(n=3,timeout=30, show_clicks=True, mouse_add = plt.MouseButton.LEFT,mouse_pop= plt.MouseButton.RIGHT,mouse_stop = plt.MouseButton.MIDDLE)
                print(tpoints)
                xps = [tpoints[0][0],tpoints[1][0],tpoints[2][0]]
                yps = [tpoints[0][1],tpoints[1][1],tpoints[2][1]]
                xh = max(xps)
                xl = min(xps)
                width = (xh-xl)/2.4
                xps.remove(xl)
                xps.remove(xh)
                xpeak = xps[0]
                amp = max(yps)-min(yps)
                height = min(yps)
                x,y = pyFTIR.manipulate_data.data_reduce(x,y,xl,xh)
                fitx,fity,parstring,par,fittype,fiterror,fwhm = pyFTIR_FITS.bandfits.fitband(x,y,amp,xpeak,width,height,fitfunc)
                print('#### Finished fit type: '+ str(fittype))
                print(parstring)
                print('estimated fit error: '+str(fiterror))

                containername = str('FWHM: '+str(fwhm))
                fitdataset = dataconstruct.j_son(fitx,fity,False,'',1,True,'red',0.9,'dashed',containername,0)
                fitname = str(str(fittype)+'_fit_')
                scrollframe.dont_double_date(name=fitname,dataset=fitdataset)

                yfwhm = par[0]/2 + par[3]
                xfwhm1 = par[1] - fwhm/2
                xfwhm2 = par[1] + fwhm/2
                fwhmset =  dataconstruct.j_son([xfwhm1,xfwhm2],[yfwhm,yfwhm],False,'',1,True,'grey',0.9,'dotted',str('FWHM:'+str(round(fwhm,3))),1)   
                fitname = str('FWHM: '+str(fwhm))
                scrollframe.dont_double_date(name=fitname,dataset=fwhmset)
            
            def fitbands(key):
                fitfunc = str(fitmode.get())
                print(fitfunc)
                x,y= scrollframe.getxy(key)
                
                if 'lorentz' in fitfunc or 'gaussian' in fitfunc:
                    print('normal bandfitting func running...')
                    fitx,fity,parstring,par,fittype,fiterror,fwhm = pyFTIR_FITS.bandfits.fitband_allg(x,y,fitfunc)

                    print('#### Finished fit type: '+ str(fittype))
                    print(parstring)
                    print('estimated fit error: '+str(fiterror))
            
                    containername = str('FWHM: '+str(fwhm))
                    fitdataset = dataconstruct.j_son(fitx,fity,False,'',1,True,'red',0.9,'dashed',containername,0)
                    fitname = str(str(fittype)+'_fit_')
                    scrollframe.dont_double_date(name=fitname,dataset=fitdataset)

                    if fwhm != 0:
                        yfwhm = par[0]/2 + par[3]
                        xfwhm1 = par[1] - fwhm/2
                        xfwhm2 = par[1] + fwhm/2
                        fwhmset =  dataconstruct.j_son([xfwhm1,xfwhm2],[yfwhm,yfwhm],False,'',1,True,'grey',0.9,'dotted',str('FWHM:'+str(round(fwhm,3))),1)   
                        fitname = str('FWHM: '+str(fwhm))
                        scrollframe.dont_double_date(name=fitname,dataset=fwhmset)

                if 'adv' in fitfunc:
                    print('lovely, you found the beautiful advanced part...')
                    fit_dict = pyFTIR_FITS.advanced_fits.init(x,y,fitfunc)
                    #print(fit_dict)
                    exisisting_colors = ['black','red','lightcoral','blue','skyblue','green','cyan','magenta','darkorange','grey','chocolate'] 

                    for fitbandname, xylist in fit_dict.items():
                        selected_color = random.choice(exisisting_colors)
                        containername = str('still empty beta')
                        fitdataset = dataconstruct.j_son(xylist[0],xylist[1],False,'',1,True,str(selected_color),0.9,'dashed',containername,0)
                        fitname = str(fitbandname)
                        scrollframe.dont_double_date(name=fitname,dataset=fitdataset)

       




        scrollframe.start_switchableframe()




        toolframe.place(x=0,y=0,width=400,height=700)



































    def plotframesetupIR(parent): 
        global canvas,ax
        mframe = tk.Frame(parent)
        mframe.config(background='grey20')

        figure, ax = plt.subplots(2,1,gridspec_kw={'height_ratios': [2, 1]},figsize=(12,8))
        canvas = FigureCanvasTkAgg(figure, master= mframe)#self.mframe)
        canvas.get_tk_widget().place(x=0,y=35,width=900,height=700)
        toolbar = NavigationToolbar2Tk(canvas,mframe)
        toolbar.pack(side=tk.TOP, fill=tk.BOTH) 

        ax[0].set_xlabel(init_dict['xlabel'])
        ax[0].set_ylabel(init_dict['ylabel'])
        ax[1].set_xlabel(init_dict['xlabel'])
        ax[1].set_ylabel(init_dict['ylabel'])
        mframe.place(x=420,y=0,width=900,height=700)


    
    def plot():
        ax[0].cla()
        ax[1].cla()
        canvas.draw()

        #print(jsondict)
        for key in jsondict:
            label = str(key)
            x = list(jsondict[key]['xdata'])
            y = list(jsondict[key]['ydata'])
            subnum = int(jsondict[key]['subplot'])
            farb = str(jsondict[key]['color'])
            bgdatakey = jsondict[key]['bgkey']
            linest = jsondict[key]['linestyle']
            #print(linest)
 
            if jsondict[key]['bg'] == True:
                xbg= list(jsondict[bgdatakey]['xdata'])
                ybg= list(jsondict[bgdatakey]['ydata'])
                scale = float(jsondict[key]['bgscale'])
                x,y = pyFTIR.manipulate_data.subtract_bg(x,y,xbg,ybg,scale)
                #print('bg substracted')

            multi = float(ymulti.get())
            y = [(item*multi) for item in y]

            if jsondict[key]['show'] == True:
                if '_trapz' in key:
                     ax[subnum].fill_between(x,y,y2=0,color=farb,linestyle=str(linest),label=label,alpha=.3)
                else:
                    ax[subnum].plot(x,y,color=farb,linestyle=str(linest),label=label)
                

        #self.ax.legend()
        
        ax[0].set_xlabel(str(xlabel.get()))
        ax[0].set_ylabel(str(ylabel.get()))
        ax[1].set_xlabel(str(xlabel.get()))
        ax[1].set_ylabel(str(ylabel.get()))
        ax[0].grid(gridbox.get())
        ax[0].set_xlim(float(xlow.get()),float(xhigh.get()))
        ax[0].set_ylim(float(ylow.get()),float(yhigh.get()))
        ax[1].set_xlim(float(xlow.get()),float(xhigh.get()))
        if labelbox.get() == True:
            print('legend True')
            ax[0].legend(loc='best', prop={'size': 10})
            

        canvas.draw()
    


    def clear():
        ax[0].cla()
        ax[1].cla()
        canvas.draw()
    
        


