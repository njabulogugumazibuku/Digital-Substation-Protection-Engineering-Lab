from protection_decision import earth_fault_protection_decision


# ---------------------------------------------------------
# Test cases
# ---------------------------------------------------------

test_cases = [

    {
        "id": "TEST-EF-001",
        "description": "Earth-fault current below pickup",
        "current": 400,
        "expected_element": "NONE",
        "expected_status": "NO OPERATE"
    },

    {
        "id": "TEST-EF-002",
        "description": "Earth-fault current at pickup boundary",
        "current": 600,
        "expected_element": "51N",
        "expected_status": "OPERATE"
    },

    {
        "id": "TEST-EF-003",
        "description": "Moderate earth fault",
        "current": 1000,
        "expected_element": "51N",
        "expected_status": "OPERATE"
    },

    {
        "id": "TEST-EF-004",
        "description": "Higher earth fault",
        "current": 1500,
        "expected_element": "51N",
        "expected_status": "OPERATE"
    },

    {
        "id": "TEST-EF-005",
        "description": "High earth fault below instantaneous pickup",
        "current": 2500,
        "expected_element": "51N",
        "expected_status": "OPERATE"
    },

    {
        "id": "TEST-EF-006",
        "description": "Instantaneous earth fault",
        "current": 3000,
        "expected_element": "50N",
        "expected_status": "OPERATE"
    },

    {
        "id": "TEST-EF-007",
        "description": "High instantaneous earth fault",
        "current": 3500,
        "expected_element": "50N",
        "expected_status": "OPERATE"
    }
]


# ---------------------------------------------------------
# Test execution
# ---------------------------------------------------------

def run_tests():

    passed = 0
    failed = 0

    print("\n")
    print("=" * 70)
    print("EARTH-FAULT PROTECTION VALIDATION")
    print("=" * 70)

    for test in test_cases:

        result = earth_fault_protection_decision(
            test["current"]
        )

        element_pass = (
            result["element"]
            == test["expected_element"]
        )

        status_pass = (
            result["status"]
            == test["expected_status"]
        )

        timing_pass = True

        if result["status"] == "OPERATE":

            timing_pass = (
                result["operating_time_s"] is not None
                and result["operating_time_s"] > 0
            )

        test_passed = (
            element_pass
            and status_pass
            and timing_pass
        )

        print("\n" + test["id"])
        print("-" * 70)

        print(
            f"Description: "
            f"{test['description']}"
        )

        print(
            f"Current: "
            f"{test['current']} A"
        )

        print(
            f"Expected Element: "
            f"{test['expected_element']}"
        )

        print(
            f"Actual Element: "
            f"{result['element']}"
        )

        print(
            f"Expected State: "
            f"{test['expected_status']}"
        )

        print(
            f"Actual State: "
            f"{result['status']}"
        )

        if result["operating_time_s"] is not None:

            print(
                f"Operating Time: "
                f"{result['operating_time_s']:.3f} s"
            )

        if test_passed:

            print("RESULT: PASS")
            passed += 1

        else:

            print("RESULT: FAIL")
            failed += 1

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    print("\n")
    print("=" * 70)
    print("EARTH-FAULT TEST SUMMARY")
    print("=" * 70)

    print(f"Total tests : {len(test_cases)}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")

    if failed == 0:

        print("\nEARTH-FAULT PROTECTION: PASS")

    else:

        print("\nEARTH-FAULT PROTECTION: REVIEW REQUIRED")

    print("=" * 70)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    run_tests()
