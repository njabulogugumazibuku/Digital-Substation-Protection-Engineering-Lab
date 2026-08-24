# ==========================================
# DIGITAL SUBSTATION PROTECTION ENGINEERING LAB
# Simplified Protection Decision Engine
# ==========================================

import sys
from pathlib import Path


# ------------------------------------------
# Add project directories to Python path
# ------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(
    str(PROJECT_ROOT / "02_protection_study")
)


from fault_scenarios import fault_scenarios
from protection_settings import protection_settings


def determine_breaker(location):
    """
    Determine which circuit breaker is responsible
    for clearing the fault.
    """

    breaker_map = {
        "Feeder 1": "CB-301",
        "Feeder 2": "CB-302",
        "Feeder 3": "CB-303",
        "Transformer T1": "CB-101 and CB-201",
        "Transformer LV Side": "No immediate trip - alarm/thermal logic",
        "33 kV Bus": "No trip"
    }

    return breaker_map.get(
        location,
        "Breaker not defined"
    )


def evaluate_protection(scenario):
    """
    Evaluate a fault scenario and determine the
    expected protection response.
    """

    current = scenario["current_a"]
    fault_type = scenario["fault_type"]
    location = scenario["location"]

    result = {
        "scenario_id": scenario["scenario_id"],
        "scenario_name": scenario["name"],
        "current_a": current,
        "protection_operated": None,
        "operation_type": None,
        "trip_action": None,
        "operating_time_s": None
    }

    # ------------------------------------------
    # Normal operation
    # ------------------------------------------

    if fault_type == "None":

        result["protection_operated"] = "None"
        result["operation_type"] = "Normal operation"
        result["trip_action"] = "No trip"
        result["operating_time_s"] = 0

        return result


    # ------------------------------------------
    # Transformer overload
    # ------------------------------------------

    if fault_type == "Overload":

        result["protection_operated"] = "49 Thermal"
        result["operation_type"] = "Alarm / delayed action"
        result["trip_action"] = "No immediate trip"
        result["operating_time_s"] = None

        return result


    # ------------------------------------------
    # Transformer internal fault
    # ------------------------------------------

    if (
        location == "Transformer T1"
        and fault_type == "Internal Fault"
    ):

        differential = protection_settings[
            "transformer_differential"
        ]

        result["protection_operated"] = (
            differential["function"]
        )

        result["operation_type"] = (
            "Primary transformer protection"
        )

        result["trip_action"] = (
            "Trip CB-101 and CB-201"
        )

        result["operating_time_s"] = 0.05

        return result


    # ------------------------------------------
    # Phase-to-phase feeder fault
    # ------------------------------------------

    if fault_type == "Phase-to-Phase":

        phase_settings = protection_settings[
            "feeder_phase_overcurrent"
        ]

        if current >= phase_settings[
            "instantaneous_pickup_a"
        ]:

            result["protection_operated"] = "50"

            result["operation_type"] = (
                "Instantaneous overcurrent"
            )

            result["trip_action"] = (
                f"Trip {determine_breaker(location)}"
            )

            result["operating_time_s"] = 0.05

            return result

        elif current >= phase_settings[
            "time_pickup_a"
        ]:

            result["protection_operated"] = "51"

            result["operation_type"] = (
                "Time-delayed overcurrent"
            )

            result["trip_action"] = (
                f"Trip {determine_breaker(location)}"
            )

            result["operating_time_s"] = (
                phase_settings["time_delay_s"]
            )

            return result


    # ------------------------------------------
    # Phase-to-earth fault
    # ------------------------------------------

    if fault_type == "Phase-to-Earth":

        earth_settings = protection_settings[
            "feeder_earth_fault"
        ]

        if current >= earth_settings[
            "instantaneous_pickup_a"
        ]:

            result["protection_operated"] = "50N"

            result["operation_type"] = (
                "Instantaneous earth fault"
            )

            result["trip_action"] = (
                f"Trip {determine_breaker(location)}"
            )

            result["operating_time_s"] = 0.05

            return result

        elif current >= earth_settings[
            "time_pickup_a"
        ]:

            result["protection_operated"] = "51N"

            result["operation_type"] = (
                "Time-delayed earth fault"
            )

            result["trip_action"] = (
                f"Trip {determine_breaker(location)}"
            )

            result["operating_time_s"] = (
                earth_settings["time_delay_s"]
            )

            return result


    # ------------------------------------------
    # Feeder protection failure
    # ------------------------------------------

    if scenario["name"] == "Feeder Protection Failure":

        backup = protection_settings[
            "transformer_backup_overcurrent"
        ]

        if current >= backup["pickup_a"]:

            result["protection_operated"] = "51 Backup"

            result["operation_type"] = (
                "Upstream backup protection"
            )

            result["trip_action"] = "Trip CB-201"

            result["operating_time_s"] = (
                backup["time_delay_s"]
            )

            return result


    # ------------------------------------------
    # Breaker failure
    # ------------------------------------------

    if fault_type == "Breaker Failure":

        breaker_failure = protection_settings[
            "breaker_failure"
        ]

        result["protection_operated"] = (
            breaker_failure["function"]
        )

        result["operation_type"] = (
            "Breaker failure protection"
        )

        result["trip_action"] = "Trip CB-201"

        result["operating_time_s"] = (
            breaker_failure["failure_timer_s"]
        )

        return result


    # ------------------------------------------
    # Default response
    # ------------------------------------------

    result["protection_operated"] = "No operation"

    result["operation_type"] = (
        "Fault below configured protection thresholds"
    )

    result["trip_action"] = "No trip"

    result["operating_time_s"] = None

    return result


def run_protection_engine():
    """
    Run all fault scenarios through the protection engine.
    """

    print("=" * 70)
    print("DIGITAL SUBSTATION PROTECTION ENGINE")
    print("=" * 70)

    for scenario in fault_scenarios:

        result = evaluate_protection(scenario)

        print(f"\nScenario: {result['scenario_id']}")
        print(f"Name: {result['scenario_name']}")
        print(f"Fault Current: {result['current_a']} A")

        print(
            f"Protection Operated: "
            f"{result['protection_operated']}"
        )

        print(
            f"Operation Type: "
            f"{result['operation_type']}"
        )

        print(
            f"Action: "
            f"{result['trip_action']}"
        )

        print(
            f"Operating Time: "
            f"{result['operating_time_s']} s"
        )

        print("-" * 70)


if __name__ == "__main__":
    run_protection_engine()
