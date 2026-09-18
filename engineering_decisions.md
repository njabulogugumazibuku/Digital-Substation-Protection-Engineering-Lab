# Digital Substation Protection Engineering Lab
## Engineering Decisions & Design Rationale

---

## 1. Purpose

This document records the major engineering decisions made during development of the Digital Substation Protection Engineering Lab.

The purpose is to explain not only what was implemented, but why particular protection functions, settings, logical structures, coordination approaches, and modelling assumptions were selected.

The project is an educational simulation using synthetic data. It is not intended to reproduce or replace a utility protection study, protection-setting calculation, commissioning procedure, or physical IED configuration.

---

# 2. System Architecture Decision

## Decision

The project models a simplified 132/33 kV digital substation containing:

- 132 kV grid infeed;
- 50 MVA transformer;
- 33 kV bus;
- three outgoing feeders;
- feeder protection IEDs;
- transformer protection;
- circuit breakers; and
- digital-substation logical functions.

## Rationale

The architecture provides enough system complexity to demonstrate protection coordination and backup protection without requiring a complete transmission-network model.

The transformer provides the boundary between the upstream and downstream protection zones, while the outgoing feeders provide a practical environment for demonstrating primary and backup protection.

The architecture also creates a natural path toward future modelling of:

- IEC 61850 communication;
- GOOSE messaging;
- transformer protection;
- breaker failure;
- asset monitoring; and
- digital-substation automation.

---

# 3. Protection Philosophy Decision

## Decision

The feeder protection scheme uses:

- 50 — instantaneous phase overcurrent;
- 51 — time-delayed phase overcurrent;
- 50N — instantaneous earth-fault overcurrent;
- 51N — time-delayed earth-fault overcurrent.

The protection functions are represented using IEC 61850-inspired logical nodes:

| Function | Logical Node |
|---|---|
| 51 | PTOC1 |
| 50 | PTOC2 |
| 51N | PTEF1 |
| 50N | PTEF2 |
| Trip conditioning | PTRC1 |
| Breaker | XCBR1 |

## Rationale

The combination provides two layers of feeder overcurrent protection.

The instantaneous elements provide rapid operation for sufficiently high fault currents, while the inverse-time elements provide time-delayed protection for lower fault currents above pickup.

Separating these functions into logical nodes also creates a structure that resembles the functional decomposition used in digital substation systems.

The implementation is explicitly described as **IEC 61850-inspired**, rather than claiming standards-compliant IEC 61850 configuration.

---

# 4. Phase Overcurrent Decision

## Decision

The simulated feeder phase protection uses:

51 pickup = 1200 A
51 TMS    = 0.10

50 pickup = 5000 A
50 trip time = 0.05 s

Additional information:

t = TMS × k / ((I / Ip)^α - 1)
k = 0.14
α = 0.02