## Scenario: 
A low interaction honeypot dynamically reallocates resources to become a high interaction honeypot when an adversary interacts with the low interaction honeypot.

1. Add appropriate prefixes


```python
{ 
    "__AE__": "AE_2022_01_01", 
    "@context": { 
        "kb": "http://example.org/kb#", 
        "@vocab": "http://example.org/ontology/local#", 
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#", 
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#", 
        "xsd": "http://www.w3.org/2001/XMLSchema#",
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
    }, 
```

2. Add Bundle object. Bundle consists of the low interaction honeypot, the high interaction honeypot, and the time trigger which converted low to high.


```python
    "@id": "kb:fluiddeception_02_02_2022", 
    "@type": "uco-observable:Bundle", 
    "uco-core:description": "Honeypot changes from low interaction to high interaction once an adversary ping sweeps the honeypot.", 
```


```python
    "uco-core:object": [ 
```

2.1. High interaction honeypot with a deployment timestamp matching that of the low honeypot timestamp trigger. "convertsInto" describes the objectproperty between the individual instance of the low interaction honeypot with the high interaction honeypot


```python
        { 
            "@id": "kb:hhoneypot", 
            "@type": "engage:honeypot", 
            "uco-core:hasFacet": [
            {
                "@type": "engage:honeypotFacet",
                "engage:convertsInto": [
                    {
                    "@id":"kb:lhoneypot",
                    "@type":"engage:honeypot",
                    "uco-core:hasFacet":[{
                        "@type":"engage:honeypotFacet",
                        "time:hasTime": [
                                        {
                                        "time:Timestamp": "01-01-2022",
                                        "time:TimeType": "deployment"
                                        },
                                        {
                                        "@id": "lowToHigh1",
                                        "time:Timestamp": "01-02-2022",
                                        "time:TimeType": "trigger"
                                        }
                                    ],
                        "engage:honeypotInteractionType": "Low"
                    }
                ],
                "time:Time": [
                    {
                    "@id": "lowToHigh1",
                    "time:Timestamp": "01-02-2022",
                    "time:TimeType": "deployment"
                    }
                ],
                "engage:deployEntity": [
                {
                    "@id" : "kb:ex1",
                    "@type": "role:defender",
                    "engage:teamIdentifier": "team-01",
                    "engage:teamMemberIdentifier": "btm-01"
                }
                ],
                "role:hasTargetEntity": [
                {
                    "@id" : "kb:ex1",
                    "@type": "role:Team",
                    "engage:teamIdentifier": "APTZ",
                    "engage:teamMemberIdentifier": "APTZ"
                }
                ],
                "objective:hasObjective": [
                  {
                    "@id": "kb:obj1",
                    "@type": "objective:trap"
                  }
                ],
                "engage:hasStagedAttackMethod": [
                    {
                        "@id": "kb:sae1",
                        "@type": "attack:Attack",
                        "uco-core:description": "Honeytoken credential access.",
                        "technique": "T1555.1",
                        "tactic": "Credential Access"
                    }
                    ],
            "engage:honeypotInteractionType": "High",
            "engage:hasStage": [
              {
                    "@id": "kb:hhp-1",
                    "@type": "uco-observable:AndroidDevice",
                    "uco-core:hasFacet": [
                    {
                        "@id": "kb:ad-hp",
                        "@type": "uco-observable:AndroidDeviceFacet",
                        "uco-core:description": "Honeypot Android device.",
                        "uco-observable:androidFingerprint": "13141516",
                        "uco-observable:androidID": "android-01m4",
                        "uco-observable:androidVersion":"1.0.2"
                        }
                    ]
              }],
            "engage:hasStagedAttackSurface": [
                {
                    "@id": "kb:sae1",
                    "@type": "uco-observable:port",
                    "uco-core:description": "Port 22 has ssh service running that can be accessed via the honeytoken credentials.",
                    "uco-core:hasFacet": [
                    {
                        "@type": "uco-observable:port",
                        "uco-observable:port": 22
                    }
                    ]
                }
            ],
            "engage:hasStagedExit": [
                    {
                        "@type": "engage:Exit",
                        "uco-core:description": "Honeypot is meant to trap adversaries so there is not available exit."
                    }
                    ],
            "engage:hasHoneyObject":[
                    {
                        "@id": "ht-1",
                        "@type": "engage:honeyToken",
                        "engage:honeyTokenIdentifier": "honeytoken-1",
                        "uco-core:hasFacet": [
                        {
                            "@id": "ht-accountcred1",
                            "@type": "engage:honeyTokenFacet",
                            "uco-core:object": [
                              {
                                "uco-observable:Credential": "HarryPeter01"
                              }
                            ]
                        }
                        ]
                    }
            ] 
            }
            ]
}
]
}
```
