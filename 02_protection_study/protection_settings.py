# ==========================================
# DIGITAL SUBSTATION PROTECTION ENGINEERING LAB
# Initial Protection Settings
# ==========================================

# NOTE:
# All settings in this file are synthetic and are
# intended for educational and portfolio purposes only.


protection_settings = {

    "feeder_phase_overcurrent": {

        "function": "50/51",

        # Instantaneous overcurrent threshold
        "instantaneous_pickup_a": 5000,

        # Time overcurrent pickup
        "time_pickup_a": 1200,

        # Simplified operating delay
        "time_delay_s": 0.40,

        "description": (
            "Primary phase overcurrent protection "
            "for 33 kV feeders."
        )
    },


    "feeder_earth_fault": {

        "function": "50N/51N",

        # Instantaneous earth fault threshold
        "instantaneous_pickup_a": 3000,

        # Time-delayed earth fault pickup
        "time_pickup_a": 600,

        # Simplified operating delay
        "time_delay_s": 0.50,

        "description": (
            "Earth fault protection for 33 kV feeders."
        )
    },


    "transformer_backup_overcurrent": {

        "function": "51",

        # Preliminary value based on earlier calculation
        "pickup_a": 1320,

        # Deliberately slower than feeder protection
        "time_delay_s": 1.00,

        "description": (
            "Backup overcurrent protection for faults "
            "not cleared by downstream feeder protection."
        )
    },


    "transformer_differential": {

        "function": "87T",

        # Simplified differential operating threshold
        "differential_pickup_a": 0.30,

        "description": (
            "Primary protection for internal transformer faults."
        )
    },


    "breaker_failure": {

        "function": "50BF",

        # Time allowed for breaker operation
        "failure_timer_s": 0.30,

        "description": (
            "Breaker failure protection initiated when "
            "fault current persists after a trip command."
        )
    }
}


def print_protection_settings():
    """
    Print the configured protection settings.
    """

    print("INITIAL PROTECTION SETTINGS")
    print("=" * 60)

    for protection, settings in protection_settings.items():

        print(f"\nProtection Element: {protection}")
        print(f"Function: {settings['function']}")

        for setting, value in settings.items():

            if setting not in ["function", "description"]:

                formatted_name = (
                    setting
                    .replace("_", " ")
                    .title()
                )

                print(
                    f"{formatted_name}: {value}"
                )

        print(
            f"Description: "
            f"{settings['description']}"
        )

        print("-" * 60)


if __name__ == "__main__":
    print_protection_settings()
