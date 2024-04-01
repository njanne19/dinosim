import numpy as np 

class DINO: 
    def __init__(self, 
                 name,
                 orbiting_body, 
                 altitude, 
                 angle_global, 
                 pointing_angle):
        """
            Initialize the spacecraft objet. 
            Args: 
                orbiting_body: the celestial body that the spacecraft is orbiting.
                altitude: altitude of the spacecraft in meters. 
                angle_global: global angle of the spacecraft in degrees. 0 starts at unit circle zero
                pointing_angle: 0 starts at pointing outwards from the orbiting body (defined by angle_global)
        """ 
        self.name = name
        self.orbiting_body = orbiting_body
        self.altitude = altitude
        self.angle_global = angle_global 
        self.pointing_angle = pointing_angle
        self.comms_params_set = False
        
    def set_comm_params(self, transmit_power, frequency, antenna_gain): 
        self.transmit_power = transmit_power
        self.frequency = frequency
        self.antenna_gain = antenna_gain
        self.comms_params_set = True
        
    def plot_noramlized_radiation_pattern(self): 
        
        if not self.comms_params_set: 
            raise ValueError("Communication parameters not set. Please call set_comm_params() first.")
            
        # Uses a simplified radiation pattern model. Under the assumption that a patch antenna 
        # with a gain of 3dB will have a half-power beamwidth of 65 degrees. 
        beamwidth_3dB = 65
        gain_3dB = 3    
            
            
        # Create a 2D cut of the radiation pattern, assuming phi = 0 
        theta = np.linspace(-np.pi/2, np.pi/2, 100)
        phi = np.zeros_like(theta) 
        
        # Get gains for all these values of theta. 
        gains = self.get_gain_abs(theta, phi)
        
        # Then make 2D polar plot 
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True)
        ax.plot(theta, gains)
        ax.set_title("Radiation pattern for {}".format(self.name))
        plt.show()
        
        
    def get_gain_abs(self, theta, phi): 
        """
            Get the gain of the spacecraft at a given theta and phi. 
            Args: 
                theta: the angle from the z-axis in radians. 
                phi: the angle from the x-axis in radians. 
        """
        if not self.comms_params_set: 
            raise ValueError("Communication parameters not set. Please call set_comm_params() first.")
            
        # Calculate the gain of the spacecraft. 
        c = 3e8
        lam = c / self.frequency
        k = 2 * np.pi / lam
        L = 0.5 * lam 
        W = 0.5 * lam
        
        E_theta = (
            (np.sin((k*W*np.sin(theta)*np.sin(phi))/2) / (k*W*np.sin(theta)*np.sin(phi)/2))
            * (np.cos((k*L/2)*np.sin(theta)*np.cos(phi)))*np.cos(phi)
        )
    
        return E_theta