import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_result_log

agents = {
    "A": "to_term",
    "B": "to_agent",
    "C": "to_agent_2"
}

class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            task = dora_event["value"][0].as_py()
            print(f"Received task: {task}")
            # The task may be a JSON string,
            # so we need to convert it back to a Python object
            # and extract the node_results field
            try:
                task_json = json.loads(task)
                task = task_json["node_results"]
            except:
                pass
            flag = task[:3]
            flag = flag.upper()
            from_agent = flag[0] # A B
            to_agent = flag[1]
            if to_agent in agents:
                to_agent = agents[to_agent]
            print(f"Received task from {from_agent}: {task}")
            if to_agent == "to_term":
                send_output(to_agent, pa.array([create_agent_output(step_name='agent_comm', output_data=task,dataflow_status=os.getenv('IS_DATAFLOW_END',True))]),dora_event['metadata'])
            else:
                send_output(to_agent, pa.array([task]),dora_event['metadata'])
        return DoraStatus.CONTINUE