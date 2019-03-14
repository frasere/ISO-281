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


