import socket
import time
from types import TracebackType
from typing import Callable
import streamlit as st
from mofa.utils.ai.conn import load_llm_api_key_by_env_file
from openai import chat
import openai

class OpenAIClient:
    def __init__(self, api_key=load_llm_api_key_by_env_file(dotenv_path="../shopping_agents/.env.secret")):
        self.api_key = api_key
    
    def generate_text(self, prompt):
        """Generate text using OpenAI's GPT-4 model."""
        # Save the previous openai.api_key
        prev_api_key = openai.api_key
        # Set the API key
        openai.api_key = self.api_key
        # Generate the text using OpenAI's GPT-4 model
        import os
        prev_env_api_key = os.environ.get("OPENAI_API_KEY", None)
        os.environ["OPENAI_API_KEY"] = self.api_key
        response = chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Help me with my text enhancement on shopping decision making. The output text should be in a markdown format and should have tables if necessary."},
                {"role": "user", "content": str(prompt) + "\r\n\r\n According to the text or json above, enhance the text further. Output should be in a markdown format and should not have any other content and should not have markdown in the ``` code blocks. If we need user input, we can ask for it in the chat interface. The original content should not be changed. Only optimize the expression."}
            ],
            max_tokens=4096,
            temperature=0.9,
        )
        # Set the API key back to the previous value
        openai.api_key = prev_api_key
        if prev_env_api_key is not None:
            os.environ["OPENAI_API_KEY"] = prev_env_api_key
        else:
            del os.environ["OPENAI_API_KEY"]

        response_text = ""

        for completion in response.choices:
            response_text += completion.message.content + "\n"

        return response_text

def send_message(sock, message, signal=False):
    """Send an arbitrary-sized string over a socket."""
    message = message.encode('utf-8')  # Encode the string into bytes
    message_length = len(message)
    if signal:
        sock.sendall(f"S{message_length:<10}".encode('utf-8'))  # Send header with fixed length
    else:
        sock.sendall(f"N{message_length:<10}".encode('utf-8'))  # Send header with fixed length
    sock.sendall(message)  # Send the actual message

def _receive_message(sock):
    """Receive an arbitrary-sized string over a socket."""
    header = sock.recv(11).decode('utf-8')  # Read the 10-byte header
    if not header:
        return None
    message_length = int(header[1:].strip())  # Get the message length from the header
    data = b""
    while len(data) < message_length:
        chunk = sock.recv(message_length - len(data))
        if not chunk:
            break
        data += chunk
    return (header[0], data.decode('utf-8'))  # Decode the bytes into a string

# Sidebar title
st.sidebar.title("Dataflow Status")

placeholder = st.sidebar.empty()

def draw_graph_at_sidebar(json_text: str = "{}"):
    global placeholder
    # Sidebar graph layout
    if "boxes" not in st.session_state:
        import yaml
        yaml_file = open("../shopping_agents/shopping_dataflow.yml", "r")
        yaml_dict = yaml.safe_load(yaml_file)
        st.session_state["boxes"] = [
            [item["id"], "#800080"] for item in yaml_dict["nodes"]
        ]

    if "first" not in st.session_state:
        st.session_state["first"] = True

    if "last_text" not in st.session_state:
        st.session_state["last_text"] = ""

    json = eval(json_text)
    label = json["agent_name"] if "agent_name" in json else None
    status = json["agent_status"] if "agent_status" in json else None

    is_changed = st.session_state["last_text"] != label

    if label is not None:
        for index in range(len(st.session_state["boxes"])):
            text, _ = st.session_state["boxes"][index]
            if text == label or text == label.replace("_", "-"):
                # Recolor the box to sky blue
                st.session_state["boxes"][index][1] = "#677EFF"
            else:
                st.session_state["boxes"][index][1] = "#800080"

    if is_changed or st.session_state["first"]:
        st.session_state["first"] = False
        st.session_state["last_text"] = label
        with placeholder.container():
            # placeholder.write(json_text)
            # Render boxes
            html_text = ''.join([
                round_corner_box(
                    text=text + " - " + status \
                        if status is not None and (text == label or text == label.replace("_", "-")) \
                            else text + " - " + "Not Running",
                    color=color
                )
                for text, color in st.session_state["boxes"]
            ])
            # print(time.clock_gettime(time.CLOCK_REALTIME), html_text)
            placeholder.markdown(html_text, unsafe_allow_html=True)
    else:
        pass
        # print(time.clock_gettime(time.CLOCK_REALTIME), is_changed, st.session_state["first"], st.session_state["boxes"])

def receive_message(sock):
    """Receive an arbitrary-sized string over a socket."""
    while True:
        header, message = _receive_message(sock)
        if header == "N":
            return message
        elif header == "S":
            draw_graph_at_sidebar(json_text=message)
        elif header == "E":
            if len(message):
                return message + "\n the current session has been terminated. You can ask for a new session to help you with your shopping decision making."

def response_prompt(prompt: str):
    send_message(st.session_state.sock, prompt)
    return receive_message(st.session_state.sock) \
        if "openai" not in st.session_state else \
            st.session_state.openai.generate_text(receive_message(st.session_state.sock))

def display_chat_history():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for message in st.session_state.chat_history:
        msg = st.chat_message(message["role"])
        msg.write(message["message"])

def handle_chat(message_callback: Callable[[], str], role: str = "user"):
    message = ""
    # display an animation when waiting for the bot to respond here
    message_container = st.chat_message(role)
    with st.spinner("Bot is typing..."):
        message = message_callback()
    message_container.write(message)
    st.session_state.chat_history.append({"role": role, "message": message})

def handle_chat_str(message: str, role="user"):
    handle_chat(lambda: message, role)

def cleanup_socket():
    """Cleanup the socket connection."""
    if "sock" in st.session_state and st.session_state.sock:
        try:
            send_message(st.session_state.sock, "exit")  # Notify the server
            st.session_state.sock.close()
        except Exception as e:
            st.warning(f"Error while closing socket: {e}")
        finally:
            del st.session_state.sock
            st.session_state.connected = False
            st.warning("Disconnected from the server.")

# This function will initialize the connection and clean up if session is reloaded
def check_connection():
    if "connected" not in st.session_state:
        st.session_state.connected = False
        st.session_state.sock = None


# Function to create a round-corner box
def round_corner_box(text, color):
    return f"""
        <div style="
            background-color: {color};
            border-radius: 10px;
            padding: 2% 2%;
            margin: 2% 0;
            color: white;
            text-align: center;
            font-size: 90%;
            font-weight: bold;">
            {text}
        </div>
        """

def main():
    st.title("Shopping Agent UI")
    server_ip = "127.0.0.1"
    server_port = 12345

    check_connection()

    draw_graph_at_sidebar()

    if "openai" not in st.session_state:
        st.session_state.openai = OpenAIClient()

    if "connected" not in st.session_state:
        st.session_state.connected = False

    if not st.session_state.connected:
        try:
            st.session_state.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            st.session_state.sock.connect((server_ip, server_port))
            st.session_state.connected = True
        except Exception as e:
            st.error(f"Connection failed: {e}")

    if st.session_state.connected:
        prompt = st.chat_input("Say something")

        if prompt:
            display_chat_history()
            handle_chat_str(prompt)
            handle_chat(lambda: response_prompt(prompt), role="bot")
    else:
        st.error("Please ensure that the server is running and try again.")


if __name__ == "__main__":
    main()
