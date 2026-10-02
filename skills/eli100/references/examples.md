# Examples

The output blocks below pass `scripts/check_ste.py` in the mode shown. Match the shape. Do not copy the facts into a different document.

## Procedure (full)

Input:

```
Before acceptance of the unit, rotate the cover until the jacks marked + and - are accessible, then commence the specified test procedure to make sure everything is functioning correctly.
```

Output (`--mode full --kind procedure`):

```
Turn the cover until you get access to the jacks.
The jacks have a + mark and a - mark.
Before you accept the unit, do the specified test.
```

## Description (full)

Input:

```
The hydraulic pump is responsible for sending fluid to the actuator which in turn moves the control surface, but if the filter is blocked the pump can't send fluid and consequently the surface won't move.
```

Output (`--mode full --kind description`):

```
The pump sends fluid to the actuator.

The actuator moves the surface.

When the filter is blocked, the pump does not send fluid.

Then the surface does not move.
```

## Safety (full)

Input:

```
Be careful around the hot pump or you might get burned and also the tool could be damaged.
```

Output (`--mode full --kind safety`):

```
Warning: Do not touch the pump.

The pump is hot. Contact can burn you.

Caution: Do not leave the tool on the pump.

The heat can damage the tool.
```

## Plan (soften)

Input:

```
We need to leverage the existing API to seamlessly facilitate onboarding before users commence the payment flow, and we should optimize the error handling so it's robust.
```

Output (`--mode soften --kind description`):

```
Use the current API for user setup.

Show each error cause in the payment flow.

Start user setup before the payment flow starts.

Out of scope: a new payment API.
```
