import SPARQLWrapper as sw
from SPARQLWrapper import SPARQLWrapper2 as sw2, JSON
import pandas as pds
import itertools

if __name__ == "__main__":
    endpoint = r"http://10.5.40.59:7200/repositories/EDR"
    
    # intitialize sparql wrapper instance
    sparql = sw2(endpoint)
    sparql.setReturnFormat(JSON)

    query = r"""
        select * where { 
    	    ?s ?p ?o .
        } limit 10
    """

    # get results from endpoint
    sparql.setQuery(query)
    results = sparql.query().convert()

    # print first 5 results
    for idx, result in enumerate(sparql.query().bindings):
        if idx > 4: break
        print(result)

    # transform resluts into dataframe
    values = {}
    for v in itertools.chain(results.variables):
        temp = [x[v].value for x in itertools.chain(results.bindings)]
        values[v] = temp
    # values # test output

    df = pds.DataFrame(values)
    print(df.head())
