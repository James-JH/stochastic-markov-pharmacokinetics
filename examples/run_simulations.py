from src.gillespie import (
    gillespie_liver,
    simulate_gillespie_no_liver,
    gillespie_dosing
)
from src.ctmc import ctmc_liver, ctmc_no_liver, ctmc_dosing
import matplotlib.pyplot as plt
import numpy as np
import os

# ==============================
# Setup figures directory
# ==============================
FIG_DIR = "figures"
os.makedirs(FIG_DIR, exist_ok=True)

max_molecules = 100
ka, km, ke = 1.0, 0.5, 0.7

# ==============================
# Single profile simulations
# ==============================
t_gil_wl, b_gil_wl = gillespie_liver(ka, km, ke, max_molecules)
t_gil_nl, b_gil_nl = simulate_gillespie_no_liver(ka, ke, max_molecules)
t_ctmc_wl, b_ctmc_wl = ctmc_liver(ka, km, ke)
t_ctmc_nl, b_ctmc_nl = ctmc_no_liver(ka, ke)

plt.figure(figsize=(10, 3.5))

plt.subplot(1, 2, 1)
plt.plot(t_gil_wl, b_gil_wl, label="Gillespie With Liver")
plt.plot(t_gil_nl, b_gil_nl, label="Gillespie No Liver")
plt.title("Gillespie: With Liver vs No Liver")
plt.xlabel("Time")
plt.ylabel("Bloodstream Molecules")
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(t_ctmc_wl, b_ctmc_wl, label="CTMC With Liver")
plt.plot(t_ctmc_nl, b_ctmc_nl, label="CTMC No Liver")
plt.title("CTMC: With Liver vs No Liver")
plt.xlabel("Time")
plt.ylabel("Bloodstream Probability")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig(
    os.path.join(FIG_DIR, "single_profile_comparison.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.close()

# ==============================
# Monte Carlo / AUC simulation
# ==============================
dosing_strategies = {
    "QID (Every 6h)": [0, 6, 12, 18],
    "BID (Every 12h)": [0, 12],
    "Single Dose": [0],
    "High Front-Loading": [0, 1, 2, 3]
}

def monte_carlo_auc(method, N, dosing_strategies):
    results = {key: [] for key in dosing_strategies}

    for _ in range(N):
        ka = max(np.random.normal(1.0, 0.2), 0.01)
        km = max(np.random.normal(0.5, 0.1), 0.01)
        ke = max(np.random.normal(0.7, 0.15), 0.01)

        for strategy, schedule in dosing_strategies.items():

            if method == "gillespie":
                t_vals, b_vals = gillespie_dosing(
                    ka,
                    km,
                    ke,
                    schedule,
                    dose_amount=max_molecules,
                    sim_time=24.0
                )

            elif method == "ctmc":
                t_vals, b_vals = ctmc_dosing(
                    ka,
                    km,
                    ke,
                    schedule
                )

            else:
                continue

            if len(t_vals) > 1:
                auc = np.trapz(b_vals, t_vals)
                results[strategy].append(auc)

    return results

N = 300
auc_gillespie = monte_carlo_auc("gillespie", N, dosing_strategies)
auc_ctmc = monte_carlo_auc("ctmc", N, dosing_strategies)

plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.boxplot(
    [auc_gillespie[strat] for strat in dosing_strategies],
    tick_labels=list(dosing_strategies.keys())
)
plt.title("Monte Carlo AUCs – Gillespie")
plt.ylabel("AUC")
plt.xticks(rotation=45)
plt.grid(True)

plt.subplot(1, 2, 2)
plt.boxplot(
    [auc_ctmc[strat] for strat in dosing_strategies],
    tick_labels=list(dosing_strategies.keys())
)
plt.title("Monte Carlo AUCs – CTMC")
plt.ylabel("AUC")
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.savefig(
    os.path.join(FIG_DIR, "monte_carlo_auc_comparison.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.close()

# ==============================
# All Profiles With Liver
# ==============================
profiles = [
    {"name": "Baseline",        "ka": 1.0, "km": 0.5, "ke": 0.7},
    {"name": "Fast Absorber",   "ka": 1.5, "km": 0.5, "ke": 0.7},
    {"name": "Fast Metaboliser","ka": 1.0, "km": 1.0, "ke": 0.7},
    {"name": "Fast Eliminator", "ka": 1.0, "km": 0.5, "ke": 1.2},
    {"name": "Slow Everything", "ka": 0.5, "km": 0.3, "ke": 0.4},
    {"name": "High Exposure",   "ka": 1.2, "km": 0.4, "ke": 0.3}
]

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
for p in profiles:
    t_gil, b_gil = gillespie_liver(
        p["ka"], p["km"], p["ke"], max_molecules
    )
    plt.plot(t_gil, b_gil, label=p["name"])
plt.title("Gillespie With Liver – All Profiles")
plt.xlabel("Time")
plt.ylabel("Bloodstream Molecules")
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
for p in profiles:
    t_ctmc, b_ctmc = ctmc_liver(
        p["ka"], p["km"], p["ke"]
    )
    plt.plot(t_ctmc, b_ctmc, label=p["name"])
plt.title("CTMC With Liver – All Profiles")
plt.xlabel("Time")
plt.ylabel("Bloodstream Probability")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig(
    os.path.join(FIG_DIR, "all_profiles_with_liver.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.close()

print("All simulations complete.")
print("Figures saved to ./figures/")
