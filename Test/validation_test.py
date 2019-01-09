# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/. */
# ------ Copyright (C) 2018 University of Strathclyde and Authors -----
# ------------------- Author: Francesco Murdaca -----------------------
# -------------- e-mail: francesco.murdaca@strath.ac.uk ---------------

import traceback
import sys
import re


def traceback_function():
    stack = traceback.extract_stack()
    filename, codeline, funcName, text = stack[-2]

    return [codeline, filename]


def system_exit(file_name, code_line_function, error_comment):

    sys.exit(f''
             f''
             f'ERROR in {file_name}'
             f', line {code_line_function}, '
             f'{error_comment}')


def check_data_type_and_length(object_1, object_2, object_type_reference, file_path_error, line_code_error):

    '''___
    DESCRIPTION: This function check that

    INPUT:
    - object 1
    - object 2
    - object type reference

    '''
    # To guarantee consistency, there is a check
    if len(object_1) != len(object_2) \
            and type(object_1) == type(object_type_reference) \
            and type(object_2) == type(object_type_reference):

        system_exit(file_path_error, line_code_error,
                    '\n\nthe two objects are of same type list, but they have different'
                    ' lengths \n\n object 1: {} \n\n object 2: {}'.format(object_1, object_2))

    if type(object_1) != type(object_type_reference):
        system_exit(file_path_error, line_code_error,
                    '\n\nthe object {} is {}. It should be of type List!!'.format(1, type(object_1)))

    if type(object_2) != type(object_type_reference):
        system_exit(file_path_error, line_code_error,
                    '\n\nthe object {} is {}. It should be of type List!!'.format(2, type(object_2)))


def check_grakn_datatype(list_attributes, list_datatype_values, counter, DEBUG=False):

    '''___
    DESCRIPTION: This function add part of a graql query regarding the datatype value of the attribute.
    In practice it is checking the value of the datatype, in order to avoid errors from the Grakn API, because
    the datatype has to follow the datatype selected by the user in the grakn schema layer.

    INPUT:
    - list of attributes
    - list of datatype values of the attributes
    - counter

    '''
    if len(list_attributes) == 1:

        # datatype long
        if isinstance(list_datatype_values[counter], (int, float)) and not isinstance(
                list_datatype_values[counter], bool):
            if DEBUG:
                print('datatype long', list_datatype_values[counter])

            return ' has {} {}; '.format(list_attributes[counter],
                                         list_datatype_values[counter])
        # datatype boolean
        elif isinstance(list_datatype_values[counter], bool):
            if DEBUG:
                print('datatype boolean', list_datatype_values[counter])

            return ' has {} {}; '.format(list_attributes[counter],
                                         str(list_datatype_values[counter]).lower())

        # datatype date ISO 8601
        elif validate_iso8601(list_datatype_values[counter]):
            if DEBUG:
                print('datatype date ISO 8601', list_datatype_values[counter])

            return ' has {} {}; '.format(list_attributes[counter],
                                         list_datatype_values[counter])

        # datatype string
        else:
            if DEBUG:
                print('datatype string', list_datatype_values[counter])

            return ' has {} "{}"; '.format(list_attributes[counter],
                                           list_datatype_values[counter])

    else:

        if counter < len(list_attributes) - 1:

            # datatype long
            if isinstance(list_datatype_values[counter], (int, float)) and not isinstance(
                    list_datatype_values[counter], bool):
                if DEBUG:
                    print('datatype long', list_datatype_values[counter])

                return ' has {} {}, '.format(list_attributes[counter],
                                             list_datatype_values[counter])
            # datatype boolean
            elif isinstance(list_datatype_values[counter], bool):
                if DEBUG:
                    print('datatype boolean', list_datatype_values[counter])

                return ' has {} {}, '.format(list_attributes[counter],
                                             str(list_datatype_values[counter]).lower())

            # datatype date ISO 8601
            elif validate_iso8601(list_datatype_values[counter]):
                if DEBUG:
                    print('datatype date ISO 8601', list_datatype_values[counter])

                return ' has {} {}, '.format(list_attributes[counter],
                                             list_datatype_values[counter])

            # datatype string
            else:
                if DEBUG:
                    print('datatype string', list_datatype_values[counter])

                return ' has {} "{}", '.format(list_attributes[counter],
                                               list_datatype_values[counter])

        else:

            # datatype long
            if isinstance(list_datatype_values[counter], (int, float)) and not isinstance(
                    list_datatype_values[counter], bool):
                if DEBUG:
                    print('datatype long', list_datatype_values[counter])

                return ' has {} {}; '.format(list_attributes[counter],
                                             list_datatype_values[counter])
            # datatype boolean
            elif isinstance(list_datatype_values[counter], bool):
                if DEBUG:
                    print('datatype boolean', list_datatype_values[counter])

                return ' has {} {}; '.format(list_attributes[counter],
                                             str(list_datatype_values[counter]).lower())

            # datatype date ISO 8601
            elif validate_iso8601(list_datatype_values[counter]):
                if DEBUG:
                    print('datatype date ISO 8601', list_datatype_values[counter])

                return ' has {} {}; '.format(list_attributes[counter],
                                             list_datatype_values[counter])

            # datatype string
            else:
                if DEBUG:
                    print('datatype string', list_datatype_values[counter])

                return ' has {} "{}"; '.format(list_attributes[counter],
                                               list_datatype_values[counter])


