import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output, load_node_result
from prompt import think_base_prompt,shopping_plan_validator_prompt
from shopping_needs_analysis import analyze_shopping_needs, ShoppingPlanSolutions, \
    extract_web_search_text_by_product_type

# class Operator:
#     def __init__(self):
#         self.shopping_data = None
#         self.product_plan = None
#     def on_event(
#         self,
#         dora_event,
#         send_output,
#     ) -> DoraStatus:
#         if dora_event["type"] == "INPUT":
#             if dora_event['id'] == 'shopping_data':
#                 self.shopping_data = load_node_result(dora_event["value"][0].as_py())
#                 messages = [
#                     {"role": "system",
#                      "content": think_base_prompt},
#                     {"role": "user",
#                      "content": shopping_plan_validator_prompt(product_data=self.shopping_data.get('product_data'),
#                                                                product_plan=self.shopping_data.get('product_plan'))}, ]
#                 result = analyze_shopping_needs(messages=messages,format_class=ShoppingPlanSolutions)
#                 result_data = result.to_dict()
#                 print('result_data:', result_data)
#                 send_output("shopping_plan_strategist_response", pa.array([create_agent_output(step_name='shopping_plan_strategist_response', output_data=result_data,dataflow_status=os.getenv('IS_DATAFLOW_END',False))]),dora_event['metadata'])
#                 print('shopping_plan_strategist_response:', result_data)
#
#         return DoraStatus.CONTINUE

# search_text = "我想要一个家庭影院系统"
# shopping_plan = analyze_shopping_needs(shopping_requirements=search_text)
# shopping_web_search = extract_web_search_text_by_product_type(shopping_plan=shopping_plan)