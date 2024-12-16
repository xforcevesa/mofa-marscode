import json
import os
import time

from dora import Node, DoraStatus
import pyarrow as pa
from mofa.utils.ai.conn import create_openai_client, load_llm_api_key_by_env_file
from mofa.kernel.utils.util import load_agent_config, create_agent_output, load_node_result
from core.web_search.scraper import christmaslightsetc_scraper
from core.web_search.util import shopping_html_structure
class Operator:
    def __init__(self):
        self.task = None
        self.timeout = 240

    def on_event(
            self,
            dora_event,
            send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event['id'] == 'christmaslightsetc_search':
                all_results = []
                t1 = time.time()
                send_output("christmaslightsetc_agent_status", pa.array([create_agent_output(step_name='christmaslightsetc_agent_status',
                                                                                    output_data={'agent_name':'christmaslightsetc_agent','agent_status':'Running'},
                                                                                    dataflow_status=os.getenv(
                                                                                        'IS_DATAFLOW_END', False))]),
                            dora_event['metadata'])
                self.task = json.loads(load_node_result(dora_event["value"][0].as_py()))
                api_key = load_llm_api_key_by_env_file()

                print('-------: ',self.task)
                web_search_tasks = [item for values_list in self.task.values() for item in values_list]
                for web_search_text in web_search_tasks:
                    if time.time() - t1 > self.timeout:
                        break
                    try:
                        web_result = christmaslightsetc_scraper(search_keyword=web_search_text,api_key=api_key,)
                        all_results.append(web_result.json())
                    except Exception as e :
                        print(e)
                        continue
                print(" christmaslightsetc_result  :  ",all_results)
                send_output("christmaslightsetc_shopping_result", pa.array([create_agent_output(step_name='christmaslightsetc_shopping_result',
                                                                               output_data=all_results,
                                                                               dataflow_status=os.getenv(
                                                                                   'IS_DATAFLOW_END', False))]),
                            dora_event['metadata'])
                send_output("christmaslightsetc_agent_status", pa.array([create_agent_output(step_name='christmaslightsetc_agent_status',
                                                                                    output_data={'agent_name':'christmaslightsetc_agent','agent_status':'Finish','use_time':time.time()-t1},
                                                                                    dataflow_status=os.getenv(
                                                                                        'IS_DATAFLOW_END', False))]),
                            dora_event['metadata'])

        return DoraStatus.CONTINUE