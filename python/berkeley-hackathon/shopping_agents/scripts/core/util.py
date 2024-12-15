import random


def assign_shopping_queries_to_agents(shopping_data:dict, shopping_agents:dict):
    all_queries = []
    for category, queries_list in shopping_data.items():
        for q in queries_list:
            all_queries.append((category, q))

    agents = list(shopping_agents.keys())
    agent_count = len(agents)
    total_queries = len(all_queries)

    assignment = {agent: [] for agent in agents}

    if total_queries > agent_count:
        random.shuffle(all_queries)
        for i, query in enumerate(all_queries):
            agent_name = agents[i % agent_count]
            assignment[agent_name].append(query)
    else:
        for i, query in enumerate(all_queries):
            assignment[agents[i]].append(query)

    final_result = []
    for agent in agents:
        queries = assignment[agent]
        web_search_data = {}
        for category, q in queries:
            if category not in web_search_data:
                web_search_data[category] = []
            web_search_data[category].append(q)

        result_item = {
            'agent_name': agent,
            'agent_output_name': shopping_agents[agent]['outputs'],
            'agent_input_name': shopping_agents[agent]['inputs'],
            'web_search_data': web_search_data
        }
        if len(web_search_data)>0:
            final_result.append(result_item)

    return final_result


