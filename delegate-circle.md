---
title: Delegate Circle
---

A pattern for coordination between several teams or circles

## Motivation for using this pattern

* several teams have overlapping domains or dependencies
* there's a need to exchange learning about these domains
* there's a need for coordination and decision making

## Overview

1. several teams identify a shared domain where they cant make decisions autonomously
1. each team selects  a delegate (e.g. through *Role Selection*)
1. delegates form a functional team which coordinates exchange and decisions about  the shared domain
1. delegates inform their team mates of pending decisions and outcome of delegate circle activities, and bring feedback to the delegate circle

Delegates will be re-elected after their term expires. If a team does not feel represented well, they can recall the delegate and send a new one.

![A Delegate Circle Consists of Delegates from other Circles](img/structural-patterns/delegate-circle.png)

## Related Patterns

* [Representative](representative.md)
* [Consent Decision Making](consent-decision-making.md) for decision making in the delegate circle
* [Governance Meeting](governance-meeting.md)
* [Governance Backlog](governance-backlog.md)
* [Role Selection](role-selection.md)
