import numpy as np 
import matplotlib.pyplot as plt 
from dinosim.spacecraft import DINO
from dinosim.bodies import Planet

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
        circle = plt.Circle((planet.x, planet.y), planet.radius, alpha=0.5)
        ax.add_patch(circle)
        plt.text(planet.x, planet.y - planet.radius - 15, planet.name, fontsize=12, ha='center', va='center')
        
    ax.set_xlim([-100, 500]) 
    ax.set_ylim([-300, 300]) 
        
    # Spacecraft plot parameters 
    direction_vector_length = 40
    
    for craft in spacecraft: 
        
        print(f"Spacecraft {craft.name} is at altitude {craft.altitude} KM, orbiting {craft.orbiting_body.name}.")
        print(f"With global angle {craft.angle_global} degrees and pointing angle {craft.pointing_angle} degrees.")
        print(f"Orbiting body: {craft.orbiting_body}")
        
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