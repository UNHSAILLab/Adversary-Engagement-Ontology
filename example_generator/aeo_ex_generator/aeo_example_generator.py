import os
import openai
import json
import rdflib


class ExampleGenerator:
    def __init__(self):
        self.ontologies = {}
        self.ontology_files = []
        self.rules = {}
    def add_ontology(self, onto):
        if onto in self.ontology_files:
            raise ValueError("Ontology file already exists.")
        else:
            onto_data = self.get_ontology_file(onto)
            if onto_data:
                self.ontology_files.append(onto)
                self.ontologies[onto] = self.get_ontology_file(onto)
                self.rules[onto] = self.generate_rules(onto)
            else:
                raise ValueError("Ontology file error.")
    def get_ontology_file(self,filename):
        text = ""
        if os.path.isfile(filename):
            with open(filename,'r') as f:
                text = f.read()
            f.close()
            return text
        else:
            raise ValueError("Invalid filename.")
    def ChatGPTTextSplitter(self,text):
        """Splits text in smaller subblocks to feed to the LLM"""
        prompt = f"""The total length of content that I want to send you is too large to send in only one piece.

    For sending you that content, I will follow this rule:

    [START PART 1/10]
    this is the content of the part 1 out of 10 in total
    [END PART 1/10]

    Then you just answer: "Instructions Sent."

    And when I tell you "ALL PARTS SENT", then you can continue processing the data and answering my requests.
        """
        if type(text) == str:
            textsize = 12000
            blocksize = int(len(text) / textsize)
            if blocksize > 0:
                yield prompt

                for b in range(1,blocksize+1):
                    if b < blocksize+1:
                        prompt = f"""Do not answer yet. This is just another part of the text I want to send you. Just receive and acknowledge as "Part {b}/{blocksize} received" and wait for the next part.
                [START PART {b}/{blocksize}]
                {text[(b-1)*textsize:b*textsize]}
                [END PART {b}/{blocksize}]
                Remember not answering yet. Just acknowledge you received this part with the message "Part {b}/{blocksize} received" and wait for the next part.
                        """
                        yield prompt
                    else:
                        prompt = f"""
                [START PART {b}/{blocksize}]
                {text[(b-1)*textsize:b*textsize]}
                [END PART {b}/{blocksize}]
                ALL PARTS SENT. Now you can continue processing the request.
                        """
                        yield prompt
            else:
                yield text
        elif type(text) == list:
            yield prompt

            for n,block in enumerate(text):
                if n+1 < len(text):
                    prompt = f"""Do not answer yet. This is just another part of the text I want to send you. Just receive and acknowledge as "Part {n+1}/{len(text)} received" and wait for the next part.
            [START PART {n+1}/{len(text)}]
            {text[n]}
            [END PART {n+1}/{len(text)}]
            Remember not answering yet. Just acknowledge you received this part with the message "Part {n+1}/{len(text)} received" and wait for the next part.
                    """
                    yield prompt
                else:
                    prompt = f"""
            [START PART {n+1}/{len(text)}]
            {text[n]}
            [END PART {n+1}/{len(text)}]
            ALL PARTS SENT. Now you can continue processing the request.
                    """
                yield prompt

    def send_ontology(self):
        ontology = ""
        if len(self.ontologies) > 0:
            for k,v in self.ontologies.items():
                ontology+=v+"\n"
            print("Sending Ontology in Parts")
            for i in self.ChatGPTTextSplitter(ontology):
                print(self.llm_api(i))
        else:
            raise ValueError("No loaded ontology to send.")
    def llm_api(self,prompt,model="gpt-3.5-turbo"):
        messages = [{
            "role":"user",
            "content":prompt
        }]
        res = openai.ChatCompletion.create(model=model,messages=messages,temperature=0)
        return res.choices[0].message['content']
    
    def generate_rule(self,onto=None):
        """Raw rule string of AEO."""
        v = """Remember make a json-ld format example that only uses classes and properties terms from Adversary Engagement Ontology, Unified Cyber Ontology. 

Each engagement:Narrative has property:
    engagement:hasStoryline connects to an engagement:Storyline
Each engagement:Storyline has property:
    engagement:hasEvent connects to a uco-types:Thread
Each uco-types:Thread has properties:
    co:element contains all engagement:PlannedEvents
    co:item contains all uco-types:ThreadItem one each for each engagement:PlannedEvent.
    co:size
    uco-types:threadOriginItem is the uco-types:ThreadItem for the first engagement:PlannedEvent
    uco-types:threadTerminalItem is the uco-types:ThreadItem for the last engagement:PlannedEvent
Each co:size has properties:
    @type as xsd:nonNegativeInteger
    @value which is the number of uco-types:ThreadItem
Each uco-types:ThreadItem has property:
    co:itemContent is the engagement:PlannedEvent
    optional uco-types:threadNextItem is the next uco-types:ThreadItem for the next engagement:PlannedEvent if there is one,
    optional uco-types:threadPreviousItem is the previous uco-types:ThreadItem for the previous engagement:PlannedEvent if there is one
Each engagement:PlannedEvent has property:
    engagement:eventContext connects to one engagement action has property @type one of the following:
        engagement:Access
        engagement:Alert
        engagement:Beacon
        engagement:Deploy
        engagement:Obfuscate
        engagement:Respond
Each engagement action has properties:
    @type is the action
    uco-core:performer
    uco-core:object connects to one of the following engagement deception object denoted as "EDO" objects:
        engagement:Honeypot
        engagement:Honeytoken
        engagement:Breadcrumb
        engagement:BreadcrumbTrail
        engagement:LureObject
        engagement:HoneyObject
        engagement:Decoy
        engagement:DataSource
Each "EDO" object has properties:
    engagement:hasCharacterization connects to a uco-core:UcoObject
    objective:hasObjective with @type objective:Objective and @id with one of the following instances:
            objective:CommandAndControl
            objective:CredentialAccess
            objective:DevelopResource
            objective:Discover
            objective:EscalatePrivilege
            objective:Evade
            objective:Execute
            objective:Exfilitrate
            objective:GainInitialAccess
            objective:Impact
            objective:MoveLaterally
            objective:Persist
            objective:Reconnaissance
            objective:Affect
            objective:Collect
            objective:Detect
            objective:Direct
            objective:Disrupt
            objective:Elicit
            objective:Expose
            objective:Motivate
            objective:Plan
            objective:Prepare
            objective:Prevent
            objective:Reassure
            objective:Analyze
            objective:Deny
            objective:ElicitBehavior
            objective:Lure
            objective:TimeSink
            objective:Track
            objective:Trap
        uco-core:name is the objective
All people have property:
    @type is uco-identity:Person
    uco-core:hasFacet that connects to one of the following: 
        uco-identity:SimpleNameFacet which has the property:
            uco-identity:familyName
            uco-identity:givenName
Each uco-core:Role has properties:
        @id is the role
        uco-core:name is the role
Each uco-core:Role there is a uco-core:Relationship with properties:
    uco-core:kindofRelationship is "has_Role"
    uco-core:source connects to the person who has the role
    uco-core:target connects to uco-core:Role
Each engagement:BreadcrumbTrail has property:
    engagement:hasBreadcrumb connects to uco-types:Thread
        This uco-types:Thread has property:
            co:element contains all engagement:Breadcrumb that belong to this engagement:BreadcrumbTrail
            co:item contains all uco-types:ThreadItem one each for each engagement:Breadcrumb
            co:size
            uco-types:threadOriginItem is the uco-types:ThreadItem for the first engagement:Breadcrumb belonging to this engagement:BreadcrumbTrail
            uco-types:threadTerminalItem is the uco-types:ThreadItem for the last engagement:Breadcrumb belonging to this engagement:BreadcrumbTrail
Each engagement:Breadcrumb has the properties:
    engagement:hasCharacterization which connects to a uco-core:UcoObject with the property:
        uco-core:description which describes the object characterizing the breadcrumb
All classes must include property:
    @type is the class
    @id is a unique identifier
    
If namespace "engagement" prefix is used then https://ontology.adversaryengagement.org/ae/engagement#
If namespace "objective" prefix is used then https://ontology.adversaryengagement.org/ae/objective#
If namespace "role" prefix is used then https://ontology.adversaryengagement.org/ae/role#
If namespace "identity" prefix is used then https://ontology.adversaryengagement.org/ae/identity#
If namespace "uco-core" prefix is used then https://ontology.unifiedcyberontology.org/uco/core#
If namespace "uco-types" prefix is used then https://ontology.unifiedcyberontology.org/uco/types#
If namespace "uco-role" prefix is used then https://ontology.unifiedcyberontology.org/uco/role#
        """
        return v
    
    def generate_continue(self):
        v = """
        continue
        """
        return v
    
    def raw_prompt(self,description):
        
        def run(val):
            prompt = f"""Give me a full json-ld format example for the following scenario:
            {description}

            {"".join(val)}
            """
            for i in self.ChatGPTTextSplitter(prompt):
                res = self.llm_api(i)
            return res
