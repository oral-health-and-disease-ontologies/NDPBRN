from SPARQLWrapper import SPARQLWrapper, SPARQLWrapper2, JSON, JSONLD, CSV, TSV, N3, RDF, RDFXML, TURTLE
import pandas as pds
import itertools
from os import path
from io import BytesIO

def make_sparql_df(results):
    df = pds.DataFrame() # create empty dataframe

    for var in itertools.chain(results.variables):
        # create a list of values
        # getValues returns a list of 'Value' objects
        # e.g., [Value(literal:'x'), Value(x:'y'), ...]
        temp = [val.value
                for val in results.getValues(var)]

        # convert temp into Series, this is needed in case
        # temp is an empty list, using a Series will fill
        # column with NaN
        df[var] = pds.Series(temp)

    return df


def iterprint(obj, limit=5, print_index=False):
    for idx, x in enumerate(obj, 1):
        if idx > limit: break

        if print_index:
            print(idx, x)
        else:
            print(x)


def make_sparql_wrapper(endpoint, result_format="json", query_method="POST"):
    result_format = result_format.lower()

    if ("json" == result_format) or ("jsonld" == result_format):
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
    for v in itertools.chain(results.variables):
        temp = [x[v].value for x in itertools.chain(results.bindings)]
        values[v] = temp
    # values # test output

    df = pds.DataFrame(values)
    return df


def df_from_sparql_csv(results):
    df = pds.read_csv(BytesIO(results), encoding='utf8')
    return df


def df_from_sparql_tsv(results):
    df = pds.read_table(BytesIO(results), encoding='utf8')
    return df