def validate_iso8601(input_date):
    '''___
    DESCRIPTION: This function check if the data format match the ISO 8601 standard for the date

    INPUT:
    - date

    '''
    regex_iso8601 = "^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$"

    match_iso8601 = re.compile(regex_iso8601).match
    try:
       if match_iso8601(input_date) is not None:
          return True
    except:
        pass
    return False


def check_if_transaction_inputs_are_valid(transaction_inputs, instance_type):
    '''___
    DESCRIPTION:
    This function verify that all the transactions inserted by the user are valid transaction in terms of the
    structure used to parse the input file containing the transactions

    INPUT:
    - transaction
    - instance type

    '''

    if instance_type == 'relationship':

        transaction_inputs_required = {'entity': [list, str],
                                       'attributes_and_values': [list, dict],
                                       'relationship': [str, str],
                                       'r_attributes_and_values': [dict, dict],
                                       'roles': [list, str]}

    else:

        transaction_inputs_required = {'entity': [str, str],
                                       'attributes_and_values': [dict, dict]}

    # Check if there are missing inputs in the transaction
    missing_inputs = []

    list_transaction_inputs = [tr for tr in transaction_inputs.keys()]

    for req_input in transaction_inputs_required.keys():

        if req_input not in list_transaction_inputs:
            missing_inputs.append(req_input)

    # Check if there are wrong inputs in the transaction
    wrong_inputs = []

    if instance_type == 'relationship':

        for input_key, input_value in transaction_inputs.items():

            # check level 0
            if type(input_value) != transaction_inputs_required[input_key][0]:

                wrong_inputs.append([input_key, type(input_value),
                                     'It should be {} of {}'.format(
                                         transaction_inputs_required[input_key][0],
                                         transaction_inputs_required[input_key][1])])

            # check level 1
            else:

                types = []

                if input_value:

                    if type(input_value) == str:
                        types.append(str)

                    if type(input_value) == dict:
                        types.append(dict)

                    if type(input_value) == list:
                        for element in input_value:
                            types.append(type(element))

                    for single_type in types:

                        if single_type != transaction_inputs_required[input_key][1]:

                            wrong_inputs.append([input_key, type(input_value),
                                                 'It should be {} of {}'.format(
                                                     transaction_inputs_required[input_key][0],
                                                     transaction_inputs_required[input_key][1])])
                            break

                        else:

                            pass

                else:
                    pass

    else:

        for input_key, input_value in transaction_inputs.items():

            if type(input_value) != transaction_inputs_required[input_key][0]:

                wrong_inputs.append([input_key, type(input_value), ''])

    if missing_inputs and wrong_inputs:

        error_text = []
        error_text.append('\n\nEVALUATED TRANSACTION TYPE ---> {}'.format(instance_type))

        error_text.append('\n\nERROR TYPE ---> Combined error: Missing inputs and Wrong inputs')

        error_text.append('\n\nMissing inputs are: \n')
        for miss_input in missing_inputs:
            error_text.append('\n {:30}'.format(miss_input))

        error_text.append('\n\nWrong inputs are: \n')

        for w_input in wrong_inputs:

            if w_input[0] in missing_inputs and w_input[2] == '':

                error_text.append('\n {:30} --> {}'.format(w_input[0], w_input[1]))

            else:

                error_text.append('\n {:30} --> {}'.format(w_input[0], w_input[1], w_input[2]))

        # ###########################################################################################################
        # ###########################################################################################################
        # REMINDER FOR THE USER

        error_text.append("\n\n----------------------------------------------------------------------------------")
        error_text.append("\n----------------------------------------------------------------------------------")
        error_text.append("\n----------------------------------------------------------------------------------")

        entity_transaction_inputs_required = {'entity': str,
                                              'attributes_and_values': dict}

        error_text.append("\n\nREMEMBER TRANSACTION INPUTS REQUIRED FOR TYPE entity are:")

        for e_input_key, e_input_value in entity_transaction_inputs_required.items():
            error_text.append('\n\n {:30} --> {}'.format(e_input_key, e_input_value))

        relationship_transaction_inputs_required = {'entity': [list, str],
                                                    'attributes_and_values': [list, dict],
                                                    'relationship': [str],
                                                    'r_attributes_and_values': [dict],
                                                    'roles': [list, str]}

        error_text.append("\n\nREMEMBER TRANSACTION INPUTS REQUIRED FOR TYPE relationship are:")

        for r_input_key, r_input_value in relationship_transaction_inputs_required.items():

            if len(r_input_value) == 2:
                error_text.append('\n\n {:30} --> {} of {}/s'.format(r_input_key, r_input_value[0], r_input_value[1]))
            else:

                error_text.append('\n\n {:30} --> {}'.format(r_input_key, r_input_value[0]))

        sys.exit(''.join(error_text))

    elif missing_inputs:

        error_text = []
        error_text.append('\n\nEVALUATED TRANSACTION TYPE ---> {}'.format(instance_type))

        error_text.append('\n\nERROR TYPE ---> Missing inputs')

        error_text.append('\n\nUSER TRANSACTION INPUTS:')

        for u_input in list_transaction_inputs:
            error_text.append('\n\n {}'.format(u_input))

        error_text.append('\n\nMISSING TRANSACTION INPUTS:')

        for m_input in missing_inputs:
            error_text.append('\n\n {}'.format(m_input))

        print('\n\nThe transaction is:')
        print(transaction_inputs)

        # ###########################################################################################################
        # ###########################################################################################################
        # REMINDER FOR THE USER

        error_text.append("\n\n----------------------------------------------------------------------------------")
        error_text.append("\n----------------------------------------------------------------------------------")
        error_text.append("\n----------------------------------------------------------------------------------")

        entity_transaction_inputs_required = {'entity': str,
                                              'attributes_and_values': dict}

        error_text.append("\n\nREMEMBER TRANSACTION INPUTS REQUIRED FOR TYPE entity are:")

        for e_input in entity_transaction_inputs_required.keys():
            error_text.append('\n\n {}'.format(e_input))

        relationship_transaction_inputs_required = {'entity': [list, str],
                                                    'attributes_and_values': [list, dict],
                                                    'relationship': [str],
                                                    'r_attributes_and_values': [dict],
                                                    'roles': [list, str]}

        error_text.append("\n\nREMEMBER TRANSACTION INPUTS REQUIRED FOR TYPE relationship are:")

        for r_input_key, r_input_value in relationship_transaction_inputs_required.items():

            if len(r_input_value) == 2:
                error_text.append('\n\n {:30} --> {} of {}/s'.format(r_input_key, r_input_value[0], r_input_value[1]))
            else:

                error_text.append('\n\n {:30} --> {}'.format(r_input_key, r_input_value[0]))

        sys.exit(''.join(error_text))

    elif wrong_inputs:

        error_text = []
        error_text.append('\n\nEVALUATED TRANSACTION TYPE ---> {}'.format(instance_type))

        error_text.append('\n\nERROR TYPE ---> Wrong inputs')

        error_text.append('\n\nUSER TRANSACTION ERROR INPUTS:')

        for ww_inputs in wrong_inputs:
            error_text.append('\n\n {:30} --> {:15} || {}'.format(ww_inputs[0], str(ww_inputs[1]), ww_inputs[2]))

        print('\n\nThe transaction is:')
        print(transaction_inputs)

        # ###########################################################################################################
        # ###########################################################################################################
        # REMINDER FOR THE USER

        error_text.append("\n\n----------------------------------------------------------------------------------")
        error_text.append("\n----------------------------------------------------------------------------------")
        error_text.append("\n----------------------------------------------------------------------------------")

        entity_transaction_inputs_required = {'entity': str,
                                              'attributes_and_values': dict}

        error_text.append("\n\nREMEMBER TRANSACTION INPUTS REQUIRED FOR TYPE entity are:")

        for e_input_key, e_input_value in entity_transaction_inputs_required.items():
            error_text.append('\n\n {:30} --> {}'.format(e_input_key, e_input_value))

        relationship_transaction_inputs_required = {'entity': [list, str],
                                                    'attributes_and_values': [list, dict],
                                                    'relationship': [str],
                                                    'r_attributes_and_values': [dict],
                                                    'roles': [list, str]}

        error_text.append("\n\nREMEMBER TRANSACTION INPUTS REQUIRED FOR TYPE relationship are:")

        for r_input_key, r_input_value in relationship_transaction_inputs_required.items():

            if len(r_input_value) == 2:

                error_text.append('\n\n {:30} --> {} of {}/s'.format(r_input_key, r_input_value[0], r_input_value[1]))

            else:

                error_text.append('\n\n {:30} --> {}'.format(r_input_key, r_input_value[0]))

        sys.exit(''.join(error_text))

    else:

        pass
