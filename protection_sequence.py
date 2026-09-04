# ==========================================
# DIGITAL SUBSTATION PROTECTION ENGINEERING LAB
# Protection Sequence Simulator
# ==========================================

from protection_engine import evaluate_protection
from protection_engine import fault_scenarios
from protection_engine import protection_settings


def simulate_protection_sequence(scenario):
    """
    Simulate the sequence of events following
    a fault or abnormal operating condition.
    """

    events = []

    scenario_name = scenario["name"]

    events.append(
        f"EVENT 1: {scenario_name} detected"
    )

    # ------------------------------------------
    # Normal operation
    # ------------------------------------------

    if scenario["fault_type"] == "None":

        events.append(
            "EVENT 2: System operating normally"
        )

        events.append(
            "RESULT: No protection operation required"
        )

        return events

    # ------------------------------------------
    # Transformer overload
    # ------------------------------------------

    if scenario["fault_type"] == "Overload":

        events.append(
            "EVENT 2: Thermal overload condition detected"
        )

        events.append(
            "EVENT 3: 49 thermal protection issues alarm"
        )

        events.append(
            "RESULT: No immediate trip"
        )

        return events

    # ------------------------------------------
    # Transformer internal fault
    # ------------------------------------------

    if (
        scenario["location"] == "Transformer T1"
        and scenario["fault_type"] == "Internal Fault"
    ):

        events.append(
            "EVENT 2: 87T differential protection operates"
        )

        events.append(
            "EVENT 3: Trip command issued to CB-101"
        )

        events.append(
            "EVENT 4: Trip command issued to CB-201"
        )

        events.append(
            "EVENT 5: Transformer isolated"
        )

        events.append(
            "RESULT: Fault cleared by primary protection"
        )

        return events

    # ------------------------------------------
    # Feeder protection failure
    # ------------------------------------------

    if scenario_name == "Feeder Protection Failure":

        backup = protection_settings[
            "transformer_backup_overcurrent"
        ]

        events.append(
            "EVENT 2: Fault detected on Feeder 3"
        )

        events.append(
            "EVENT 3: Primary feeder protection unavailable"
        )

        events.append(
            "EVENT 4: Fault current persists"
        )

        events.append(
            "EVENT 5: Upstream 51 backup timer starts"
        )

        events.append(
            f"EVENT 6: Backup delay expires "
            f"after {backup['time_delay_s']} s"
        )

        events.append(
            "EVENT 7: Trip command issued to CB-201"
        )

        events.append(
            "RESULT: Fault cleared by upstream backup protection"
        )

        return events

    # ------------------------------------------
    # Breaker failure
    # ------------------------------------------

    if scenario["fault_type"] == "Breaker Failure":

        breaker_failure = protection_settings[
            "breaker_failure"
        ]

        events.append(
            "EVENT 2: Primary protection detects fault"
        )

        events.append(
            "EVENT 3: Trip command issued to CB-301"
        )

        events.append(
            "EVENT 4: CB-301 fails to open"
        )

        events.append(
            "EVENT 5: Fault current persists"
        )

        events.append(
            "EVENT 6: 50BF breaker failure timer starts"
        )

        events.append(
            f"EVENT 7: Breaker failure timer expires "
            f"after {breaker_failure['failure_timer_s']} s"
        )

        events.append(
            "EVENT 8: Backup trip issued to CB-201"
        )

        events.append(
            "RESULT: Fault cleared by backup isolation"
        )

        return events

    # ------------------------------------------
    # Standard feeder protection operation
    # ------------------------------------------

    protection_result = evaluate_protection(scenario)

    events.append(
        f"EVENT 2: Protection element "
        f"{protection_result['protection_operated']} operates"
    )

    events.append(
        f"EVENT 3: {protection_result['trip_action']}"
    )

    events.append(
        "EVENT 4: Circuit breaker opens successfully"
    )

    events.append(
        "RESULT: Fault cleared by primary protection"
    )

    return events


def run_protection_sequence():

    print("=" * 70)
    print("DIGITAL SUBSTATION PROTECTION SEQUENCE SIMULATOR")
    print("=" * 70)

    for scenario in fault_scenarios:

        print(f"\nSCENARIO: {scenario['scenario_id']}")
        print(f"NAME: {scenario['name']}")

        print("-" * 70)

        events = simulate_protection_sequence(scenario)

        for event in events:

            print(event)

        print("=" * 70)


if __name__ == "__main__":
    run_protection_sequence()
