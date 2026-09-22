# Digital Substation Protection Engineering Lab

## IED Protection Configuration, Coordination & Breaker-Failure Simulation

A practical engineering simulation of a 132/33 kV digital substation protection system, demonstrating the progression from system definition and protection studies through IED logical modelling, protection decision-making, coordination analysis, breaker-failure behaviour, and automated verification.

> **Project scope:** Educational engineering simulation using synthetic system data and protection settings. This project is not intended to represent utility-specific protection settings, a field commissioning package, or a standards-compliant IEC 61850 configuration.

---

## 1. Project Overview

Protection engineering sits at the intersection of electrical power systems, instrumentation, control, communications, and operational reliability.

This project models that interaction through a simplified digital-substation environment.

The simulated system contains:

- 132 kV grid infeed
- 50 MVA 132/33 kV transformer
- 33 kV bus
- Three outgoing feeders
- Feeder protection IEDs
- Transformer protection
- Circuit breakers
- IEC 61850-inspired logical nodes
- Primary and backup protection
- Breaker-failure protection
- Protection coordination analysis
- Automated engineering tests

The central engineering objective is to demonstrate how a protection requirement can be translated into:

```text
System Model
      ↓
Protection Study
      ↓
Protection Settings
      ↓
IED Configuration
      ↓
Protection Logic
      ↓
Trip Sequence
      ↓
Breaker Behaviour
      ↓
Coordination
      ↓
Verification
````

---

## 2. System Architecture


                         132 kV GRID
                              │
                              │
                           CB-101
                              │
                              ▼
                     ┌─────────────────┐
                     │   132/33 kV     │
                     │ Transformer T1  │
                     │     50 MVA      │
                     └─────────────────┘
                              │
                           CB-201
                              │
                              ▼
                         33 kV BUS
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
           CB-301          CB-302          CB-303
              │               │               │
              ▼               ▼               ▼
          Feeder 1         Feeder 2         Feeder 3
              │
              │
       FEEDER PROTECTION IED
              │
       ┌──────┼──────┬──────┐
       │      │      │      │
      51     50     51N    50N
     PTOC1  PTOC2   PTEF1  PTEF2
       │      │      │      │
       └──────┴──────┴──────┘
                    │
                  PTRC1
                    │
                  XCBR1
                    │
                  CB-301
```
## 3. Protection Functions

The feeder protection model implements four primary overcurrent functions:

| Function | Logical Node | Role                            |
| -------- | ------------ | ------------------------------- |
| 51       | PTOC1        | Time-delayed phase overcurrent  |
| 50       | PTOC2        | Instantaneous phase overcurrent |
| 51N      | PTEF1        | Time-delayed earth fault        |
| 50N      | PTEF2        | Instantaneous earth fault       |

Trip conditioning is represented by:

PTRC1


The circuit breaker is represented by:

XCBR1


Breaker-failure protection is represented by:

50BF

## 4. Protection Behaviour

 Phase Protection

Current < 1200 A
        ↓
No operation

1200 A < Current < 5000 A
        ↓
51 / PTOC1
        ↓
IEC Standard Inverse

Current ≥ 5000 A
        ↓
50 / PTOC2
        ↓
Instantaneous operation

## Earth-Fault Protection

Current < 600 A
        ↓
No operation

600 A < Current < 3000 A
        ↓
51N / PTEF1
        ↓
IEC Standard Inverse

Current ≥ 3000 A
        ↓
50N / PTEF2
        ↓
Instantaneous operation

The numerical values are synthetic project parameters selected for educational modelling.

## 5. IED Architecture

The feeder protection IED is modelled using an IEC 61850-inspired logical structure:

FEEDER_01_PROTECTION
        │
        └── LD_PROTECTION
              │
              ├── MMXU1
              │
              ├── PTOC1
              │    └── 51 Phase Overcurrent
              │
              ├── PTOC2
              │    └── 50 Phase Overcurrent
              │
              ├── PTEF1
              │    └── 51N Earth Fault
              │
              ├── PTEF2
              │    └── 50N Earth Fault
              │
              ├── PTRC1
              │    └── Trip Conditioning
              │
              └── XCBR1
                   └── CB-301

