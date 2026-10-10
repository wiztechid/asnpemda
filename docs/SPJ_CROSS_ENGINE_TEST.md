# SPJ same-input cross-engine gate

Node.js runs the actual browser JavaScript under a simulated DOM and calls the Python decision engine with the **same transaction payload**. Twelve cases cover UP/GU, LS, KKPD, marketplace, and three transaction dates. The test compares verification state, null tax output, KKPD evidence checks, marketplace platform checks, and historical effective-date flags.

This is **not a real browser test** and does not establish complete legal correctness, accessibility, or full checklist-text equivalence. No tax rates or automatic calculations are enabled. Status: PRE_RELEASE / HOLD.
