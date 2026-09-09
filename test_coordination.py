from protection_engine import (
    calculate_feeder_51_time,
    calculate_transformer_backup_time,
)


MIN_COORDINATION_MARGIN = 0.30

test_currents = [2000, 3000, 4000, 6000, 7000, 10000]


def run_coordination_test():
    """Validate feeder and transformer-backup time coordination."""
    print("\n" + "=" * 70)
    print("PROTECTION COORDINATION VALIDATION")
    print("=" * 70)

    passed = 0
    failed = 0

    for current in test_currents:
        feeder_time = calculate_feeder_51_time(current)
        backup_time = calculate_transformer_backup_time(current)

        print(f"\nFault Current: {current} A")
        print("-" * 70)

        if feeder_time is None:
            print("Feeder 51: BELOW PICKUP")
            continue
        if backup_time is None:
            print("Transformer Backup 51: BELOW PICKUP")
            continue

        coordination_margin = backup_time - feeder_time
        print(f"Feeder 51 operating time: {feeder_time:.3f} s")
        print(f"Transformer backup 51 operating time: {backup_time:.3f} s")
        print(f"Coordination margin: {coordination_margin:.3f} s")

        if coordination_margin >= MIN_COORDINATION_MARGIN:
            print("RESULT: PASS")
            passed += 1
        else:
            print("RESULT: FAIL")
            failed += 1

    print("\n" + "=" * 70)
    print("COORDINATION SUMMARY")
    print("=" * 70)
    print(f"Minimum required margin: {MIN_COORDINATION_MARGIN:.2f} s")
    print(f"Tests passed: {passed}")
    print(f"Tests failed: {failed}")
    print("\nCOORDINATION STUDY: PASS" if failed == 0 else "\nCOORDINATION STUDY: REVIEW REQUIRED")
    print("=" * 70)


if __name__ == "__main__":
    run_coordination_test()
