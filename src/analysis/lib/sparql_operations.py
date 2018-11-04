from SPARQLWrapper import SPARQLWrapper, SPARQLWrapper2, JSON, JSONLD, CSV, TSV, N3, RDF, RDFXML, TURTLE
import pandas as pds
import itertools
from os import path
from io import BytesIO

def get_sparql_variables(results, sparql_wrapper="SPARQLWrapper2"):
    return results.variables if ("sparqlwrapper2" == sparql_wrapper.lower()) else results['head']['vars']
    # if "sparqlwrapper2" == sparql_wrapper.lower():
    #     results.variables
    # else:
    #     return results['head']['vars']


def get_sparql_bindings(results, sparql_wrapper="SPARQLWrapper2"):
    return results.bindings \
              if ("sparqlwrapper2" == sparql_wrapper.lower()) else results['results']['bindings']
    # if "sparqlwrapper2" == sparql_wrapper.lower():
    #     return results.bindings
    # else:
    #     return results['results']['bindings']


def get_sparql_binding_variable_value(binding, variable, sparql_wrapper="SPARQLWrapper2"):
    return binding[variable].value \
             if ("sparqlwrapper2" == sparql_wrapper.lower()) else binding[variable]['value']
    # if "sparqlwrapper2" == sparql_wrapper.lower():
    #     return binding[variable].value
    # else:
    #     return binding[variable]['value']


def make_sparql_dict_list(bindings, variables, sparql_wrapper="SPARQLWrapper2"):
    def binding_value(binding, var): # helper function for returning values
        return \
            get_sparql_binding_variable_value(binding, var, sparql_wrapper) if (var in binding) else None

    dict_list = []  # list to contain dictionaries
    for binding in itertools.chain(bindings):
        ## create values using a list comprehension; functions same as code below
        values = [binding_value(binding, var) for var in itertools.chain(variables)]
        dict_list.append(dict(zip(variables, values)))

        # values = []  # for each binding create a list of values
        # for var in itertools.chain(variables):
        #     values.append(binding_value(binding, var))
        # dict_list.append(dict(zip(variables, values)))  # append dict of values into data list
    return dict_list


def make_sparql_df(results, sparql_wrapper="SPARQLWrapper2"):
    variables = get_sparql_variables(results, sparql_wrapper)
    bindings = get_sparql_bindings(results, sparql_wrapper)

    # create a list of dictionaries to use as data for dataframe
    data_list = make_sparql_dict_list(bindings, variables, sparql_wrapper)

    df = pds.DataFrame(data_list) # create dataframe from data list
    return df[variables] # return dataframe with columns reordered


def make_sparql2_df(results, sparql_wrapper="SPARQLWrapper2"):
    df = pds.DataFrame(columns=results.variables)  # create empty dataframe with variables as columns

    for b in itertools.chain(results.bindings):
        values = []                                # for each binding create a list of values
        for var in itertools.chain(results.variables):
            if var in b:                           # check for columns that don't have values
                values.append(b[var].value)
            else:
                values.append(None)
        df.loc[len(df)] = values                   # append list as a row in dataframe

    return df # return dataframe

def iterprint(obj, limit=5, print_index=False):
    for idx, x in enumerate(obj, 1):
        if idx > limit: break

        if print_index:
            print(idx, x)
        else:
            print(x)


def make_sparql_wrapper(endpoint, result_format="json", query_method="POST", sparql_wrapper="SPARQLWrapper2"):
    result_format = result_format.lower()

    # print(sparql_wrapper)
    # if ("json" == result_format) or ("jsonld" == result_format):
    if "sparqlwrapper2" == sparql_wrapper.lower():
        wrapper = SPARQLWrapper2(endpoint)
    else:
        wrapper = SPARQLWrapper(endpoint)

    # json, jsonld, csv, tsv, n3, rdf, rdfxml, turtle
    wrapper.setReturnFormat(result_format)
    wrapper.setMethod(query_method)
    return wrapper


def get_test_query(limit=5):
    my_path = path.abspath(path.dirname(__file__))
    query_path = path.join(my_path, r"""../analysis_queries/test_query.txt""")

    # contents of query file
    with open(query_path) as f:
        query = f.read()

    if limit > 0:
        limit_string = " \nlimit %s" % str(limit)
        query = query + limit_string

    return query


def df_from_sparql(results, result_format="json"):
    result_format = result_format.lower()

    if ("json" == result_format) or ("jsonld" == result_format):
        df = df_from_sparql_json(results)
    elif ("csv" == result_format):
        df = df_from_sparql_csv(results)
    else:
        df = df_from_sparql_csv(results)

    return df


def df_from_sparql_json(results):
    # transform query results into dataframe
    values = {}
    # for v in itertools.chain(results.variables):
    for v in results.variables:
        temp = [x[v].value for x in itertools.chain(results.bindings)]
        values[v] = temp
    # values # test output

    df = pds.DataFrame(values, columns=results.variables)
    return df


def df_from_sparql_csv(results):
    df = pds.read_csv(BytesIO(results), encoding='utf8')
    return df


def df_from_sparql_tsv(results):
    df = pds.read_table(BytesIO(results), encoding='utf8')
    return df
