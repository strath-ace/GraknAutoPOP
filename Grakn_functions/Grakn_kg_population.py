# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/. */
# ------ Copyright (C) 2018 University of Strathclyde and Author ------
# ------------------- Author: Francesco Murdaca -----------------------
# -------------- e-mail: francesco.murdaca@strath.ac.uk ---------------

from Functions.graql_insert import *
from Test.validation_test import *
import grakn
import json


def grakn_knowledge_graph_population(path):
    '''___
    DESCRIPTION: This function populates the knowledge graph, performing the transactions using the Python Grakn client

    INPUT:
    - path of the input file with instances for the knowledge graph

    '''

    transaction_counter = 0

    client = grakn.Grakn(uri="localhost:48555")

    with open(path, 'r') as infile:

        input_file = json.load(infile)

        with client.session(keyspace=input_file['keyspace']) as session:

            if input_file['query_type'] == 'insert':

                entity_inserted_counter = 0
                relationship_inserted_counter = 0
                entity_not_inserted_counter = 0
                relationship_not_inserted_counter = 0

                total_transactions = len(input_file['transactions'])

                for transaction in input_file['transactions']:

                    if isinstance(transaction['entity'], list) and 'relationship' in transaction.keys():

                        instance_type = 'relationship'

                        # Verify that the transaction has the correct structure
                        check_if_transaction_inputs_are_valid(transaction, instance_type)

                        transaction_counter += 1

                        check_relationship = graql_insert_relationship_instance(session,
                                                                       transaction['entity'],
                                                                       transaction['attributes_and_values'],
                                                                       transaction['relationship'],
                                                                       transaction['r_attributes_and_values'],
                                                                       transaction['roles'])

                        if check_relationship == 1:

                            relationship_inserted_counter += 1

                        else:

                            relationship_not_inserted_counter += 1

                    else:

                        instance_type = 'entity'

                        # Verify that the transaction has the correct structure
                        check_if_transaction_inputs_are_valid(transaction, instance_type)
                        transaction_counter += 1

                        check_entity = graql_insert_entity_instance(session,
                                                                      transaction['entity'],
                                                                      transaction['attributes_and_values'])

                        if check_entity == 1:

                            entity_inserted_counter += 1

                        else:
                            entity_not_inserted_counter += 1

                    print("\n\nTransactions performed: {}/{}".format(transaction_counter, total_transactions))

                print("\n\n---------------------------------------------------------")
                print("\n\nEntity instances inserted: {}/{}".format(entity_inserted_counter, total_transactions))
                print("\n\nEntity instances not inserted: {}/{}".format(entity_not_inserted_counter, total_transactions))
                print("\n\nRelationship instances inserted: {}/{}".format(relationship_inserted_counter, total_transactions))
                print("\n\nRelationship instances not inserted: {}/{}".format(relationship_not_inserted_counter, total_transactions))

    return 0
