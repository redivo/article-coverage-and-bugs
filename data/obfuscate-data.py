#!/usr/bin/python3

import argparse
import json
import os

####################################################################################################

def get_obfuscated_json_data(json_data):
    new_json = {}
    component_index = 1
    repo_index = 1

    # Iterate over first level (component and others)
    for item in json_data:
        name = item

        # If it's a component, translate name
        if json_data[item]['isComponent']:
            name = "Component_%03d" % component_index
            component_index += 1

        # Create item
        new_json[name] = {}

        # Iterate over fields
        for field in json_data[item]:

            # If it is reposCoverage, convert it
            if field == 'reposCoverage':
                new_json[name][field] = {}

                # Iterate over repos
                for repo in json_data[item][field]:
                    obfuscated_repo = "Repository_%03d" % repo_index
                    repo_index += 1
                    new_json[name][field][obfuscated_repo] = json_data[item][field][repo]

            # Otherwise just copy
            else:
                new_json[name][field] = json_data[item][field]

    return new_json

####################################################################################################

###################
# Argument parser #
###################
parser = argparse.ArgumentParser(
         description="Obfuscate data contained in repository and generate a new JSON file called "
                     "obfuscated_data.json.")
parser.parse_args()

# Initialize vars
script_dir = os.path.dirname(os.path.realpath(__file__))
data_path = script_dir + '/../article-coverage-and-bugs-private/data/data.json'
obfuscated_data_path = script_dir + '/obfuscated_data.json'
json_data = None
obfuscated_data = None

# Read json file
with open(data_path) as f:
    json_data = json.load(f)

# Convert
obfuscated_data = get_obfuscated_json_data(json_data)

# Save file
with open(obfuscated_data_path, 'w') as f:
    f.write(json.dumps(obfuscated_data, indent=4))
