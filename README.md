# Preliminary Tidal Range Turbine Sizing

A Python tool for estimating the number and size of turbines required for a lagoon-based tidal energy project.

The methodology follows Neil et al. (2021) *Tidal Range Resource in Australia* and the turbine performance model is based on Angeloudis et al. (2018) *Optimising tidal range power plant operation*.

## Usage

Run the script directly to size a tidal lagoon project:

```bash
python estimate_turbine.py
```

Edit the inputs at the bottom of the script:

```python
mean_lagoon_area = 72   # km²
mean_tidal_range = 3    # m
```

The script will print the predicted capacity, rated power per turbine, rotor diameter, rated head, and the number of turbines required.

## Functions

### `determine_capacity(mean_area, mean_tidal_range, efficiency=0.4, capacity_factor=0.2)`
Estimates the total installed capacity (MW) of the lagoon from its area and tidal range, using the potential energy stored in the tidal prism.

### `determine_rated_power(mean_tidal_range, turbine_params=None)`
Returns the peak power output (MW) of a single turbine by scanning its hill chart across a range of head values.

### `hill_chart_parametrisation_h(h, turbine_params)`
Core performance model. Returns the power (MW) and discharge (m³/s) of a turbine at a given tidal head difference `h`, following empirical hill chart equations.

### `extract_hill_chart(h_array, turbine_params)`
Sweeps `hill_chart_parametrisation_h` over an array of head values and returns a dataset suitable for plotting the full turbine performance curve.

## Dependencies

- Python 3
- [NumPy](https://numpy.org/)

## References

- Neil, C., Angeloudis, A., Robins, P.E., Walkington, I., Ward, S.L., Masters, I., Lewis, M.J., Piano, M., Avdis, A., Piggott, M.D., Aggidis, G., Evans, P., Adcock, T.A.A., Zidonis, A., Ahmadian, R., Falconer, R. (2018). Tidal range energy resource and optimization – Past perspectives and future challenges. *Renewable Energy*, 127, 763–778.
- Angeloudis, A., Kramer, S.C., Avdis, A., & Piggott, M.D. (2018). Optimising tidal range power plant operation. *Applied Energy*, 212, 680–690.
- Pappas, K., et al. (2024). On the economic feasibility of tidal range power plants. *Proceedings of the Royal Society A: Mathematical, Physical and Engineering Sciences*. doi: [10.1098/rspa.2023.0867](https://doi.org/10.1098/rspa.2023.0867)
- Pappas, K., et al. (2023). Sensitivity of tidal range assessments to harmonic constituents and analysis timeframe. *Renewable Energy*. doi: [10.1016/j.renene.2023.01.062](https://doi.org/10.1016/j.renene.2023.01.062)
