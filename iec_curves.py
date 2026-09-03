import math
import matplotlib.pyplot as plt


# IEC standard inverse curve constants
IEC_CURVES = {
    "standard_inverse": {
        "k": 0.14,
        "alpha": 0.02
    },
    "very_inverse": {
        "k": 13.5,
        "alpha": 1.0
    },
    "extremely_inverse": {
        "k": 80.0,
        "alpha": 2.0
    }
}


def inverse_time(current_a, pickup_a, tms, curve="standard_inverse"):
    """
    Calculate IEC inverse-time operating time.

    t = TMS * k / ((I/Ip)^alpha - 1)

    current_a : fault current in amperes
    pickup_a  : protection pickup current in amperes
    tms       : time multiplier setting
    curve     : IEC curve type
    """

    if current_a <= pickup_a:
        return None

    k = IEC_CURVES[curve]["k"]
    alpha = IEC_CURVES[curve]["alpha"]

    multiple = current_a / pickup_a

    return tms * k / (multiple ** alpha - 1)


# ---------------------------------------------------------
# Protection settings for this portfolio study
# ---------------------------------------------------------

FEEDER_PICKUP = 1200
FEEDER_TMS = 0.10

TRANSFORMER_BACKUP_PICKUP = 1320
TRANSFORMER_BACKUP_TMS = 0.25

CURVE_TYPE = "standard_inverse"


# ---------------------------------------------------------
# Generate TCC data
# ---------------------------------------------------------

currents = []

current = 1300

while current <= 20000:
    currents.append(current)
    current += 100


feeder_times = []
transformer_backup_times = []

for current in currents:

    feeder_time = inverse_time(
        current,
        FEEDER_PICKUP,
        FEEDER_TMS,
        CURVE_TYPE
    )

    backup_time = inverse_time(
        current,
        TRANSFORMER_BACKUP_PICKUP,
        TRANSFORMER_BACKUP_TMS,
        CURVE_TYPE
    )

    feeder_times.append(feeder_time)
    transformer_backup_times.append(backup_time)


# ---------------------------------------------------------
# Print coordination checks
# ---------------------------------------------------------

test_currents = [2000, 4000, 6000, 7000, 10000]

print("\nProtection Coordination Check")
print("--------------------------------")

for current in test_currents:

    feeder_time = inverse_time(
        current,
        FEEDER_PICKUP,
        FEEDER_TMS,
        CURVE_TYPE
    )

    backup_time = inverse_time(
        current,
        TRANSFORMER_BACKUP_PICKUP,
        TRANSFORMER_BACKUP_TMS,
        CURVE_TYPE
    )

    print(f"\nFault Current: {current} A")

    if feeder_time:
        print(f"Feeder 51 operating time: {feeder_time:.3f} s")
    else:
        print("Feeder 51: Below pickup")

    if backup_time:
        print(
            f"Transformer backup 51 operating time: "
            f"{backup_time:.3f} s"
        )
    else:
        print("Transformer backup 51: Below pickup")

    if feeder_time and backup_time:

        margin = backup_time - feeder_time

        print(
            f"Coordination margin: "
            f"{margin:.3f} s"
        )


# ---------------------------------------------------------
# Plot TCC
# ---------------------------------------------------------

plt.figure(figsize=(10, 7))

plt.loglog(
    currents,
    feeder_times,
    label="Feeder 51 - Standard Inverse",
    linewidth=2
)

plt.loglog(
    currents,
    transformer_backup_times,
    label="Transformer Backup 51 - Standard Inverse",
    linewidth=2
)


# Feeder instantaneous protection threshold
plt.axvline(
    5000,
    color="red",
    linestyle="--",
    label="Feeder 50 Pickup (5000 A)"
)


# Transformer backup pickup
plt.axvline(
    TRANSFORMER_BACKUP_PICKUP,
    color="orange",
    linestyle=":",
    label="Transformer Backup Pickup (1320 A)"
)


plt.xlabel("Fault Current (A)")
plt.ylabel("Operating Time (s)")

plt.title(
    "Digital Substation Protection Coordination - TCC"
)

plt.grid(
    which="both",
    linestyle="--",
    alpha=0.4
)

plt.legend()

plt.xlim(1000, 20000)
plt.ylim(0.01, 20)

plt.tight_layout()

plt.savefig(
    "05_coordination/tcc_coordination.png",
    dpi=300
)

plt.show()