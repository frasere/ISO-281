#### Classes and functions for ISO 281 Calculations

import numpy as np
import pandas as pd
import math
import glob
import os
import scipy.stats as ss

###############################################################################################################

class brg_design():
    # create bearing objects using this class
    # all bearings have design parameters listed in __init__
    # Ca_rot is brg dynamic axial load rating and is a feature of brg design
    
    def __init__(self,i,z,dw,alpha,D,d,pu,kind,H,ca_manuf=None):
        # attributes of a bearing       
        self.i = i # no. of rows
        self.z = z # no. of brgs in a row
        self.dw = dw # diameter of indiv. brg  mm
        self.alpha = alpha # contact angle in degrees
        self.H = H # individual unit heiht in mm
        self.D = D # outside diameter mm
        self.d = d # inside (bore) diameter mm
        self.pu = pu    # fatigue limit load (from manufacturers catalogue)  in N
        self.kind = kind  # is the bearing a ball or roller
        if self.kind == 'ball':
            self.p = 3
        elif self.kind == 'roller':
            self.p = 3.3
        self.ca_manuf = ca_manuf # axial load rating (from manuf. catalogue else can calculate)  N
        
    def dp(self):
        # pitch diameter mm
        return (self.D + self.d)/2
    
    def Ca_rot(self):
        # brg dynamic axial load rating rotational
        if self.ca_manuf != None:
            ca = self.ca_manuf
        else:
            fc = float(input('Enter fc value (from ISO 281 tables): '))    # user inputs fc value if not providing Ca_manuf
            if self.kind == 'ball':
                ca = 1.1*(3.647*fc*(self.i*np.cos(np.deg2rad(self.alpha))**0.7)*(self.z**(2/3))*(self.dw**1.4)*np.tan(np.deg2rad(self.alpha)))
            else:
                ca = 1.1*fc*((self.H*np.cos(np.deg2rad(self.alpha))**(7/9))*(self.z**(3/4))*(self.dw**(29/37))*np.tan(np.deg2rad(self.alpha)))
        return ca

######################################################################################################################

def import_excel_file(file_name,file_location,cols):
    # function to load excel file of loading data from specified file location 
    # (cols is column names in excel file - must incl. time column)

        working_location = os.getcwd()
        os.chdir(file_location)
        data = pd.read_excel(file_name,header=1)
        data.columns = cols
        os.chdir(working_location)
    
        return data

###############################################################################################################

class load_case_comb():
    # combine load cases for each tidal profile and calculate theta, N, P
    
    def __init__(self,file_location,col_headers,brg_p,brg_dp):
        self.file_location = file_location
        self.col_headers = col_headers
        self.brg_p = brg_p
        self.brg_dp = brg_dp
        
    def load_data(self):
        # load raw load case data from TB
        sim_data = [import_excel_file(os.listdir(self.file_location)[i],self.file_location,self.col_headers) for i in range(len(os.listdir(self.file_location)))]
        return sim_data
    
    def lc_df(self):
        # units are kN and m
        TB_data = self.load_data()
        Fr = [np.sqrt((np.sum((np.absolute(TB_data[i]['Fxy'])**2))/np.size(TB_data[i]['Fxy']))) for i in range(len(TB_data))]
        Fa = [np.sqrt((np.sum((np.absolute(TB_data[i]['Fz'])**2))/np.size(TB_data[i]['Fz'])))for i in range(len(TB_data))]
        My = [np.sqrt((np.sum((np.absolute(TB_data[i]['My'])**2))/np.size(TB_data[i]['My'])))for i in range(len(TB_data))]
        P_eak = [(0.75*Fr[i])+(Fa[i])+(2*My[i]/(self.brg_dp/1000)) for i in range(len(TB_data))]
        osc_amp = [abs(TB_data[i]['PS deg'].diff()).mean() for i in range(len(TB_data))]   # amplitude
        osc_opm = [(abs(TB_data[i]['PS deg'].diff()).sum()/(len(TB_data[i]['PS deg'])/60)) for i in range(len(TB_data))]  # speed
        df = pd.DataFrame({'Osc_amp deg':osc_amp,'Speed opm':osc_opm,'Fr rms':Fr,'Fa rms':Fa,'My rms': My,'Dyn Equiv Load':P_eak})
        return df

###########################################################################################################
    
