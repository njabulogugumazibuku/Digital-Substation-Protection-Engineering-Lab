import os
import sys


# ---------------------------------------------------------
# Import protection decision functions
# ---------------------------------------------------------

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "02_protection_study"
        )
    )
)

from protection_decision import (
    phase_protection_decision,
    earth_fault_protection_decision
)
from protection_settings import protection_settings


def run_feeder_protection_sequence(
    current_a,
    fault_type,
    breaker_failure=False
):
    """
    Simulate the protection sequence for a feeder fault.

    fault_type:
        "phase-to-phase"
        "phase-to-earth"

    breaker_failure:
        False = feeder breaker successfully opens
        True  = feeder breaker fails and backup protection operates
    """

    print("=" * 70)
    print("DIGITAL SUBSTATION PROTECTION SEQUENCE")
    print("=" * 70)

    print(f"Fault Current : {current_a} A")
    print(f"Fault Type    : {fault_type}")
    print(f"Breaker Fail  : {breaker_failure}")
    print()

    # ---------------------------------------------------------
    # STEP 1 — FAULT DETECTION
    # ---------------------------------------------------------

    print("STEP 1 - FAULT DETECTION")
    print("-" * 70)
    print(f"MMXU1 detects current = {current_a} A")
    print("Fault condition detected")
    print()

    # ---------------------------------------------------------
    # STEP 2 — PRIMARY PROTECTION
    # ---------------------------------------------------------

    print("STEP 2 - PRIMARY PROTECTION")
    print("-" * 70)

    if fault_type == "phase-to-earth":
        protection = earth_fault_protection_decision(current_a)
    else:
        protection = phase_protection_decision(current_a)

    print(f"Logical Node : {protection['logical_node']}")
    print(f"Function     : {protection['element']}")
    print(f"State        : {protection['status']}")

    if protection["operating_time_s"] is not None:
        print(f"Operating Time: {protection['operating_time_s']:.3f} s")

    print()

    # ---------------------------------------------------------
    # STEP 3 — TRIP DECISION
    # ---------------------------------------------------------

    print("STEP 3 - TRIP DECISION")
    print("-" * 70)

    if protection["status"] != "OPERATE":

        print("Protection does not operate")
        print("No trip command issued")
        return

    print("Protection operates")
    print("PTRC1 receives trip signal")
    print("PTRC1 issues trip command to XCBR1")
    print()

    # ---------------------------------------------------------
    # STEP 4 — BREAKER RESPONSE
    # ---------------------------------------------------------

    print("STEP 4 - BREAKER RESPONSE")
    print("-" * 70)

    if not breaker_failure:

        print("XCBR1 receives trip command")
        print("CB-301 opens")
        print("Fault cleared by primary protection")
        print()

        print("FINAL RESULT")
        print("-" * 70)
        print("PRIMARY PROTECTION SUCCESS")
        print("CB-301 OPEN")
        print("FAULT CLEARED")

        return

    # ---------------------------------------------------------
    # STEP 5 — BREAKER FAILURE
    # ---------------------------------------------------------

    print("XCBR1 receives trip command")
    print("CB-301 FAILS TO OPEN")
    print()

    print("STEP 5 - BREAKER FAILURE PROTECTION")
    print("-" * 70)

    breaker_failure_timer = protection_settings[
        "breaker_failure"
    ]["failure_timer_s"]

    print("50BF detects breaker failure")
    print(f"Breaker failure timer = {breaker_failure_timer:.3f} s")
    print("Timer expires")
    print()

    # ---------------------------------------------------------
    # STEP 6 — BACKUP TRIP
    # ---------------------------------------------------------

    print("STEP 6 - BACKUP PROTECTION")
    print("-" * 70)

    print("Backup trip command issued")
    print("CB-201 opens")
    print("Fault isolated from transformer LV side")
    print()

    print("FINAL RESULT")
    print("-" * 70)
    print("BREAKER FAILURE SEQUENCE SUCCESS")
    print("CB-301 FAILED")
    print("50BF OPERATED")
    print("CB-201 OPEN")
    print("FAULT ISOLATED")


if __name__ == "__main__":

    print("\nTEST 1 - PHASE FAULT\n")

    run_feeder_protection_sequence(
        current_a=2000,
        fault_type="phase-to-phase",
        breaker_failure=False
    )

    print("\n\nTEST 2 - PHASE FAULT + BREAKER FAILURE\n")

    run_feeder_protection_sequence(
        current_a=6000,
        fault_type="phase-to-phase",
        breaker_failure=True
    )

    print("\n\nTEST 3 - EARTH FAULT + BREAKER FAILURE\n")

    run_feeder_protection_sequence(
        current_a=1500,
        fault_type="phase-to-earth",
        breaker_failure=True
    )
