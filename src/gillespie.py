import numpy as np

# Gillespie with liver compartment
def gillespie_liver(k_a, k_m, k_e, max_molecules=100):
    I, L, B, U = [max_molecules], [0], [0], [0]
    t = [0]
    times, blood_levels = [], []

    while I[-1] > 0 or L[-1] > 0 or B[-1] > 0:
        a1 = k_a * I[-1]
        a2 = k_m * L[-1]
        a3 = k_e * B[-1]
        a0 = a1 + a2 + a3
        if a0 == 0:
            break

        dt = np.random.exponential(1 / a0)
        r = np.random.uniform(0, a0)

        if r < a1 and I[-1] > 0:
            I.append(I[-1]-1); L.append(L[-1]+1); B.append(B[-1]); U.append(U[-1])
        elif r < a1 + a2 and L[-1] > 0:
            I.append(I[-1]); L.append(L[-1]-1); B.append(B[-1]+1); U.append(U[-1])
        elif B[-1] > 0:
            I.append(I[-1]); L.append(L[-1]); B.append(B[-1]-1); U.append(U[-1]+1)

        t.append(t[-1]+dt)
        times.append(t[-1])
        blood_levels.append(B[-1])

    return np.array(times), np.array(blood_levels)

# Gillespie with no liver compartment
def simulate_gillespie_no_liver(k_a, k_e, max_molecules=100):
    I, B, U = [max_molecules], [0], [0]
    t = [0]
    times, blood_levels = [], []

    while I[-1] > 0 or B[-1] > 0:
        a1 = k_a * I[-1]
        a2 = k_e * B[-1]
        a0 = a1 + a2
        if a0 == 0:
            break

        dt = np.random.exponential(1 / a0)
        r = np.random.uniform(0, a0)

        if r < a1 and I[-1] > 0:
            I.append(I[-1]-1); B.append(B[-1]+1); U.append(U[-1])
        elif B[-1] > 0:
            I.append(I[-1]); B.append(B[-1]-1); U.append(U[-1]+1)

        t.append(t[-1]+dt)
        times.append(t[-1])
        blood_levels.append(B[-1])

    return np.array(times), np.array(blood_levels)

def gillespie_dosing(
    ka,
    km,
    ke,
    dosing_schedule,
    dose_amount=100,
    sim_time=24.0
):
    # Compartments
    I = [0]   # Intestine
    L = [0]   # Liver
    B = [0]   # Blood
    U = [0]   # Eliminated

    t = [0.0]
    times = []
    blood_levels = []

    dosing_schedule = sorted(dosing_schedule)
    next_dose_index = 0

    while t[-1] < sim_time:

        # Propensities
        a1 = ka * I[-1]
        a2 = km * L[-1]
        a3 = ke * B[-1]
        a0 = a1 + a2 + a3

        # If no reactions left, just fast-forward dosing
        if a0 == 0:
            if next_dose_index < len(dosing_schedule):
                t.append(dosing_schedule[next_dose_index])
                I.append(I[-1] + dose_amount)
                L.append(L[-1])
                B.append(B[-1])
                U.append(U[-1])
                next_dose_index += 1
                continue
            else:
                break

        # Time to next reaction
        dt = np.random.exponential(1 / a0)
        t_next = t[-1] + dt

        # Check if next dose happens before next reaction
        if (
            next_dose_index < len(dosing_schedule)
            and dosing_schedule[next_dose_index] <= t_next
        ):
            # Process dose first
            t.append(dosing_schedule[next_dose_index])
            I.append(I[-1] + dose_amount)
            L.append(L[-1])
            B.append(B[-1])
            U.append(U[-1])
            next_dose_index += 1
            continue

        # Otherwise, process reaction
        r = np.random.uniform(0, a0)

        if r < a1:
            I.append(I[-1] - 1)
            L.append(L[-1] + 1)
            B.append(B[-1])
            U.append(U[-1])
        elif r < a1 + a2:
            I.append(I[-1])
            L.append(L[-1] - 1)
            B.append(B[-1] + 1)
            U.append(U[-1])
        else:
            I.append(I[-1])
            L.append(L[-1])
            B.append(B[-1] - 1)
            U.append(U[-1] + 1)

        t.append(t_next)

        times.append(t[-1])
        blood_levels.append(B[-1])

    return np.array(times), np.array(blood_levels)