#             return json.loads(res)
        res_val =  run(self.generate_rule())
        #res_val =  run(self.generate_rules())
        try:
            val = json.loads(res_val)
            return val
        except:
            #the response was cut off, prompt for the continuation.
            data = []
            data.append(res_val)
            while True:
                res = self.llm_api(self.generate_continue())
                data.append(res)
                try:
                    full = "".join(data)
                    return json.loads(full)
                except:
                    pass
                     
        return None
    
    def get_ns(self,string):
        return string.split(":")[0]

    
    def prompt(self,description):
        res = self.raw_prompt(description)
        
        #include only relevent namespaces
        prefixes = []

        def is_nested(LIST):
            if type(LIST) == list:
                for JSON in LIST:
                    for key in JSON.keys():
                        if type(JSON[key]) == dict:
                            is_nested(JSON[key])
                    if '@type' in JSON.keys():
                        prefixes.append(self.get_ns(JSON['@type']))
            else:
                JSON = LIST
                for key in JSON.keys():
                    if type(JSON[key]) == dict:
                        is_nested(JSON[key])
                if '@type' in JSON.keys():
                    prefixes.append(self.get_ns(JSON['@type']))
                    
        
        is_nested(res['@graph'])
        prefixes = set(prefixes)
        
        new_prefixes = {}
        for prefix in prefixes:
            if prefix in res['@context']:
                new_prefixes[prefix] = res['@context'][prefix]
        
        res['@context'] = new_prefixes
 
        return res
