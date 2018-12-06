# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/. */
# ------ Copyright (C) 2018 University of Strathclyde and Authors -----
# ------------------- Author: Francesco Murdaca -----------------------
# -------------- e-mail: francesco.murdaca@strath.ac.uk ---------------

# Python Packages:
import pip


def install(package):
    pip.main(['install', package])


DEA_dependancies = {'grakn': {'Version': '1.3.2'}}            # Grakn Interface

list_packages = []
for k in DEA_dependancies.keys():
    list_packages.append(k)

for package in list_packages:
    print('\nInstalling', package, '...')
    install(package)
