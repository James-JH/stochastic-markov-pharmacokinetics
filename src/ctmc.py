import numpy as np
from scipy.integrate import odeint

def CTMC_Q_liver(ka, km, ke):
    return np.array([
        [-ka, ka, 0, 0],
        [0, -km, km, 0],
        [0, 0, -ke, ke],
        [0, 0, 0, 0]
    ])

def CTMC_Q_no_liver(ka, ke):
    return np.array([
        [-ka, ka, 0, 0],
        [0, -ke, ke, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])

def forward_eqs(p, t, Q):
    return p @ Q

def ctmc_liver(k_a, k_m, k_e, t_end=10, num_points=200):
    Q = CTMC_Q_liver(k_a, k_m, k_e)
    p0 = [1, 0, 0, 0]
    t_ctmc = np.linspace(0, t_end, num_points)
    ps = odeint(forward_eqs, p0, t_ctmc, args=(Q,))
    blood_prob = ps[:, 2]
    return t_ctmc, blood_prob

def ctmc_no_liver(k_a, k_e, t_end=10, num_points=200):
    Q = CTMC_Q_no_liver(k_a, k_e)
    p0 = [1, 0, 0, 0]
    t_ctmc = np.linspace(0, t_end, num_points)
    ps = odeint(forward_eqs, p0, t_ctmc, args=(Q,))
    blood_prob = ps[:, 1]
    return t_ctmc, blood_prob

def ctmc_dosing(ka, km, ke, dosing_schedule, dose_amount=1.0, sim_time=24, num_points=200):
    t = np.linspace(0, sim_time, num_points)
    dt = t[1] - t[0]
    Q = CTMC_Q_liver(ka, km, ke)
    ps = np.zeros((len(t), 4))
    p = np.array([0.0, 0.0, 0.0, 0.0])
    ps[0] = p
    dose_index = 0

    for i in range(1, len(t)):
        if dose_index < len(dosing_schedule) and t[i] >= dosing_schedule[dose_index]:
            p[0] += dose_amount
            dose_index += 1
        p += dt * forward_eqs(p, t[i], Q)
        ps[i] = p

    blood_probs = ps[:, 2]
    return t, blood_probs
