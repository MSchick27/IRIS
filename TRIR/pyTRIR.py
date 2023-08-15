import numpy as np
from scipy import optimize as opt
from scipy import signal
import os
from tkinter import filedialog

import time

import matplotlib.pyplot as plt
import asyncio

import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap

import os
from tkinter import filedialog

dirpath = os.path.dirname(os.path.dirname(__file__))

class PYTRIR():
    def j_son(data_array_tolist,bg_array_tolist,delayarray,wnarray,stdarray,s2s_stdarray,scannumber,scanslice,delaynumber,delayslice):
        dataset = {'data': data_array_tolist,
                    'bgdata': bg_array_tolist,
                    'delays': delayarray,
                    'wn' : wnarray,
                    'std_deviation':stdarray,
                    'noise': s2s_stdarray,
                    'scannumber': scannumber,
                    'scanslice': scanslice,
                    'delaynumber': delaynumber,
                    'delayslice': delayslice,
                            }
        return dataset
    
    def exportdata(jsondataset):
        databgsub = modify_arrays.subtract_bg(jsondataset)
        print(np.shape(databgsub))
        myFile = filedialog.asksaveasfile(mode='w',initialfile = 'Untitled.txt', defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
        for i,delay in enumerate(jsondataset['delays']):
            for j,wn in enumerate(jsondataset['wn']):
                arrayvalue = databgsub[j,i]
                myFile.write(str(delay)+'\t'+str(wn)+'\t'+str(arrayvalue)+'\n')

        myFile.close()




    def importinitfunction(scanslice,delayslice,detektor_size):
        delays_times,wavnumbers,alphamatrix = PYTRIR.get_scans(scanslice,delayslice,detektor_size)
        weighteddata = PYTRIR.get_s2s_DIFF(alphamatrix)
        weighteddatatr = np.transpose(weighteddata)
        print('Weigthed data format:'+ str(np.shape(weighteddatatr)))
        
        bgdata= np.zeros(np.shape(weighteddatatr))
        stddev_array = np.transpose(np.average(alphamatrix[:,:,:,1],axis=1))
        s2s_stddata= PYTRIR.getnoise(alphamatrix)
        scannum = scannumber
        delaynum = len(delayfilearray)

        datasetjson = PYTRIR.j_son(weighteddatatr,bgdata,delays_times,wavnumbers,stddev_array,s2s_stddata,scannum,scanslice,delaynum,delayslice)
        print('##########jsonified !')
        #print(datasetjson)
        return datasetjson








    def get_scans(scanslice,delayslice,detektor_size):
        filenames = filedialog.askopenfilenames(initialdir = str(dirpath), 
                                          title = "Open Files") 
        pathtup = filenames
        datadir = os.path.dirname(os.path.dirname(pathtup[0]))
        
        search_files =os.listdir(datadir)


        def cut1darray(listofslices,arr):
            if listofslices == ':':
                new_arr = arr
            else:
                new_arr_list = []
                listofslices = listofslices.split(',')
                for slice in listofslices:
                    slice = slice.split(':')
                    arrpart = arr[int(slice[0]):int(slice[1])]
                    for value in arrpart:
                        new_arr_list.append(value)
                
                new_arr = np.array(new_arr_list)
                #print(new_arr)

            return new_arr


        
        for file in search_files:
            if 'delay_file' in str(file):
                delayfile= str(file)            #define variabel for delayfilepath
                print('Found delayfile:  ' + str(delayfile))
                delay = np.load(str(datadir+'/'+delayfile))
                delay = 10**(-3) * (delay[:,0])             #delays femtosekunden zu picosekunden
                delay = cut1darray(delayslice,delay)        #slice gewollte delays 
                print('...Delayfile loaded successfully')   #delay = 1d array mit den Zeitpunkten in picosekunden

            if 'probe_wn_axis' in str(file):
                wnfile = str(file)              #define variabel for wavenumberfilepath
                print('Found Probeaxefile:' + str(wnfile))
                wn = np.load(str(datadir+'/'+wnfile))       #wn = 1d array mit wellenzahlen in reihenfolge der pixel
                print('...Probeaxisfile loaded successfully')

            
        try:
            #scandir = os.chdir(str(str(datadir)+'/scans'))
            scdir =str(str(datadir)+'/scans')
            delay_files = os.listdir(scdir)
            delay_files = sorted(delay_files)
            #print(delay_files)
            delay_files = np.array(delay_files)
            global delayfilearray
            delayfilearray = cut1darray(delayslice,delay_files)
        except:
            print('no directory: /scans opr delayfiles missing')

        
        global scannumber
        if scanslice== ':':
            scannumber =len(os.listdir(str(str(scdir)+'/'+str(delayfilearray[0]))))//5 -1
        else:
            scannumberall = len(os.listdir(str(str(scdir)+'/'+str(delayfilearray[0]))))//5 -1
            fillinarray = np.zeros(scannumberall)
            fillarray = cut1darray(scanslice,fillinarray)
            scannumber = len(fillarray)
            print('Number of scans taken into account: '+str(scannumber)+'/'+str(scannumberall))

        

        alpha = np.zeros((len(delayfilearray),scannumber,len(wn),2))
        print(np.shape(alpha))

        for i in range(len(delayfilearray)):
            delayf = delayfilearray[i]
            objectsperdelaylist = os.listdir(str(str(scdir)+'/'+str(delayf)))
            objectsperdelaylist.sort()
            
            s2ssignal_scanlist = []
            s2s_std_scanlist = []
            counts_scanlist = []
            weights_scanlist = []

            for object in objectsperdelaylist:
                if 's2s_signal' in object:
                    s2ssignal_scanlist.append(object)
                if 's2s_std' in object:
                    s2s_std_scanlist.append(object)
                if 'counts' in object:
                    counts_scanlist.append(object)
                if 'weights' in object:
                    weights_scanlist.append(object)

            s2ssignal_scanarray = cut1darray(scanslice,np.array(s2ssignal_scanlist))
            s2s_std_scanarray = cut1darray(scanslice,np.array(s2s_std_scanlist))
            counts_scanarray = cut1darray(scanslice,np.array(counts_scanlist))
            weights_scanarray = cut1darray(scanslice,np.array(weights_scanlist))

            #print(s2ssignal_scanarray)
            #print(s2s_std_scanarray)
            rho = np.zeros((scannumber,len(wn),2))

            timestart = time.time()

            for j in range(scannumber):
                scanf = str(str(scdir)+'/'+str(delayf)+'/'+str(s2ssignal_scanarray[j]))
                s2sf = str(str(scdir)+'/'+str(delayf)+'/'+str(s2s_std_scanarray[j]))
                scandata = np.load(scanf)
                scandata = np.reshape(scandata,(detektor_size,1))
                #print(np.shape(scandata))
                s2sdata = np.load(s2sf)
                s2sdata = np.reshape(s2sdata,(detektor_size,1))
                #print(np.shape(s2sdata))
                s2sscandata = np.hstack((scandata,s2sdata))
                rho[j,:,:]= s2sscandata

            
                timeend = time.time()
                timeblock = timeend-timestart
                timetillend = int(10-int(j/scannumber))*timeblock/(int(j/scannumber+1))
                hashs = '#'
                points = '-'
                print((int(j/scannumber))*hashs + int(scannumber-int(j/scannumber))*points+':'+ str('{:5.3f}s'.format(timetillend)), end='\r')
                
        
            alpha[i,:,:,:] = rho
            timeending = time.time()
            runtime = timeending-timestart
            print('loaded Delay: '+str(i) + str('  ')+str('{:5.3f}s'.format(runtime)))
        

        print('(Delays, Scans, Pixel, P-NP:s2s_std)')
        print(np.shape(alpha))
    
        return delay,wn, alpha



    def get_s2s_DIFF(data4d):
        print('weighting data bei s2s_std')
        signaldata = data4d[:,:,:,0]
        weights = data4d[:,:,:,1]
        weights = (1/weights)**2
        print('## weights: '+str(np.shape(weights)))
        addweights = signaldata*weights
        weightedODsum = np.sum(addweights,axis=1)
        print('## ODs: '+str(np.shape(weightedODsum)))
        weightsum = np.sum(weights,axis=1)
        #print(np.shape(weightsum))

        #function to see the weights as a function of time and wn to see if meas good
        DIFF = weightedODsum/weightsum 
        return DIFF




    def getnoise(data4d):
        weightsdata = data4d[:,:,:,1]
        print(np.shape(weightsdata))

        return weightsdata





















class weighted_import:
    def init_weightedimport(scanslice,delayslice,detektor_size):
        print('import data averaged by weights')
        delays_times,wavnumbers, alpha = weighted_import.getscansbyweights(scanslice,delayslice,detektor_size)  #alpha shape (Delays, Scans, Pixel, P-NP-wP-wNP) (28, 101, 1024, 4)
        print('all delays imported successfully')

        weightedPUMP = np.average(alpha[:,:,:,0],axis=1,weights= alpha[:,:,:,2])
        weightedNONEPUMP = np.average(alpha[:,:,:,1],axis=1,weights= alpha[:,:,:,3])
 
        DIFF = np.log10(weightedPUMP/weightedNONEPUMP)
        DIFF = np.transpose(DIFF)
        print('Weigthed data format:'+ str(np.shape(DIFF)))
        
        bgdata= np.zeros(np.shape(DIFF))
        stddev_array = weighted_import.weighted_stddeviation(alpha)
        stddev_array= np.transpose(stddev_array)
        noisedata =weighted_import.weightednoise(alpha)
        scannum = scannumber
        delaynum = len(delayfilearray)

        datasetjson = PYTRIR.j_son(DIFF,bgdata,delays_times,wavnumbers,stddev_array,noisedata,scannum,scanslice,delaynum,delayslice)
        print('##########jsonified !')
        return datasetjson





    def weightednoise(data4d):
        weightsdata = data4d[:,:,:,2:3]
        weights_mean = np.sum(weightsdata,axis=3)/2

        return weights_mean
    
    def weighted_stddeviation(alpha):
        print('calculating the weighted std')
        weighted_mean_PUMP = np.average(alpha[:,:,:,0],axis=1,weights=alpha[:,:,:,2])
        weighted_mean_PUMP_ = np.expand_dims(weighted_mean_PUMP,axis=1)
        weighted_mean_PUMP_3d = np.broadcast_to(weighted_mean_PUMP_,np.shape(alpha[:,:,:,0]))

        weighted_mean_NPUMP = np.average(alpha[:,:,:,1],axis=1,weights=alpha[:,:,:,3])
        weighted_mean_NPUMP_ = np.expand_dims(weighted_mean_NPUMP,axis=1)
        weighted_mean_NPUMP_3d = np.broadcast_to(weighted_mean_NPUMP_,np.shape(alpha[:,:,:,0]))

        weighted_variance_PUMP = np.average(np.square(np.subtract(alpha[:,:,:,0],weighted_mean_PUMP_3d)), axis= 1,weights=alpha[:,:,:,2])
        weighted_variance_NPUMP = np.average(np.square(np.subtract(alpha[:,:,:,1],weighted_mean_NPUMP_3d)), axis=1,weights=alpha[:,:,:,3])

        weighted_std_PUMP = np.sqrt(weighted_variance_PUMP)
        weighted_std_NPUMP = np.sqrt(weighted_variance_NPUMP)

        def gaussche_Fehlerfortpflanzung(weighted_mean_PUMP,weighted_mean_NPUMP,weighted_std_PUMP,weighted_std_NPUMP):
            #ableitung von log10(x1/x2) -> 1/x1*ln(10)
            def derivative_loga(a,x):
                return 1/(x*np.log(10))
            
            return np.sqrt( np.square(derivative_loga(10,weighted_mean_PUMP)) * np.square(weighted_std_PUMP) + np.square(derivative_loga(10,weighted_mean_NPUMP)) * np.square(weighted_std_NPUMP) )
        
        gauss_and_weighted_std = gaussche_Fehlerfortpflanzung(weighted_mean_PUMP,weighted_mean_NPUMP,weighted_std_PUMP,weighted_std_NPUMP)
        print(np.shape(gauss_and_weighted_std))

        return gauss_and_weighted_std

 





    def getscansbyweights(scanslice,delayslice,detektor_size):
        filenames = filedialog.askopenfilenames(initialdir = str(dirpath), 
                                          title = "Open Files") 
        pathtup = filenames
        datadir = os.path.dirname(os.path.dirname(pathtup[0]))
        
        search_files =os.listdir(datadir)

        def cut1darray(listofslices,arr):
            if listofslices == ':':
                new_arr = arr
            else:
                new_arr_list = []
                listofslices = listofslices.split(',')
                for slice in listofslices:
                    slice = slice.split(':')
                    arrpart = arr[int(slice[0]):int(slice[1])]
                    for value in arrpart:
                        new_arr_list.append(value)
                
                new_arr = np.array(new_arr_list)
                #print(new_arr)

            return new_arr

        for file in search_files:
            if 'delay_file' in str(file):
                delayfile= str(file)            #define variabel for delayfilepath
                print('Found delayfile:  ' + str(delayfile))
                delay = np.load(str(datadir+'/'+delayfile))
                delay = 10**(-3) * (delay[:,0])             #delays femtosekunden zu picosekunden
                delay = cut1darray(delayslice,delay)        #slice gewollte delays 
                print('...Delayfile loaded successfully')   #delay = 1d array mit den Zeitpunkten in picosekunden

            if 'probe_wn_axis' in str(file):
                wnfile = str(file)              #define variabel for wavenumberfilepath
                print('Found Probeaxefile:' + str(wnfile))
                wn = np.load(str(datadir+'/'+wnfile))       #wn = 1d array mit wellenzahlen in reihenfolge der pixel
                print('...Probeaxisfile loaded successfully')

        try:
            #scandir = os.chdir(str(str(datadir)+'/scans'))
            scdir =str(str(datadir)+'/scans')
            delay_files = os.listdir(scdir)
            delay_files = sorted(delay_files)
            #print(delay_files)
            delay_files = np.array(delay_files)
            global delayfilearray
            delayfilearray = cut1darray(delayslice,delay_files)
        except:
            print('no directory: /scans or delayfiles missing')

        
        global scannumber
        if scanslice== ':':
            scannumber =len(os.listdir(str(str(scdir)+'/'+str(delayfilearray[0]))))//5 -1
        else:
            scannumberall = len(os.listdir(str(str(scdir)+'/'+str(delayfilearray[0]))))//5 -1
            fillinarray = np.zeros(scannumberall)
            fillarray = cut1darray(scanslice,fillinarray)
            scannumber = len(fillarray)
            print('Number of scans taken into account: '+str(scannumber)+'/'+str(scannumberall))

        

        alpha = np.zeros((len(delayfilearray),scannumber,len(wn),4))
        print(np.shape(alpha))

        for i in range(len(delayfilearray)):
            delayf = delayfilearray[i]
            objectsperdelaylist = os.listdir(str(str(scdir)+'/'+str(delayf)))
            objectsperdelaylist.sort()
            
            s2ssignal_scanlist = []
            s2s_std_scanlist = []
            counts_scanlist = []
            dataPNP_scanlist = []
            weights_scanlist = []

            for object in objectsperdelaylist:
                if 's2s_signal' in object:
                    s2ssignal_scanlist.append(object)
                elif 's2s_std' in object:
                    s2s_std_scanlist.append(object)
                elif 'counts' in object:
                    counts_scanlist.append(object)
                elif 'weights' in object:
                    weights_scanlist.append(object)
                else:
                    dataPNP_scanlist.append(object)

            s2ssignal_scanarray = cut1darray(scanslice,np.array(s2ssignal_scanlist))
            s2s_std_scanarray = cut1darray(scanslice,np.array(s2s_std_scanlist))
            counts_scanarray = cut1darray(scanslice,np.array(counts_scanlist))
            dataPNP_scanarray = cut1darray(scanslice,np.array(dataPNP_scanlist))
            weights_scanarray = cut1darray(scanslice,np.array(weights_scanlist))

            #print(dataPNP_scanarray)
            #print(s2s_std_scanarray)
            rho = np.zeros((scannumber,len(wn),4))

            timestart = time.time()

            for j in range(scannumber):
                dataPNP = str(str(scdir)+'/'+str(delayf)+'/'+str(dataPNP_scanarray[j]))
                weightsPNP = str(str(scdir)+'/'+str(delayf)+'/'+str(weights_scanarray[j]))
                scandata = np.load(dataPNP)
                scandata = np.reshape(scandata,(detektor_size,2))
                #print(np.shape(scandata))
                weightsdata = np.load(weightsPNP)
                weightsdata = np.reshape(weightsdata,(detektor_size,2))
                #print(np.shape(weightsdata))
                s2sscandata = np.hstack((scandata,weightsdata))
                rho[j,:,:]= s2sscandata

                timeend = time.time()
                timeblock = timeend-timestart
                timetillend = int(10-int(j/scannumber))*timeblock/(int(j/scannumber+1))
                hashs = '#'
                points = '-'
                print((int(j/scannumber))*hashs + int(scannumber-int(j/scannumber))*points+':'+ str('{:5.3f}s'.format(timetillend)), end='\r')
                
        
            alpha[i,:,:,:] = rho
            timeending = time.time()
            runtime = timeending-timestart
            print('loaded Delay: '+str(i) + str('  ')+str('{:5.3f}s'.format(runtime)))
        

        print('(Delays, Scans, Pixel, P-NP-wP-wNP)')
        print(np.shape(alpha))
    
        return delay,wn, alpha























class modify_arrays():
    def subtract_bg(jsonfile):
        diffdata = np.subtract(jsonfile['data'],jsonfile['bgdata'])
        #print(np.shape(diffdata))
        return diffdata
    
    def subtract_bg_rms(jsonfile):
        diffdata = np.abs(np.subtract(jsonfile['data'],jsonfile['bgdata'])) 
        return diffdata


    def sub_delay1(weighteddata):
        delay1 = weighteddata[:,0]
        subdelay1array = np.zeros(np.shape(weighteddata))
        for i in range(len(weighteddata[0,:])):
            subdelay1array[:,i] = delay1
    
        #subDIFF = np.transpose(subDIFF)
        newweighteddata = np.subtract(weighteddata,subdelay1array)
        print('successfully subtracted first delay as background')
        return newweighteddata



    def noiseallscans(datajson):
        noisearray = datajson['noise']
        shape = np.shape(noisearray)
        noisescan = np.zeros((shape[0]*shape[1],shape[2]))
        #print('zeroes: '+ str(np.shape(noisescan)))
        counter = 0
        for i in range(shape[1]):
            for j in range(shape[0]):
                noisescan[counter] = noisearray[j,i]
                counter = counter + 1

        #print('noisewrap: '+ str(np.shape(noisescan)))
        return noisescan
    



    def getlogaxis(datajson):
        delaays = datajson['delays']
        for i,timestamp in enumerate(delaays):
            if timestamp > 0:
                break
        xlow = delaays[i]
        xhigh = delaays[-1]
        return xlow,xhigh























class colormapsfor_TRIR():
    def findmaxval(dataarray,valfactor):
        absarray = np.abs(dataarray)
        maxval = float(np.nanmax(absarray)) * float(valfactor)
        minval = -maxval

        if type(maxval) != float:
            print('colormap ERROR: nan encountered as maxvalue')
            maxval=0.1
            minval=-0.1

        print('Maxvalue for colormap:' +str(maxval))
        #print(absarray)
        return maxval,minval
    

    def create_custom_colormap(start_color, end_color, min_value, max_value,levels):
        # Convert hex colors to RGB values
        start_rgb = mcolors.hex2color(start_color)
        end_rgb = mcolors.hex2color(end_color)
    
        # Normalize the data range based on min and max values
        norm = mcolors.Normalize(vmin=min_value, vmax=max_value)
    
        # Create a linear gradient between the start and end colors
        colormap = mcolors.LinearSegmentedColormap.from_list(
            'custom_colormap',
            [start_rgb, (1, 1, 1), end_rgb],
            N=256,  # Number of colors in the colormap
        )
    
        return colormap, norm
        

        






