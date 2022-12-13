# Honeypot Example

## Scenario:
This example instantiates a UCO bundle of objects relating to the deployment of a honeypot in jsonld format. 

A honeypot is instantiated by teamX for an APT group called APTZ with the desired tactic of credential access and specific method of entrance through a honeytoken.

1. Add relevant UCO and AE prefixes


```python
"@context": { 
    "kb": "http://example.org/kb#", 
    "@vocab": "http://example.org/ontology/local#", 
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#", 
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#", 
    "xsd": "http://www.w3.org/2001/XMLSchema#" 
    "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/", 
    "uco-configuration": "https://ontology.unifiedcyberontology.org/uco/configuration/", 
    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/", 
    "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/", 
    "uco-location": "https://ontology.unifiedcyberontology.org/uco/location/", 
    "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/", 
    "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/", 
    "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/", 
    "uco-vocabulary": "https://ontology.unifiedcyberontology.org/uco/vocabulary/", 
    "engage": "https://ontology.adversaryengagement.org/ae/engage/",
    "identity": "https://ontology.adversaryengagement.org/ae/identity/",
    "role": "https://ontology.adversaryengagement.org/ae/role/",
    "attack": "https://ontology.adversaryengagement.org/ae/attack/"
}
```

2. The bundle instantiation and description


```python
    "@id": "kb:honeypot_02_02_2022", 
    "@type": "uco-observable:Bundle", 
    "uco-core:description": "Honeypot deployed onto network by XTeam was accessed by honey token user-credentials.", 
    "uco-core:object": [ ...]
```

3. Honeypot object instantiation


```python
"@id": "kb:honeypot1", 
"@type": "engage:honeypot", 
"uco-core:hasFacet": [...]
```

3.1 Attach a honeypotFacet or a honeyObjectFacet.


```python
"@type": "engage:honeypotFacet"
```

3.2. Time is treated as a namespace / domain object which has a TimeType and a Unit property. Timestamp inherits these properties to be able to be used as an object. time:Time is a property of the honeypotFacet / honeyObjectFacet


```python
"time:hasTime": [
    {
    "time:Timestamp": "01-01-2022",
    "time:TimeType": "deployment"
    },
    {
    "time:Timestamp: "02-02-2022",
    "time:TimeType": "trigger"
    },
```

3.3. deployEntity is a property that is either an identity or a role. the entity/team that deployed/performed has an unique ID.


```python
"engage:deployEntity": [
{
    "@id" : "kb:ex1",
    "@type": "role:defender"
    "engage:teamIdentifier": "team-01"
    "engage:teamMemberIdentifier": "btm-01"
}
],
```

3.4. engage:TargetEntity is an optional property of honeypot which specifies an intended target entity or team at which it was deployed for.


```python
"role:hasTargetEntity": [
{
    "@id" : "kb:ex1",
    "@type": "role:adversary"
    "engage:teamIdentifier": "APTZ"
    "engage:teamMemberIdentifier": "APTZ"
}
],
```

3.5. objective:Objective is a property which is the immediate or long-term/mission goal relating to the scope and lifespan of the honeypot. objective:trap is one type of standard objectives for adversary engagement.


```python
"objective:hasObjective": [
    "@id": "kb:obj1",
    "@type": "objective:trap"
],
```

3.6. stagedAttackMethod is a property which preferences the expected TTP / attack methodology the deploying team/entity believes a targetEntity/team will use to gain access to the honeypot


```python
"engage:hasStagedAttackMethod": [
    {
        "@id": "kb:sae1",
        "@type": "attack:Attack"
        "uco-core:description": "Honeytoken credential access."
        "technique": "T1555.1"
        "tactic": "Credential Access"
    }
    ],
```

3.7. Conventionally, honeypots are often described as high/low interactive which determines both the resource expenditure and expectations for a honeypot's usage in an operation.


```python
"engage:honeypotInteractionType": "High",
```

3.8. A stage is a UcoObject or Bundle which describes the desired perception a deploying team/entity has for a honeypot to a targetEntity/team. Here we can express it simply as an uco-observable android device with its standard usage of a facet.


```python
"engage:hasStage": [
        "@id": "kb:hhp-1",
        "@type": "uco-observable:AndroidDevice",
        "uco-core:hasFacet": [
        {
            "@id": "kb:ad-hp",
            "@type": "uco-observable:AndroidDeviceFacet"
            "uco-core:description": "Honeypot Android device."
            "uco-observable:androidFingerprint": "13141516",
            "uco-observable:androidID": "android-01m4",
            "uco-observable:androidVersion:"1.0.2"
            }
        ]
    ],
```

3.9. stagedAttackSurface is the property which more specifically describes a component of the stage which the stagedAttackMethod directly applies to. This is useful for describing all expected methods of entry into a honeypot as objects themselves than through techniques.


```python
"engage:hasStagedAttackSurface": [
    {
        "@id": "kb:sae1",
        "@type": "uco-observable:port"
        "uco-core:description": "Port 22 has ssh service running that can be accessed via the honeytoken credentials."
        "uco-core:hasFacet": [
        {
            "@type": "uco-observable:port"
            "uco-observable:port": 22
        }
        ]
    }
],
```

3.10. stageExit is an optional property in which trapping an adversary within a honeypot is not the end-goal. Instead, this can be used to describe the sequences of entering/exiting from stage to stage.


```python
"engage:hasStagedExit": [
        {
            "@type": "engage:Exit"
            "uco-core:description": "Honeypot is meant to trap adversaries so there is not available exit."
        }
        ],
```

3.11. HoneyObject as a property of a honeypot refers to any "props" and necessary supplemental deception objects which is directly related to this honeypot. In this case, the desired method of entry was to use honeyToken credentials. Normally we would use something as "CredentialFacet" to attach as a facet to the honeyToken, but UCO treats Credential as a property so we attach the object to honeyTokenFacet.


```python
"engage:hasHoneyObject":[
        {
            "@id": "ht-1",
            "@type": "engage:honeyToken",
            "engage:honeyTokenIdentifier": "honeytoken-1"
            "uco-core:hasFacet": [
            {
                "@id": "ht-accountcred1",
                "@type": "engage:honeyTokenFacet",
                "uco-core:object": [
                    "uco-observable:Credential": "HarryPeter01"
                ]
            }
            ]
        }
] 		
}
]
```
