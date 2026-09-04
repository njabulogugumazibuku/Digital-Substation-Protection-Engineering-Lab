# ==========================================
# DIGITAL SUBSTATION PROTECTION ENGINEERING LAB
# Fault Scenario Definitions
# ==========================================

fault_scenarios = [

    {
        "scenario_id": "SC-001",
        "name": "Normal Operation",
        "location": "33 kV Bus",
        "fault_type": "None",
        "current_a": 850,
        "expected_protection": "None",
        "expected_action": "No trip",
        "description": (
            "System operating below the assumed maximum "
            "continuous operating current."
        )
    },

    {
        "scenario_id": "SC-002",
        "name": "Transformer Overload",
        "location": "Transformer LV Side",
        "fault_type": "Overload",
        "current_a": 1150,
        "expected_protection": "49 Thermal / Alarm",
        "expected_action": "Alarm or delayed protection action",
        "description": (
            "Sustained loading above the assumed normal "
            "operating range."
        )
    },

    {
        "scenario_id": "SC-003",
        "name": "Feeder Phase Fault",
        "location": "Feeder 1",
        "fault_type": "Phase-to-Phase",
        "current_a": 6000,
        "expected_protection": "50/51 Phase Overcurrent",
        "expected_action": "Trip CB-301",
        "description": (
            "Fault occurring within the protection zone "
            "of Feeder 1."
        )
    },

    {
        "scenario_id": "SC-004",
        "name": "Feeder Earth Fault",
        "location": "Feeder 2",
        "fault_type": "Phase-to-Earth",
        "current_a": 2500,
        "expected_protection": "50N/51N Earth Fault",
        "expected_action": "Trip CB-302",
        "description": (
            "Earth fault occurring within the protection "
            "zone of Feeder 2."
        )
    },

    {
        "scenario_id": "SC-005",
        "name": "Transformer Internal Fault",
        "location": "Transformer T1",
        "fault_type": "Internal Fault",
        "current_a": 10000,
        "expected_protection": "87T Transformer Differential",
        "expected_action": "Trip CB-101 and CB-201",
        "description": (
            "Internal transformer fault requiring rapid "
            "isolation of the transformer."
        )
    },

    {
        "scenario_id": "SC-006",
        "name": "Feeder Protection Failure",
        "location": "Feeder 3",
        "fault_type": "Phase-to-Earth",
        "current_a": 7000,
        "expected_protection": "Backup 51 / 51N",
        "expected_action": (
            "Trip upstream CB-201 after coordination delay"
        ),
        "description": (
            "Primary feeder protection fails to clear "
            "the fault."
        )
    },

    {
        "scenario_id": "SC-007",
        "name": "Breaker Failure",
        "location": "Feeder 1 Breaker",
        "fault_type": "Breaker Failure",
        "current_a": 6500,
        "expected_protection": "50BF Breaker Failure",
        "expected_action": (
            "Trip upstream CB-201 after breaker failure timer"
        ),
        "description": (
            "Trip command issued to CB-301 but breaker "
            "fails to interrupt fault current."
        )
    }
]


def print_fault_scenarios():
    """
    Print all defined fault scenarios.
    """

    print("FAULT SCENARIO LIBRARY")
    print("=" * 60)

    for scenario in fault_scenarios:

        print(f"\nScenario: {scenario['scenario_id']}")
        print(f"Name: {scenario['name']}")
        print(f"Location: {scenario['location']}")
        print(f"Fault Type: {scenario['fault_type']}")
        print(f"Current: {scenario['current_a']} A")

        print(
            f"Expected Protection: "
            f"{scenario['expected_protection']}"
        )

        print(
            f"Expected Action: "
            f"{scenario['expected_action']}"
        )

        print(
            f"Description: "
            f"{scenario['description']}"
        )

        print("-" * 60)


if __name__ == "__main__":
    print_fault_scenarios()
