import numpy as np 
import matplotlib.pyplot as plt 
from dinosim.spacecraft import DINO
from dinosim.bodies import Planet
from dinosim.comms import get_power_received_field_from_spacecraft

def plot_planets_and_spacecraft(planets, spacecraft): 
    """
        Plots the planets and spacecraft in 2D. 
        X and Y coordinates of planets define their position on the graph 
        Altitudes of spacecraft define their distance from the planets.
        Their orbiting bodies are defined by the planets they are orbiting.
        Global angles define the angle of the spacecraft in the graph relative 
        to its orbiting body (effectively the x-axis). 
        Pointing angles define the direction the spacecraft is pointing in (relative frame). 
    """  
    
    fig, ax = plt.subplots()
    
    for planet in planets: 
        planet_radius_text_offset = -1 * planet.radius - 15 if planet.radius < 20 else 0
        circle = plt.Circle((planet.x, planet.y), planet.radius, alpha=0.5)
        ax.add_patch(circle)
        plt.text(planet.x, planet.y + planet_radius_text_offset, planet.name, fontsize=12, ha='center', va='center')
        
    ax.set_xlim([-100, 500]) 
    ax.set_ylim([-300, 300]) 
        
    # Spacecraft plot parameters 
    direction_vector_length = 40
    
    for craft in spacecraft: 
        
        # print(f"Spacecraft {craft.name} is at altitude {craft.altitude} KM, orbiting {craft.orbiting_body.name}.")
        # print(f"With global angle {craft.angle_global} degrees and pointing angle {craft.pointing_angle} degrees.")
        # print(f"Orbiting body: {craft.orbiting_body}")
        
        global_x = craft.orbiting_body.x + (craft.altitude + craft.orbiting_body.radius) * np.cos(np.radians(craft.angle_global))
        global_y = craft.orbiting_body.y + (craft.altitude + craft.orbiting_body.radius) * np.sin(np.radians(craft.angle_global))
        
        # Plot the spacecraft
        plt.plot(global_x, global_y, 'ro')
        
        # Plot the direction vector
        direction_x = global_x + direction_vector_length * np.cos(craft.get_absolute_pointing_angle(degrees=False))
        direction_y = global_y + direction_vector_length * np.sin(craft.get_absolute_pointing_angle(degrees=False))
        ax.annotate("", xy=(direction_x, direction_y), xytext=(global_x, global_y), arrowprops=dict(arrowstyle="->"))
        
        
    # ax.set_aspect('equal', adjustable='datalim')
    ax.set_xlabel('X Coordinate (km * 10^3)') 
    ax.set_ylabel('Y Coordinate (km * 10^3)')
    ax.set_title('DINOs Spacecraft Configuration')
    ax.set_aspect('equal', 'box')
    plt.show()
    
    
