from src.analysis.lib.sparql_operations import *

def get_endpiont():
    return r"http://localhost:7200/repositories/EDR"


def get_survival_query(query_type, limit=100, use_order_by=False):
    my_path = path.abspath(path.dirname(__file__))
    if query_type == "procedure":
        query_file = "dental_procedures_survival.txt"
    else:
        query_file = "caries_findings_survival.txt"

    query_path = path.join(my_path, r"""./analysis_queries""", query_file)

    # contents of query file
    with open(query_path) as f:
        query = f.read()

    if use_order_by:
        order_by_path = path.join(my_path, r"""./analysis_queries/survival_data_order.txt""")
        with open(order_by_path) as f:
            order_string = f.read()
        query = query + "\n" + order_string

    if limit > 0:
        limit_string = " \nlimit %s" % str(limit)
        query = query + limit_string

    return query



def get_sparql_query(query_file, limit=100):
    my_path = path.abspath(path.dirname(__file__))
    query_path = path.join(my_path, r"""../sparql""", query_file)

    # contents of query file
    with open(query_path) as f:
        query = f.read()

    if limit > 0:
        limit_string = " \nlimit %s" % str(limit)
        query = query + limit_string

    return query

def save_caries_results(limit=100, result_format="json", print_query=False):
    #  build query string
    query = get_survival_query("caries", limit=limit)
    # query = get_test_query(5)

    if print_query:
        print(query)

    # build sparql object
    sparql = make_sparql_wrapper(get_endpiont(), result_format=result_format)

    # get results from endpoint
    sparql.setQuery(query)
    results = sparql.query().convert()

    df = make_sparql_df(results)
    print(df.head())
    print("len: ", len(df))

    df.to_csv("caries_survival_results.txt", index=False)


def save_procedures_reults(limit=100, result_format="json", print_query=False):
    #  build query string
    query = get_survival_query("procedure", limit=0)
    # query = get_test_query(5)

    if print_query:
        print(query)

    # build sparql object
    sparql = make_sparql_wrapper(get_endpiont(), result_format=result_format)

    # get results from endpoint
    sparql.setQuery(query)
    results = sparql.query().convert()

    df = make_sparql_df(results)
    print(df.head())
    print("len: ", len(df))

    # df.to_csv("caries_survival_results.txt", index_label="row")
    df.to_csv("procedure_survival_results.txt", index=False)

def save_query_results(query, filename, result_format="json", print_query=False):
    if print_query:
        print(query)

    # build sparql object
    sparql = make_sparql_wrapper(get_endpiont(), result_format=result_format)

    # get results from endpoint
    sparql.setQuery(query)
    results = sparql.query().convert()

    df = make_sparql_df(results)
    print(df.head())
    print("len: ", len(df))

    # df.to_csv("caries_survival_results.txt", index_label="row")
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    pds.set_option('display.width', 500)
    # save_caries_results(limit=0)
    # save_procedures_reults(limit=0)

    result_limit = 0 # set number of results to return

    # save patient demographic info
    # query = get_sparql_query("patient_demographics.sparql", result_limit)
    # save_query_results(query, "patients.csv")

    # save patient teeth info
    query = get_sparql_query("patient_teeth.sparql", result_limit)
    save_query_results(query, "patient_teeth.csv")

    # save tooth caries info
    # query = get_sparql_query("tooth_caries.sparql", result_limit)
    # save_query_results(query, "tooth_caries.csv")
    #
    # # save surface info about tooth caries
    # query = get_sparql_query("tooth_surface_caries.sparql", result_limit)
    # save_query_results(query, "tooth_surface_caries.csv")
    #
    # # save tooth procedure info
    # query = get_sparql_query("tooth_procedures_no_es.sparql", result_limit)
    # save_query_results(query, "tooth_procedures_no_es.csv")
    #
    # # save surface info about tooth procedures
    # query = get_sparql_query("tooth_surface_procedures_no_es.sparql", result_limit)
    # save_query_results(query, "tooth_surface_procedures_no_es.csv")
