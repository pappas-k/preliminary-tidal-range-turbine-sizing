"""
Description:
Calculate the size and number of turbines required for a lagoon-based tidal energy project.
We follow the methodology used in Tidal Range Resource in Australia (2021) by Neil et al.
"""

import numpy as np

def hill_chart_parametrisation_h(h, turbine_params):
    """
    Hill chart parametrisation, which represents the performance of a tidal turbine
    across different tidal head differences. The script is based on the methodology
    of Angeloudis et al. in Optimising tidal range power plant operation (2018).

    Parameters:
    - h (float): The tidal head difference (in m) for which parameters are calculated.
    - turbine_params (dict): A dictionary containing turbine specifications, including grid frequency f_g (Hz),
        generator poles g_p, turbine capacity t_cap (MW), gravity acceleration g (m/s^2), rotor diameter t_d (m),
        water density dens (kg/m^3), rated head h_cap (m), minimum operational head h_min (m), and efficiency
        ebb, flood coefficients eta.

    Returns:
    - p_value (float): Power value (MW)
    - q_value (float): Discharge value (m^3/s)

    Example:
    h = 5.0
    turbine_params = {"f_g": 50, "g_p": 96, "t_d": 7.35, "g": 9.807, "h_cap": 5.5,
                      "dens": 1025, "h_min": 1.0, "eta": [0.93, 0.83]}
    p, q = hill_chart_parametrisation_h(h, turbine_params=turbine_params)
    """

    turb_sp = 2 * 60 * turbine_params["f_g"] / turbine_params["g_p"]

    # Step 1: Calculate Hill Chart based on empirical equations
    n_11 = turb_sp * turbine_params["t_d"] / np.sqrt(h)

    if n_11 < 255:
        q_11 = 0.0166 * n_11 + 0.4861
    else:
        q_11 = 4.75

    q = q_11 * (turbine_params["t_d"] ** 2) * np.sqrt(h)
    h_efficiency = -0.0019 * n_11 + 1.2461

    p1 = turbine_params["dens"] * turbine_params["g"] * q * h / (10 ** 6)
    # Step 2 - Adjust Curve according to capacity
    if h < turbine_params["h_cap"]:  # 97.25% Gearbox efficiency
        p2 = p1 * 0.9725 * h_efficiency
    else:
        n_11 = turb_sp * turbine_params["t_d"] / np.sqrt(turbine_params["h_cap"])
        q_11 = 0.0166 * n_11 + 0.4861
        h_efficiency = -0.0019 * n_11 + 1.2461
        q = q_11 * (turbine_params["t_d"] ** 2) * np.sqrt(turbine_params["h_cap"])
        p2 = turbine_params["dens"] * turbine_params["g"] * q * turbine_params["h_cap"] / \
             (10 ** 6) * h_efficiency * 0.9725
        p1 = p2 / (h_efficiency * 0.9725)

    q = p1 * (10 ** 6) / (turbine_params["dens"] * turbine_params["g"] * h)

    return max(0., p2), q

def extract_hill_chart(h_array, turbine_params):
    """
    Produces a dataset for plotting hill charts.

    Parameters:
        h_array (array-like): An array of values representing tidal head values.
        turbine_params (dict): A dictionary containing turbine specifications.

    Returns:
        numpy.ndarray: An array containing h_array, p-values, and q-values.

    Example:
        turbine_params = {"f_g": 50, "g_p": 96, "t_d": 7.35, "g": 9.807, "h_cap": 5.5,
                      "dens": 1025, "h_min": 1.0, "eta": [0.93, 0.83]}
        h_array = np.arange(0.1, 10, 0.1)
        hill_chart = extract_hill_chart(h_array, turbine_params)
    """
    p, q = zip(*(hill_chart_parametrisation_h(h_val, turbine_params=turbine_params) for h_val in h_array))
    return np.array([h_array, np.array(p), np.array(q)]).T

def determine_capacity(mean_area, mean_tidal_range, efficiency=0.4, capacity_factor=0.2):
    """
    Calculate the capacity of a tidal energy system.
    Parameters:
        mean_area (float): The mean area over which the tidal energy system operates (in km^2).
        mean_tidal_range (float): The mean tidal range (in m).
        efficiency (float, optional): The efficiency of the energy conversion process (default is 0.4).
        capacity_factor (float, optional): The capacity factor (default is 0.2).
    Returns:
        float: The predicted capacity in megawatts (MW).

    Example:
        area = 100.0       (in km^2)
        tidal_range = 5.0  (in m)
        capacity = determine_capacity(area, tidal_range)
    """
    grav, dens = 9.807, 1025

    capacity = efficiency * mean_area * 1e6 * ((0.5 * grav * dens * mean_tidal_range * mean_tidal_range / 1e6 * 0.000277778) / (12.42 / 2) / capacity_factor)

    print(f"Capacity predicted = {capacity} MW")
    return capacity

def determine_rated_power(mean_tidal_range, turbine_params=None):
    """
    Calculate the rated power of a tidal turbine based on specified parameters.
    Parameters:
        mean_tidal_range (float): The mean tidal range over a specified time period.
        turbine_params (dict): A dictionary containing turbine specifications.
    Returns:
        float: The rated power of the tidal turbine in megawatts (MW).

    Example:
        mean_tidal_range = 6.0  # meters
        rated_power = determine_rated_power(mean_tidal_range)
    """
    if turbine_params is None:
        turbine_params = {"f_g": 50, "g_p": 96, "g": 9.807, "t_d": 7.35,
                          "h_cap": 0.8 * mean_tidal_range, "dens": 1025, "h_min": 1.00,
                          "eta": [0.93, 0.83]}

    h_array = np.arange(0.1, 10, 0.1)
    hill_chart = extract_hill_chart(h_array, turbine_params)

    rated_power = np.max(hill_chart[:, 1])

    return rated_power

if __name__ == "__main__":

    # Inputs:
    mean_lagoon_area = 72  # in km^2
    mean_tidal_range = 3   # in m

    # Calculate predicted capacity:
    capacity = determine_capacity(mean_lagoon_area, mean_tidal_range, efficiency=0.4, capacity_factor=0.20)

    # Specified turbines specifications. Check the hill_chart_parametrisation_h dockstring for keys definitions:
    turbine_params = {"f_g": 50, "g_p": 96, "g": 9.807, "t_d": 7.35,
                      "h_cap": 0.8 * mean_tidal_range, "dens": 1025, "h_min": 1.00,
                      "eta": [0.93, 0.83]}

    # Calculate turbine rated power:
    rated_power = determine_rated_power(mean_tidal_range, turbine_params=turbine_params)

    # Calculate number of turbines:
    turbines_num = capacity / rated_power

    print(f"Rotor diameter = {turbine_params['t_d']} m")
    print(f"Rated head = {turbine_params['h_cap']} m")
    print(f"Rated power = {rated_power} MW")
    print(f"Number of turbines = {turbines_num}")

