import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize as opt
from FTIR import pyFTIR
import lmfit

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
            return fitx,fity,parstring,par,fittype,fiterror,fwhm


    def lorentz(x,a,b,c,g):
            return ((a*c**2)/((x-b)**2+c**2)) + g
    def lorentzFWHM(c):
            return np.abs(c)*2#*np.pi
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

        guess=[amp,xpeak,width,height]
        print('Guess: '+str(guess))
        par,cov = opt.curve_fit(bandfits.lorentz,x,y,guess,maxfev=100000)
        fiterror=  np.sqrt(np.diag(cov))
        print('Err: '+str(fiterror))
        fitx = x
        fity = []
        for i in range(len(x)):
            y_val = bandfits.lorentz(x[i],*par)
            fity.append(y_val)

        print('check')
        fwhm = round(bandfits.lorentzFWHM(par[2]),2)
        parstring = str('Amplitude:' + str(round(par[0],5)) + ', x:' + str(round(par[1],3)) +', c:' + str(round(par[2],3)) +', FWHM:' + str(round(bandfits.lorentzFWHM(par[2]),2)))
        print(parstring)

        return fitx,fity,parstring,par,fittype,fiterror,fwhm










class advanced_fits():
    def init(x,y,fitfunc):
        if fitfunc == 'adv_multi-lrnz':
            list_of_stuff= advanced_fits.curvefitbased_lorentz(x,y)
            return list_of_stuff
        if fitfunc == 'adv_multi-lrnz':
            list_of_stuff= advanced_fits.multi_lorentz(x,y)
            return list_of_stuff

    def curvefitbased_lorentz(x,y):
        print('method: scipy')
        fittype='multi-Lorentz'
        tpoints = plt.ginput(n=10,timeout=40, show_clicks=True, mouse_add = plt.MouseButton.LEFT,mouse_pop= plt.MouseButton.RIGHT,mouse_stop = plt.MouseButton.MIDDLE)
        xcords_points = list(item[0] for item in tpoints)
        ycords_points = list(item[1] for item in tpoints)
        xcord_left = min(xcords_points)
        xcords_points.remove(xcord_left)
        xcord_right = max(xcords_points)
        xcords_points.remove(xcord_right)
        peaknumber = len(xcords_points)
        x,y = pyFTIR.manipulate_data.data_reduce(x,y,xcord_left,xcord_right)

        def lorentzmodel(x,a,b,c):
            return ((a*c**2)/((x-b)**2+c**2))
        
        def linearmodel(x,a):
            return a
        
        #generate model
        model = linearmodel
        



    def multi_lorentz(x,y):
        fittype='multi-Lorentz'
        tpoints = plt.ginput(n=10,timeout=40, show_clicks=True, mouse_add = plt.MouseButton.LEFT,mouse_pop= plt.MouseButton.RIGHT,mouse_stop = plt.MouseButton.MIDDLE)
        
        xcords_points = list(item[0] for item in tpoints)
        ycords_points = list(item[1] for item in tpoints)
        xcord_left = min(xcords_points)
        xcords_points.remove(xcord_left)
        xcord_right = max(xcords_points)
        xcords_points.remove(xcord_right)
        peaknumber = len(xcords_points)
        x,y = pyFTIR.manipulate_data.data_reduce(x,y,xcord_left,xcord_right)

        #for i in range(peaknumber): write function with lmfit
        def add_peak(prefix, center, amplitude=0.005, sigma=0.05):
            peak = lmfit.models.LorentzianModel(prefix=prefix)
            pars = peak.make_params()
            pars[prefix + 'center'].set(center)
            pars[prefix + 'amplitude'].set(amplitude,min = 0,max = max(ycords_points))
            pars[prefix + 'sigma'].set(sigma, min=0)
            return peak, pars
        
        model = lmfit.models.ConstantModel(prefix='C0_')
        params = model.make_params(a=0)
        #model = lmfit.models.LorentzianModel(prefix='C0_')
        #params = model.make_params(a=0,b=0,c=0)

        rough_peak_positions = xcords_points
        #print(rough_peak_positions)
        for i, cen in enumerate(rough_peak_positions):
            print(cen)
            peak, pars = add_peak('lz%d_' % (i+1), cen)
            model = model + peak
            params.update(pars)

            
        result = model.fit(y, params, x=x)
        comps = result.eval_components()

        print(result.fit_report(min_correl=0.5))
        fitx = x
        fity = result.best_fit
        comps = result.eval_components()    #for name, comp in comps.items():

        dict_of_fitbands = {'mainfit':[fitx,fity]}
        for name,comp in comps.items():
            dict_of_fitbands[name]= [fitx,comp]

        print(len(dict_of_fitbands))
        return dict_of_fitbands
    
    


