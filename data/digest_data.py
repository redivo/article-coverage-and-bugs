#!/usr/bin/python3

import argparse
import json
import os
import plotly.graph_objects as go
import plotly.express as px
import math

# Global vars
script_dir = os.path.dirname(os.path.realpath(__file__))
in_file = script_dir + '/obfuscated_data.json'
out_file_sys_repo = 'system_repos.csv'
out_file_zero_bugs = 'zero_bugs_comp.csv'
out_file_with_bugs = 'with_bugs_comp.csv'
out_file_generic = 'generic_comp.csv'

####################################################################################################

def generate_chart(title, x, x_title, y, y_title, sizes):
    fig = px.scatter(x=x, y=y, size=sizes, trendline="ols")
    fig.update_layout(title_text = title, title_font_size=24)
    fig.update_xaxes(title_text = x_title)
    fig.update_yaxes(title_text = y_title)

    fig.show()

####################################################################################################

def get_json_data():
    data = None

    with open(in_file) as f:
        data = json.load(f)

    return data

####################################################################################################

def is_valid_component(component):
    # To be a valid component it has to contain at least one repository
    return len(component['reposCoverage']) > 0

####################################################################################################

def system_repos_report(output_type):
    # Initialize body
    csv_body = "Repository,Total,Covered\n"
    chart_x = []
    chart_y = []
    chart_size = []

    # Get data
    data = get_json_data()

    # Parse data
    for repo in data['System repos']['reposCoverage']:
        covered = data['System repos']['reposCoverage'][repo]['lines-covered']
        total = data['System repos']['reposCoverage'][repo]['lines-valid']
        rate = covered/total

        # Fill for CSV
        csv_body += "{0},{1},{2}\n".format(repo, total, covered)

        # Fill for chart
        chart_x.append(total)
        chart_y.append(rate * 100)
        chart_size.append(10)

    if output_type == 'csv':
        # Write file
        print('Generating CSV file...')
        with open(script_dir + '/'  + out_file_sys_repo, 'w') as f:
            f.write(csv_body)
    else:
        # Generate chart
        generate_chart('Tamanho em linhas x Cobertura de código',
                       chart_x, 'Linhas de código',
                       chart_y, 'Cobertura de código (%)',
                       chart_size)

####################################################################################################

def zero_bugs_report(output_type):
    # Initialize body
    csv_body = "Component,Bugs,Total,Covered\n"
    chart_x = []
    chart_y = []
    chart_size = []

    # Get data
    data = get_json_data()

    # Parse data
    for item in data:
        # Skip not component items
        if not data[item]['isComponent']:
            continue

        # Skip invalid components
        if not is_valid_component(data[item]):
            continue

        # Skip components with bugs
        if int(data[item]['bugs']) > 0:
            continue

        # Sum lines of repositories
        total = 0
        covered = 0
        for repo in data[item]['reposCoverage']:
            total += data[item]['reposCoverage'][repo]['lines-valid']
            covered += data[item]['reposCoverage'][repo]['lines-covered']

        # Fill for CSV
        csv_body += "{0},{1},{2},{3}\n".format(item, 0, total, covered)

        # Fill for chart
        chart_x.append(total)
        chart_y.append((covered/total) * 100)
        chart_size.append(10)

    if output_type == 'csv':
        # Write file
        with open(script_dir + '/'  + out_file_zero_bugs, 'w') as f:
            f.write(csv_body)
    else:
        # Generate chart
        generate_chart('Tamanho em linhas x Cobertura de código '
                       '(funcionalidades sem falhas reportadas)',
                       chart_x, 'Linhas de código',
                       chart_y, 'Cobertura de código (%)',
                       chart_size)

####################################################################################################

