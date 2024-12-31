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
import threading
import time

class Click:

    def __init__(self):
        self.msg = ""
        self.node_info = {}
        self.node_info_lock = threading.Lock()
        self.message_lock = threading.Lock()
        self.start_server()
        self.first_run = True
        self.thread = threading.Thread(target=Click.listen_loop, args=(self,))
        self.thread.start()

    def listen_loop(self):
        while True:
            with self.node_info_lock:
                node_info_str = str(self.node_info)
            self.send_message(self.conn, node_info_str, signal=True)
            time.sleep(0.1)

    def echo(self, message):
        self.msg += message + "\n\n"

    def input(self, prompt: str, send=True):
        if send:
            print(f"Sending: {self.msg}")
            self.send_message(self.conn, self.msg)
            print(f"Sent: {self.msg}")
        elif not self.first_run:
            self.send_message(self.conn, self.msg, end=True)
        else:
            self.first_run = False
        self.msg = ""
        print("Receiving input...")
        recv_msg = self.receive_message(self.conn)
        print(f"Received: {recv_msg}")
        return recv_msg

    def send_message(self, conn, message, signal=False, end=False):
        """Send an arbitrary-sized string over a socket connection."""
        message = message.encode('utf-8')  # Encode the string into bytes
        message_length = len(message)
        with self.message_lock:
            # print(f"Sending {message_length} bytes, message: {message.decode('utf-8')}, header: " + f"S{message_length:<10}, len: {len(f'S{message_length:<10}'.encode('utf-8'))}")
            if signal:
                conn.sendall(f"S{message_length:<10}".encode('utf-8'))  # Send header with fixed length
            elif not end:
                conn.sendall(f"N{message_length:<10}".encode('utf-8'))  # Send header with fixed length
            else:
                conn.sendall(f"E{message_length:<10}".encode('utf-8'))  # Send header with fixed length
            conn.sendall(message)  # Send the actual message

    def receive_message(self, conn):
        """Receive an arbitrary-sized string over a socket connection."""
        with self.message_lock:
            header = conn.recv(11).decode('utf-8')  # Read the 10-byte header
            if not header:
                return None
            message_length = int(header[1:].strip())  # Get the message length from the header
            data = b""
            while len(data) < message_length:
                chunk = conn.recv(message_length - len(data))
                if not chunk:
                    break
                data += chunk
        # print(f"Received {message_length} bytes, message: {data.decode('utf-8')}")
        return data.decode('utf-8')  # Decode the bytes into a string

    def start_server(self, host='127.0.0.1', port=12345):
        with self.message_lock:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((host, port))
            server_socket.listen(5)  # Allow 5 connections to queue
            print(f"Server running on {host}:{port}...")
            self.server_socket = server_socket
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")
            self.conn = conn

    def release_server(self):
        with self.message_lock:
            self.conn.close()
            self.server_socket.close()


click = Click()

# import signal


def signal_handler(sig, frame):
    click.release_server()
    sys.exit(0)

def click_log(event,click,node_ids:list=None):
    if node_ids is None:
        node_ids = ['user_shopping_requirement_agent_status','shopping_plan_agent_status','amazon_agent_status','bronners_agent_status','worldmarket_agent_status','minted_agent_status','balsamhill_agent_status','shopping_solution_agent_status','christmaslightsetc_agent_status','notonthehighstreet_agent_status']
    if event['id'] in node_ids:
        node_results = json.loads(event['value'].to_pylist()[0])
        results = node_results.get('node_results')
        with click.node_info_lock:
            click.node_info = results

# signal.signal(signal.SIGINT, signal_handler)
# signal.signal(signal.SIGTERM, signal_handler)
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
                    click_log(event=event,click=click)
                    if shopping_requirement_status is False:
                        while True:
                            click_log(event=event, click=click)
                            if event['id'] == "user_shopping_requirement_status":
                                click_log(event=event, click=click)
                                node_results = json.loads(event['value'].to_pylist()[0])
                                results = node_results.get('node_results')
                                click.echo(results)
                                data = click.input(
                                    " Shopping Requirement Suggestions :  ",
                                )
                                node.send_output("user_input", pa.array([clean_string(data)]))
                                click_log(event=event, click=click)
                            if event['id'] == "user_shopping_requirement_result":
                                click_log(event=event, click=click)
                                node_results = json.loads(event['value'].to_pylist()[0])
                                results = node_results.get('node_results')
                                click.echo("This is the user's requirement description.")
                                click.echo(results)
                                shopping_requirement_status = True
                                click_log(event=event, click=click)
                                break
                            click_log(event=event, click=click)
                            event = node.next(timeout=5000)
                    if shopping_planning_status is False:
                        while True:
                            click_log(event=event, click=click)
                            if event['id'] == "shopping_planning_status":
                                click_log(event=event, click=click)
                                node_results = json.loads(event['value'].to_pylist()[0])
                                results = node_results.get('node_results')
                                click.echo(results)
                                click_log(event=event, click=click)
                                data = click.input(
                                    " Agent Shopping Plan Suggestions:  ",
                                )
                                node.send_output("shopping_plan_user_input", pa.array([clean_string(data)]))
                                click_log(event=event, click=click)

                            if event['id'] == "shopping_planning_result":
                                click_log(event=event, click=click)
                                node_results = json.loads(event['value'].to_pylist()[0])
                                results = node_results.get('node_results')
                                click_log(event=event, click=click)
                                click.echo("This is the user's requirement description.")
                                click.echo(results)
                                shopping_requirement_status = True
                                break
                            click_log(event=event, click=click)
                            event = node.next(timeout=5000)
                    if shopping_solution_status is False:
                        click_log(event=event, click=click)
                        while True:
                            click_log(event=event, click=click)
                            if event['id'] == "shopping_solution_status":
                                click_log(event=event, click=click)
                                node_results = json.loads(event['value'].to_pylist()[0])
                                results = node_results.get('node_results')
                                click.echo(results)
                                data = click.input(" Please re-enter your suggestions for the shopping plan :  ",)
                                node.send_output("shopping_solution_user_input", pa.array([clean_string(data)]))
                                click_log(event=event, click=click)
                            if event['id'] == "shopping_solution_result":
                                click_log(event=event, click=click)
                                node_results = json.loads(event['value'].to_pylist()[0])
                                results = node_results.get('node_results')
                                click.echo("This is the user's requirement description.")
                                click.echo(results)
                                shopping_requirement_status = True
                                click_log(event=event, click=click)
                                break
                            event = node.next(timeout=5000)

                    click_log(event=event, click=click)
                    node_results = json.loads(event['value'].to_pylist()[0])
                    results = node_results.get('node_results')
                    dataflow_end = node_results.get('dataflow_status', False)
                    click_log(event=event, click=click)
                    if dataflow_end == False:
                        click.echo(f"{node_results.get('step_name', '')}: {results} ", )
                    else:
                        click.echo(f"{node_results.get('step_name', '')}: {results} :dataflow_status", )
                    sys.stdout.flush()
                    if dataflow_end:
                        break
                    sys.stdout.flush()
                    event = node.next(timeout=5000)
                    click_log(event=event, click=click)
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
