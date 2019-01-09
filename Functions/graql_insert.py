# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/. */
# ------ Copyright (C) 2018 University of Strathclyde and Author ------
# ------------------- Author: Francesco Murdaca -----------------------
# -------------- e-mail: francesco.murdaca@strath.ac.uk ---------------

import grakn
from Functions.graql_match import *
from Test.validation_test import *
import uuid


def graql_insert_entity_instance(session, entity, attributes_and_values, DEBUG=False):
    '''___
    DESCRIPTION: This function use 'insert' of graql language to generate:
            - instance of entity
            - instance of entity with attributes values

    INPUT:
    - session
    - entity name (type String)
    - attributes names and values (type Dict)
    - [OPTIONAL] DEBUG = True to see the query created for the transaction

    '''

    graql_insert_query = []
    graql_match_query = []

    entity_variable = 'x'
    attributes = [single_attribute for single_attribute in attributes_and_values.keys()]
    datatypes_values = [single_attribute for single_attribute in attributes_and_values.values()]

    if not attributes:

        check_entity = 0

        try:
            with session.transaction(grakn.TxType.READ) as tx:

                graql_match_query.append("match\n\n${} isa {}; get ${};".format(entity_variable, entity, entity_variable))
                results = tx.query(graql_match_query).collect_concepts()

                print(results)

                if DEBUG:

                    print('\nIt is already in the KG!!\n')



        except:

            if DEBUG:
                print('Not in the KG!')

            with session.transaction(grakn.TxType.WRITE) as tx:
                graql_insert_query = "insert\n\n${} isa {};".format(entity_variable, entity)

                if DEBUG:
                    print("-----------------------------------------------\n\n"
                          "Executing Graql 'insert' Query: \n\n-----------------------------------------------\n\n" + graql_insert_query)
                    print("\n-----------------------------------------------")
                tx.query(graql_insert_query)
                tx.commit()

                check_entity = 1

    else:


        try:

            check_entity = 0

            graql_match_entity_instance(session, entity, attributes_and_values)

        except:

            if DEBUG:
                print('Not in the KG!')

            with session.transaction(grakn.TxType.WRITE) as tx:

                graql_insert_query.append("insert\n\n${} isa {},".format(entity_variable, entity))

                for attribute_counter in range(0, len(attributes)):

                    graql_insert_query.append(
                        check_grakn_datatype(attributes, datatypes_values, attribute_counter))
                if DEBUG:
                    print("-----------------------------------------------\n\n"
                          "Executing Graql 'insert' Query: \n\n-----------------------------------------------\n\n" + ''.join(graql_insert_query))
                    print("\n-----------------------------------------------")
                tx.query(''.join(graql_insert_query))
                tx.commit()

                check_entity = 1

    return check_entity


