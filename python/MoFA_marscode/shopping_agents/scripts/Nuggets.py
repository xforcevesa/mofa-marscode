import json
import os
import time
from typing import List, Dict

from dora import Node, DoraStatus
import pyarrow as pa
from mofa.utils.ai.conn import create_openai_client
from mofa.kernel.utils.util import load_agent_config, create_agent_output, load_node_result
from core.web_search.bronners_chrismas_wonderland import fetch_html_with_undetected_chromedriver
from bs4 import BeautifulSoup  # new module


class JueJinOperator:
    def __init__(self):
        self.task = None
        self.timeout = 600  

    def on_event(
            self,
            dora_event,
            send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event['id'] == 'juejin_search':
                all_results = []
                t1 = time.time()
                send_output("juejin_agent_status", pa.array([create_agent_output(step_name='juejin_agent_status',
                                                                                output_data={
                                                                                    'agent_name': 'juejin_agent',
                                                                                    'agent_status': 'Running'},
                                                                                dataflow_status=os.getenv(
                                                                                    'IS_DATAFLOW_END', False))]),
                           dora_event['metadata'])

                self.task = json.loads(load_node_result(dora_event["value"][0].as_py()))
                print('任务数据: ', self.task)

                search_keywords = [item for values_list in self.task.values() for item in values_list]

                for keyword in search_keywords:
                    if time.time() - t1 > self.timeout: 
                        break
                    try:
                        url = f"https://juejin.cn/search?query={keyword}&type=all"
                        html_content = fetch_html_with_undetected_chromedriver(url=url)

                        articles = self.parse_juejin_html(html_content)
                        all_results.extend(articles)
                    except Exception as e:
                        print(f"爬取过程中发生错误: {e}")
                        continue

                print('掘金爬取结果: ', all_results)

                send_output("juejin_search_result", pa.array([create_agent_output(step_name='juejin_search_result',
                                                                                 output_data=all_results,
                                                                                 dataflow_status=os.getenv(
                                                                                     'IS_DATAFLOW_END', False))]),
                           dora_event['metadata'])

                send_output("juejin_agent_status", pa.array([create_agent_output(step_name='juejin_agent_status',
                                                                                output_data={
                                                                                    'agent_name': 'juejin_agent',
                                                                                    'agent_status': 'Finish',
                                                                                    'use_time': time.time() - t1},
                                                                                dataflow_status=os.getenv(
                                                                                    'IS_DATAFLOW_END', False))]),
                           dora_event['metadata'])

        return DoraStatus.CONTINUE

    @staticmethod
    def parse_juejin_html(html_content: str) -> List[Dict]:
        """
        :param html_content: get html content
        :return:get artical imformation
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = []

        # HACK: need to adjust selector
        for item in soup.select('.content-box'):
            title = item.select_one('.title')
            author = item.select_one('.user-name')
            link = item.select_one('a')['href']
            if title and author and link:
                articles.append({
                    'title': title.text.strip(),
                    'author': author.text.strip(),
                    'link': f"https://juejin.cn{link}"
                })

        return articles
