import argparse
import json
import os
import ast
import sys

import click
import pyarrow as pa
from dora import Node
from pycparser.c_ast import While

from mofa.utils.install_pkg.load_task_weaver_result import extract_important_content

RUNNER_CI = True if os.getenv("CI") == "true" else False

def clean_string(input_string:str):
    return input_string.encode('utf-8', 'replace').decode('utf-8')
def send_task_and_receive_data(node):
    shopping_requirement_status = False
    shopping_planning_status = False
    shopping_solution_status = False
    while True:
        data = input(
            " Send You Task :  ",
        )
        node.send_output("user_input", pa.array([clean_string(data)]))
        event = node.next(timeout=5000)
        if event is not None:
            while True:
                if event is not None:

                    if shopping_requirement_status is False:
                        while True:
                            if event['id'] == "user_shopping_requirement_status":
                                node_results = json.loads(event['value'].to_pylist()[0])
                                results = node_results.get('node_results')

                                if 'yes' in results or 'Yes' in results:
                                    click.echo("This is the user's requirement description.")
                                    click.echo(results)
                                    shopping_requirement_status = True
                                    break
                                else:
                                    click.echo(results)

                                    data = input(
                                        " Shopping Requirement Suggestions :  ",
                                    )
                                    node.send_output("user_input", pa.array([clean_string(data)]))
                            event = node.next(timeout=5000)
                    if shopping_planning_status is False:
                        while True:
                            if event['id'] == "shopping_planning_status":
                                node_results = json.loads(event['value'].to_pylist()[0])
                                results = node_results.get('node_results')

                                if 'yes' in results or 'Yes' in results:
                                    click.echo("This is the final shopping assembly plan.")
                                    click.echo(results)
                                    click.echo("Please wait, we are going to web search")
                                    shopping_planning_status = True
                                    break
                                else:
                                    click.echo(results)
                                    data = input(
                                        " Agent Shopping Plan Suggestions:  ",
                                    )
                                    node.send_output("user_input", pa.array([clean_string(data)]))
                            event = node.next(timeout=5000)
                    if shopping_solution_status is False:
                        while True:
                            if event['id'] == "shopping_solution_status":
                                node_results = json.loads(event['value'].to_pylist()[0])
                                results = node_results.get('node_results')
                                if 'yes' in results or 'Yes' in results:
                                    click.echo("This is the final shopping solution.")
                                    click.echo(results)
                                    shopping_planning_status = True
                                    break
                                else:
                                    click.echo(results)
                                    data = input(" Please re-enter your suggestions for the shopping plan :  ",)
                                    node.send_output("shopping_solution_user_input", pa.array([clean_string(data)]))
                            event = node.next(timeout=5000)

                    node_results = json.loads(event['value'].to_pylist()[0])
                    results = node_results.get('node_results')
                    dataflow_end = node_results.get('dataflow_status', False)

                    if dataflow_end == False:
                        click.echo(f"{node_results.get('step_name', '')}: {results} ", )
                    else:
                        click.echo(f"{node_results.get('step_name', '')}: {results} :dataflow_status", )
                    sys.stdout.flush()
                    if dataflow_end:
                        break
                    sys.stdout.flush()
                    event = node.next(timeout=5000)
def main():

    parser = argparse.ArgumentParser(description="Simple arrow sender")

    parser.add_argument(
        "--name",
        type=str,
        required=False,
        help="The name of the node in the dataflow.",
        default="hitl-agent",
    )
    parser.add_argument(
        "--data",
        type=str,
        required=False,
        help="Arrow Data as string.",
        default=None,
    )

    args = parser.parse_args()

    data = os.getenv("DATA", args.data)

    node = Node(
        args.name
    )  # provide the name to connect to the dataflow if dynamic node

    # if data is None and os.getenv("DORA_NODE_CONFIG") is None:
    send_task_and_receive_data(node)


if __name__ == "__main__":
    main()
