import random


# def assign_shopping_queries_to_agents(shopping_data:dict, shopping_agents:dict):
#     all_queries = []
#     for category, queries_list in shopping_data.items():
#         for q in queries_list:
#             all_queries.append((category, q))
#
#     agents = list(shopping_agents.keys())
#     agent_count = len(agents)
#     total_queries = len(all_queries)
#
#     assignment = {agent: [] for agent in agents}
#
#     if total_queries > agent_count:
#         random.shuffle(all_queries)
#         for i, query in enumerate(all_queries):
#             agent_name = agents[i % agent_count]
#             assignment[agent_name].append(query)
#     else:
#         for i, query in enumerate(all_queries):
#             assignment[agents[i]].append(query)
#
#     final_result = []
#     for agent in agents:
#         queries = assignment[agent]
#         web_search_data = {}
#         for category, q in queries:
#             if category not in web_search_data:
#                 web_search_data[category] = []
#             web_search_data[category].append(q)
#
#         result_item = {
#             'agent_name': agent,
#             'agent_output_name': shopping_agents[agent]['outputs'],
#             'agent_input_name': shopping_agents[agent]['inputs'],
#             'web_search_data': web_search_data
#         }
#         if len(web_search_data)>0:
#             final_result.append(result_item)
#
#     return final_result
import random
import json
from typing import List, Dict


def assign_shopping_queries_to_agents(shopping_data: Dict[str, List[str]],
                                      shopping_agents: Dict[str, Dict[str, List[str]]]) -> List[Dict]:
    """
    将购物查询随机分配给各个代理，并返回最终的分配结果列表。

    参数：
        shopping_data (dict): 购物数据，键为类别，值为查询列表。
        shopping_agents (dict): 购物代理配置，键为代理名称，值为包含 'inputs' 和 'outputs' 的字典。

    返回：
        list: 包含每个代理分配查询的字典列表。
    """
    all_queries = []
    # 收集所有 (category, query) 对
    for category, queries_list in shopping_data.items():
        for q in queries_list:
            all_queries.append((category, q))

    if not all_queries:
        return []

    agents = list(shopping_agents.keys())
    if not agents:
        raise ValueError("No shopping agents available for assignment.")

    # 初始化每个代理的分配列表
    assignment = {agent: [] for agent in agents}

    # 确保代理列表被正确打乱
    random.shuffle(agents)

    # 随机分配每个查询给一个代理
    for query in all_queries:
        agent_name = random.choice(agents)
        assignment[agent_name].append(query)

    final_result = []
    # 构建最终的分配结果
    for agent in agents:
        queries = assignment[agent]
        web_search_data = {}
        for category, q in queries:
            if category not in web_search_data:
                web_search_data[category] = []
            web_search_data[category].append(q)

        if len(web_search_data) > 0:
            result_item = {
                'agent_name': agent,
                'agent_output_name': shopping_agents[agent]['outputs'],
                'agent_input_name': shopping_agents[agent]['inputs'],
                'web_search_data': web_search_data
            }
            final_result.append(result_item)

    return final_result


if __name__ == "__main__":
    shopping_data = {
        'Laptop': ['gaming laptop', ],
        'Phone': ['smartphone', 'feature phone'],
        'Accessories': ['mouse', 'keyboard', 'headphones'],
        # 'Tablet': ['Android tablet', 'iPad']
    }

    # 示例购物代理配置
    shopping_agents = {
        'amazon_agent': {'inputs': ['amazon_search'], 'outputs': ['amazon_shopping_result']},
        'bestbuy_agent': {'inputs': ['bestbuy_search'], 'outputs': ['bestbuy_shopping_result']},
        'ebay_agent': {'inputs': ['ebay_search'], 'outputs': ['ebay_shopping_result']},
        'newegg_agent': {'inputs': ['newegg_search'], 'outputs': ['newegg_shopping_result']}
    }
    result = assign_shopping_queries_to_agents_chunk_random(shopping_agents=shopping_agents,shopping_data=shopping_data)
    print(result)