def graql_insert_relationship_instance(session, entities, attributes_and_values, relationship,
                                       r_attributes_and_values, roles, DEBUG=False):
    '''___
    DESCRIPTION: This function use 'insert' of graql language to generate:
            - entities instances
            - relationship instance

    INPUT:
    - session
    - entities (type List of String)
    - entities attributes and values (type List of Dict)
    - relationship name (type String)
    - relationship attributes and values (type Dict)
    - roles (type List of String)
    - [OPTIONAL] DEBUG = True to see the query created for the transaction

    '''
    graql_match_insert_query = []

    r_attributes = [single_attribute for single_attribute in r_attributes_and_values.keys()]
    r_datatypes_values = [single_attribute for single_attribute in r_attributes_and_values.values()]

    entities_variables = []

    for variable_counter in range(0, len(entities)):
        entities_variables.append(str(uuid.uuid1()))

    # CASE 1: roles are same number of entities

    if len(entities) == len(roles):

        # Verify that entities and roles values are compatible
        check_data_type_and_length(entities, roles, [], traceback_function()[1], traceback_function()[0])

        # CASE 1.1 relationship has no attribute

        if not r_attributes:

            try:

                graql_match_relationship_instance(session, entities, attributes_and_values, relationship,
                                         r_attributes_and_values, roles)

                check_relationship = 0

            except:

                tx = session.transaction(grakn.TxType.WRITE)

                graql_match_insert_query.append("match\n\n")

                for counter in range(0, len(entities)):

                    attributes = [single_attribute for single_attribute in attributes_and_values[counter].keys()]
                    datatypes_values = [single_attribute for single_attribute in attributes_and_values[counter].values()]

                    # Verify that attributes and datatypes values are compatible
                    check_data_type_and_length(attributes, datatypes_values, [], traceback_function()[1],
                                               traceback_function()[0])

                    graql_match_insert_query.append("${} isa {}".format(roles[counter], entities[counter]))

                    if len(attributes) == 0:

                        graql_match_insert_query.append(';')

                    else:

                        for attribute_counter in range(0, len(attributes)):

                            graql_match_insert_query.append(
                                check_grakn_datatype(attributes, datatypes_values, attribute_counter))

                graql_match_insert_query.append("\n")

                graql_match_insert_query.append("\ninsert\n\n(")

                for r_counter in range(0, len(entities)):

                    if r_counter < len(entities) - 1:

                        graql_match_insert_query.append("{}:${}, ".format(roles[r_counter], roles[r_counter]))

                    else:
                        graql_match_insert_query.append("{}:${})".format(roles[r_counter], roles[r_counter]))

                graql_match_insert_query.append(" isa {};".format(relationship))

                if DEBUG:
                    print("-----------------------------------------------\n\n"
                          "Executing Graql 'match/insert' Query: \n\n-----------------------------------------------\n\n" + ''.join(
                        graql_match_insert_query))
                    print("\n-----------------------------------------------")
                tx.query(''.join(graql_match_insert_query))
                tx.commit()

                check_relationship = 1

        # CASE 1.2 relationship has attribute
        else:

            # Verify that attributes and datatypes values are compatible
            check_data_type_and_length(r_attributes, r_datatypes_values, [], traceback_function()[1],
                                       traceback_function()[0])

            try:

                graql_match_relationship_instance(session, entities, attributes_and_values, relationship,
                                         r_attributes_and_values, roles)

                check_relationship = 0

            except:

                tx = session.transaction(grakn.TxType.WRITE)

                graql_match_insert_query.append("match\n\n")

                for counter in range(0, len(entities)):

                    attributes = [single_attribute for single_attribute in attributes_and_values[counter].keys()]
                    datatypes_values = [single_attribute for single_attribute in
                                        attributes_and_values[counter].values()]

                    # Verify that attributes and datatypes values are compatible
                    check_data_type_and_length(attributes, datatypes_values, [], traceback_function()[1],
                                               traceback_function()[0])

                    graql_match_insert_query.append("${} isa {}".format(roles[counter], entities[counter]))

                    if len(attributes) == 0:

                        graql_match_insert_query.append(';')

                    else:

                        for attribute_counter in range(0, len(attributes)):

                            graql_match_insert_query.append(
                                check_grakn_datatype(attributes, datatypes_values, attribute_counter))

                graql_match_insert_query.append("\n")

                graql_match_insert_query.append("\ninsert\n\n")

                graql_match_insert_query.append("${} (".format(relationship))

                for r_counter in range(0, len(entities)):

                    if r_counter < len(entities) - 1:

                        graql_match_insert_query.append("{}:${}, ".format(roles[r_counter], roles[r_counter]))

                    else:
                        graql_match_insert_query.append("{}:${})".format(roles[r_counter], roles[r_counter]))

                graql_match_insert_query.append(" isa {};".format(relationship))

                graql_match_insert_query.append(" ${}".format(relationship))

                if len(r_attributes) == 0:

                    graql_match_insert_query.append(';')

                else:

                    for r_attribute_counter in range(0, len(r_attributes)):

                        graql_match_insert_query.append(
                            check_grakn_datatype(r_attributes, r_datatypes_values, r_attribute_counter))

                if DEBUG:
                    print("-----------------------------------------------\n\n"
                          "Executing Graql 'match/insert' Query: \n\n-----------------------------------------------\n\n" + ''.join(
                        graql_match_insert_query))
                    print("\n-----------------------------------------------")
                tx.query(''.join(graql_match_insert_query))
                tx.commit()

                check_relationship = 1

        return check_relationship

    # CASE 2: roles are less than number of entities

    elif len(entities) > len(roles):

        # CASE 2.1 relationship has no attribute

        if not r_attributes:

            try:

                graql_match_relationship_instance(session, entities, attributes_and_values, relationship,
                                         r_attributes_and_values, roles)

                check_relationship = 0

            except:

                tx = session.transaction(grakn.TxType.WRITE)

                graql_match_insert_query.append("match\n\n")

                for counter in range(0, len(entities)):

                    attributes = [single_attribute for single_attribute in attributes_and_values[counter].keys()]
                    datatypes_values = [single_attribute for single_attribute in
                                        attributes_and_values[counter].values()]

                    # Verify that attributes and datatypes values are compatible
                    check_data_type_and_length(attributes, datatypes_values, [], traceback_function()[1],
                                               traceback_function()[0])

                    graql_match_insert_query.append("${} isa {}".format(entities_variables[counter], entities[counter]))

                    if len(attributes) == 0:

                        graql_match_insert_query.append(';')

                    else:

                        for attribute_counter in range(0, len(attributes)):

                            graql_match_insert_query.append(
                                check_grakn_datatype(attributes, datatypes_values, attribute_counter))

                graql_match_insert_query.append("\n")

                if DEBUG:
                    print("-----------------------------------------------\n\n"
                          "Executing Graql 'match' Query: \n\n-----------------------------------------------\n\n" + ''.join(
                        graql_match_insert_query))

                graql_match_insert_query.append("\ninsert\n\n(")

                for r_counter in range(0, len(entities)):

                    if r_counter < len(entities) - 1:

                        graql_match_insert_query.append("{}:${}, ".format(roles[0], entities_variables[r_counter]))

                    else:
                        graql_match_insert_query.append("{}:${})".format(roles[0], entities_variables[r_counter]))

                graql_match_insert_query.append(" isa {};".format(relationship))

                if DEBUG:
                    print("-----------------------------------------------\n\n"
                          "Executing Graql 'match/insert' Query: \n\n-----------------------------------------------\n\n" + ''.join(
                        graql_match_insert_query))
                    print("\n-----------------------------------------------")
                tx.query(''.join(graql_match_insert_query))
                tx.commit()

                check_relationship = 1

        # CASE 2.2 relationship has attribute
        else:

            # Verify that attributes and datatypes values are compatible
            check_data_type_and_length(r_attributes, r_datatypes_values, [], traceback_function()[1],
                                       traceback_function()[0])

            try:

                graql_match_relationship_instance(session, entities, attributes_and_values, relationship,
                                         r_attributes_and_values, roles)

                check_relationship = 0

            except:

                tx = session.transaction(grakn.TxType.WRITE)

                graql_match_insert_query.append("match\n\n")

                for counter in range(0, len(entities)):

                    attributes = [single_attribute for single_attribute in attributes_and_values[counter].keys()]
                    datatypes_values = [single_attribute for single_attribute in
                                        attributes_and_values[counter].values()]

                    # Verify that attributes and datatypes values are compatible
                    check_data_type_and_length(attributes, datatypes_values, [], traceback_function()[1],
                                               traceback_function()[0])

                    graql_match_insert_query.append("${} isa {}".format(roles[counter], entities[counter]))

                    if len(attributes) == 0:

                        graql_match_insert_query.append(';')

                    else:

                        for attribute_counter in range(0, len(attributes)):

                            graql_match_insert_query.append(
                                check_grakn_datatype(attributes, datatypes_values, attribute_counter))

                graql_match_insert_query.append("\n")

                if DEBUG:
                    print("-----------------------------------------------\n\n"
                          "Executing Graql 'match' Query: \n\n-----------------------------------------------\n\n" + ''.join(
                        graql_match_insert_query))

                graql_match_insert_query.append("\ninsert\n\n")

                graql_match_insert_query.append("${} (".format(relationship))

                for r_counter in range(0, len(entities)):

                    if r_counter < len(entities) - 1:

                        graql_match_insert_query.append("{}:${}, ".format(roles[r_counter], roles[r_counter]))

                    else:
                        graql_match_insert_query.append("{}:${})".format(roles[r_counter], roles[r_counter]))

                graql_match_insert_query.append(" isa {};".format(relationship))

                graql_match_insert_query.append(" ${}".format(relationship))

                if len(r_attributes) == 0:

                    graql_match_insert_query.append(';')

                else:

                    for r_attribute_counter in range(0, len(r_attributes)):
                        graql_match_insert_query.append(
                            check_grakn_datatype(r_attributes, r_datatypes_values, r_attribute_counter))
                if DEBUG:
                    print("-----------------------------------------------\n\n"
                          "Executing Graql 'match/insert' Query: \n\n-----------------------------------------------\n\n" + ''.join(
                        graql_match_insert_query))
                    print("\n-----------------------------------------------")
                tx.query(''.join(graql_match_insert_query))
                tx.commit()

                check_relationship = 1

        return check_relationship

    # CASE 3: roles are more than number of entities
    else:
        sys.exit('\n\nWARNING: \n\nCASE 3: roles are more than number of entities \n\nNOT ALLOWED!!!')
