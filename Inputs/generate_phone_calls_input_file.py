# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/. */
# ------ Copyright (C) 2018 University of Strathclyde and Author ------
# ------------------- Author: Francesco Murdaca -----------------------
# -------------- e-mail: francesco.murdaca@strath.ac.uk ---------------

import json


def generate_phone_calls_input_file():
    '''___
    DESCRIPTION:
    This function is used to generate the standardized input file that allows automatic
    insertion of instances in the Grakn Knowledge Graph according to the phone calls schema 

    '''

    # Generate the transactions for the instances
    transactions = []

    with open('./Inputs/companies.json', 'r') as infile:
        companies = json.load(infile)

        for company in companies:

            transaction = {}

            # Insert entities
            transaction['entity'] = "company"

            keys = [key for key in company.keys()]

            transaction["attributes_and_values"] = {}

            for key in keys:

                # Insert attributes for the entities
                transaction["attributes_and_values"][key] = company[key]
                
            # print(transaction)
            transactions.append(transaction)

    with open('./Inputs/people.json', 'r') as infile:
        people = json.load(infile)

        for person in people:

            transaction = {}

            # Insert entities
            transaction['entity'] = "person"

            if "first_name" in person.keys():
                keys = [key for key in person.keys()]

                transaction["attributes_and_values"] = {}

                for key in keys:

                    # Insert attributes for the entities
                    transaction["attributes_and_values"][key] = person[key]

                transaction["attributes_and_values"]['is_customer'] = True

            else:
                keys = [key for key in person.keys()]

                transaction["attributes_and_values"] = {}

                for key in keys:

                    # Insert attributes for the entities
                    transaction["attributes_and_values"][key] = person[key]
                transaction["attributes_and_values"]['is_customer'] = False

            # print(transaction)
            transactions.append(transaction)

    with open('./Inputs/contracts.json', 'r') as infile:
        contracts = json.load(infile)

        for contract in contracts:
            transaction = {}

            # Insert entities
            transaction['entity'] = ["company", "person"]

            attributes_e_1 = {"name": contract['company_name']}
            attributes_e_2 = {"phone_number": contract['person_id']}

            # Insert attributes for the entities
            transaction["attributes_and_values"] = [attributes_e_1, attributes_e_2]

            # Insert relationship
            transaction["relationship"] = "contract"

            # Insert relationship attributes
            transaction["r_attributes_and_values"] = {}

            # Insert relationship roles
            transaction["roles"] = ["provider", "customer"]

            # print(transaction)
            transactions.append(transaction)

    with open('./Inputs/calls.json', 'r') as infile:
        calls = json.load(infile)

        for call in calls:
            transaction = {}

            # Insert entities
            transaction['entity'] = ["person", "person"]

            attributes_e_1 = {"phone_number": call["caller_id"]}
            attributes_e_2 = {"phone_number": call["callee_id"]}

            # Insert attributes for the entities
            transaction["attributes_and_values"] = [attributes_e_1, attributes_e_2]

            # Insert relationship
            transaction["relationship"] = "call"
            
            # Insert relationship attributes
            transaction["r_attributes_and_values"] = {"started_at": call['started_at'],
                                                      "duration": call['duration']}
            # Insert relationship roles
            transaction["roles"] = ["caller", "callee"]

            # print(transaction)
            transactions.append(transaction)

    return transactions