The model separates:

1. Measurement
2. Protection functions
3. Trip conditioning
4. Breaker control

This allows the protection chain to be tested and extended independently.

## 6. Protection Settings

The main synthetic feeder protection settings are:

| Function |  Pickup | Characteristic        |
| -------- | ------: | --------------------- |
| 51       |  1200 A | IEC Standard Inverse  |
| 50       |  5000 A | Instantaneous         |
| 51N      |   600 A | IEC Standard Inverse  |
| 50N      |  3000 A | Instantaneous         |
| 50BF     | 0.300 s | Breaker-failure timer |

The settings are synthetic and are intended to demonstrate protection concepts rather than represent field-ready relay settings.

## 7. Inverse-Time Protection

The 51 and 51N functions use an IEC Standard Inverse characteristic.

The model uses:

t = TMS × k / ((I / Ip)^α - 1)

where:


k = 0.14
α = 0.02

The operating time therefore changes according to the magnitude of the fault current.

For example, the 1500 A earth-fault test produced:


Protection : PTEF1
Function   : 51N
State      : OPERATE
Time       : approximately 0.606 s

This demonstrates that the 51N function is not simply using a fixed delay.


## 8. Protection Sequence

The normal feeder protection sequence is:


Fault Detected
      │
      ▼
MMXU1 Measurement
      │
      ▼
Protection Decision
      │
      ▼
PTOC / PTEF
      │
      ▼
PTRC1
      │
      ▼
XCBR1
      │
      ▼
CB-301 Opens
      │
      ▼
Fault Cleared


## 9. Breaker-Failure Protection

The project also models the situation where primary protection operates but the feeder breaker fails to open.

Fault Detected
      │
      ▼
Primary Protection
      │
      ▼
PTRC1 Trip
      │
      ▼
CB-301
      │
 ┌────┴────┐
 │         │
OPEN      FAIL
 │         │
 ▼         ▼
CLEAR     50BF
            │
            ▼
         CB-201
            │
            ▼
      Fault Isolated

This demonstrates the distinction between:

**Protection operation**

and:

**Successful fault interruption**

A relay issuing a trip command does not by itself guarantee that the circuit breaker successfully interrupts the fault.

## 10. Coordination Study

The project evaluates the time separation between feeder primary protection and transformer backup protection.

A project-defined minimum coordination margin of:

0.30 s

is used as the educational acceptance criterion.

The automated coordination sweep produced:

| Fault Current | Feeder Time | Backup Time |  Margin |
| ------------: | ----------: | ----------: | ------: |
|          4 kA |     0.574 s |     1.561 s | 0.987 s |
|          6 kA |     0.428 s |     1.138 s | 0.710 s |
|          7 kA |     0.390 s |     1.032 s | 0.642 s |
|         10 kA |     0.323 s |     0.847 s | 0.524 s |
|         15 kA |     0.270 s |     0.703 s | 0.432 s |
|         20 kA |     0.242 s |     0.626 s | 0.385 s |

The smallest tested margin was approximately:

0.385 s

at 20 kA.

> **Note:** The 0.30 s coordination margin is a project-defined educational criterion. It should not be interpreted as a universal protection-setting requirement.

The feeder 50 instantaneous element is configured at 5000 A. Therefore, calculated 51 curve values above 5000 A are useful for studying the theoretical inverse characteristic but do not represent the final clearing time of the complete protection scheme once the instantaneous element operates.

## 11. Testing & Verification

The project includes automated tests covering:

* Primary phase protection
* Primary earth-fault protection
* Phase fault with breaker failure
* Earth fault with breaker failure
* Protection coordination

The current functional tests have passed.

Example test structure:

TEST-001 - Primary Phase Protection
PASS

TEST-002 - Primary Earth Fault Protection
PASS

TEST-003 - Phase Fault Breaker Failure
PASS

TEST-004 - Earth Fault Breaker Failure
PASS

The test suite provides a basic verification layer between the implemented protection logic and the expected engineering behaviour.

## 12. Repository Structure

