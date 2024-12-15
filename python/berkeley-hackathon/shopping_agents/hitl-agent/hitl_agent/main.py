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

import socket


class Click:

    def __init__(self):
        self.msg = ""
        self.start_server()

    def echo(self, message):
        self.msg += message + "\n\n"

    def input(self, prompt: str, send=True):
        while True:
            try:
                if send:
                    Click.send_message(self.conn, self.msg)
                self.msg = ""
                return Click.receive_message(self.conn)
            except:
                self.echo("Connection lost, please try again.")
                self.conn.close()
                conn, addr = self.server_socket.accept()
                print(f"Connected by {addr}")
                self.conn = conn
                continue

    def send_message(conn, message):
        """Send an arbitrary-sized string over a socket connection."""
        message = message.encode('utf-8')  # Encode the string into bytes
        message_length = len(message)
        conn.sendall(f"{message_length:<10}".encode('utf-8'))  # Send header with fixed length
        conn.sendall(message)  # Send the actual message

    def receive_message(conn):
        """Receive an arbitrary-sized string over a socket connection."""
        header = conn.recv(10).decode('utf-8')  # Read the 10-byte header
        if not header:
            return None
        message_length = int(header.strip())  # Get the message length from the header
        data = b""
        while len(data) < message_length:
            chunk = conn.recv(message_length - len(data))
            if not chunk:
                break
            data += chunk
        return data.decode('utf-8')  # Decode the bytes into a string

    def start_server(self, host='127.0.0.1', port=12345):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)  # Allow 5 connections to queue
        print(f"Server running on {host}:{port}...")
        self.server_socket = server_socket
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        self.conn = conn

    def release_server(self):
        self.conn.close()
        self.server_socket.close()


click = Click()

import signal


def signal_handler(sig, frame):
    click.release_server()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
def clean_string(input_string:str):
    return input_string.encode('utf-8', 'replace').decode('utf-8')
def send_task_and_receive_data(node):
    shopping_requirement_status = False
    shopping_planning_status = False
    shopping_solution_status = False
    while True:
        data = click.input(
            " Send You Task :  ",
            send=False
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
                                click.echo(results)
                                data = click.input(
                                    " Shopping Requirement Suggestions :  ",
                                    send=False
                                )
                                node.send_output("user_input", pa.array([clean_string(data)]))
                            if event['id'] == "user_shopping_requirement_result":
                                node_results = json.loads(event['value'].to_pylist()[0])
                                results = node_results.get('node_results')
                                click.echo("This is the user's requirement description.")
                                click.echo(results)
                                shopping_requirement_status = True
                                break
                            event = node.next(timeout=5000)
                    if shopping_planning_status is False:
                        while True:
                            if event['id'] == "shopping_planning_status":
                                node_results = json.loads(event['value'].to_pylist()[0])
                                results = node_results.get('node_results')
                                click.echo(results)
                                data = click.input(
                                    " Agent Shopping Plan Suggestions:  ",
                                    send=False
                                )
                                node.send_output("shopping_plan_user_input", pa.array([clean_string(data)]))

                            if event['id'] == "shopping_planning_result":
                                node_results = json.loads(event['value'].to_pylist()[0])
                                results = node_results.get('node_results')
                                click.echo("This is the user's requirement description.")
                                click.echo(results)
                                shopping_requirement_status = True
                                break
                            event = node.next(timeout=5000)
                    if shopping_solution_status is False:
                        while True:
                            if event['id'] == "shopping_solution_status":
                                node_results = json.loads(event['value'].to_pylist()[0])
                                results = node_results.get('node_results')
                                click.echo(results)
                                data = click.input(" Please re-enter your suggestions for the shopping plan :  ",
                                                   send=False)
                                node.send_output("shopping_solution_user_input", pa.array([clean_string(data)]))

                            if event['id'] == "shopping_solution_result":
                                node_results = json.loads(event['value'].to_pylist()[0])
                                results = node_results.get('node_results')
                                click.echo("This is the user's requirement description.")
                                click.echo(results)
                                shopping_requirement_status = True
                                break
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
