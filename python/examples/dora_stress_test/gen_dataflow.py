import yaml

def create_dataflow(num_agents=30):
    dataflow = {
        "nodes": [
            {
                "id": "terminal-input",
                "build": "pip install -e ../../node-hub/terminal-input",
                "path": "dynamic",
                "outputs": ["data"],
                "inputs": {
                    "agent_response": "final-node/final_output"
                }
            }
        ]
    }

    # 定义基础 agent IDs
    agent_base_ids = [f"agent_{i}" for i in range(5)]  # agent_0 至 agent_4
    agent_counters = {agent_id: 0 for agent_id in agent_base_ids}  # 记录每个 agent_id 的实例数量

    # 创建多个 agent 节点，确保每个 ID 唯一
    for i in range(num_agents):
        agent_base_id = agent_base_ids[i % 5]
        agent_counters[agent_base_id] += 1
        instance = agent_counters[agent_base_id]
        unique_agent_id = f"{agent_base_id}_{instance}"
        agent_node = {
            "id": unique_agent_id,
            "operator": {
                "python": "scripts/agent.py",
                "inputs": {
                    "task": "terminal-input/data"
                },
                "outputs": ["agent_response"]
            }
        }
        dataflow["nodes"].append(agent_node)

    # 创建 final-node，收集所有 agent 节点的输出
    final_node = {
        "id": "final-node",
        "operator": {
            "python": "scripts/final_node.py",
            "inputs": {},
            "outputs": ["final_output"]
        }
    }

    # 添加所有 agent 节点的输出到 final-node 的 inputs，确保键唯一
    for agent_base_id in agent_base_ids:
        for instance in range(1, agent_counters[agent_base_id] + 1):
            input_key = f"{agent_base_id}_response_{instance}"
            input_value = f"{agent_base_id}_{instance}/agent_response"
            final_node["operator"]["inputs"][input_key] = input_value

    # 添加 terminal-input 的输出到 final-node 的 inputs
    final_node["operator"]["inputs"]["terminal-input/data"] = "data"

    # 将 final-node 添加到 dataflow
    dataflow["nodes"].append(final_node)

    return dataflow

# 生成 dataflow.yml
dataflow = create_dataflow(num_agents=30)

# 将 dataflow 转换为 YAML 格式并保存到文件
with open("dataflow.yml", "w", encoding='utf-8') as file:
    yaml.dump(dataflow, file, sort_keys=False, allow_unicode=True)

print("dataflow.yml 已生成。")
