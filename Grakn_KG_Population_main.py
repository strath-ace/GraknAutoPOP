# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/. */
# ------ Copyright (C) 2018 University of Strathclyde and Author ------
# ------------------- Author: Francesco Murdaca -----------------------
# -------------- e-mail: francesco.murdaca@strath.ac.uk ---------------

from Inputs.generate_phone_calls_input_file import *
from Grakn_functions.Grakn_kg_population import *
import json


def grakn_kg_population_main():
    '''___
    DESCRIPTION:
    This is the main function that populates the Grakn Knowledge Graph automatically from a single input file

    ASSUMPTIONS:

    - The knowledge graph schema is already defined in Grakn
    - Each transaction follows the structure created to generalize the process (described below)

    ----------------------------------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------

    TRANSACTION STRUCTURE
    ----------------------------------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------

    TRANSACTION INPUTS REQUIRED FOR TYPE entity are:

     entity                         --> <class 'str'>

     attributes_and_values          --> <class 'dict'>

    TRANSACTION INPUTS REQUIRED FOR TYPE relationship are:

     entity                         --> <class 'list'> of <class 'str'>/s

     attributes_and_values          --> <class 'list'> of <class 'dict'>/s

     relationship                   --> <class 'str'>

     r_attributes_and_values        --> <class 'dict'>

     roles                          --> <class 'list'> of <class 'str'>/s
    ----------------------------------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------
    '''

    # ############################################################################################################
    # ############################################################################################################

    # Generate the single input file (.json)

    # ############################################################################################################
    # ############################################################################################################

    graql_insert_input_file = {}

    # Select the keyspace
    keyspace = 'phone_calls_test'

    # Select the graql query type
    query_type = 'insert'

    graql_insert_input_file['keyspace'] = keyspace
    graql_insert_input_file['query_type'] = query_type

    # Save all the transactions
    graql_insert_input_file['transactions'] = generate_phone_calls_input_file()

    with open('./Inputs/{}_instances_transactions.json'.format(keyspace), 'w') as outfile:
        json.dump(graql_insert_input_file, outfile)

    # ############################################################################################################
    # ############################################################################################################

    # Populate the Grakn Knowledge Graph automatically

    # ############################################################################################################
    # ############################################################################################################

    input_file_path = './Inputs/{}_instances_transactions.json'.format(keyspace)
    grakn_knowledge_graph_population(input_file_path)


if __name__ == '__main__':
    grakn_kg_population_main()
