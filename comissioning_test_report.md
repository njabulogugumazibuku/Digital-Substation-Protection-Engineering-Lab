# Digital Substation Protection Engineering Lab
## Protection & Breaker-Failure Commissioning Test Report

---

## 1. Purpose

This document records the functional verification of the protection logic implemented for the simulated NorthGrid 132/33 kV Digital Substation.

The objective is to demonstrate that the simulated protection system:

- detects abnormal feeder conditions;
- selects the appropriate protection element;
- applies the configured protection characteristic;
- issues a trip through the simulated trip-conditioning logic;
- commands the feeder circuit breaker to open;
- detects a simulated breaker failure; and
- initiates backup protection to isolate the fault.

All values and system parameters in this project are synthetic and intended for educational and portfolio purposes only.

---

## 2. System Under Test

The simulated system represents a 132/33 kV digital substation consisting of:

- 132 kV grid infeed;
- 50 MVA 132/33 kV transformer;
- 33 kV bus;
- three outgoing feeders;
- feeder protection IEDs;
- transformer protection IED;
- simulated IEC 61850-inspired logical nodes;
- feeder circuit breaker CB-301; and
- transformer LV circuit breaker CB-201.

### Primary Feeder Protection

The feeder protection model contains:

| Function | Logical Node | Purpose |
|---|---|---|
| 50 | PTOC2 | Instantaneous phase overcurrent |
| 51 | PTOC1 | Time-delayed phase overcurrent |
| 50N | PTEF2 | Instantaneous earth fault |
| 51N | PTEF1 | Time-delayed earth fault |
| Trip Logic | PTRC1 | Trip conditioning |
| Breaker | XCBR1 | Circuit breaker model |

---

## 3. Protection Philosophy

The protection scheme is based on the following principles:

1. Primary feeder protection should operate for faults within the feeder protection zone.
2. Instantaneous elements should provide rapid operation for sufficiently high fault currents.
3. Time-delayed elements should provide inverse-time operation for lower fault currents above pickup.
4. The feeder breaker should clear the fault following a valid trip command.
5. If the feeder breaker fails to open, breaker-failure protection should initiate backup isolation.
6. Backup protection should operate after the primary protection path has failed.

The protection sequence is therefore:

    Fault
      |
      v
    MMXU1
      |
      v
    Protection Element
      |
      v
    PTRC1
      |
      v
    XCBR1 / CB-301
      |
      +---- Successful opening ---> Fault cleared
      |
      +---- Breaker failure
                    |
                    v
                   50BF
                    |
                    v
                  CB-201
                    |
                    v
              Fault isolated

---

## 4. Test Methodology

Protection functions were tested using synthetic fault-current scenarios.

For each scenario, the protection decision engine determines:

- applicable protection function;
- logical node;
- operating state;
- operating time; and
- trip requirement.

Breaker-failure scenarios additionally simulate failure of CB-301 to open following a valid trip command.

---

## 5. Functional Test Results

### TEST-001 — Primary Phase Protection

**Input**

- Fault type: Phase-to-phase
- Fault current: 2,000 A

**Expected behaviour**

The current is above the 51 pickup and below the instantaneous 50 pickup. The feeder 51 element should therefore operate using its configured inverse-time characteristic.

**Observed behaviour**

- Protection: PTOC1
- Function: 51
- State: OPERATE
- Trip path: PTRC1 → CB-301
- Result: PASS

---

### TEST-002 — Primary Earth-Fault Protection

**Input**

- Fault type: Phase-to-earth
- Fault current: 1,500 A

**Expected behaviour**

The current is above the 51N pickup and below the instantaneous 50N pickup. The 51N element should operate using its inverse-time characteristic.

**Observed behaviour**

- Protection: PTEF1
- Function: 51N
- State: OPERATE
- Operating time: approximately 0.606 s
- Trip path: PTRC1 → CB-301
- Result: PASS

---

### TEST-003 — Phase Fault with Breaker Failure

**Input**

- Fault type: Phase-to-phase
- Fault current: 6,000 A
- Feeder breaker: CB-301
- Breaker condition: Failed to open

**Expected behaviour**

The high fault current should cause instantaneous 50 operation. Following failure of CB-301 to open, 50BF should operate after the configured breaker-failure timer and initiate backup tripping.

**Observed behaviour**

- Primary protection: PTOC2
- Function: 50
- Primary trip issued
- CB-301 simulated as failed
- 50BF timer: 0.300 s
- Backup breaker: CB-201
- Result: PASS