Digital-Substation-Protection-Engineering-Lab/
│
├── README.md
│
├── rated_current_calculations.py
├── fault_scenarios.py
├── protection_settings.py
├── ied_model.py
├── ied_configuration.py
├── ied_simulator.py
├── protection_engine.py
├── protection_sequence.py
├── protection_decision.py
├── iec_curves.py
├── tcc_coordination.png
├── test_ied_protection.py
├── test_earth_fault_protection.py
├── test_coordination.py
├── coordination_sweep.py
├── test_breaker_failure.py
└── comissioning_test_report.md


## 13. Engineering Concepts Demonstrated

## Electrical Power Systems

* Three-phase transformer calculations
* Transformer ratings
* Fault scenarios
* Protection zones
* Overcurrent protection
* Earth-fault protection
* Protection coordination

## Protection Engineering

* ANSI 50/51 functions
* ANSI 50N/51N functions
* IEC inverse-time characteristics
* Time-current coordination
* Breaker-failure protection
* Trip conditioning
* Backup protection

## Digital Substations

* IED architecture
* Logical devices
* Logical nodes
* Measurement functions
* Protection functions
* Breaker control
* IEC 61850-inspired modelling

## Software Engineering

* Modular architecture
* Reusable protection functions
* Simulation
* Automated testing
* Parameterized studies
* Engineering documentation


## 14. Engineering Limitations

This project is deliberately simplified.

It does not currently model:

* CT saturation
* CT transient behaviour
* Transformer vector-group compensation
* Restrained transformer differential protection
* Restricted earth-fault protection
* Directional overcurrent
* Detailed network impedance
* Detailed short-circuit calculations
* Physical breaker mechanics
* Breaker interrupting time
* Breaker contact feedback
* Autoreclose
* Real IEC 61850 SCL files
* GOOSE communication
* Physical IED configuration software

The system parameters, fault currents, and protection settings are synthetic.

The project therefore demonstrates engineering concepts, system thinking, and software implementation rather than field-ready protection design.


## 15. Future Development

Potential future extensions include:

1. Transformer differential protection model
2. CT saturation simulation
3. Directional overcurrent protection
4. Breaker-failure current supervision
5. IEC 61850 SCL modelling
6. GOOSE message simulation
7. Disturbance-record analysis
8. Automated protection-setting sensitivity studies
9. Interactive protection dashboard
10. Automated commissioning documentation


## 16. Engineering Approach

The project follows a systems-engineering approach to protection.

Rather than treating the relay as an isolated calculation, the model connects:

Electrical System
      ↓
Measurements
      ↓
Protection Algorithms
      ↓
IED Logical Functions
      ↓
Trip Logic
      ↓
Circuit Breaker
      ↓
Breaker-Failure Protection
      ↓
Backup Isolation
      ↓
Verification

This creates a traceable relationship between:

* system assumptions;
* electrical calculations;
* protection settings;
* IED configuration;
* protection decisions;
* breaker behaviour;
* coordination;
* testing; and
* engineering documentation.


## 17. Project Status

### Completed

* [x] System model
* [x] Protection philosophy
* [x] Rated-current calculations
* [x] Fault scenarios
* [x] Protection settings
* [x] IEC inverse-time curve model
* [x] IED logical model
* [x] IED configuration
* [x] Protection decision engine
* [x] Protection sequence simulation
* [x] Breaker-failure simulation
* [x] Coordination study
* [x] Coordination sweep
* [x] Automated protection tests
* [x] Breaker-failure tests
* [x] Commissioning test report
* [x] Engineering decisions document

### Next

* [ ] Improve repository visualisation
* [ ] Add TCC plot to README
* [ ] Add protection sequence diagram
* [ ] Improve IED configuration model
* [ ] Add transformer differential protection
* [ ] Explore IEC 61850 SCL modelling
* [ ] Add GOOSE communication simulation
* [ ] Add disturbance-record analysis
s
## 18. Scope & Disclaimer

This repository is a portfolio and educational engineering project.

All equipment identifiers, system parameters, fault currents, and protection settings are synthetic.

The implementation should not be used to configure protection equipment, operate electrical infrastructure, or replace a formal protection study, commissioning procedure, manufacturer documentation, or utility engineering standard.
