
# Protection Philosophy

## 1. Purpose

This project develops a simulated protection scheme for a fictional
132/33 kV digital substation.

The objective is to demonstrate the engineering process from system
definition and protection principles through to IED logical modelling,
protection coordination and functional testing.

All system parameters, settings and event data used in this project are
synthetic and are intended for educational and portfolio purposes only.

---

## 2. Protection Objectives

The protection system is designed according to the following principles:

- Selectivity
- Sensitivity
- Speed
- Reliability
- Security
- Backup protection

The primary protection system should isolate only the affected section
of the network while maintaining supply to healthy sections where possible.

---

## 3. Transformer Protection

The main transformer is protected against internal and external faults.

Primary protection functions include:

- 87T - Transformer Differential Protection
- 50/51 - Phase Overcurrent Protection
- 50N/51N - Earth Fault Protection
- 49 - Thermal Overload Protection

Backup protection is provided through time-delayed overcurrent elements.

---

## 4. Feeder Protection

Each 33 kV feeder is protected using:

- 50 - Instantaneous Phase Overcurrent
- 51 - Time Overcurrent
- 50N - Instantaneous Earth Fault
- 51N - Time Earth Fault

The feeder protection is expected to operate before upstream backup
protection for faults occurring within the feeder protection zone.

---

## 5. Protection Coordination

Protection settings will be developed to achieve coordination between:

1. Feeder protection
2. Transformer backup protection
3. Upstream protection

The project will use simulated fault scenarios to evaluate selectivity
and backup operation.

---

## 6. Digital Substation Concepts

The project models selected IEC 61850 concepts, including:

- Logical Nodes
- Logical Devices
- Data Objects
- GOOSE messaging concepts
- Protection-to-trip logic

These concepts will be progressively introduced during the IED
configuration and protection logic phases.
