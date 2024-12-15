import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output, load_node_result
from core.prompt import think_base_prompt,shopping_plan_validator_prompt
from core.shopping_needs_analysis import analyze_shopping_needs,ShoppingPlanSolutions

class Operator:
    def __init__(self):
        self.shopping_planning_result = None
        self.product_data = None
        self.user_inputs = []
        self.max_loop_num = 3
        self.shopping_agents = []
        self.shopping_agent_ids = []
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event['id'] == 'shopping_planning_result':
                self.shopping_planning_result = load_node_result(dora_event["value"][0].as_py())
            if dora_event['id'] == 'product_data':
                self.product_data = load_node_result(dora_event["value"][0].as_py())
            if dora_event['id'] == 'shopping_solution_user_input':
                self.user_inputs.append({"role": "user", "content":dora_event["value"][0].as_py()})
            if dora_event['id'] == "shopping_planning_output_agents":
                self.shopping_agents = json.loads(load_node_result(dora_event["value"][0].as_py()))
                self.shopping_agent_ids = [item['agent_output_name'] for item in self.shopping_agents]
                print('shopping_agents : ',self.shopping_agents)
                print('shopping_agent_ids : ',self.shopping_agent_ids)
            if dora_event['id'] in self.shopping_agent_ids:
                for i in self.shopping_agents:
                    if i['agent_output_name'] == dora_event['id']:
                        i['agent_status'] = True
                        i['shopping_web_result'] = load_node_result(dora_event["value"][0].as_py())
            print('----- self.shopping_agent_ids : ',self.shopping_agent_ids)
            agent_ready = all(d.get('agent_status') == True for d in self.shopping_agents)
            if agent_ready:

                messages = [
                    {"role": "system",
                     "content": think_base_prompt},
                    {"role": "user",
                     "content": shopping_plan_validator_prompt(product_data=self.shopping_planning_result,product_plan=json.dumps(self.product_data))},]
                if len(self.user_inputs) >0:
                    messages+= self.user_inputs

                result = analyze_shopping_needs(messages=messages,format_class=ShoppingPlanSolutions)
                print('shopping_solution_result  : ',result.json())
                if result.User_Review is True or self.max_loop_num >3:
                    send_output("shopping_solution_result",pa.array([create_agent_output(step_name='shopping_solution_result',output_data=result.json(),dataflow_status=os.getenv('IS_DATAFLOW_END', True))]),dora_event['metadata'])
                    self.shopping_agents = []
                    self.shopping_planning_result = None
                    self.shopping_agent_ids = []
                    self.max_loop_num = 3
                else:
                    send_output("shopping_solution_status",pa.array([create_agent_output(step_name='shopping_solution_status',output_data=result.json(),dataflow_status=os.getenv('IS_DATAFLOW_END', False))]),dora_event['metadata'])
                    self.max_loop_num +=1
        return DoraStatus.CONTINUE