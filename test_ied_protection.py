# ==========================================
# DIGITAL SUBSTATION PROTECTION ENGINEERING LAB
# Automated IED Protection Tests
# ==========================================

import sys
from pathlib import Path

# ------------------------------------------
# Add project directories to Python path
# ------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(
    str(PROJECT_ROOT / "03_ied_configuration")
)

from ied_simulator import simulate_ied


# ==========================================
# TEST CASES
# ==========================================

test_cases = [

    {
        "id": "TEST-001",
        "name": "Normal Load",
        "current_a": 850,
        "fault_type": "Phase-to-Phase",
        "expected_protection": "PTOC",
        "expected_state": "NO OPERATE",
        "expected_breaker": "CLOSED"
    },

    {
        "id": "TEST-002",
        "name": "High Phase Fault",
        "current_a": 6000,
        "fault_type": "Phase-to-Phase",
        "expected_protection": "PTOC2",
        "expected_state": "OPERATE",
        "expected_breaker": "OPEN"
    },

    {
        "id": "TEST-003",
        "name": "Moderate Phase Fault",
        "current_a": 2000,
        "fault_type": "Phase-to-Phase",
        "expected_protection": "PTOC1",
        "expected_state": "OPERATE",
        "expected_breaker": "OPEN"
    },

    {
        "id": "TEST-004",
        "name": "High Earth Fault",
        "current_a": 3500,
        "fault_type": "Phase-to-Earth",
        "expected_protection": "PTEF2",
        "expected_state": "OPERATE",
        "expected_breaker": "OPEN"
    },

    {
        "id": "TEST-005",
        "name": "Moderate Earth Fault",
        "current_a": 1500,
        "fault_type": "Phase-to-Earth",
        "expected_protection": "PTEF1",
        "expected_state": "OPERATE",
        "expected_breaker": "OPEN"
    },

    {
        "id": "TEST-006",
        "name": "Current Below Pickup",
        "current_a": 400,
        "fault_type": "Phase-to-Phase",
        "expected_protection": "PTOC",
        "expected_state": "NO OPERATE",
        "expected_breaker": "CLOSED"
    }
]


# ==========================================
# RUN TEST
# ==========================================

def run_test(test):

    print("\n" + "=" * 70)

    print(
        f"{test['id']} - {test['name']}"
    )

    print("=" * 70)

    result = simulate_ied(
        current_a=test["current_a"],
        fault_type=test["fault_type"]
    )

    actual_protection = (
        result["protection"]["logical_node"]
    )

    actual_state = (
        result["protection"]["state"]
    )

    actual_breaker = (
        result["breaker"]["state"]
    )

    protection_pass = (
        actual_protection ==
        test["expected_protection"]
    )

    state_pass = (
        actual_state ==
        test["expected_state"]
    )

    breaker_pass = (
        actual_breaker ==
        test["expected_breaker"]
    )

    test_passed = (
        protection_pass
        and state_pass
        and breaker_pass
    )

    print("\nTEST EXPECTATIONS")
    print("-" * 70)

    print(
        f"Expected Protection: "
        f"{test['expected_protection']}"
    )

    print(
        f"Actual Protection: "
        f"{actual_protection}"
    )

    print(
        f"Expected State: "
        f"{test['expected_state']}"
    )

    print(
        f"Actual State: "
        f"{actual_state}"
    )

    print(
        f"Expected Breaker: "
        f"{test['expected_breaker']}"
    )

    print(
        f"Actual Breaker: "
        f"{actual_breaker}"
    )

    print("\nRESULT")

    if test_passed:

        print("PASS")

    else:

        print("FAIL")

    return test_passed


# ==========================================
# RUN ALL TESTS
# ==========================================

def run_all_tests():

    print("\n")
    print("=" * 70)
    print("IED PROTECTION TEST SUITE")
    print("=" * 70)

    results = []

    for test in test_cases:

        result = run_test(test)

        results.append(result)

    passed = sum(results)
    total = len(results)

    print("\n")
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    print(
        f"Tests Passed: {passed}/{total}"
    )

    print(
        f"Tests Failed: {total - passed}/{total}"
    )

    if passed == total:

        print("OVERALL RESULT: PASS")

    else:

        print("OVERALL RESULT: REVIEW REQUIRED")


if __name__ == "__main__":

    run_all_tests()
