## # Protection Sequence & Fault Isolation

## 1. Purpose

This document describes the protection operating sequence for the simulated NorthGrid 132/33 kV Digital Substation.

The objective is to show how a fault progresses through the protection system from initial measurement through primary protection, circuit-breaker operation, breaker-failure detection, and backup isolation.

The model uses synthetic system data and is intended for educational and portfolio purposes.

---

# 2. Protection System Sequence

The overall protection sequence is:

```text
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