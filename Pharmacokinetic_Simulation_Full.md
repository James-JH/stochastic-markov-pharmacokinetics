# Pharmacokinetic Drug Simulation – Full Project

## Overview

This project simulates the movement and metabolism of a drug in the human body, accounting for patient variability and liver metabolism. The aim is to investigate how absorption, liver metabolism, and elimination impact drug exposure and to explore optimal dosing strategies.

**Techniques used:**
- Gillespie Algorithm (stochastic, molecule-level)
- Continuous-Time Markov Chains (CTMC, probabilistic compartment transitions)
- Monte Carlo Simulation (population variability and AUC analysis)

---

## Introduction

Understanding how a drug behaves in the body is crucial for effective treatment. Variability between patients in absorption, metabolism, and elimination rates can significantly impact drug efficacy and safety.  

This project simulates these dynamics and evaluates different dosing strategies to highlight the importance of personalised medicine.

**Key questions addressed:**
1. How does liver metabolism affect the timing and peak concentration of drugs in the bloodstream?  
2. How do individual differences affect optimal dosing strategies?

---

## Model Description

### Base Model (No Liver)
- Deterministic, linear compartmental model using ODEs  
- Compartments: Intestine → Bloodstream → Urine  
- Constant absorption (ka) and elimination (ke) rates across individuals  

**ODEs:**
```math
dI = -ka * I

dB = ka * I - ke * B

dU = ke * B
```

### Extended Model (With Liver)
- Adds a liver compartment: Intestine → Liver → Bloodstream → Urine  
- Absorption (ka), metabolism (km), and elimination (ke) vary per individual  
- Stochastic model using **Gillespie Algorithm**  
- Probabilistic transitions using **CTMC**  
- Population variability captured with **Monte Carlo simulations**  

---

## Techniques

### Gillespie Algorithm
- Simulates molecule-level stochastic events  
- Propensities:
  - Intestine → Liver: `a1 = ka * I`  
  - Liver → Bloodstream: `a2 = km * L`  
  - Bloodstream → Urine: `a3 = ke * B`  
- Time until next event: exponential distribution  
- Event selection: weighted random choice based on propensities  

### Continuous-Time Markov Chains (CTMC)
- Q-matrix defines transition rates between compartments  
- Forward Kolmogorov Equation: \(dp(t)/dt = p(t) \cdot Q\)  
- Probabilities computed numerically using `scipy.integrate.odeint`  
- Provides smooth, population-level trends  

### Monte Carlo Simulation
- Randomly samples ka, km, ke for N simulated patients  
- Computes drug concentration curves using **Gillespie dosing** or CTMC  
- Calculates Area Under the Curve (AUC) for each dosing strategy  
- Dosing strategies:
  - Single Dose: [0]  
  - BID (every 12h): [0, 12]  
  - QID (every 6h): [0, 6, 12, 18]  
  - High Front-Loading: [0, 1, 2, 3]  

---

## Implementation

- Python used for all simulations  
- Functions:
  - `gillespie_liver()` – Gillespie simulation with liver compartment  
  - `simulate_gillespie_no_liver()` – Gillespie simulation without liver  
  - `gillespie_dosing()` – Gillespie with dosing schedule  
  - `ctmc_liver()` – CTMC simulation with liver  
  - `ctmc_no_liver()` – CTMC without liver  
  - `ctmc_dosing()` – CTMC with dosing schedule  
  - `monte_carlo_auc()` – Monte Carlo simulation with AUC calculations  
- Plotting: `matplotlib` line plots and boxplots  
- Figures saved to `./figures/`  
- Parameters: max molecules = 100, time units arbitrary  

---

## Results and Analysis

### Liver Metabolism Effect
- Liver delays **Tmax** (time to peak) by 3–4 units vs 1–2 units without liver  
- Peak concentration (Cmax) lower with liver: 30–35 molecules vs 40 molecules without  
- Gillespie shows stochastic fluctuations; CTMC shows smooth population trends  

### Patient Variability
- Profiles:
  - **Fast Absorber** – early peak, risk of acute side effects  
  - **Fast Metaboliser** – peak drops quickly due to liver metabolism  
  - **Fast Eliminator** – lower peak concentration  
  - **Slow Everything** – gradual rise, prolonged presence  
  - **High Exposure** – high, sustained concentration, risk of toxicity  
- Variation significantly affects drug exposure; no single dosing strategy suits all  

### Dosing Strategy Analysis
- Single dose: lowest AUC, most predictable  
- BID & QID: moderate AUC, higher variability  
- High Front-Loading: highest AUC, highest variability and toxicity risk  
- Implication: **personalised dosing necessary for safety and efficacy**  

---

## Insights

- Liver metabolism reduces peak concentration (acts as a filter)  
- Population variability requires flexible dosing strategies  
- High front-loading or frequent dosing may be unsafe for slow metabolising patients  
- Gillespie captures stochastic effects; CTMC captures population averages  
- Monte Carlo effectively demonstrates risk across patient populations  

---

## Figures Generated

- `single_profile_comparison.png` – Gillespie vs CTMC (with and without liver)  
- `monte_carlo_auc_comparison.png` – Boxplots of AUC by dosing strategy  
- `all_profiles_with_liver.png` – All patient profiles simulated with liver  

---

## Future Improvements

- Include multi-drug interactions and combination therapies  
- Validate with real-world pharmacokinetic data  
- Extend to organ-level multi-compartment models  
- Develop interactive dashboards to explore dosing strategies  

---

## Key Concepts Highlighted

- Deterministic ODE modelling  
- Stochastic simulations (Gillespie)  
- Continuous-Time Markov Chains  
- Monte Carlo simulations for population variability  
- Compartmental modelling (Intestine, Liver, Bloodstream, Urine)  
- AUC calculations using trapezoidal numerical integration  
- Data visualisation for population-level insights  

---

## Usage

```bash
# Run all simulations and generate figures
python -m examples.run_simulations
