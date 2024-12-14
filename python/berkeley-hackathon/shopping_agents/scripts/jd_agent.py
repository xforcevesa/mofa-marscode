# import os
# from dora import Node, DoraStatus
# import pyarrow as pa
# from mofa.kernel.utils.util import load_agent_config, create_agent_output, load_node_result
# from mofa.run.run_agent import run_dspy_or_crewai_agent
# from mofa.utils.files.dir import get_relative_path
# from mofa.utils.log.agent import record_agent_result_log
#
#
# class Operator:
#     def __init__(self):
#         self.task = None
#         self.context_rag = None
#
#     def on_event(
#             self,
#             dora_event,
#             send_output,
#     ) -> DoraStatus:
#         if dora_event["type"] == "INPUT":
#             if dora_event['id'] == 'web_search_task':
#                 self.task = load_node_result(dora_event["value"][0].as_py())
#                 web_search_tasks = list(self.task.values())
#                 for web_search_text in web_search_tasks:
#
#                 send_output("reasoner_response", pa.array([create_agent_output(step_name='reasoner_response',
#                                                                                output_data=agent_result,
#                                                                                dataflow_status=os.getenv(
#                                                                                    'IS_DATAFLOW_END', True))]),
#                             dora_event['metadata'])
#                 print({"task": self.task, 'response': agent_result})
#                 print('reasoner_response:', agent_result)
#
#         return DoraStatus.CONTINUE