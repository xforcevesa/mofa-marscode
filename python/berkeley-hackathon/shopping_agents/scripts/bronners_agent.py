import json
import os
import time

from dora import Node, DoraStatus
import pyarrow as pa
from mofa.utils.ai.conn import create_openai_client
from mofa.kernel.utils.util import load_agent_config, create_agent_output, load_node_result
from core.web_search.bronners_chrismas_wonderland import fetch_html_with_undetected_chromedriver
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
            if dora_event['id'] == 'bronners_search':
                all_results = []
                t1 = time.time()
                self.task = json.loads(load_node_result(dora_event["value"][0].as_py()))
                llm_client = create_openai_client()
                print('-------: ',self.task)
                # web_search_tasks = [item for values_list in self.task.values() for item in values_list]
                web_search_tasks = [item for values_list in self.task.values() for item in values_list]
                for web_search_text in web_search_tasks:
                    if time.time() - t1 > self.timeout:
                        break
                    try:
                        html_context = fetch_html_with_undetected_chromedriver(search_text=web_search_text)
                        web_result = shopping_html_structure(llm_client=llm_client,html_content=html_context,search_text=web_search_text)
                        all_results.append(web_result)
                    except Exception as e:
                        print(e)
                        continue
                print('bronners_shopping_result : ',all_results )

                send_output("bronners_shopping_result", pa.array([create_agent_output(step_name='bronners_shopping_result',
                                                                               output_data=all_results,
                                                                               dataflow_status=os.getenv(
                                                                                   'IS_DATAFLOW_END', False))]),
                            dora_event['metadata'])

        return DoraStatus.CONTINUE



