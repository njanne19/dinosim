import numpy as np 
import matplotlib.pyplot as plt

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
        
    def get_absolute_pointing_angle(self, degrees=True): 
        if degrees: 
            return self.angle_global + self.pointing_angle
        else: 
            return np.radians(self.angle_global + self.pointing_angle)
        
    def set_comm_params(self, transmit_power_dBm, frequency_hz, antenna_gain_dB): 
        self.transmit_power_dBm = transmit_power_dBm
        self.frequency_hz = frequency_hz
        self.antenna_gain_dB = antenna_gain_dB
        self.antenna_gain_abs = 10 ** (antenna_gain_dB / 10)
        self.comms_params_set = True
        
    def get_absolute_radiation_pattern(self, degrees=True): 
        
        if not self.comms_params_set: 
            raise ValueError("Communication parameters not set. Please call set_comm_params() first.")
            
        # Uses a simplified radiation pattern model. Under the assumption that a patch antenna 
        # with a gain of 3dB will have a half-power beamwidth of 65 degrees. 
        # These values are hardcoded, as they define the shape of the radiation pattern.
        # As it changes with gain value. 
        beamwidth_3dB = 65
        gain_3dB = 3    
        K = beamwidth_3dB * np.sqrt(gain_3dB)
            
        # Calculate gaussian parameters for satellite's specific architecture
        antenna_beamwidth = K / np.sqrt(self.antenna_gain_dB)
        sigma = np.radians(antenna_beamwidth) / 2
        theta = np.linspace(-np.pi, np.pi, 360)
        
        # Get gains for all these values of theta. 
        pattern = self.antenna_gain_dB * np.exp(-0.5 * (theta / sigma) ** 2)
        
        if not degrees: 
            theta = np.radians(theta) # Return theta in radians
        
        return theta, pattern
    
    def get_absolute_radiation_pattern_dB(self, degrees=True): 
        theta, pattern = self.get_absolute_radiation_pattern(degrees=degrees)
        return theta, 10 * np.log10(pattern)
    
    def get_normalized_radiation_pattern(self, degrees=True):
        theta, pattern = self.get_absolute_radiation_pattern(degrees=degrees)
        return theta, pattern / np.max(pattern)
    
    def get_normalized_radiation_pattern_dB(self, degrees=True):
        theta, pattern_dB = self.get_absolute_radiation_pattern_dB(degrees=degrees)
        return theta, pattern_dB - np.max(pattern_dB)
    
    def plot_absolute_radiation_pattern(self):
        theta, pattern = self.get_absolute_radiation_pattern() # No radians option available.
        plt.figure()
        ax = plt.subplot(111, polar=True)
        ax.plot(theta, pattern)
        ax.set_title(f"Absolute Radiation Pattern for {self.name}, Gain = {self.antenna_gain_dB} dB = {self.antenna_gain_abs} linear")
        ax.set_ylim(0, 1.75*self.antenna_gain_abs)
        ax.grid(True)
        
    def plot_absolute_radiation_pattern_dB(self):
        theta, pattern_dB = self.get_absolute_radiation_pattern_dB() # No radians option available.
        plt.figure()
        ax = plt.subplot(111, polar=True)
        ax.plot(theta, pattern_dB)
        ax.set_title(f"Absolute Radiation Pattern (dB) for {self.name}, Gain = {self.antenna_gain_dB} dB")
        ax.set_ylim(-40, 3*self.antenna_gain_dB)
        ax.grid(True)
    
    def get_absolute_gain(self, theta, degrees=True): 
        if not self.comms_params_set: 
            raise ValueError("Communication parameters not set. Please call set_comm_params() first.")
        
        # Uses a simplified radiation pattern model. Under the assumption that a patch antenna 
        # with a gain of 3dB will have a half-power beamwidth of 65 degrees. 
        # These values are hardcoded, as they define the shape of the radiation pattern.
        # As it changes with gain value. 
        beamwidth_3dB = 65
        gain_3dB = 3    
        K = beamwidth_3dB * np.sqrt(gain_3dB)
            
        # Calculate gaussian parameters for satellite's specific architecture
        antenna_beamwidth = K / np.sqrt(self.antenna_gain_dB)
        sigma = np.radians(antenna_beamwidth) / 2
        
        if not degrees: 
            theta = np.degrees(theta) # Theta is passed in as radians 
        
        return self.antenna_gain_dB * np.exp(-0.5 * (theta / sigma) ** 2)
    
    def get_absolute_gain_dB(self, theta, degrees=True): 
        return 10 * np.log10(self.get_absolute_gain(theta, degrees=degrees))