# ==========================================
# DIGITAL SUBSTATION PROTECTION ENGINEERING LAB
# Feeder Protection IED Simulator
# ==========================================

from iec_curves import inverse_time
from ied_configuration import ied_configuration


def _node(name):
    """Return a configured IEC 61850 logical node."""
    return ied_configuration["logical_nodes"][name]


def evaluate_phase_overcurrent(current_a):
    """Evaluate instantaneous (50) and inverse-time (51) phase protection."""
    ptoc1 = _node("PTOC1")
    ptoc2 = _node("PTOC2")
    if ptoc2["enabled"] and current_a >= ptoc2["pickup_a"]:
        return {"logical_node": "PTOC2", "function": ptoc2["function"], "state": "OPERATE", "delay_s": ptoc2["delay_s"]}
    if ptoc1["enabled"] and current_a >= ptoc1["pickup_a"]:
        return {"logical_node": "PTOC1", "function": ptoc1["function"], "state": "OPERATE", "delay_s": inverse_time(current_a, ptoc1["pickup_a"], 0.10)}
    return {"logical_node": "PTOC", "function": "Phase Overcurrent", "state": "NO OPERATE", "delay_s": None}


def evaluate_earth_fault(current_a):
    """Evaluate instantaneous (50N) and time-delayed (51N) earth protection."""
    ptef1 = _node("PTEF1")
    ptef2 = _node("PTEF2")
    if ptef2["enabled"] and current_a >= ptef2["pickup_a"]:
        return {"logical_node": "PTEF2", "function": ptef2["function"], "state": "OPERATE", "delay_s": ptef2["delay_s"]}
    if ptef1["enabled"] and current_a >= ptef1["pickup_a"]:
        return {"logical_node": "PTEF1", "function": ptef1["function"], "state": "OPERATE", "delay_s": ptef1["delay_s"]}
    return {"logical_node": "PTEF", "function": "Earth Fault Protection", "state": "NO OPERATE", "delay_s": None}


def process_trip(protection_result):
    """Simulate PTRC1 trip conditioning."""
    state = "TRIP" if protection_result["state"] == "OPERATE" else "NO TRIP"
    return {"logical_node": "PTRC1", "state": state, "input": protection_result["logical_node"]}


def operate_breaker(trip_result):
    """Simulate XCBR1 circuit-breaker operation."""
    breaker = _node("XCBR1")
    if trip_result["state"] == "TRIP":
        return {"logical_node": "XCBR1", "breaker_id": breaker["breaker_id"], "command": "OPEN", "state": "OPEN"}
    return {"logical_node": "XCBR1", "breaker_id": breaker["breaker_id"], "command": "NONE", "state": breaker["normal_state"]}


def simulate_ied(current_a, fault_type):
    """Run a fault condition through the simulated feeder-protection IED."""
    if fault_type == "Phase-to-Phase":
        protection_result = evaluate_phase_overcurrent(current_a)
    elif fault_type == "Phase-to-Earth":
        protection_result = evaluate_earth_fault(current_a)
    else:
        protection_result = {"logical_node": "NONE", "function": "No Protection Function Selected", "state": "NO OPERATE", "delay_s": None}
    trip_result = process_trip(protection_result)
    breaker_result = operate_breaker(trip_result)
    return {"protection": protection_result, "trip": trip_result, "breaker": breaker_result}


if __name__ == "__main__":
    print(simulate_ied(2000, "Phase-to-Phase"))
