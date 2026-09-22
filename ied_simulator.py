from protection_decision import (
    phase_protection_decision,
    earth_fault_protection_decision
)


# ---------------------------------------------------------
# Trip Conditioning - PTRC1
# ---------------------------------------------------------

def process_trip(protection_result):

    if protection_result["status"] == "OPERATE":

        return {
            "logical_node": "PTRC1",
            "state": "TRIP",
            "input": protection_result["logical_node"]
        }

    return {
        "logical_node": "PTRC1",
        "state": "NO TRIP",
        "input": None
    }


# ---------------------------------------------------------
# Circuit Breaker - XCBR1
# ---------------------------------------------------------

def operate_breaker(trip_result):

    if trip_result["state"] == "TRIP":

        return {
            "logical_node": "XCBR1",
            "breaker_id": "CB-301",
            "command": "OPEN",
            "state": "OPEN"
        }

    return {
        "logical_node": "XCBR1",
        "breaker_id": "CB-301",
        "command": "NO COMMAND",
        "state": "CLOSED"
    }


# ---------------------------------------------------------
# Complete IED Simulation
# ---------------------------------------------------------

def simulate_ied(current_a, fault_type):

    print("\n")
    print("=" * 70)
    print("IED PROTECTION SIMULATION")
    print("=" * 70)

    print(f"Measured current: {current_a} A")
    print(f"Fault type: {fault_type}")

    # -----------------------------------------------------
    # MMXU1 - Measurement
    # -----------------------------------------------------

    measurement = {
        "logical_node": "MMXU1",
        "current_a": current_a
    }

    print("\nMMXU1 - Measurement")
    print(f"Current: {measurement['current_a']} A")

    # -----------------------------------------------------
    # Protection decision
    # -----------------------------------------------------

    if fault_type.strip().lower() == "phase-to-earth":

        protection_result = earth_fault_protection_decision(
            current_a
        )

    else:

        protection_result = phase_protection_decision(
            current_a
        )

    print("\nProtection Decision")

    print(
        f"Element: "
        f"{protection_result['element']}"
    )

    print(
        f"Logical Node: "
        f"{protection_result['logical_node']}"
    )

    print(
        f"Status: "
        f"{protection_result['status']}"
    )

    print(
        f"Reason: "
        f"{protection_result['reason']}"
    )

    if protection_result["operating_time_s"] is not None:

        print(
            f"Operating time: "
            f"{protection_result['operating_time_s']:.3f} s"
        )

    # -----------------------------------------------------
    # PTRC1 - Trip Conditioning
    # -----------------------------------------------------

    trip_result = process_trip(
        protection_result
    )

    print("\nPTRC1 - Trip Conditioning")

    print(
        f"State: "
        f"{trip_result['state']}"
    )

    if trip_result["input"]:

        print(
            f"Trip source: "
            f"{trip_result['input']}"
        )

    # -----------------------------------------------------
    # XCBR1 - Circuit Breaker
    # -----------------------------------------------------

    breaker_result = operate_breaker(
        trip_result
    )

    print("\nXCBR1 - Circuit Breaker")

    print(
        f"Breaker: "
        f"{breaker_result['breaker_id']}"
    )

    print(
        f"Command: "
        f"{breaker_result['command']}"
    )

    print(
        f"Final state: "
        f"{breaker_result['state']}"
    )

    print("=" * 70)

    return {
        "measurement": measurement,
        "protection": protection_result,
        "trip": trip_result,
        "breaker": breaker_result
    }


# ---------------------------------------------------------
# Demonstration cases
# ---------------------------------------------------------

if __name__ == "__main__":

    test_cases = [

        {
            "current": 850,
            "fault_type": "phase-to-phase"
        },

        {
            "current": 1500,
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
