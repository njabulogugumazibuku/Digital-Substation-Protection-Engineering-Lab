import os
import sys

# ---------------------------------------------------------
# Import IED configuration
# ---------------------------------------------------------

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "03_ied_configuration")
    )
)

from ied_configuration import ied_configuration


# ---------------------------------------------------------
# Import IEC inverse-time calculation
# ---------------------------------------------------------

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "05_coordination")
    )
)

from iec_curves import inverse_time


# ---------------------------------------------------------
# Phase Overcurrent Protection
# ---------------------------------------------------------

def evaluate_phase_overcurrent(current_a):

    phase_config = ied_configuration[
        "logical_devices"
    ]["LD_PROTECTION"]["logical_nodes"]

    instantaneous = phase_config["PTOC2"]
    time_overcurrent = phase_config["PTOC1"]

    # -----------------------------------------------------
    # 50 Instantaneous Overcurrent
    # -----------------------------------------------------

    if current_a >= instantaneous["pickup_a"]:

        return {
            "logical_node": "PTOC2",
            "function": "50",
            "status": "OPERATE",
            "operating_time_s": instantaneous["delay_s"]
        }

    # -----------------------------------------------------
    # 51 Time Overcurrent
    # -----------------------------------------------------

    if current_a >= time_overcurrent["pickup_a"]:

        operating_time = inverse_time(
            current_a=current_a,
            pickup_a=time_overcurrent["pickup_a"],
            tms=0.10,
            curve="standard_inverse"
        )

        return {
            "logical_node": "PTOC1",
            "function": "51",
            "status": "OPERATE",
            "operating_time_s": operating_time
        }

    # -----------------------------------------------------
    # No Operation
    # -----------------------------------------------------

    return {
        "logical_node": "PTOC",
        "function": "50/51",
        "status": "NO OPERATE",
        "operating_time_s": None
    }


# ---------------------------------------------------------
# Earth Fault Protection
# ---------------------------------------------------------

def evaluate_earth_fault(current_a):

    phase_config = ied_configuration[
        "logical_devices"
    ]["LD_PROTECTION"]["logical_nodes"]

    instantaneous = phase_config["PTEF2"]
    time_overcurrent = phase_config["PTEF1"]

    # -----------------------------------------------------
    # 50N Instantaneous Earth Fault
    # -----------------------------------------------------

    if current_a >= instantaneous["pickup_a"]:

        return {
            "logical_node": "PTEF2",
            "function": "50N",
            "status": "OPERATE",
            "operating_time_s": instantaneous["delay_s"]
        }

    # -----------------------------------------------------
    # 51N Time Earth Fault
    # -----------------------------------------------------

    if current_a >= time_overcurrent["pickup_a"]:

        return {
            "logical_node": "PTEF1",
            "function": "51N",
            "status": "OPERATE",
            "operating_time_s": time_overcurrent["delay_s"]
        }

    # -----------------------------------------------------
    # No Operation
    # -----------------------------------------------------

    return {
        "logical_node": "PTEF",
        "function": "50N/51N",
        "status": "NO OPERATE",
        "operating_time_s": None
    }


# ---------------------------------------------------------
# Trip Conditioning - PTRC1
# ---------------------------------------------------------

def process_trip(protection_result):

    if protection_result["status"] == "OPERATE":

        return {
            "logical_node": "PTRC1",
            "status": "TRIP",
            "source_protection": protection_result["logical_node"]
        }

    return {
        "logical_node": "PTRC1",
        "status": "NO TRIP",
        "source_protection": None
    }


# ---------------------------------------------------------
# Circuit Breaker - XCBR1
# ---------------------------------------------------------

def operate_breaker(trip_result):

    if trip_result["status"] == "TRIP":

        return {
            "logical_node": "XCBR1",
            "breaker": "CB-301",
            "state": "OPEN"
        }

    return {
        "logical_node": "XCBR1",
        "breaker": "CB-301",
        "state": "CLOSED"
    }


# ---------------------------------------------------------
# Complete IED Simulation
# ---------------------------------------------------------

def simulate_ied(current_a, fault_type):

    print("\n----------------------------------------")
    print("IED PROTECTION SIMULATION")
    print("----------------------------------------")

    print(f"Fault current: {current_a} A")
    print(f"Fault type: {fault_type}")

    # -----------------------------------------------------
    # Measurement
    # -----------------------------------------------------

    print("\nMMXU1 - Measurement")
    print(f"Measured current: {current_a} A")

    # -----------------------------------------------------
    # Protection evaluation
    # -----------------------------------------------------

    if fault_type == "phase-to-earth":

        protection_result = evaluate_earth_fault(current_a)

    else:

        protection_result = evaluate_phase_overcurrent(current_a)

    print("\nProtection Element")
    print(
        f"Logical Node: "
        f"{protection_result['logical_node']}"
    )

    print(
        f"Function: "
        f"{protection_result['function']}"
    )

    print(
        f"Status: "
        f"{protection_result['status']}"
    )

    if protection_result["operating_time_s"] is not None:

        print(
            f"Operating time: "
            f"{protection_result['operating_time_s']:.3f} s"
        )

    # -----------------------------------------------------
    # Trip conditioning
    # -----------------------------------------------------

    trip_result = process_trip(protection_result)

    print("\nPTRC1 - Trip Conditioning")
    print(f"Trip status: {trip_result['status']}")

    # -----------------------------------------------------
    # Breaker operation
    # -----------------------------------------------------

    breaker_result = operate_breaker(trip_result)

    print("\nXCBR1 - Circuit Breaker")
    print(
        f"Breaker: "
        f"{breaker_result['breaker']}"
    )

    print(
        f"Final state: "
        f"{breaker_result['state']}"
    )

    print("----------------------------------------")

    return {
        "measurement": current_a,
        "protection": protection_result,
        "trip": trip_result,
        "breaker": breaker_result
    }


# ---------------------------------------------------------
# Test the IED
# ---------------------------------------------------------

if __name__ == "__main__":

    test_cases = [
        {
            "current": 850,
            "fault_type": "phase-to-phase"
        },
        {
            "current": 2000,
            "fault_type": "phase-to-phase"
        },
        {
            "current": 6000,
            "fault_type": "phase-to-phase"
        },
        {
            "current": 1500,
            "fault_type": "phase-to-earth"
        },
        {
            "current": 3500,
            "fault_type": "phase-to-earth"
        }
    ]

    for test in test_cases:

        simulate_ied(
            current_a=test["current"],
            fault_type=test["fault_type"]
        )