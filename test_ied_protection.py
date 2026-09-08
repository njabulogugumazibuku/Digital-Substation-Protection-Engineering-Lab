import os
import sys

# ---------------------------------------------------------
# Import IED simulator
# ---------------------------------------------------------

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "03_ied_configuration"
        )
    )
)

from ied_simulator import simulate_ied


# ---------------------------------------------------------
# Test cases
# ---------------------------------------------------------

test_cases = [

    {
        "id": "TEST-001",
        "description": "Normal feeder loading",
        "current": 850,
        "fault_type": "phase-to-phase",
        "expected_element": "PTOC",
        "expected_status": "NO OPERATE",
        "expected_breaker": "CLOSED"
    },

    {
        "id": "TEST-002",
        "description": "High phase fault",
        "current": 6000,
        "fault_type": "phase-to-phase",
        "expected_element": "PTOC2",
        "expected_status": "OPERATE",
        "expected_breaker": "OPEN"
    },

    {
        "id": "TEST-003",
        "description": "Moderate phase fault",
        "current": 2000,
        "fault_type": "phase-to-phase",
        "expected_element": "PTOC1",
        "expected_status": "OPERATE",
        "expected_breaker": "OPEN"
    },

    {
        "id": "TEST-004",
        "description": "High earth fault",
        "current": 3500,
        "fault_type": "phase-to-earth",
        "expected_element": "PTEF2",
        "expected_status": "OPERATE",
        "expected_breaker": "OPEN"
    },

    {
        "id": "TEST-005",
        "description": "Moderate earth fault",
        "current": 1500,
        "fault_type": "phase-to-earth",
        "expected_element": "PTEF1",
        "expected_status": "OPERATE",
        "expected_breaker": "OPEN"
    },

    {
        "id": "TEST-006",
        "description": "Current below pickup",
        "current": 400,
        "fault_type": "phase-to-phase",
        "expected_element": "PTOC",
        "expected_status": "NO OPERATE",
        "expected_breaker": "CLOSED"
    }
]


# ---------------------------------------------------------
# Test execution
# ---------------------------------------------------------

def run_tests():

    passed = 0
    failed = 0

    print("\n")
    print("=" * 60)
    print("IED PROTECTION VALIDATION TEST SUITE")
    print("=" * 60)

    for test in test_cases:

        print(f"\n{test['id']} - {test['description']}")

        result = simulate_ied(
            current_a=test["current"],
            fault_type=test["fault_type"]
        )

        protection = result["protection"]
        breaker = result["breaker"]

        actual_element = protection["logical_node"]
        actual_status = protection["status"]
        actual_breaker = breaker["state"]

        # -------------------------------------------------
        # Validate protection element
        # -------------------------------------------------

        element_pass = (
            actual_element == test["expected_element"]
        )

        # -------------------------------------------------
        # Validate protection status
        # -------------------------------------------------

        status_pass = (
            actual_status == test["expected_status"]
        )

        # -------------------------------------------------
        # Validate breaker state
        # -------------------------------------------------

        breaker_pass = (
            actual_breaker == test["expected_breaker"]
        )

        # -------------------------------------------------
        # Validate operating time
        # -------------------------------------------------

        timing_pass = True

        if actual_status == "OPERATE":

            operating_time = protection[
                "operating_time_s"
            ]

            timing_pass = (
                operating_time is not None
                and operating_time > 0
            )

        # -------------------------------------------------
        # Overall result
        # -------------------------------------------------

        test_passed = (
            element_pass
            and status_pass
            and breaker_pass
            and timing_pass
        )

        if test_passed:

            print("RESULT: PASS")
            passed += 1

        else:

            print("RESULT: FAIL")
            failed += 1

        print(
            f"  Element:  "
            f"{actual_element} "
            f"(expected {test['expected_element']})"
        )

        print(
            f"  Status:   "
            f"{actual_status} "
            f"(expected {test['expected_status']})"
        )

        print(
            f"  Breaker:  "
            f"{actual_breaker} "
            f"(expected {test['expected_breaker']})"
        )

        if protection["operating_time_s"] is not None:

            print(
                f"  Operating time: "
                f"{protection['operating_time_s']:.3f} s"
            )

    # -----------------------------------------------------
    # Test summary
    # -----------------------------------------------------

    total = passed + failed

    print("\n")
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    print(f"Total tests : {total}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")

    if failed == 0:

        print("\nALL TESTS PASSED")

    else:

        print("\nSOME TESTS FAILED")

    print("=" * 60)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":
    run_tests()