#### Classes for ISO 281 Calculations

###############################################################################################################

class brg_design():
    # create bearing objects using this class
    # all bearings have design parameters listed in __init__
    # Ca_rot is brg dynamic axial load rating and is a feature of brg design
    
    def __init__(self,i,z,dw,alpha,dp,pu,kind,ca_manuf=None):
        # attributes of a bearing       
        self.i = i # no. of rows
        self.z = z # no. of brgs in a row
        self.dw = dw # diameter of indiv. brg  mm
        self.alpha = alpha # contact angle in degrees
        self.dp = dp # pitch diameter m
        self.pu = pu    # fatigue limit load (from manufacturers catalogue)  in N
        self.kind = kind  # is the bearing a ball or roller
        if self.kind == 'ball':
            self.p = 3
        elif self.kind == 'roller':
            self.p = 3.3
        self.ca_manuf = ca_manuf # axial load rating (from manuf. catalogue else can calculate)  N
    
    def Ca_rot(self,fc):
        # brg dynamic axial load rating rotational
        if self.kind == 'ball':
            ca = (3.647*(self.i*fc*np.cos(np.deg2rad(self.alpha))**0.7)*(self.z**(2/3))*(self.dw**1.4)*np.tan(np.deg2rad(self.alpha)))
        else:
            ca = ((self.i*fc*np.cos(np.deg2rad(self.alpha))**0.7)*(self.z**(2/3))*(self.dw**1.4)*np.tan(np.deg2rad(self.alpha)))
        return ca

######################################################################################################################

class load_case_comb():
    # combine load cases for each tidal profile and calculate theta, N, P
    
    def __init__(self,file_location,col_headers,brg_p):
        self.file_location = file_location
        self.col_headers = col_headers
        self.brg_p = brg_p
        
    def load_TB_data(self):
        # load raw load case data from TB
        sim_data = [import_TB_runs(os.listdir(self.file_location)[i],self.file_location,self.col_headers) for i in range(len(os.listdir(self.file_location)))]
        return sim_data
    
    def lc_df(self,brg_dp):
        # units are kN and m
        TB_data = self.load_TB_data()
        Fr = [np.sqrt((np.sum((np.absolute(TB_data[i]['Fxy'])**2))/np.size(TB_data[i]['Fxy']))) for i in range(len(TB_data))]
        Fa = [np.sqrt((np.sum((np.absolute(TB_data[i]['Fz'])**2))/np.size(TB_data[i]['Fz'])))for i in range(len(TB_data))]
        My = [np.sqrt((np.sum((np.absolute(TB_data[i]['My'])**2))/np.size(TB_data[i]['My'])))for i in range(len(TB_data))]
        P_eak = [(0.75*Fr[i])+(Fa[i])+(2*My[i]/(brg_dp/1000)) for i in range(len(TB_data))]
        osc_amp = [abs(TB_data[i]['PS deg'].diff()).mean() for i in range(len(TB_data))]
        osc_opm = [(abs(TB_data[i]['PS deg'].diff()).sum()/(len(TB_data[i]['PS deg'])/60)) for i in range(len(TB_data))]
        df = pd.DataFrame({'Osc_amp deg':osc_amp,'Speed opm':osc_opm,'Fr rms':Fr,'Fa rms':Fa,'My rms': My,'Dyn Equiv Load':P_eak})
        return df
