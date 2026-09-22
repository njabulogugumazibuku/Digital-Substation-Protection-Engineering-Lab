# Protection Sequence & Fault Isolation

## 1. Purpose

This document describes the protection operating sequence for the simulated NorthGrid 132/33 kV Digital Substation.

The objective is to show how a fault progresses through the protection system from initial measurement through primary protection, circuit-breaker operation, breaker-failure detection, and backup isolation.

The model uses synthetic system data and is intended for educational and portfolio purposes.

## 2. Protection System Sequence

The overall protection sequence is:

                         FAULT
                           │
                           ▼
                    ┌─────────────┐
                    │    MMXU1    │
                    │ Measurement │
                    └──────┬──────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Protection       │
                  │ Decision Engine  │
                  └────────┬─────────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
       PHASE FAULT                  EARTH FAULT
             │                           │
        ┌────┴────┐                 ┌────┴────┐
        │         │                 │         │
       51        50                51N       50N
      PTOC1     PTOC2             PTEF1     PTEF2
        │         │                 │         │
        └────┬────┘                 └────┬────┘
             │                           │
             └─────────────┬─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    PTRC1    │
                    │ Trip Logic  │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    XCBR1    │
                    │    CB-301   │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │             │
                  OPENS          FAILS
                    │             │
                    ▼             ▼
              FAULT CLEARED     50BF
                                  │
                                  ▼
                              CB-201
                                  │
                                  ▼
                           FAULT ISOLATED

## 3. Stage 1 — Fault Detection

The protection system first receives a current measurement through the simulated measurement function:

MMXU1

The measured current is then evaluated against the configured protection thresholds.

The model uses different decision paths depending on the fault type.

Phase fault
Current
   │
   ▼
PTOC1 / PTOC2
Earth fault
Current
   │
   ▼
PTEF1 / PTEF2

## 4. Stage 2 — Protection Element Selection

The protection decision engine determines which protection element should operate.

Phase Overcurrent

The simulated phase protection uses:

51 pickup = 1200 A
50 pickup = 5000 A

The decision path is:

Current < 1200 A
        │
        ▼
   No operation

1200 A < Current < 5000 A
        │
        ▼
       51
     PTOC1
        │
        ▼
 IEC Standard Inverse

Current ≥ 5000 A
        │
        ▼
       50
     PTOC2
        │
        ▼
Instantaneous operation
Earth Fault

The simulated earth-fault protection uses:

51N pickup = 600 A
50N pickup = 3000 A

The decision path is:

Current < 600 A
        │
        ▼
   No operation

600 A < Current < 3000 A
        │
        ▼
      51N
     PTEF1
        │
        ▼
 IEC Standard Inverse

Current ≥ 3000 A
        │
        ▼
      50N
     PTEF2
        │
        ▼
Instantaneous operation

##  5. Stage 3 — Trip Conditioning

When a protection element operates, its output is passed to:

PTRC1

PTRC1 represents the trip-conditioning layer between the protection functions and the circuit breaker.

The simplified sequence is:

Protection Element
        │
        ▼
      PTRC1
        │
        ▼
Trip Command
        │
        ▼
      XCBR1

This architecture keeps protection decision-making separate from breaker control.

##  6. Stage 4 — Circuit-Breaker Operation

The simulated feeder breaker is:

CB-301

When the breaker successfully responds to the trip command:

Protection Operates
        │
        ▼
    PTRC1 Trip
        │
        ▼
    CB-301 Opens
        │
        ▼
    Fault Cleared

This represents successful primary protection.

##  7. Stage 5 — Breaker Failure

Protection operation does not automatically guarantee successful fault interruption.

The model therefore includes a simplified breaker-failure function:

50BF

If CB-301 fails to open after receiving a valid trip command, the breaker-failure sequence begins.

Primary Protection
        │
        ▼
    Trip CB-301
        │
        ▼
 CB-301 Fails
        │
        ▼
       50BF
        │
        ▼
Breaker-Failure Timer
        │
        ▼
Backup Trip

The simulated breaker-failure timer is:

0.300 s

## 8. Stage 6 — Backup Isolation

When the breaker-failure timer expires, the backup trip is issued to:

CB-201

The simplified sequence is:

CB-301 Fails
      │
      ▼
     50BF
      │
      ▼
0.300 s Timer
      │
      ▼
 Backup Trip
      │
      ▼
   CB-201
      │
      ▼
