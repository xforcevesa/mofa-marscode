import os
import time

from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, create_agent_output, load_node_result
from core.user_shopping_requirement import RequirementClarificationAgent
from dotenv import load_dotenv

class Operator:
    def __init__(self):
        load_dotenv('.env.secret')
        self.api_key = os.getenv("API_KEY")
        self.user_shopping_requirement = RequirementClarificationAgent(api_key=self.api_key)
        self.task = None
        self.max_loop_num = 3
        self.local_loop_num = 0
    def on_event(
            self,
            dora_event,
            send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event['id'] == "user_input":
                t1 = time.time()
                send_output("user_shopping_requirement_agent_status", pa.array([create_agent_output(step_name='user_shopping_requirement_agent_status',
                                                                                 output_data={
                                                                                     'agent_name': 'user_shopping_requirement_agent',
                                                                                     'agent_status': 'Running'},
                                                                                 dataflow_status=os.getenv(
                                                                                     'IS_DATAFLOW_END', False))]),
                            dora_event['metadata'])
                self.task = dora_event["value"][0].as_py()
                message = self.user_shopping_requirement.generate_message(user_input=self.task)
                llm_output = self.user_shopping_requirement.send_request(messages=message)
                print('-------: ',llm_output)
                json_data = self.user_shopping_requirement.extract_json(llm_output)

                if json_data:
                    self.user_shopping_requirement.final_json = json_data
                    send_output("user_shopping_requirement_result",
                                pa.array([create_agent_output(step_name='user_shopping_requirement_result',
                                                              output_data=json_data,
                                                              dataflow_status=os.getenv(
                                                                  'IS_DATAFLOW_END', True))]),
                                dora_event['metadata'])
                    self.user_shopping_requirement = RequirementClarificationAgent(api_key=self.api_key)
                    send_output("user_shopping_requirement_agent_status", pa.array([create_agent_output(step_name='user_shopping_requirement_agent_status',
                                                                                     output_data={
                                                                                         'agent_name': 'user_shopping_requirement_agent',
                                                                                         'agent_status': 'Finish',
                                                                                         'use_time': time.time() - t1},
                                                                                     dataflow_status=os.getenv(
                                                                                         'IS_DATAFLOW_END', False))]),
                                dora_event['metadata'])
                    self.local_loop_num = 0

                else:
                    self.local_loop_num += 1
                    send_output("user_shopping_requirement_status",
                                pa.array([create_agent_output(step_name='user_shopping_requirement_status',
                                                              output_data=llm_output,
                                                              dataflow_status=os.getenv(
                                                                  'IS_DATAFLOW_END', False))]),
                                dora_event['metadata'])

        return DoraStatus.CONTINUE

