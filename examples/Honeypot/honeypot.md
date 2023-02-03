# Honeypot

<!--- # NOTICE

# This software was produced for the U.S. Government under contract FA8702-23-C-0001,

# and is subject to the Rights in Data-General Clause 52.227-14, Alt. IV (DEC 2007)

# ©2023 The MITRE Corporation. Published under the Linux Foundation’s Cyber Domain Ontology project’s Apache 2 license.

# Released under MITRE PRS 18-4297.
-->


This simple example outlines how to describe a simple and bare example of planning a honeypot deception operation.

In the `Narrative` example, you will see how to narrative and story concepts such as:
- `engage:Narrative`
- `engage:Storyline`
- `engage:PlannedEvent`
- `engage:stageAttackSurface`
- `engage:Stage`
	
Each `PlannedEvent` has an `eventContext` ObjectProperty that directly connects to an action class from the uco's base class `Action` such as:
- `engage:Alert`
- `engage:Access`
	
The UCO `action` has properties which we are interested in:
- `performer` - the `Identity` that performs the action
- `object` - the `UcoObject` of which the action is applied upon or to.

The class `engage:Alert` has an `alertContext` ObjectProperty that is used to describe the contents of an alert between two identities or objects.


In the `Operational` example, you will see how operational events pan out that leverage other `UcoObject` properties such as:
- `startTime`
- `endTime`
	
There are tradeoffs between merging the `PlannedEvent(s)` from the narrative and planning phase of an operation with reports from its operation.
1. Merging events with `PlannedEvents` can allow users to determine how successful an operation followed a storyline
2. Keeping events separated can allow users to fully scope the duration of a deception from its conception to its analysis if desired