class tidal_profile_comb():
    # combine equivalent loads from each load case and calc P_osc, theta_equiv and N_ave

    def __init__(self,duty_cycles,load_cases,brg_p,Ca,z):
        self.duty_cycles = duty_cycles   # list of time fractions
        self.load_cases = load_cases   # list of dataframes
        self.brg_p = brg_p
        self.Ca = Ca
        self.z = z

    def tp_comb(self):
        # combine load case dataframes and calculate dyn_equiv_osc
        df = pd.concat(self.load_cases,ignore_index=True)
        df['Duty Cycle'] = self.duty_cycles
        return df
    
    def dyn_equiv_osc(self):
        # dynamic equivalent load (oscillatory)
        df = self.tp_comb()
        numerator = np.sum((df['Dyn Equiv Load']**self.brg_p)*df['Speed opm']*df['Duty Cycle']*df['Osc_amp deg'])
        denominator = np.sum(df['Speed opm']*df['Duty Cycle']*df['Osc_amp deg'])
        return (numerator/denominator)**(1/self.brg_p)

    def N_opm_ave(self):
        # N_ave
        n_ave = np.sum(self.tp_comb()['Speed opm']*self.tp_comb()['Duty Cycle'])
        return n_ave

    def theta_equiv(self):
        # theta equivalent       
        numerator = np.sum(self.tp_comb()['Speed opm']*self.tp_comb()['Duty Cycle']*self.tp_comb()['Osc_amp deg'])
        denominator = np.sum(self.tp_comb()['Speed opm']*self.tp_comb()['Duty Cycle'])
        return (numerator/denominator) 

    def Ca_osc(self):
        # brg dynamic axial load rating oscillatory
        if self.brg_p == 3.3:
            ca_osc = self.Ca*((180/self.theta_equiv())**(2/9))*(self.z**0.028)
        else:
            ca_osc = self.Ca*((180/self.theta_equiv())**(3/10))*(self.z**0.033)
        return ca_osc

######################################################################################################################################################################
    
class life_calcs():
    # class for performing life calculations
    
    def __init__(self,brg_ca_osc,Pea_osc,kind,dp,lub_contam_level,pu,rel_level,use_ISO_correction,k=0.076):
        self.brg_ca_osc = brg_ca_osc   # brg osc axial load rating
        self.Pea_osc = Pea_osc  # oscillatory dynamic equivalent load
        self.kind = kind   # brg type
        self.dp = dp    # pitch diameter of brg mm
        self.lub_contam_level = lub_contam_level  # level of contamination in brg grease lubricant (see Table 7 NREL DG03)
        self.k = k   # measure of adequacy of lubrication (for yaw, pitch brgs assumed to be 0.076 see NREL DG03)
        if self.kind == 'ball':
            self.p = 3
        else:
            self.p = 3.3
        self.pu = pu  # bearing fatigue limit (from manufacturers catalogue)
        self.rel_level = rel_level
        self.use_ISO_correction = use_ISO_correction
        
    def eta(self):
        # parameter of a_iso calculation
        # level of particulate contam in grease lubricant
        contam_table = pd.DataFrame({'Contam Level':['high cleanliness','normal cleanliness','typical contamination','severe contamination','very severe contamination'],
               'c1':[0.0864,0.0432,0.0177,0.0115,0.00617],'c2':[0.6796,1.141,1.887,2.662,4.06]})
        eta = 0.173*contam_table.loc[contam_table['Contam Level']==self.lub_contam_level]['c1'].values*(self.k**0.68)*(self.dp**0.55)*(1-(contam_table.loc[contam_table['Contam Level']==self.lub_contam_level][['c2']].values/(self.dp**(1/3))))
        return eta
    
    def a_iso(self):
        # ISO correction factor
        if self.kind == 'ball':
            params = [2.5671,2.2649,0.053481,0.83,0.333,-9.3]
        else:
            params = [1.5859,1.3993,0.054381,1,0.4,-9.185]
        a_iso = 0.1*(1-((params[0]-(params[1]/(0.076**params[2])))**params[3])*(((self.eta()*self.pu)/self.Pea_osc)**params[4]))**params[5]
        return a_iso[0][0]
    
    def a1(self):
        # a1 life modification factor
        a1_table = pd.DataFrame({'Reliability %':[90,95,96,97,98,99,99.95],'a1':[1,0.64,0.55,0.47,0.37,0.25,0.077]})
        a1 = a1_table.loc[a1_table['Reliability %']==self.rel_level]['a1']
        return a1
    
    def L10_mill_osc(self):
        # L10 ISO life equation (millions of oscillations)
        if self.use_ISO_correction =='Yes':
            l10 = self.a_iso()*self.a1()*(self.brg_ca_osc/self.Pea_osc)**self.p
        elif self.use_ISO_correction =='No':
            l10 = (self.brg_ca_osc/self.Pea_osc)**self.p
        else: 
            print('Huh? Tell me Yes or No')
        return l10
    
    def L10_hrs(self,N_ave):
        # L10 ISO life equation (hrs)
        l10 = (self.L10_mill_osc()*1000000)/(N_ave*60)
        return l10