def with_bugs_report(output_type):
    # Initialize body
    csv_body = "Component,Bugs,Total,Covered\n"
    chart_x = []
    chart_y = []
    chart_size = []

    # Get data
    data = get_json_data()

    # Parse data
    for item in data:
        # Skip not component items
        if not data[item]['isComponent']:
            continue

        # Skip invalid components
        if not is_valid_component(data[item]):
            continue

        # Skip components with no bugs
        if int(data[item]['bugs']) == 0:
            continue

        # Sum lines of repositories
        total = 0
        covered = 0
        for repo in data[item]['reposCoverage']:
            total += data[item]['reposCoverage'][repo]['lines-valid']
            covered += data[item]['reposCoverage'][repo]['lines-covered']

        # Fill for CSV
        csv_body += "{0},{1},{2},{3}\n".format(item, data[item]['bugs'], total, covered)

        # Fill for chart
        chart_x.append((covered/total) * 100)
        chart_y.append(data[item]['bugs'])
        chart_size.append(math.sqrt(total)/3)

    if output_type == 'csv':
        # Write file
        with open(script_dir + '/'  + out_file_with_bugs, 'w') as f:
            f.write(csv_body)
    else:
        # Generate chart
        generate_chart('Cobertura de código x Falhas reportadas '
                       '(excluindo funcionalidades sem falhas reportadas)',
                       chart_x, 'Cobertura de código (%)',
                       chart_y, 'Falhas reportadas',
                       chart_size)

####################################################################################################

def generic_report(output_type):
    # Initialize body
    csv_body = "Component,Bugs,Total,Covered\n"
    csv_body = "Component,Bugs,Total,Covered\n"
    chart_x = []
    chart_y = []
    chart_size = []

    # Get data
    data = get_json_data()

    # Parse data
    for item in data:
        # Skip not component items
        if not data[item]['isComponent']:
            continue

        # Skip invalid components
        if not is_valid_component(data[item]):
            continue

        # Sum lines of repositories
        total = 0
        covered = 0
        for repo in data[item]['reposCoverage']:
            total += data[item]['reposCoverage'][repo]['lines-valid']
            covered += data[item]['reposCoverage'][repo]['lines-covered']

        # Fill for CSV
        csv_body += "{0},{1},{2},{3}\n".format(item, data[item]['bugs'], total, covered)

        # Fill for chart
        chart_x.append((covered/total) * 100)
        chart_y.append(data[item]['bugs'])
        chart_size.append(math.sqrt(total)/3)

    if output_type == 'csv':
        # Write file
        with open(script_dir + '/'  + out_file_generic, 'w') as f:
            f.write(csv_body)
    else:
        # Generate chart
        generate_chart('Cobertura de código x Falhas reportadas',
                       chart_x, 'Cobertura de código (%)',
                       chart_y, 'Falhas reportadas',
                       chart_size)

####################################################################################################

###################
# Argument parser #
###################
parser = argparse.ArgumentParser(
         description='Digest ' + in_file + ' and create a CSV file or a chart.')
parser.add_argument('-o', '--output', default='csv', choices=['csv', 'chart'],
                    help='Output type. Default is \'csv\'.')

group_input = parser.add_mutually_exclusive_group(required=True)

group_input.add_argument('-s', '--system-repos-report', action='store_true',
                         help='Generate a report of system repositories. '
                              'Output file is ' + out_file_sys_repo)

group_input.add_argument('-z', '--zero-bugs-report', action='store_true',
                         help='Generate a report of valid components without bugs.'
                              'Output file is ' + out_file_zero_bugs)

group_input.add_argument('-b', '--with-bugs-report', action='store_true',
                         help='Generate a report of valid components with bugs.'
                              'Output file is ' + out_file_with_bugs)

group_input.add_argument('-g', '--generic-report', action='store_true',
                         help='Generate a report a report containing all valid components.'
                              'Output file is ' + out_file_generic)

args = parser.parse_args()

###########
# Execute #
###########

if args.system_repos_report:
    system_repos_report(args.output)

elif args.zero_bugs_report:
    zero_bugs_report(args.output)

elif args.with_bugs_report:
    with_bugs_report(args.output)

else:
    generic_report(args.output)

print('Done!')
