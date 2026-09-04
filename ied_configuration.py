# ==========================================
# DIGITAL SUBSTATION PROTECTION ENGINEERING LAB
# Feeder Protection IED Configuration
# ==========================================

import sys
from pathlib import Path


# ------------------------------------------
# Add project directories to Python path
# ------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

sys.path.append(
    str(PROJECT_ROOT / "02_protection_study")
)


from protection_settings import protection_settings


# ==========================================
# IED CONFIGURATION
# ==========================================

ied_configuration = {

    "ied_name": "FEEDER_01_PROTECTION",

    "logical_device": "LD_PROTECTION",

    "logical_nodes": {

        "MMXU1": {
            "function": "Measurement",
            "enabled": True
        },

        "PTOC1": {
            "function": "51 Phase Overcurrent",
            "enabled": True,

            "pickup_a": protection_settings[
                "feeder_phase_overcurrent"
            ]["time_pickup_a"],

            "delay_s": protection_settings[
                "feeder_phase_overcurrent"
            ]["time_delay_s"],

            "output": "PTRC1"
        },

        "PTOC2": {
            "function": "50 Phase Overcurrent",
            "enabled": True,

            "pickup_a": protection_settings[
                "feeder_phase_overcurrent"
            ]["instantaneous_pickup_a"],

            "delay_s": 0.05,

            "output": "PTRC1"
        },

        "PTEF1": {
            "function": "51N Earth Fault",
            "enabled": True,

            "pickup_a": protection_settings[
                "feeder_earth_fault"
            ]["time_pickup_a"],

            "delay_s": protection_settings[
                "feeder_earth_fault"
            ]["time_delay_s"],

            "output": "PTRC1"
        },

        "PTEF2": {
            "function": "50N Earth Fault",
            "enabled": True,

            "pickup_a": protection_settings[
                "feeder_earth_fault"
            ]["instantaneous_pickup_a"],

            "delay_s": 0.05,

            "output": "PTRC1"
        },

        "PTRC1": {
            "function": "Trip Conditioning",

            "inputs": [
                "PTOC1",
                "PTOC2",
                "PTEF1",
                "PTEF2"
            ],

            "output": "XCBR1"
        },

        "XCBR1": {
            "function": "Circuit Breaker",

            "breaker_id": "CB-301",

            "normal_state": "CLOSED"
        }
    }
}


# ==========================================
# PRINT IED CONFIGURATION
# ==========================================

def print_ied_configuration():

    print("=" * 70)
    print("FEEDER PROTECTION IED CONFIGURATION")
    print("=" * 70)

    print(
        f"\nIED Name: "
        f"{ied_configuration['ied_name']}"
    )

    print(
        f"Logical Device: "
        f"{ied_configuration['logical_device']}"
    )

    print("\nLOGICAL NODE CONFIGURATION")
    print("-" * 70)

    for node_name, node_data in (
        ied_configuration["logical_nodes"].items()
    ):

        print(f"\nLogical Node: {node_name}")

        for key, value in node_data.items():

            formatted_key = (
                key.replace("_", " ").title()
            )

            print(
                f"{formatted_key}: {value}"
            )

        print("-" * 40)


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    print_ied_configuration()