def plot_received_power_field(planets, spacecraft, spacecraft_index=0, antenna_correction=True): 
    """
       Plots the recieved power at any given point in the map given the reception of a specific spacecraft.
       This spacecraft is defined with spacecraft_index. 
       The received power is the power received by any spacecraft at any given point.
    """  
    
    fig, ax = plt.subplots()
    xlim = [-100, 500]
    ylim = [-300, 300]
    
    # First, get the power recieved field and add it to the plot 
    X, Y, power_received = get_power_received_field_from_spacecraft(xlim, ylim, spacecraft[spacecraft_index], antenna_correction=antenna_correction)
    
    # Then, plot the power recieved field using pcolormesh 
    c = ax.pcolormesh(X, Y, power_received, cmap='plasma', shading='auto')
    fig.colorbar(c, ax=ax, label='Power Received (dBm)')
    
    for planet in planets: 
        planet_radius_text_offset = -1 * planet.radius - 15 if planet.radius < 20 else 0
        circle = plt.Circle((planet.x, planet.y), planet.radius, alpha=0.5, color='grey')
        ax.add_patch(circle)
        plt.text(planet.x, planet.y + planet_radius_text_offset, planet.name, fontsize=12, ha='center', va='center', color='white')
        
    ax.set_xlim(xlim) 
    ax.set_ylim(ylim) 
        
    # Spacecraft plot parameters 
    direction_vector_length = 40
    
    for craft in spacecraft: 
        
        # print(f"Spacecraft {craft.name} is at altitude {craft.altitude} KM, orbiting {craft.orbiting_body.name}.")
        # print(f"With global angle {craft.angle_global} degrees and pointing angle {craft.pointing_angle} degrees.")
        # print(f"Orbiting body: {craft.orbiting_body}")
        
        global_x = craft.orbiting_body.x + (craft.altitude + craft.orbiting_body.radius) * np.cos(np.radians(craft.angle_global))
        global_y = craft.orbiting_body.y + (craft.altitude + craft.orbiting_body.radius) * np.sin(np.radians(craft.angle_global))
        
        # Plot the spacecraft
        if craft == spacecraft[spacecraft_index]: 
            plt.plot(global_x, global_y, 'go')
        else: 
            plt.plot(global_x, global_y, 'ro')
        
        # Plot the direction vector
        direction_x = global_x + direction_vector_length * np.cos(craft.get_absolute_pointing_angle(degrees=False))
        direction_y = global_y + direction_vector_length * np.sin(craft.get_absolute_pointing_angle(degrees=False))
        ax.annotate("", xy=(direction_x, direction_y), xytext=(global_x, global_y), arrowprops=dict(arrowstyle="->"))
        
        
    # ax.set_aspect('equal', adjustable='datalim')
    ax.set_xlabel('X Coordinate (km * 10^3)') 
    ax.set_ylabel('Y Coordinate (km * 10^3)')
    ax.set_title(f'Best Power Recieved From DINOs Spacecraft {spacecraft_index}')
    ax.set_aspect('equal', 'box')
    plt.show()
    
    
def plot_best_received_power_field(planets, spacecraft, antenna_correction=True): 
    """
       Plots the best recieved power at any given point in the map given the reception of all spacecraft. 
       The best received power is the highest power received by any spacecraft at any given point.
    """  
    
    fig, ax = plt.subplots()
    xlim = [-100, 500]
    ylim = [-300, 300]
    
    # First, get the power recieved field and add it to the plot 
    power_maps = []
    
    for craft in spacecraft: 
        X, Y, power_received = get_power_received_field_from_spacecraft(xlim, ylim, craft, antenna_correction=antenna_correction)
        power_maps.append(power_received)
        
    best_power_map = np.max(np.array(power_maps), axis=0)
    
    # Then, plot the power recieved field using pcolormesh 
    c = ax.pcolormesh(X, Y, best_power_map, cmap='plasma', shading='auto')
    fig.colorbar(c, ax=ax, label='Power Received (dBm)')

    for planet in planets: 
        planet_radius_text_offset = -1 * planet.radius - 15 if planet.radius < 20 else 0
        circle = plt.Circle((planet.x, planet.y), planet.radius, alpha=0.5, color='grey')
        ax.add_patch(circle)
        plt.text(planet.x, planet.y + planet_radius_text_offset, planet.name, fontsize=12, ha='center', va='center', color='white')
        
    ax.set_xlim(xlim) 
    ax.set_ylim(ylim) 
        
    # Spacecraft plot parameters 
    direction_vector_length = 40
    
    for craft in spacecraft: 
        
        # print(f"Spacecraft {craft.name} is at altitude {craft.altitude} KM, orbiting {craft.orbiting_body.name}.")
        # print(f"With global angle {craft.angle_global} degrees and pointing angle {craft.pointing_angle} degrees.")
        # print(f"Orbiting body: {craft.orbiting_body}")
        
        global_x = craft.orbiting_body.x + (craft.altitude + craft.orbiting_body.radius) * np.cos(np.radians(craft.angle_global))
        global_y = craft.orbiting_body.y + (craft.altitude + craft.orbiting_body.radius) * np.sin(np.radians(craft.angle_global))
        
        # Plot the spacecraft
        plt.plot(global_x, global_y, 'ro')
        
        # Plot the direction vector
        direction_x = global_x + direction_vector_length * np.cos(craft.get_absolute_pointing_angle(degrees=False))
        direction_y = global_y + direction_vector_length * np.sin(craft.get_absolute_pointing_angle(degrees=False))
        ax.annotate("", xy=(direction_x, direction_y), xytext=(global_x, global_y), arrowprops=dict(arrowstyle="->"))
        
        
    # ax.set_aspect('equal', adjustable='datalim')
    ax.set_xlabel('X Coordinate (km * 10^3)') 
    ax.set_ylabel('Y Coordinate (km * 10^3)')
    ax.set_title('Best Power Recieved From Any DINOs Spacecraft')
    ax.set_aspect('equal', 'box')
    plt.show()
    
    
