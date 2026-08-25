# ==========================================
# DIGITAL SUBSTATION PROTECTION ENGINEERING LAB
# IEC 61850-Inspired IED Model
# ==========================================


ied_model = {

    "ied_name": "FEEDER_01_PROTECTION",

    "manufacturer": "Simulated",

    "model": "Digital Protection IED",

    "logical_devices": {

        "LD_PROTECTION": {

            "description": (
                "Logical device containing feeder "
                "protection functions."
            ),

            "logical_nodes": {

                "MMXU1": {
                    "class": "MMXU",
                    "function": "Measurement",
                    "description": (
                        "Provides electrical measurements "
                        "including current and voltage."
                    )
                },

                "PTOC1": {
                    "class": "PTOC",
                    "function": "51 Phase Overcurrent",
                    "description": (
                        "Time-delayed phase overcurrent "
                        "protection."
                    )
                },

                "PTOC2": {
                    "class": "PTOC",
                    "function": "50 Phase Overcurrent",
                    "description": (
                        "Instantaneous phase overcurrent "
                        "protection."
                    )
                },

                "PTEF1": {
                    "class": "PTEF",
                    "function": "51N Earth Fault",
                    "description": (
                        "Time-delayed earth fault protection."
                    )
                },

                "PTEF2": {
                    "class": "PTEF",
                    "function": "50N Earth Fault",
                    "description": (
                        "Instantaneous earth fault protection."
                    )
                },

                "PTRC1": {
                    "class": "PTRC",
                    "function": "Trip Conditioning",
                    "description": (
                        "Processes protection trip signals "
                        "before issuing a trip command."
                    )
                },

                "XCBR1": {
                    "class": "XCBR",
                    "function": "Circuit Breaker",
                    "description": (
                        "Represents the feeder circuit breaker."
                    )
                }
            }
        }
    }
}


def print_ied_model():
    """
    Print the structure of the simulated IED.
    """

    print("=" * 70)
    print("SIMULATED IEC 61850 IED MODEL")
    print("=" * 70)

    print(f"\nIED Name: {ied_model['ied_name']}")

    print(
        f"Manufacturer: "
        f"{ied_model['manufacturer']}"
    )

    print(
        f"Model: "
        f"{ied_model['model']}"
    )

    for ld_name, ld_data in (
        ied_model["logical_devices"].items()
    ):

        print("\n" + "-" * 70)

        print(
            f"Logical Device: {ld_name}"
        )

        print(
            f"Description: "
            f"{ld_data['description']}"
        )

        print("\nLogical Nodes:")

        for ln_name, ln_data in (
            ld_data["logical_nodes"].items()
        ):

            print(f"\n  {ln_name}")

            print(
                f"  Class: "
                f"{ln_data['class']}"
            )

            print(
                f"  Function: "
                f"{ln_data['function']}"
            )

            print(
                f"  Description: "
                f"{ln_data['description']}"
            )


if __name__ == "__main__":
    print_ied_model()
