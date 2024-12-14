import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import  create_agent_output, load_node_result
from core.shopping_needs_analysis import analyze_shopping_needs,ShoppingPlan,extract_web_search_text_by_product_type

class Operator:
    def __init__(self):
        self.user_requirement = None
        self.user_suggestions_messages = []
        self.max_loop_num = 3
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event['id'] == 'user_requirement':

                self.user_requirement = load_node_result(dora_event["value"][0].as_py())
                print("-------: self.user_requirement   : ",self.user_requirement)
                result = analyze_shopping_needs(shopping_requirements=self.user_requirement,format_class=ShoppingPlan,)
                result_data = result.json()
                print('result_data:', result_data)
                send_output("shopping_planning_status", pa.array([create_agent_output(step_name='shopping_plan_generator_response', output_data=result_data,dataflow_status=os.getenv('IS_DATAFLOW_END',False))]),dora_event['metadata'])
                self.max_loop_num += 1
            elif dora_event['id'] == 'user_input':
                user_input = dora_event["value"][0].as_py()
                self.user_suggestions_messages.append(json.dumps({"user_input":user_input}))
                result = analyze_shopping_needs(format_class=ShoppingPlan,shopping_requirements=self.user_requirement,user_suggestions=json.dumps(self.user_suggestions_messages))
                print('user_input output-------- : ',result.json())
                if result.Continue_Analysis is False:
                    send_output("shopping_planning_status",
                                pa.array([create_agent_output(step_name='shopping_planning_status',
                                                              output_data=result.json(),
                                                              dataflow_status=os.getenv(
                                                                  'IS_DATAFLOW_END', False))]),
                                dora_event['metadata'])
                    self.max_loop_num+=1
                elif self.max_loop_num >5 or result.Continue_Analysis is True:
                    send_output("shopping_planning_status",
                                pa.array([create_agent_output(step_name='shopping_planning_status',
                                                              output_data="yes",
                                                              dataflow_status=os.getenv(
                                                                  'IS_DATAFLOW_END', False))]),

                                dora_event['metadata'])
                    shopping_web_search = extract_web_search_text_by_product_type(shopping_plan=result)
                    print('  shopping_web_search   : ',shopping_web_search)
                    send_output("shopping_planning_result",
                                pa.array([create_agent_output(step_name='shopping_planning_result',
                                                              output_data=shopping_web_search,
                                                              dataflow_status=os.getenv(
                                                                  'IS_DATAFLOW_END', False))]),

                                dora_event['metadata'])
                    self.max_loop_num = 0
        return DoraStatus.CONTINUE