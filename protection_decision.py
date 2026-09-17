import sys
from pathlib import Path

# ---------------------------------------------------------
# Import protection settings
# ---------------------------------------------------------

sys.path.append(
    str(Path(__file__).resolve().parent / "02_protection_study")
)

from protection_settings import protection_settings


from iec_curves import inverse_time


# ---------------------------------------------------------
# Phase protection decision
# ---------------------------------------------------------

def phase_protection_decision(current_a):
    """
    Determine which phase overcurrent element governs.

    Protection hierarchy:

        Below 51 pickup
            -> No operation

        Above 51 pickup but below 50 pickup
            -> 51 inverse-time

        Above 50 pickup
            -> 50 instantaneous
    """

    settings = protection_settings["feeder_phase_overcurrent"]

    instantaneous_pickup = settings["instantaneous_pickup_a"]
    time_pickup = settings["time_pickup_a"]
    tms = settings.get("tms", 0.10)

    # -----------------------------------------------------
    # 50 Instantaneous
    # -----------------------------------------------------

    if current_a >= instantaneous_pickup:

        return {
            "element": "50",
            "logical_node": "PTOC2",
            "status": "OPERATE",
            "operating_time_s": 0.05,
            "reason": "Current exceeds instantaneous pickup"
        }

    # -----------------------------------------------------
    # 51 Inverse-Time
    # -----------------------------------------------------

    if current_a >= time_pickup:

        operating_time = inverse_time(
            current_a=current_a,
            pickup_a=time_pickup,
            tms=tms,
            curve="standard_inverse"
        )

        return {
            "element": "51",
            "logical_node": "PTOC1",
            "status": "OPERATE",
            "operating_time_s": operating_time,
            "reason": "Current exceeds time-overcurrent pickup"
        }

    # -----------------------------------------------------
    # No Operation
    # -----------------------------------------------------

    return {
        "element": "NONE",
        "logical_node": "PTOC",
        "status": "NO OPERATE",
        "operating_time_s": None,
        "reason": "Current below protection pickup"
    }


# ---------------------------------------------------------
# Earth-fault protection decision
# ---------------------------------------------------------

def earth_fault_protection_decision(current_a):
    """
    Determine earth-fault protection operation for a feeder.

    50N = instantaneous earth-fault overcurrent
    51N = time-delayed inverse earth-fault overcurrent
    """

    settings = protection_settings["feeder_earth_fault"]

    # Instantaneous earth-fault protection
    if current_a >= settings["instantaneous_pickup_a"]:
        return {
            "logical_node": "PTEF2",
            "function": "50N Earth Fault",
            "state": "OPERATE",
            "delay_s": 0.05,
            "reason": "Current exceeds instantaneous earth-fault pickup"
        }

    # Time-delayed inverse earth-fault protection
    elif current_a > settings["time_pickup_a"]:
        operating_time = inverse_time(
            current_a=current_a,
            pickup_a=settings["time_pickup_a"],
            tms=settings["tms"],
            curve="standard_inverse"
        )

        return {
            "logical_node": "PTEF1",
            "function": "51N Earth Fault",
            "state": "OPERATE",
            "delay_s": operating_time,
            "reason": "Current exceeds 51N pickup; IEC inverse-time operation"
        }

    # Below pickup
    else:
        return {
            "logical_node": "PTEF1",
            "function": "51N Earth Fault",
            "state": "NO OPERATE",
            "delay_s": None,
            "reason": "Current below earth-fault pickup"
        }


# ---------------------------------------------------------
# Display test decisions
# ---------------------------------------------------------

def run_decision_examples():

    print("\n")
    print("=" * 70)
    print("PROTECTION DECISION HIERARCHY")
    print("=" * 70)

    phase_currents = [
        400,
        1200,
        1500,
        2000,
        4000,
        5000,
        6000,
        10000
    ]

    print("\nPHASE OVERCURRENT")
    print("-" * 70)

    for current in phase_currents:

        result = phase_protection_decision(current)

        time = result["operating_time_s"]

        if time is not None:
            time_text = f"{time:.3f} s"
        else:
            time_text = "N/A"

        print(
            f"{current:>6} A | "
            f"{result['element']:<4} | "
            f"{result['status']:<10} | "
            f"{time_text}"
        )

    earth_currents = [
        400,
        600,
        1000,
        1500,
        2500,
        3000,
        3500
    ]

    print("\nEARTH FAULT")
    print("-" * 70)

    for current in earth_currents:

        result = earth_fault_protection_decision(current)

        time = result["operating_time_s"]

        if time is not None:
            time_text = f"{time:.3f} s"
        else:
            time_text = "N/A"

        print(
            f"{current:>6} A | "
            f"{result['element']:<4} | "
            f"{result['status']:<10} | "
            f"{time_text}"
        )

    print("=" * 70)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    run_decision_examples()
