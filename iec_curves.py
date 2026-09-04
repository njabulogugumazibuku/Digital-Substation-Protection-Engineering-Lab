from pathlib import Path

import matplotlib.pyplot as plt


IEC_CURVES = {
    "standard_inverse": {"k": 0.14, "alpha": 0.02},
    "very_inverse": {"k": 13.5, "alpha": 1.0},
    "extremely_inverse": {"k": 80.0, "alpha": 2.0},
}


def inverse_time(current_a, pickup_a, tms, curve="standard_inverse"):
    """Return IEC inverse-time operation, or ``None`` below pickup."""
    if current_a <= pickup_a:
        return None
    curve_data = IEC_CURVES[curve]
    multiple = current_a / pickup_a
    return tms * curve_data["k"] / (multiple ** curve_data["alpha"] - 1)


def run_coordination_study(output_path="05_coordination/tcc_coordination.png"):
    """Print coordination checks and save the time-current coordination plot."""
    feeder_pickup, feeder_tms = 1200, 0.10
    backup_pickup, backup_tms = 1320, 0.25
    currents = list(range(1300, 20001, 100))
    feeder_times = [inverse_time(current, feeder_pickup, feeder_tms) for current in currents]
    backup_times = [inverse_time(current, backup_pickup, backup_tms) for current in currents]

    print("\nProtection Coordination Check")
    print("--------------------------------")
    for current in [2000, 4000, 6000, 7000, 10000]:
        feeder_time = inverse_time(current, feeder_pickup, feeder_tms)
        backup_time = inverse_time(current, backup_pickup, backup_tms)
        print(f"\nFault Current: {current} A")
        print(f"Feeder 51 operating time: {feeder_time:.3f} s")
        print(f"Transformer backup 51 operating time: {backup_time:.3f} s")
        print(f"Coordination margin: {backup_time - feeder_time:.3f} s")

    plt.figure(figsize=(10, 7))
    plt.loglog(currents, feeder_times, label="Feeder 51 - Standard Inverse", linewidth=2)
    plt.loglog(currents, backup_times, label="Transformer Backup 51 - Standard Inverse", linewidth=2)
    plt.axvline(5000, color="red", linestyle="--", label="Feeder 50 Pickup (5000 A)")
    plt.axvline(backup_pickup, color="orange", linestyle=":", label="Transformer Backup Pickup (1320 A)")
    plt.xlabel("Fault Current (A)")
    plt.ylabel("Operating Time (s)")
    plt.title("Digital Substation Protection Coordination - TCC")
    plt.grid(which="both", linestyle="--", alpha=0.4)
    plt.legend()
    plt.xlim(1000, 20000)
    plt.ylim(0.01, 20)
    plt.tight_layout()
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=300)
    plt.show()


if __name__ == "__main__":
    run_coordination_study()
