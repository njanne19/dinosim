import numpy as np 
import matplotlib.pyplot as plt 
from dinosim.spacecraft import DINO
from dinosim.bodies import Planet


def get_power_received_field_from_spacecraft(xlim, ylim, craft, num_points=100, antenna_correction=True): 
    """
        Generates a grid of points over the specified xlim and ylim that represent the power received at each point
        from a single spacecraft. Implements free space pathloss equation given frequency. 
    """
    
    # First generate the grid of points 
    x = np.linspace(xlim[0], xlim[1], num_points)
    y = np.linspace(ylim[0], ylim[1], num_points)
    
    # Meshgrid
    X, Y = np.meshgrid(x, y)
    
    # Initialize the power received field 
    distance_field = np.zeros_like(X)
    
    # Then get the global position of the spacecraft in question 
    global_x = craft.orbiting_body.x + (craft.altitude + craft.orbiting_body.radius) * np.cos(np.radians(craft.angle_global))
    global_y = craft.orbiting_body.y + (craft.altitude + craft.orbiting_body.radius) * np.sin(np.radians(craft.angle_global))
    
    # Then for each point in the field, calculate the distance
    for i in range(num_points): 
        for j in range(num_points): 
            distance_field[i, j] = np.sqrt((X[i, j] - global_x) ** 2 + (Y[i, j] - global_y) ** 2)
    
    # Since X/Y units are in km * 10e3, multiply by 1000
    path_loss_field = 20 * np.log10(distance_field * 1000) + 20 * np.log10(craft.frequency_hz/1e6) + 32.44
    
    # Calculate the power recieved at each point (without antenna correction)
    power_received = craft.transmit_power_dBm - path_loss_field
    
    # Finally, apply the antenna gain correction. To do this, for a given point, calculate the angle between the
    # spacecraft's pointing direction and the vector from the spacecraft to the point.
    # Then, calculate the gain at that angle and apply it to the received power.
    if antenna_correction: 
        for i in range(num_points): 
            for j in range(num_points): 
                # Calculate the angle between the pointing direction and the vector from the spacecraft to the point
                pointing_angle = -1*craft.get_absolute_pointing_angle(degrees=False)
                vector_to_point = np.array([X[i, j] - global_x, Y[i, j] - global_y])
                rotation_matrix = np.array([[np.cos(pointing_angle), -np.sin(pointing_angle)], [np.sin(pointing_angle), np.cos(pointing_angle)]])
                vector_to_point_in_new_frame = np.dot(rotation_matrix, vector_to_point)
                angle_to_point = np.arctan2(vector_to_point_in_new_frame[1], vector_to_point_in_new_frame[0])
                
                # Calculate the angle between the two vectors
                angle_diff = angle_to_point
                
                # Calculate the gain at that angle
                gain_at_angle = craft.get_absolute_gain_dB(angle_diff, degrees=False) 
                
                # Apply the gain to the received power
                power_received[i, j] += gain_at_angle
                
                # if i % 50 == 0 and j % 50 == 0:
                #     print(f"Spacecraft absolute angle is {craft.get_absolute_pointing_angle(degrees=True)} degrees.")
                #     print(f"For point ({X[i, j]}, {Y[i, j]}), angle to point is {np.degrees(angle_to_point)} and angle diff is {np.degrees(angle_diff)}.")
                #     print(f"Gain at angle is {gain_at_angle} dB.")
    
    return X, Y, power_received