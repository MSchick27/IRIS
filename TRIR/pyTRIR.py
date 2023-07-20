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
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap

import os
from tkinter import filedialog

dirpath = os.path.dirname(os.path.dirname(__file__))

class PYTRIR():
    def j_son(data_array_tolist,bg_array_tolist,delayarray,wnarray,s2s_stdarray,scannumber,scanslice,delaynumber,delayslice):
        dataset = {'data': data_array_tolist,
                    'bgdata': bg_array_tolist,
                    'delays': delayarray,
                    'wn' : wnarray,
                    'noise': s2s_stdarray,
                    'scannumber': scannumber,
                    'scanslice': scanslice,
                    'delaynumber': delaynumber,
                    'delayslice': delayslice,
                            }
        return dataset
    




    def importinitfunction(scanslice,delayslice):
        delays_times,wavnumbers,alphamatrix = PYTRIR.get_scans(scanslice,delayslice)
        weighteddata = PYTRIR.get_s2s_DIFF(alphamatrix)
        weighteddatatr = np.transpose(weighteddata)
        print('Weigthed data format:'+ str(np.shape(weighteddatatr)))
        
        bgdata= np.zeros(np.shape(weighteddatatr))
        
        s2s_stddata= PYTRIR.getnoise(alphamatrix)

        scannum = scannumber
        delaynum = len(delayfilearray)

        datasetjson = PYTRIR.j_son(weighteddatatr,bgdata,delays_times,wavnumbers,s2s_stddata,scannum,scanslice,delaynum,delayslice)
        print('##########jsonified !')
        #print(datasetjson)
        return datasetjson








    def get_scans(scanslice,delayslice):
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
                scandata = np.reshape(scandata,(32,1))
                #print(np.shape(scandata))
                s2sdata = np.load(s2sf)
                s2sdata = np.reshape(s2sdata,(32,1))
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
    def findmaxval(dataarray):
        absarray = np.abs(dataarray)
        maxval = float(absarray.max())
        #print('Maxvalue for colormap:' +str(maxval))
        minval = -maxval

        return maxval,minval
    

    def gencmap():
        print('hello')

        






