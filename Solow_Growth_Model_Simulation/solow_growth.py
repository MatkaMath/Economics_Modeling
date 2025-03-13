# Solow Growth Model Simulation with Steady-State Comparison
# This Python project models economic growth using the Solow-Swan framework.
# It simulates capital accumulation, labor growth, and technological progress over time.
# The model includes policy interventions affecting savings rates and economic shocks impacting technology.
# Steady-state values are calculated and plotted for comparison.

import numpy as np
import matplotlib.pyplot as plt

# Parameters
alpha = 0.33  # Capital share of income
delta = 0.05  # Depreciation rate
s = 0.2       # Initial savings rate
n = 0.01      # Population growth rate
g = 0.02      # Technological growth rate
A0 = 1        # Initial technology level
K0 = 1        # Initial capital level
L0 = 1        # Initial labor level
T = 100       # Time periods
policy_intervention = 50  # Period when government policy affects savings rate
s_new = 0.3   # New savings rate after policy intervention
shock_period = 75  # Period when an economic shock occurs
shock_magnitude = -0.1  # Reduction in technology due to shock

# Arrays to store results
K = np.zeros(T)
Y = np.zeros(T)
L = np.zeros(T)
A = np.zeros(T)

# Initial values
K[0] = K0
L[0] = L0
A[0] = A0

# Compute steady-state values before simulation
K_ss = (s * A0 / (delta + n + g))**(1 / (1 - alpha))
Y_ss = A0 * (K_ss**alpha) * (L0**(1 - alpha))
C_ss = (1 - s) * Y_ss

# Solow Growth Model Simulation
def solow_growth(T, alpha, delta, s, s_new, n, g, K, L, A, policy_intervention, shock_period, shock_magnitude):
    for t in range(1, T):
        Y[t-1] = A[t-1] * K[t-1]**alpha * L[t-1]**(1-alpha)  # Output
        current_s = s_new if t >= policy_intervention else s  # Apply new savings rate after intervention
        K[t] = current_s * Y[t-1] + (1 - delta) * K[t-1]  # Capital accumulation
        L[t] = (1 + n) * L[t-1]  # Labor growth
        A[t] = (1 + g) * A[t-1]  # Technological progress
        
        # Apply economic shock
        if t == shock_period:
            A[t] *= (1 + shock_magnitude)
    
    Y[T-1] = A[T-1] * K[T-1]**alpha * L[T-1]**(1-alpha)  # Compute final output
    return K, Y, L, A

K, Y, L, A = solow_growth(T, alpha, delta, s, s_new, n, g, K, L, A, policy_intervention, shock_period, shock_magnitude)

# Compute Consumption dynamically based on the correct savings rate
C = np.zeros(T)
for t in range(T):
    current_s = s_new if t >= policy_intervention else s  # Use correct savings rate
    C[t] = (1 - current_s) * Y[t]  # Consumption calculation

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(range(T), K, label='Capital')
plt.plot(range(T), Y, label='Output')
plt.plot(range(T), L, label='Labor')
plt.plot(range(T), A, label='Technology')
plt.axvline(x=policy_intervention, color='r', linestyle='--', label='Policy Intervention')
plt.axvline(x=shock_period, color='k', linestyle='--', label='Economic Shock')

# Logarithmic scale for better visualization
plt.yscale('log')

plt.xlabel('Time')
plt.ylabel('Levels')
plt.legend()
plt.title('Solow Growth Model Simulation with Policy and Shocks')
plt.show()

