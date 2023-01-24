from pyshacl import validate
import rdflib
import sys
import argparse


def validate_graphs(eg_graph, egtyp, og_graph, ogtyp):
       # Graph that needs to be compared, it could be an example
      example_graph = rdflib.Graph()
      example_graph.parse(eg_graph,format=egtyp)
      ontology_graph = rdflib.Graph()
      ontology_graph.parse(og_graph, format=ogtyp)
      r = validate(example_graph,
            shacl_graph=ontology_graph,
            ont_graph=ontology_graph, # this could be UCO
            inference='rdfs',
            abort_on_first=False,
            allow_infos=False,
            allow_warnings=False,
            meta_shacl=False,
            advanced=False,
            js=False,
            debug=False)
      return r

def diff_graphs(eg_graph, egtyp, og_graph, ogtyp, ignore_bnodes=False):
    print("-")
    eg_subject, eg_predicate, eg_object = [],[],[]
    og_subject, og_predicate, og_object= [],[],[]
    
    example_graph = rdflib.Graph()
    example_graph.parse(eg_graph,format=egtyp)
    
    ontology_graph = rdflib.Graph()
    ontology_graph.parse(og_graph, format=ogtyp)

    try:
            for subject, predicate, rdf_object in example_graph:
                if ignore_bnodes is True:
                    if isinstance(subject, rdflib.term.BNode) or isinstance(predicate, rdflib.term.BNode) or \
                            isinstance(object, rdflib.term.BNode):
                        pass
                    else:
                        eg_subject.append(subject)
                        eg_predicate.append(predicate)
                        eg_object.append(rdf_object)
                else:
                    eg_subject.append(subject)
                    eg_predicate.append(predicate)
                    eg_object.append(rdf_object)

    except AttributeError as attr_err:
            print("[iter] Error parsing graph: %s" % str(attr_err))

    try:
            for subject, predicate, rdf_object in ontology_graph:
                if ignore_bnodes is True:
                    if isinstance(subject, rdflib.term.BNode) or isinstance(predicate, rdflib.term.BNode) or \
                            isinstance(object, rdflib.term.BNode):
                        pass
                    else:
                        og_subject.append(subject)
                        og_predicate.append(predicate)
                        og_object.append(rdf_object)
                else:
                    og_subject.append(subject)
                    og_predicate.append(predicate)
                    og_object.append(rdf_object)

    except AttributeError as attr_err:
            print("[iter] Error parsing graph: %s" % str(attr_err))

    # Check if the predicate in examples are in the Ontology or not
    for predicate in eg_predicate:
        if (predicate in og_predicate)\
            or (predicate in og_subject) \
            or (predicate in og_object):
            print(f"Match {predicate} in both Example and in Onto")
        else:
            print(f"[XX] {predicate} is in Example but not in Onto")
    
    # Check if the predicate in examples are in the Ontology or not
    for subject in eg_subject:
        if (subject in og_predicate)\
            or (subject in og_subject) \
            or (subject in og_object):
            print(f"Match {subject} in both Example and in Onto")
        else:
            print(f"[XX] {subject} is in Example but not in Onto")



        

if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    try:
        parser.add_argument("-og","--ontologygraph",required=True,help="Specify the main Ontology Graph")
        parser.add_argument("-ogtyp","--ontographtype", required=True, help="Specify the type of the Ontology Graph", default="turtle")
        parser.add_argument("-eg","--examplegraph",required=True,help="Specify the Example Graph")
        parser.add_argument("-egtyp","--examplegraphtype", required=True, help="Specify the type of the Example Graph", default="turtle")
        parser.add_argument("-val", required=False, help="Must be true to perform validation", default=True)
        parser.add_argument("-diff", required=False, help="Must be true to perform RDFDiff ")
    except argparse.ArgumentError as err:
        print(f"{err} must be there")
    finally:
        parser.parse_args()
        args=parser.parse_args()                                                                                                                                                                                                                                                      


        


    #eg_graph="case5sub.ttl"
    #og_graph="case5.ttl"

    if args.val:
        conforms, results_graph, results_text = \
            validate_graphs(args.ontologygraph,
                            args.ontographtype , 
                            args.examplegraph, 
                            args.examplegraphtype)
        print("\n\n Conforms: ", conforms)
        print("\n\n Results graph \n\n", results_graph)
        print("\n\n results_text: ",results_text)
    if args.diff:
        diff_graphs(args.ontologygraph, 
                        args.ontographtype,
                        args.examplegraph, 
                        args.examplegraphtype)
    
