#!/usr/bin/python3

import argparse
import json
import os

# Global vars
script_dir = os.path.dirname(os.path.realpath(__file__))
in_file = script_dir + '/obfuscated_data.json'
out_file_sys_repo = 'system_repos.csv'
out_file_zero_bugs = 'zero_bugs_comp.csv'
out_file_with_bugs = 'with_bugs_comp.csv'
out_file_generic = 'generic_comp.csv'

####################################################################################################

def get_json_data():
    data = None

    with open(in_file) as f:
        data = json.load(f)

    return data

####################################################################################################

def count_repos():
    total = 0

    # Get data
    data = get_json_data()

    # Iterate over first division
    for division in data:
        # Skip divisions that do not have reposCoverage label
        if not 'reposCoverage' in data[division]:
            continue

        # Get number of repos
        total += len(data[division]['reposCoverage'])

    # Print result
    print("Number of repositories: " + str(total))

####################################################################################################

def count_components():
    total = 0

    # Get data
    data = get_json_data()

    # Iterate over first division
    for division in data:
        # Increment if it is a component
        if data[division]['isComponent']:
            total += 1

    # Print result
    print("Number of components: " + str(total))

####################################################################################################

def count_lines():
    total = 0

    # Get data
    data = get_json_data()

    # Iterate over first division
    for division in data:
        # Skip divisions that do not have reposCoverage label
        if not 'reposCoverage' in data[division]:
            continue

        # Iterate over repos
        for repo in data[division]['reposCoverage']:
            total += data[division]['reposCoverage'][repo]['lines-valid']

    # Print result
    print("Number of valid lines: " + str(total))

####################################################################################################

###################
# Argument parser #
###################
parser = argparse.ArgumentParser(
         description='Count things in obfuscated_data.json.')
parser.add_argument('-e', '--element', choices=['repos', 'components', 'lines'], required=True,
                    help='Element to be counted.')

args = parser.parse_args()

###########
# Execute #
###########

if args.element == "repos":
    count_repos()

elif args.element == "components":
    count_components()

elif args.element == "lines":
    count_lines()

else:
    print("ERROR! Invalid element option.")
    parser.print_help()