def plot_min_satellite_acquisition(planets, spacecraft, min_power=-135, antenna_correction=True): 
    """
       Plots the minimum number of satellites satisfying the minimum power requirement at any given point in the map. 
       The minimum power requirement is defined by min_power.
    """  
    
    fig, ax = plt.subplots()
    xlim = [-100, 500]
    ylim = [-300, 300]
    
    # First, get the power recieved field and add it to the plot 
    power_maps = []
    
    for craft in spacecraft: 
        X, Y, power_received = get_power_received_field_from_spacecraft(xlim, ylim, craft, antenna_correction=antenna_correction)
        power_maps.append(power_received)
        
    power_maps = np.array(power_maps)
    
    # now for each point, count the number of power maps that satisfy the min_power requirement
    num_satellites = np.sum(power_maps >= min_power, axis=0)
    
    # Then, plot the power recieved field using pcolormesh 
    c = ax.pcolormesh(X, Y, num_satellites, cmap='plasma', shading='auto')
    fig.colorbar(c, ax=ax, label='Number of Satellites Acquired')

    for planet in planets: 
        planet_radius_text_offset = -1 * planet.radius - 15 if planet.radius < 20 else 0
        circle = plt.Circle((planet.x, planet.y), planet.radius, alpha=0.5, color='grey')
        ax.add_patch(circle)
        plt.text(planet.x, planet.y + planet_radius_text_offset, planet.name, fontsize=12, ha='center', va='center', color='black' if planet.name == 'moon' else 'white')
        
    ax.set_xlim(xlim) 
    ax.set_ylim(ylim) 
        
    # Spacecraft plot parameters 
    direction_vector_length = 40
    
    for craft in spacecraft: 
        
        # print(f"Spacecraft {craft.name} is at altitude {craft.altitude} KM, orbiting {craft.orbiting_body.name}.")
        # print(f"With global angle {craft.angle_global} degrees and pointing angle {craft.pointing_angle} degrees.")
        # print(f"Orbiting body: {craft.orbiting_body}")
        
        global_x = craft.orbiting_body.x + (craft.altitude + craft.orbiting_body.radius) * np.cos(np.radians(craft.angle_global))
        global_y = craft.orbiting_body.y + (craft.altitude + craft.orbiting_body.radius) * np.sin(np.radians(craft.angle_global))
        
        # Plot the spacecraft
        plt.plot(global_x, global_y, 'go')
        
        # Plot the direction vector
        direction_x = global_x + direction_vector_length * np.cos(craft.get_absolute_pointing_angle(degrees=False))
        direction_y = global_y + direction_vector_length * np.sin(craft.get_absolute_pointing_angle(degrees=False))
        ax.annotate("", xy=(direction_x, direction_y), xytext=(global_x, global_y), arrowprops=dict(arrowstyle="->"))
        
        
    # ax.set_aspect('equal', adjustable='datalim')
    ax.set_xlabel('X Coordinate (km * 10^3)') 
    ax.set_ylabel('Y Coordinate (km * 10^3)')
    ax.set_title(f'Minimum DINOS Sats Under Acquisition Requirement')
    ax.set_aspect('equal', 'box')
    plt.show()