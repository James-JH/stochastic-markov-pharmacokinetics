import numpy as np
from src.gillespie import gillespie_dosing
from src.ctmc import ctmc_dosing

def monte_carlo_auc(method, N, dosing_strategies):
    results = {key: [] for key in dosing_strategies}
    for _ in range(N):
        ka = max(np.random.normal(1.0, 0.2), 0.01)
        km = max(np.random.normal(0.5, 0.1), 0.01)
        ke = max(np.random.normal(0.7, 0.15), 0.01)

        for strategy, schedule in dosing_strategies.items():
            if method == "gillespie":
                t_vals, b_vals = gillespie_dosing(ka, km, ke, schedule)
            elif method == "ctmc":
                t_vals, b_vals = ctmc_dosing(ka, km, ke, schedule)
            else:
                continue
            if len(t_vals) > 1:
                auc = np.trapz(b_vals, t_vals)
                results[strategy].append(auc)
    return results
