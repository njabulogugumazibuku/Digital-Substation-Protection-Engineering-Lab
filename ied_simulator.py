# ==========================================
# DIGITAL SUBSTATION PROTECTION ENGINEERING LAB
# Feeder Protection IED Simulator
# ==========================================

from ied_configuration import ied_configuration


def evaluate_phase_overcurrent(current_a):
    """
    Evaluate phase overcurrent protection.

    PTOC2 represents instantaneous 50 protection.
    PTOC1 represents time-delayed 51 protection.
    """

    ptoc1 = ied_configuration["logical_nodes"]["PTOC1"]
    ptoc2 = ied_configuration["logical_nodes"]["PTOC2"]

    if (
        ptoc2["enabled"]
        and current_a >= ptoc2["pickup_a"]
    ):

        return {
            "logical_node": "PTOC2",
            "function": ptoc2["function"],
            "state": "OPERATE",
            "delay_s": ptoc2["delay_s"]
        }

    if (
        ptoc1["enabled"]
        and current_a >= ptoc1["pickup_a"]
    ):

        return {
            "logical_node": "PTOC1",
            "function": ptoc1["function"],
            "state": "OPERATE",
            "delay_s": ptoc1["delay_s"]
        }

    return {
        "logical_node": "PTOC",
        "function": "Phase Overcurrent",
        "state": "NO OPERATE",
        "delay_s": None
    }


def evaluate_earth_fault(current_a):
    """
    Evaluate earth fault protection.

    PTEF2 represents instantaneous 50N protection.
    PTEF1 represents time-delayed 51N protection.
    """

    ptef1 = ied_configuration["logical_nodes"]["PTEF1"]
    ptef2 = ied_configuration["logical_nodes"]["PTEF2"]

    if (
        ptef2["enabled"]
        and current_a >= ptef2["pickup_a"]
    ):

        return {
            "logical_node": "PTEF2",
            "function": ptef2["function"],
            "state": "OPERATE",
            "delay_s": ptef2["delay_s"]
        }

    if (
        ptef1["enabled"]
        and current_a >= ptef1["pickup_a"]
    ):

        return {
            "logical_node": "PTEF1",
            "function": ptef1["function"],
            "state": "OPERATE",
            "delay_s": ptef1["delay_s"]
        }

    return {
        "logical_node": "PTEF",
        "function": "Earth Fault Protection",
        "state": "NO OPERATE",
        "delay_s": None
    }


def process_trip(protection_result):
    """
    Simulate PTRC1 trip conditioning.
    """

    if protection_result["state"] == "OPERATE":

        return {
            "logical_node": "PTRC1",
            "state": "TRIP",
            "input": protection_result["logical_node"]
        }

    return {
        "logical_node": "PTRC1",
        "state": "NO TRIP",
        "input": protection_result["logical_node"]
    }


def operate_breaker(trip_result):
    """
    Simulate XCBR1 circuit breaker operation.
    """

    breaker = ied_configuration["logical_nodes"]["XCBR1"]

    if trip_result["state"] == "TRIP":

        return {
            "logical_node": "XCBR1",
            "breaker_id": breaker["breaker_id"],
            "command": "OPEN",
            "state": "OPEN"
        }

    return {
        "logical_node": "XCBR1",
        "breaker_id": breaker["breaker_id"],
        "command": "NONE",
        "state": breaker["normal_state"]
    }


def simulate_ied(current_a, fault_type):
    """
    Run a fault condition through the simulated IED.
    """

    print("=" * 60)
    print("FEEDER PROTECTION IED SIMULATION")
    print("=" * 60)

    print(f"\nMeasured Current: {current_a} A")
    print(f"Fault Type: {fault_type}")

    # ------------------------------------------
    # Select protection function
    # ------------------------------------------

    if fault_type == "Phase-to-Phase":

        protection_result = (
            evaluate_phase_overcurrent(current_a)
        )

    elif fault_type == "Phase-to-Earth":

        protection_result = (
            evaluate_earth_fault(current_a)
        )

    else:

        protection_result = {
            "logical_node": "NONE",
            "function": "No Protection Function Selected",
            "state": "NO OPERATE",
            "delay_s": None
        }

    # ------------------------------------------
    # Display protection decision
    # ------------------------------------------

    print("\nPROTECTION ELEMENT")

    print(
        f"Logical Node: "
        f"{protection_result['logical_node']}"
    )

    print(
        f"Function: "
        f"{protection_result['function']}"
    )

    print(
        f"State: "
        f"{protection_result['state']}"
    )

    if protection_result["delay_s"] is not None:

        print(
            f"Operating Delay: "
            f"{protection_result['delay_s']} s"
        )

    # ------------------------------------------
    # Trip conditioning
    # ------------------------------------------

    trip_result = process_trip(
        protection_result
    )

    print("\nTRIP CONDITIONING")

    print(
        f"Logical Node: "
        f"{trip_result['logical_node']}"
    )

    print(
        f"State: "
        f"{trip_result['state']}"
    )

    print(
        f"Input: "
        f"{trip_result['input']}"
    )

    # ------------------------------------------
    # Circuit breaker
    # ------------------------------------------

    breaker_result = operate_breaker(
        trip_result
    )

    print("\nCIRCUIT BREAKER")

    print(
        f"Logical Node: "
        f"{breaker_result['logical_node']}"
    )

    print(
        f"Breaker: "
        f"{breaker_result['breaker_id']}"
    )

    print(
        f"Command: "
        f"{breaker_result['command']}"
    )

    print(
        f"State: "
        f"{breaker_result['state']}"
    )

    print("\n" + "=" * 60)

    return {
        "protection": protection_result,
        "trip": trip_result,
        "breaker": breaker_result
    }


# ==========================================
# TEST CASES
# ==========================================

if __name__ == "__main__":

    # Test 1:
    # High phase fault current

    simulate_ied(
        current_a=6000,
        fault_type="Phase-to-Phase"
    )

    # Test 2:
    # Lower magnitude phase fault

    simulate_ied(
        current_a=2000,
        fault_type="Phase-to-Phase"
    )

    # Test 3:
    # Earth fault

    simulate_ied(
        current_a=2500,
        fault_type="Phase-to-Earth"
    )

    # Test 4:
    # Normal current

    simulate_ied(
        current_a=850,
        fault_type="Phase-to-Phase"
    )
