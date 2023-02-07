# This software was produced for the U.S. Government under contract FA8702-23-C-0001,
# and is subject to the Rights in Data-General Clause 52.227-14, Alt. IV (DEC 2007)
# ©2023 The MITRE Corporation. Published under the Linux Foundation’s Cyber Domain Ontology project’s Apache 2 license.
# Released under MITRE PRS 18-4297.

from pyshacl import validate
import rdflib
import sys
import argparse



def validate_graphs(eg_graph, egtyp, og_graph, ogtyp):
      """
      Validates the example graph against the Ontology graph.
      
      Parameters
      ----------
      example_graph: graph object to be validated
      egtyp: type of the graph object
      og_graph: graph object containing the SHACL shapes to validate with
      ogtyp: type of the ontology graph object 

      Returns
      -------
      results: a three-component tuple containing:
        conforms: a bool, indicating whether or not the example_graph conform to the og_graph
        result_graph: a Graph object built according to the SHACL specification's Validation Report structure
        results_text: python string representing a verbose textual representation of the Validation Report
    
      """
      
      example_graph = rdflib.Graph()
      example_graph.parse(eg_graph,format=egtyp)
      ontology_graph = rdflib.Graph()
      ontology_graph.parse(og_graph, format=ogtyp)
      uco_graph= rdflib.Graph()
      uco_graph.parse("uco.ttl", format="turtle")  
      results = validate(data_graph= example_graph,
            shacl_graph= ontology_graph,
            ont_graph=ontology_graph, 
            inference='rdfs',
            abort_on_first=False,
            allow_infos=False,
            allow_warnings=False,
            meta_shacl=False,
            advanced=False,
            js=False,
            debug=False)
      
      # Release the memory
      del example_graph
      del ontology_graph,uco_graph
      return results

def diff_graphs(eg_graph, egtyp, og_graph, ogtyp, ignore_bnodes=True):
    """
    Checks if the subjects and predicates in the example graphs are in the ontology graph or not
    Parameters
    ----------
    example_graph: A graph object to be validated
    egtyp: The type of the graph object
    og_graph: A graph object containing the SHACL shapes to validate with
    ogtyp:  The type of the ontology graph object

    Returns
    -------
    None

    Output
    _______
    Prints out whether the subjects and predicates matched or not in the ontology graph and example graph


    """

    eg_subject, eg_predicate, eg_object = [],[],[]
    og_subject, og_predicate, og_object= [],[],[]
    
    example_graph = rdflib.Graph()
    example_graph.parse(eg_graph, format=egtyp)
    
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

    # Check if the predicates in the examples are in the Ontology or not
    for predicate in eg_predicate:
        if (predicate in og_predicate)\
            or (predicate in og_subject) \
            or (predicate in og_object):
            print(f"Match {predicate} in both Example and in Onto")
        else:
            print(f"[XX] {predicate} is in Example but not in Onto")
    
    # Check if the subjects in the examples are in the Ontology or not
    for subject in eg_subject:
        if (subject in og_predicate)\
            or (subject in og_subject) \
            or (subject in og_object):
            print(f"Match {subject} in both Example Graph and in Ontology Graph")
        else:
            print(f"[XX] {subject} is in Example Graph but not in Ontology Graph")


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
        print(f" {err} must be there")
    finally:
        parser.parse_args()
        args=parser.parse_args()                                                                                                                                                                                                                                                      

    if args.val:
        conforms, results_graph, results_text = \
            validate_graphs(args.ontologygraph,
                            args.ontographtype , 
                            args.examplegraph, 
                            args.examplegraphtype)
        print("\n Conforms: ", conforms)
        print("\n Results graph: ", results_graph)
        print("\n Results text: ",results_text)
    if args.diff:
        diff_graphs(args.ontologygraph, 
                        args.ontographtype,
                        args.examplegraph, 
                        args.examplegraphtype)
    
