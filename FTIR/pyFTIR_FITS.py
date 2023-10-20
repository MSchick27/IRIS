import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize as opt
import pyFTIR

class advanced():
    def fouriersmooth(y,vac):
        rft = np.fft.rfft(y)
        rft[vac:] = 0   # Note, rft.shape = 21
        y_smooth = list(np.fft.irfft(rft))
        return y_smooth
    

class bandfits():
    def fitband(x,y,amp,xpeak,width,height,fitfunc):
        if fitfunc == 'lorentz':
            fitx,fity,parstring,par,fittype,fiterror,fwhm=bandfits.lorentzfit(x,y,amp,xpeak,width,height)
        return fitx,fity,parstring,par,fittype,fiterror,fwhm

    
    def lorentzfit(x,y,amp,xpeak,width,height):
        print(x,y,amp,xpeak,width,height)
        fittype ='lorentz'
        def lorentz(x,a,b,c,g):
            return ((a*c**2)/((x-b)**2+c**2)) + g
        def FWHM(c):
            return np.abs(c)*2#*np.pi

        guess=[amp,xpeak,width,height]
        print('Guess: '+str(guess))
        par,cov = opt.curve_fit(lorentz,x,y,guess,maxfev=100000)
        fiterror=  np.sqrt(np.diag(cov))
        print('Err: '+str(fiterror))
        fitx = x
        fity = []
        for i in range(len(x)):
            y_val = lorentz(x[i],*par)
            fity.append(y_val)

        print('check')
        fwhm = round(FWHM(par[2]),2)
        parstring = str('Amplitude:' + str(round(par[0],5)) + ', x:' + str(round(par[1],3)) +', c:' + str(round(par[2],3)) +', FWHM:' + str(round(FWHM(par[2]),2)))
        print(parstring)

        return fitx,fity,parstring,par,fittype,fiterror,fwhm








    def fitband_allg(x,y,fitfunc):
        if fitfunc == 'lorentz':
            fitx,fity,parstring,par,fittype,fiterror,fwhm=bandfits.lorentzfit_spec(x,y)
        
        if fitfunc == 'multi-lorentz':
            print('please have time to code this')

    def lorentzfit_spec(x,y):
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

        fittype ='lorentz'
        def lorentz(x,a,b,c,g):
            return ((a*c**2)/((x-b)**2+c**2)) + g
        def FWHM(c):
            return np.abs(c)*2#*np.pi

        guess=[amp,xpeak,width,height]
        print('Guess: '+str(guess))
        par,cov = opt.curve_fit(lorentz,x,y,guess,maxfev=100000)
        fiterror=  np.sqrt(np.diag(cov))
        print('Err: '+str(fiterror))
        fitx = x
        fity = []
        for i in range(len(x)):
            y_val = lorentz(x[i],*par)
            fity.append(y_val)

        print('check')
        fwhm = round(FWHM(par[2]),2)
        parstring = str('Amplitude:' + str(round(par[0],5)) + ', x:' + str(round(par[1],3)) +', c:' + str(round(par[2],3)) +', FWHM:' + str(round(FWHM(par[2]),2)))
        print(parstring)

        return fitx,fity,parstring,par,fittype,fiterror,fwhm
