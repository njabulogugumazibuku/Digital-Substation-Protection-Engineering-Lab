from protection_engine import (
    calculate_feeder_51_time,
    calculate_transformer_backup_time
)


# ---------------------------------------------------------
# Project coordination criterion
# ---------------------------------------------------------

MIN_COORDINATION_MARGIN = 0.30


# ---------------------------------------------------------
# Sweep parameters
# ---------------------------------------------------------

START_CURRENT = 1400
END_CURRENT = 20000
STEP_CURRENT = 100


# ---------------------------------------------------------
# Run coordination sweep
# ---------------------------------------------------------

def run_coordination_sweep():

    results = []

    current = START_CURRENT

    while current <= END_CURRENT:

        feeder_time = calculate_feeder_51_time(current)

        backup_time = calculate_transformer_backup_time(current)

        # Only evaluate points where both
        # protection elements are above pickup.

        if feeder_time is not None and backup_time is not None:

            margin = backup_time - feeder_time

            results.append({
                "current_a": current,
                "feeder_time_s": feeder_time,
                "backup_time_s": backup_time,
                "margin_s": margin
            })

        current += STEP_CURRENT


    # -----------------------------------------------------
    # Find worst-case coordination point
    # -----------------------------------------------------

    if not results:

        print("No valid coordination points found.")

        return

    worst_case = min(
        results,
        key=lambda result: result["margin_s"]
    )


    # -----------------------------------------------------
    # Print results
    # -----------------------------------------------------

    print("\n")
    print("=" * 70)
    print("PROTECTION COORDINATION SENSITIVITY ANALYSIS")
    print("=" * 70)

    print(
        f"\nCurrent range: "
        f"{START_CURRENT} A - {END_CURRENT} A"
    )

    print(
        f"Current step: "
        f"{STEP_CURRENT} A"
    )

    print(
        f"Minimum required margin: "
        f"{MIN_COORDINATION_MARGIN:.2f} s"
    )

    print("\n")
    print("WORST-CASE COORDINATION POINT")
    print("-" * 70)

    print(
        f"Fault current: "
        f"{worst_case['current_a']} A"
    )

    print(
        f"Feeder 51 operating time: "
        f"{worst_case['feeder_time_s']:.3f} s"
    )

    print(
        f"Transformer backup 51 operating time: "
        f"{worst_case['backup_time_s']:.3f} s"
    )

    print(
        f"Coordination margin: "
        f"{worst_case['margin_s']:.3f} s"
    )


    # -----------------------------------------------------
    # Pass / fail decision
    # -----------------------------------------------------

    if worst_case["margin_s"] >= MIN_COORDINATION_MARGIN:

        print("\nRESULT: PASS")

        print(
            "The minimum coordination margin "
            "remains above the project criterion."
        )

    else:

        print("\nRESULT: FAIL")

        print(
            "The coordination margin falls below "
            "the project criterion."
        )


    # -----------------------------------------------------
    # Selected results
    # -----------------------------------------------------

    print("\n")
    print("SELECTED SWEEP RESULTS")
    print("-" * 70)

    selected_currents = [
        2000,
        3000,
        4000,
        6000,
        7000,
        10000,
        15000,
        20000
    ]

    for result in results:

        if result["current_a"] in selected_currents:

            print(
                f"{result['current_a']:>6} A | "
                f"Feeder: {result['feeder_time_s']:.3f} s | "
                f"Backup: {result['backup_time_s']:.3f} s | "
                f"Margin: {result['margin_s']:.3f} s"
            )

    print("=" * 70)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    run_coordination_sweep()
