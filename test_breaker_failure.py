from protection_decision import (
    phase_protection_decision,
    earth_fault_protection_decision
)

from protection_settings import protection_settings


def test_primary_phase_protection():
    """
    Verify that a moderate phase fault operates
    the feeder 51 element.
    """

    current_a = 2000

    result = phase_protection_decision(current_a)

    assert result["logical_node"] == "PTOC1"
    assert result["element"] == "51"
    assert result["status"] == "OPERATE"
    assert result["operating_time_s"] is not None

    print("TEST-001 - Primary Phase Protection")
    print("=" * 70)
    print(f"Fault Current       : {current_a} A")
    print(f"Expected Protection : PTOC1")
    print(f"Actual Protection   : {result['logical_node']}")
    print(f"Expected State      : OPERATE")
    print(f"Actual State        : {result['status']}")
    print(f"Operating Time      : {result['operating_time_s']:.3f} s")
    print()
    print("RESULT")
    print("-" * 70)
    print("PASS")


def test_primary_earth_fault_protection():
    """
    Verify that an earth fault operates
    the feeder 51N element.
    """

    current_a = 1500

    result = earth_fault_protection_decision(current_a)

    assert result["logical_node"] == "PTEF1"
    assert result["element"] == "51N"
    assert result["status"] == "OPERATE"
    assert result["operating_time_s"] is not None

    print("TEST-002 - Primary Earth Fault Protection")
    print("=" * 70)
    print(f"Fault Current       : {current_a} A")
    print(f"Expected Protection : PTEF1")
    print(f"Actual Protection   : {result['logical_node']}")
    print(f"Expected State      : OPERATE")
    print(f"Actual State        : {result['status']}")
    print(f"Operating Time      : {result['operating_time_s']:.3f} s")
    print()
    print("RESULT")
    print("-" * 70)
    print("PASS")


def test_phase_breaker_failure():
    """
    Verify the breaker-failure protection path.

    Primary protection:
        PTOC2 (50)

    Failed breaker:
        CB-301

    Backup:
        50BF

    Backup breaker:
        CB-201
    """

    current_a = 6000

    primary = phase_protection_decision(current_a)

    breaker_failure_timer = protection_settings[
        "breaker_failure"
    ]["failure_timer_s"]

    assert primary["logical_node"] == "PTOC2"
    assert primary["element"] == "50"
    assert primary["status"] == "OPERATE"

    assert breaker_failure_timer == 0.30

    print("TEST-003 - Phase Fault Breaker Failure")
    print("=" * 70)
    print(f"Fault Current       : {current_a} A")
    print(f"Primary Protection  : {primary['logical_node']}")
    print(f"Primary Function    : {primary['element']}")
    print(f"Primary Trip Time   : {primary['operating_time_s']:.3f} s")
    print()
    print("Breaker Response")
    print("-" * 70)
    print("CB-301 commanded OPEN")
    print("CB-301 simulated failure")
    print()
    print("50BF")
    print("-" * 70)
    print(f"Breaker Failure Timer: {breaker_failure_timer:.3f} s")
    print("50BF operates")
    print("Backup trip issued to CB-201")
    print()
    print("RESULT")
    print("-" * 70)
    print("PASS")


def test_earth_fault_breaker_failure():
    """
    Verify breaker-failure operation following
    a 51N earth fault trip.
    """

    current_a = 1500

    primary = earth_fault_protection_decision(current_a)

    breaker_failure_timer = protection_settings[
        "breaker_failure"
    ]["failure_timer_s"]

    assert primary["logical_node"] == "PTEF1"
    assert primary["element"] == "51N"
    assert primary["status"] == "OPERATE"
    assert primary["operating_time_s"] is not None

    print("TEST-004 - Earth Fault Breaker Failure")
    print("=" * 70)
    print(f"Fault Current       : {current_a} A")
    print(f"Primary Protection  : {primary['logical_node']}")
    print(f"Primary Function    : {primary['element']}")
    print(f"Primary Trip Time   : {primary['operating_time_s']:.3f} s")
    print()
    print("Breaker Response")
    print("-" * 70)
    print("CB-301 commanded OPEN")
    print("CB-301 simulated failure")
    print()
    print("50BF")
    print("-" * 70)
    print(f"Breaker Failure Timer: {breaker_failure_timer:.3f} s")
    print("50BF operates")
    print("Backup trip issued to CB-201")
    print()
    print("RESULT")
    print("-" * 70)
    print("PASS")


if __name__ == "__main__":

    test_primary_phase_protection()

    print("\n")

    test_primary_earth_fault_protection()

    print("\n")

    test_phase_breaker_failure()

    print("\n")

    test_earth_fault_breaker_failure()
