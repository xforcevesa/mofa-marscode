



import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import  create_agent_output, load_node_result
from core.shopping_needs_analysis import analyze_shopping_needs,ShoppingPlan,extract_web_search_text_by_product_type
from core.util import assign_shopping_queries_to_agents
from mofa.utils.files.dir import get_relative_path
from mofa.utils.files.read import read_yaml


class Operator:
    def __init__(self):
        self.user_requirement = None
        self.user_suggestions_messages = []
        self.max_loop_num = 4
        yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs',
                                           target_file_name='shopping_agent.yml')
        shopping_data = read_yaml(file_path=yaml_file_path)
        self.shopping_agents = shopping_data

    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":


            if dora_event['id'] == 'user_requirement':

                self.user_requirement = load_node_result(dora_event["value"][0].as_py())
                # print("-------: self.user_requirement   : ",self.user_requirement)
                # result = analyze_shopping_needs(shopping_requirements=self.user_requirement,format_class=ShoppingPlan,)
                # result_data = result.json()
                # print('result_data:', self.user_requirement)
                send_output("shopping_planning_status", pa.array([create_agent_output(step_name='shopping_planning_status', output_data='data',dataflow_status=os.getenv('IS_DATAFLOW_END',False))]),dora_event['metadata'])
                self.max_loop_num += 1
            elif dora_event['id'] == 'shopping_plan_user_input':
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
                elif self.max_loop_num >self.max_loop_num or result.Continue_Analysis is True:

                    shopping_web_search = extract_web_search_text_by_product_type(shopping_plan=result)
                    print('shopping_web_search: ',shopping_web_search)
                    all_output_names = []
                    for data in assign_shopping_queries_to_agents(shopping_data=shopping_web_search,shopping_agents=self.shopping_agents):
                        send_output(data.get('agent_input_name'),
                                    pa.array([create_agent_output(step_name=data.get('agent_input_name'),
                                                                  output_data=data.get("web_search_data"),
                                                                  dataflow_status=os.getenv(
                                                                      'IS_DATAFLOW_END', False))]),

                                    dora_event['metadata'])
                        all_output_names.append({'agent_output_name':data.get('agent_output_name'),'agent_status':False})
                    print('shopping_planning_output_agents : ',all_output_names)
                    send_output("shopping_planning_output_agents",
                                pa.array([create_agent_output(step_name="shopping_planning_output_agents",
                                                              output_data=all_output_names,
                                                              dataflow_status=os.getenv(
                                                                  'IS_DATAFLOW_END', False))]),

                                dora_event['metadata'])
                    print('  shopping_web_search   : ',shopping_web_search)
                    send_output("shopping_planning_result",
                                pa.array([create_agent_output(step_name='shopping_planning_result',
                                                              output_data=shopping_web_search,
                                                              dataflow_status=os.getenv(
                                                                  'IS_DATAFLOW_END', False))]),

                                dora_event['metadata'])

                    self.max_loop_num = 0
        return DoraStatus.CONTINUE