---

### TEST-004 — Earth Fault with Breaker Failure

**Input**

- Fault type: Phase-to-earth
- Fault current: 1,500 A
- Feeder breaker: CB-301
- Breaker condition: Failed to open

**Expected behaviour**

The 51N element should operate using its inverse-time characteristic. If CB-301 fails to open, 50BF should subsequently initiate backup isolation through CB-201.

**Observed behaviour**

- Primary protection: PTEF1
- Function: 51N
- Operating time: approximately 0.606 s
- Primary trip issued
- CB-301 simulated as failed
- 50BF timer: 0.300 s
- CB-201 opens
- Fault isolated
- Result: PASS

---

## 6. Coordination Verification

The protection coordination study evaluates the time separation between feeder protection and transformer backup protection.

The project uses a minimum coordination margin of:

    0.30 s

This value is a project-defined educational criterion and is not intended to represent a universal utility protection standard.

The coordination sweep produced the following results:

| Fault Current | Feeder Time | Backup Time | Margin |
|---:|---:|---:|---:|
| 4,000 A | 0.574 s | 1.561 s | 0.987 s |
| 6,000 A | 0.428 s | 1.138 s | 0.710 s |
| 7,000 A | 0.390 s | 1.032 s | 0.642 s |
| 10,000 A | 0.323 s | 0.847 s | 0.524 s |
| 15,000 A | 0.270 s | 0.703 s | 0.432 s |
| 20,000 A | 0.242 s | 0.626 s | 0.385 s |

All tested points satisfied the project's 0.30 s coordination criterion.

### Important modelling note

The feeder instantaneous 50 element is configured to operate at 5,000 A.

Consequently, the 51 curve values above 5,000 A are useful for studying the theoretical inverse-time characteristic but do not represent the actual final clearing time of the complete protection scheme once the instantaneous element operates.

---

## 7. Breaker-Failure Sequence

The verified breaker-failure sequence is:

    Primary Fault Detection
            |
            v
    Protection Element Operates
            |
            v
       PTRC1 Trip
            |
            v
       CB-301 Trip
            |
            v
       CB-301 Failure
            |
            v
          50BF
            |
            v
     50BF Timer = 0.300 s
            |
            v
       Backup Trip
            |
            v
         CB-201
            |
            v
      Fault Isolated

This sequence demonstrates the distinction between **protection operation** and **successful circuit-breaker interruption**.

A protection relay issuing a trip command does not by itself guarantee fault clearance; breaker-failure protection provides a secondary isolation path when the primary breaker does not respond.

---

## 8. Verification Summary

| Test | Description | Result |
|---|---|---|
| TEST-001 | Primary phase protection | PASS |
| TEST-002 | Primary earth-fault protection | PASS |
| TEST-003 | Phase fault + breaker failure | PASS |
| TEST-004 | Earth fault + breaker failure | PASS |
| Coordination sweep | Protection grading | PASS |

---

## 9. Limitations

This project is a simplified engineering simulation and should not be interpreted as a utility-grade protection study or commissioning package.

The model does not currently include detailed representations of:

- CT saturation;
- CT transient behaviour;
- transformer vector-group compensation;
- transformer differential restraint;
- restricted earth-fault protection;
- directional overcurrent;
- actual network impedance;
- detailed short-circuit calculations;
- breaker mechanical operating characteristics;
- breaker interrupting time;
- autoreclose;
- real IEC 61850 SCL files;
- physical IED configuration software; or
- real substation communication networks.

The numerical settings are synthetic and were selected to demonstrate protection concepts and software implementation.

---

## 10. Future Engineering Enhancements

Potential extensions include:

1. Restrained transformer differential protection model.
2. CT ratio and saturation modelling.
3. Transformer vector-group compensation.
4. Directional overcurrent protection.
5. Breaker-failure current supervision.
6. IEC 61850 SCL/ICD/CID modelling.
7. GOOSE trip-message simulation.
8. Disturbance-record analysis.
9. Automated protection-setting sweeps.
10. Interactive protection coordination dashboard.
11. Automated commissioning test report generation.

---

## 11. Conclusion

The simulated protection system successfully demonstrates the complete path from fault detection through primary protection, trip conditioning, circuit-breaker operation, breaker-failure detection, and backup isolation.

The test results provide evidence that the implemented protection logic behaves consistently with the simplified protection philosophy defined for the project.

The model provides a foundation for further development toward a more comprehensive digital-substation engineering laboratory.