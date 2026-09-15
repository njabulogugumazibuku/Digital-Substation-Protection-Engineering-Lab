import os
import sys


# ---------------------------------------------------------
# Import protection decision functions
# ---------------------------------------------------------

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "04_protection_logic"
        )
    )
)

from protection_decision import (
    phase_protection_decision,
    earth_fault_protection_decision
)


# ---------------------------------------------------------
# Protection sequence simulation
# ---------------------------------------------------------

def simulate_feeder_fault(
    current_a,
    fault_type,
    breaker_failure=False
):
    """
    Simulate a feeder fault from detection through
    primary protection, breaker operation and,
    where applicable, breaker-failure backup.

    This is a simplified educational model.
    """

    print("\n")
    print("=" * 70)
    print("FEEDER PROTECTION SEQUENCE")
    print("=" * 70)

    print(f"Fault current: {current_a} A")
    print(f"Fault type: {fault_type}")

    # -----------------------------------------------------
    # Step 1 - Fault detection
    # -----------------------------------------------------

    print("\n[1] FAULT DETECTION")

    print(
        f"Protection IED detects "
        f"{current_a} A fault current."
    )

    # -----------------------------------------------------
    # Step 2 - Protection decision
    # -----------------------------------------------------

    print("\n[2] PRIMARY PROTECTION")

    if fault_type == "phase-to-earth":

        protection_result = earth_fault_protection_decision(
            current_a
        )

    else:

        protection_result = phase_protection_decision(
            current_a
        )

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

    operating_time = (
        protection_result["operating_time_s"]
    )

    if operating_time is not None:

        print(
            f"Operating time: "
            f"{operating_time:.3f} s"
        )

    # -----------------------------------------------------
    # Step 3 - No protection operation
    # -----------------------------------------------------

    if protection_result["status"] == "NO OPERATE":

        print("\n[3] NO TRIP")

        print(
            "Fault current is below "
            "protection pickup."
        )

        return {
            "primary_operated": False,
            "breaker_open": False,
            "breaker_failure": False,
            "backup_operated": False
        }

    # -----------------------------------------------------
    # Step 4 - Trip command
    # -----------------------------------------------------

    print("\n[3] TRIP COMMAND")

    print(
        "PTRC1 issues a trip command "
        "to feeder breaker CB-301."
    )

    # -----------------------------------------------------
    # Step 5 - Breaker operation
    # -----------------------------------------------------

    print("\n[4] CIRCUIT BREAKER RESPONSE")

    if not breaker_failure:

        print("CB-301 receives trip command.")

        print("CB-301 opens successfully.")

        print("Fault is cleared.")

        return {
            "primary_operated": True,
            "breaker_open": True,
            "breaker_failure": False,
            "backup_operated": False
        }

    # -----------------------------------------------------
    # Step 6 - Breaker failure
    # -----------------------------------------------------

    print("CB-301 receives trip command.")

    print("CB-301 FAILS TO OPEN.")

    print(
        "Fault current remains present."
    )

    # -----------------------------------------------------
    # Step 7 - Breaker failure protection
    # -----------------------------------------------------

    print("\n[5] BREAKER FAILURE PROTECTION")

    print(
        "50BF timer starts."
    )

    breaker_failure_timer = 0.30

    print(
        f"Breaker failure timer: "
        f"{breaker_failure_timer:.3f} s"
    )

    print(
        "50BF operates after timer expiry."
    )

    # -----------------------------------------------------
    # Step 8 - Backup trip
    # -----------------------------------------------------

    print("\n[6] BACKUP TRIP")

    print(
        "Backup trip command issued "
        "to transformer-side breaker CB-201."
    )

    print("CB-201 opens.")

    print(
        "Fault is isolated from the "
        "upstream transformer connection."
    )

    return {
        "primary_operated": True,
        "breaker_open": False,
        "breaker_failure": True,
        "backup_operated": True
    }


# ---------------------------------------------------------
# Demonstration scenarios
# ---------------------------------------------------------

if __name__ == "__main__":

    # -----------------------------------------------------
    # Scenario 1 - Normal primary clearing
    # -----------------------------------------------------

    simulate_feeder_fault(
        current_a=2000,
        fault_type="phase-to-phase",
        breaker_failure=False
    )

    # -----------------------------------------------------
    # Scenario 2 - Breaker failure
    # -----------------------------------------------------

    simulate_feeder_fault(
        current_a=6000,
        fault_type="phase-to-phase",
        breaker_failure=True
    )

    # -----------------------------------------------------
    # Scenario 3 - Earth fault with breaker failure
    # -----------------------------------------------------

    simulate_feeder_fault(
        current_a=1500,
        fault_type="phase-to-earth",
        breaker_failure=True
    )