Fault Isolated

CB-201 therefore provides a backup isolation path when the feeder breaker fails.

## 9. Example — 1500 A Earth Fault

A representative test case uses:

Fault Type   : Phase-to-earth
Fault Current: 1500 A
Breaker      : CB-301
Breaker State: Failed to open

The protection sequence is:

1500 A Fault
      │
      ▼
    MMXU1
      │
      ▼
    PTEF1
      │
      ▼
     51N
      │
      ▼
  OPERATE
      │
      ▼
  ~0.606 s
      │
      ▼
    PTRC1
      │
      ▼
 Trip CB-301
      │
      ▼
CB-301 FAILS
      │
      ▼
     50BF
      │
      ▼
 0.300 s Timer
      │
      ▼
    CB-201
      │
      ▼
Fault Isolated

The test demonstrates that the 51N element uses inverse-time operation rather than a fixed operating delay.

## 10. Example — 6000 A Phase Fault

A high-current phase fault uses:

Fault Type   : Phase-to-phase
Fault Current: 6000 A
Breaker      : CB-301
Breaker State: Failed to open

Because the current exceeds the 50 pickup:

6000 A
   │
   ▼
PTOC2
   │
   ▼
50 Phase Overcurrent
   │
   ▼
Instantaneous Trip
   │
   ▼
PTRC1
   │
   ▼
CB-301
   │
   ▼
Breaker Failure
   │
   ▼
50BF
   │
   ▼
CB-201
   │
   ▼
Fault Isolated

This demonstrates the high-current instantaneous protection path and subsequent breaker-failure backup.

## 11. Protection Zones

The simplified protection philosophy can be represented as:

             132 kV
                │
              CB-101
                │
        ┌───────┴────────┐
        │ Transformer T1 │
        └───────┬────────┘
                │
              CB-201
                │
        ┌───────┴────────┐
        │    33 kV BUS   │
        └───────┬────────┘
                │
              CB-301
                │
                ▼
             Feeder 1

The feeder protection is primarily responsible for faults within its protected feeder zone.

The transformer backup protection provides a higher-level protection layer if the feeder protection path does not successfully clear the fault.

## 12. Primary vs Backup Protection

The protection architecture intentionally separates primary and backup functions.

Primary Protection
Fault
  ↓
Feeder IED
  ↓
50 / 51 / 50N / 51N
  ↓
PTRC1
  ↓
CB-301

The objective is selective and timely clearing of the feeder fault.

Breaker-Failure Backup
Primary Trip
     ↓
CB-301
     ↓
Failure
     ↓
50BF
     ↓
CB-201

The objective is to isolate the fault when the primary circuit breaker fails.

## 13. Engineering Principle

The key principle demonstrated by the simulation is:

Protection operation and fault interruption are separate events.

The protection IED can correctly detect a fault and issue a trip command while the circuit breaker may still fail to interrupt the fault.

Breaker-failure protection provides an additional layer of system security by initiating backup isolation when this occurs.

## 14. Current Model Limitations

The breaker-failure model is intentionally simplified.

It does not currently model:

detailed breaker contact feedback;
current supervision;
breaker mechanical operating time;
breaker interrupting time;
CT saturation;
communication delay;
protection relay measurement error;
detailed bus protection;
detailed transformer differential protection; or
physical IEC 61850 communication.

The current model therefore demonstrates the logical protection sequence rather than reproducing the complete behaviour of a physical substation.

## 15. Related Files

The protection sequence is implemented through:

04_protection_logic/
├── protection_engine.py
├── protection_decision.py
└── protection_sequence.py

The IED logical model is represented through:

03_ied_configuration/
├── ied_model.py
├── ied_configuration.py
└── ied_simulator.py

The verification is performed through:

06_testing/
├── test_ied_protection.py
├── test_coordination.py
├── coordination_sweep.py
└── test_breaker_failure.py

## 16. Summary

The simulated protection sequence connects:

Fault
  ↓
Measurement
  ↓
Protection Decision
  ↓
Protection Element
  ↓
Trip Conditioning
  ↓
Circuit Breaker
  ↓
Breaker Failure Detection
  ↓
Backup Protection
  ↓
Fault Isolation

This provides a systems-level representation of how protection functions interact with IED logic, circuit breakers, and backup protection within a simplified digital substation.