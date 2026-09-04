import os
import sys

# Allow imports from the protection study directory
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "02_protection_study")
    )
)

from fault_scenarios import fault_scenarios
from protection_settings import protection_settings

# Import IEC inverse-time calculation
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "05_coordination")
    )
)

from iec_curves import inverse_time


# ---------------------------------------------------------
# Breaker mapping
# ---------------------------------------------------------

def determine_breaker(location):
    """
    Determine which circuit breaker is associated
    with the fault location.
    """

    breaker_map = {
        "Feeder 1": ["CB-301"],
        "Feeder 2": ["CB-302"],
        "Feeder 3": ["CB-303"],
        "Transformer T1": ["CB-101", "CB-201"],
        "Transformer LV Side": [],
        "33 kV Bus": []
    }

    return breaker_map.get(location, [])


# ---------------------------------------------------------
# Feeder 51 inverse-time protection
# ---------------------------------------------------------

def calculate_feeder_51_time(current_a):
    """
    Calculate feeder 51 operating time using
    the IEC standard inverse characteristic.
    """

    settings = protection_settings["feeder_phase_overcurrent"]

    pickup = settings["time_pickup_a"]
    tms = settings.get("tms", 0.10)

    return inverse_time(
        current_a=current_a,
        pickup_a=pickup,
        tms=tms,
        curve="standard_inverse"
    )


# ---------------------------------------------------------
# Transformer backup 51 inverse-time protection
# ---------------------------------------------------------

def calculate_transformer_backup_time(current_a):
    """
    Calculate transformer backup 51 operating time
    using the IEC standard inverse characteristic.
    """

    settings = protection_settings["transformer_backup_overcurrent"]

    pickup = settings["pickup_a"]
    tms = settings.get("tms", 0.25)

    return inverse_time(
        current_a=current_a,
        pickup_a=pickup,
        tms=tms,
        curve="standard_inverse"
    )


# ---------------------------------------------------------
# Protection evaluation
# ---------------------------------------------------------

def evaluate_protection(scenario):
    """
    Evaluate the protection response for a fault scenario.

    Returns a dictionary describing:
    - protection function
    - operating time
    - breaker(s)
    - trip status
    - protection role
    """

    scenario_id = scenario["id"]
    location = scenario["location"]
    fault_type = scenario["fault_type"]
    current = scenario["fault_current_a"]

    breakers = determine_breaker(location)

    # -----------------------------------------------------
    # Normal operation
    # -----------------------------------------------------

    if scenario_id == "SC-001":

        return {
            "scenario": scenario_id,
            "protection": "NONE",
            "status": "NO OPERATE",
            "operating_time_s": None,
            "breakers": [],
            "role": "Normal operation"
        }

    # -----------------------------------------------------
    # Transformer overload
    # -----------------------------------------------------

    if scenario_id == "SC-002":

        return {
            "scenario": scenario_id,
            "protection": "49",
            "status": "ALARM",
            "operating_time_s": None,
            "breakers": [],
            "role": "Thermal protection / overload"
        }

    # -----------------------------------------------------
    # Transformer internal fault
    # -----------------------------------------------------

    if scenario_id == "SC-005":

        return {
            "scenario": scenario_id,
            "protection": "87T",
            "status": "OPERATE",
            "operating_time_s": 0.05,
            "breakers": ["CB-101", "CB-201"],
            "role": "Primary transformer protection"
        }

    # -----------------------------------------------------
    # Feeder protection failure
    # -----------------------------------------------------

    if scenario_id == "SC-006":

        backup_time = calculate_transformer_backup_time(current)

        # If backup 51 is below pickup, use the configured
        # protection delay as a fallback for this synthetic scenario.
        if backup_time is None:
            backup_time = protection_settings[
                "transformer_backup_overcurrent"
            ]["time_delay_s"]

        return {
            "scenario": scenario_id,
            "protection": "51",
            "status": "OPERATE",
            "operating_time_s": backup_time,
            "breakers": ["CB-201"],
            "role": "Backup transformer protection"
        }

    # -----------------------------------------------------
    # Breaker failure
    # -----------------------------------------------------

    if scenario_id == "SC-007":

        return {
            "scenario": scenario_id,
            "protection": "50BF",
            "status": "OPERATE",
            "operating_time_s": protection_settings[
                "breaker_failure"
            ]["failure_timer_s"],
            "breakers": ["CB-201"],
            "role": "Breaker failure backup protection"
        }

    # -----------------------------------------------------
    # Feeder phase fault
    # -----------------------------------------------------

    if fault_type == "phase-to-phase":

        instantaneous_pickup = protection_settings[
            "feeder_phase_overcurrent"
        ]["instantaneous_pickup_a"]

        time_pickup = protection_settings[
            "feeder_phase_overcurrent"
        ]["time_pickup_a"]

        # 50 instantaneous element
        if current >= instantaneous_pickup:

            return {
                "scenario": scenario_id,
                "protection": "50",
                "status": "OPERATE",
                "operating_time_s": 0.05,
                "breakers": breakers,
                "role": "Primary feeder instantaneous protection"
            }

        # 51 inverse-time element
        if current >= time_pickup:

            operating_time = calculate_feeder_51_time(current)

            return {
                "scenario": scenario_id,
                "protection": "51",
                "status": "OPERATE",
                "operating_time_s": operating_time,
                "breakers": breakers,
                "role": "Primary feeder time-overcurrent protection"
            }

    # -----------------------------------------------------
    # Feeder earth fault
    # -----------------------------------------------------

    if fault_type == "phase-to-earth":

        instantaneous_pickup = protection_settings[
            "feeder_earth_fault"
        ]["instantaneous_pickup_a"]

        time_pickup = protection_settings[
            "feeder_earth_fault"
        ]["time_pickup_a"]

        # 50N instantaneous element
        if current >= instantaneous_pickup:

            return {
                "scenario": scenario_id,
                "protection": "50N",
                "status": "OPERATE",
                "operating_time_s": 0.05,
                "breakers": breakers,
                "role": "Primary feeder instantaneous earth-fault protection"
            }

        # 51N time-overcurrent element
        if current >= time_pickup:

            return {
                "scenario": scenario_id,
                "protection": "51N",
                "status": "OPERATE",
                "operating_time_s": protection_settings[
                    "feeder_earth_fault"
                ]["time_delay_s"],
                "breakers": breakers,
                "role": "Primary feeder time earth-fault protection"
            }

    # -----------------------------------------------------
    # No protection operation
    # -----------------------------------------------------

    return {
        "scenario": scenario_id,
        "protection": "NONE",
        "status": "NO OPERATE",
        "operating_time_s": None,
        "breakers": [],
        "role": "No protection threshold exceeded"
    }


# ---------------------------------------------------------
# Run all protection scenarios
# ---------------------------------------------------------

def run_protection_engine():

    print("\nDIGITAL SUBSTATION PROTECTION ENGINE")
    print("====================================")

    for scenario in fault_scenarios:

        result = evaluate_protection(scenario)

        print("\nScenario:", scenario["id"])
        print("Description:", scenario["description"])
        print("Location:", scenario["location"])
        print("Fault current:", scenario["fault_current_a"], "A")
        print("Protection:", result["protection"])
        print("Status:", result["status"])
        print("Role:", result["role"])

        if result["operating_time_s"] is not None:
            print(
                "Operating time:",
                f"{result['operating_time_s']:.3f}",
                "s"
            )

        if result["breakers"]:
            print("Trip breaker(s):", ", ".join(result["breakers"]))


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":
    run_protection_engine()