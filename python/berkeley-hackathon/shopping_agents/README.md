
# **智能购物代理系统开发方案**

## **一、项目概述**

本项目旨在搭建一套通过多代理（Agents）协同工作的智能购物系统。该系统由一个人机交互代理（HITL-Agent）和多个功能代理组成，通过自动化的任务分解与执行来满足用户的个性化购物需求。用户输入购物需求（如预算、喜好、用途）后，系统将自动分解为多个子任务（如特定平台的产品搜索）、调用相应的电商代理执行查询，并整合结果形成最终的购物方案。

本系统的核心特色在于其模块化与可扩展性：通过独立的代理（如 Amazon、Bronners、Worldmarket、Minted、Balsamhill、Christmaslightsetc、Notonthehighstreet 等）对接各电商平台，实现数据来源的平行扩展。购物规划和需求解析分离，支持动态调整用户需求和方案，让系统可以在用户反馈下快速迭代并优化最终推荐。

---

## **二、系统目标**

- **自动化需求解析**：从用户文本输入中提取购物预算、产品偏好、用途场景等关键信息。
- **任务分解与规划**：根据用户需求自动生成查询任务清单（如对多个电商平台的搜索指令）。
- **多源信息聚合**：从不同电商代理获取产品信息（价格、规格、库存等），进行跨平台比较与筛选。
- **方案生成与反馈**：为用户提供候选购物方案，并支持用户对方案的反馈与再次调整。

---

## **三、系统架构与数据流**

### **1. 关键节点（Agents）简述**

1. **HITL-Agent（hitl-agent）**  
   - **角色**：用户与系统交互的入口。  
   - **功能**：  
     - 接收用户初始需求 (`user_input`)：例如“我要在预算8000元内买一台用于游戏的笔记本电脑”。  
     - 接收用户对方案的反馈 (`shopping_solution_user_input`、`shopping_plan_user_input`)，如“更喜欢NVIDIA显卡”或“预算提高到8500元”等。  
   - **输出**：  
     - 将用户输入发送给下游的用户需求解析代理和购物规划代理。
   - **输入**：  
     - 从下游代理处获取需求解析状态、规划状态、最终方案和各代理的执行状态，便于与用户交互和展示方案。

2. **用户购物需求代理（user-shopping-requirement-agent）**  
   - **输入**：`user_input`（来自hitl-agent）  
   - **输出**：  
     - `user_shopping_requirement_status`：需求分析状态（如成功解析/需要补充信息）  
     - `user_shopping_requirement_result`：解析后的用户需求要点（预算、喜好品牌、用途场景）  
     - `user_shopping_requirement_agent_status`：该代理自身状态信息（健康度、执行时间、错误信息等）

   **作用**：将用户模糊、自然语言需求解析为结构化数据，为后续规划做准备。

3. **购物规划代理（shopping-plan-agent）**  
   - **输入**：  
     - `shopping_plan_user_input`（来自hitl-agent，用于方案规划的额外输入，如用户对方案的特定要求）  
     - `user_shopping_requirement_result`（来自需求代理的结构化需求信息）
   - **输出**：  
     - `shopping_planning_status` / `shopping_planning_result`：规划状态与结果（如已生成查询任务列表）  
     - `amazon_search`、`bronners_search`、`worldmarket_search`、`minted_search`、`balsamhill_search`、`christmaslightsetc_search`、`notonthehighstreet_search`：针对不同电商代理的搜索指令  
     - `shopping_planning_output_agents`：规划结果中涉及的目标代理列表，便于后续整合  
     - `shopping_plan_agent_status`：状态信息（如规划完成时间、规划质量指标）

   **作用**：根据用户需求，将任务分解为多个电商搜索指令，为各平台代理提供明确的查询参数（例如搜索价格区间、品牌、产品类型）。

4. **各电商代理**（如 `amazon-agent`、`bronners-agent`、`worldmarket-agent`、`minted-agent`、`balsamhill-agent`、`christmaslightsetc-agent`、`notonthehighstreet-agent`）  
   - **输入**：对应的 ..._search 指令（如 `amazon_search`）  
   - **输出**：  
     - 对应的 ..._shopping_result（如 `amazon_shopping_result`）：获取到的电商平台产品列表、价格信息和其他数据  
     - 对应的 ..._agent_status：执行状态（成功、失败、请求耗时等）

   **作用**：执行特定平台的产品查询与数据获取，为方案生成提供候选商品数据。

5. **购物解决方案代理（shopping-solution-agent）**  
   - **输入**：  
     - `shopping_planning_result`：来自规划代理的结果，用于参照用户需求  
     - `shopping_solution_user_input`：用户针对最终方案的反馈  
     - `shopping_planning_output_agents`：规划阶段所涉及的电商代理列表  
     - 各电商代理的 ..._shopping_result：来自不同平台的产品数据
   - **输出**：  
     - `shopping_solution_status` / `shopping_solution_result`：最终方案的状态与结果（如已生成3个备选方案）  
     - `shopping_solution_agent_status`：该代理自身状态信息

   **作用**：根据用户需求和各平台返回的数据，对候选产品进行筛选、组合与排序，生成最终购物方案。如多个方案超出预算，则提供替换建议；若用户不满意，可依其反馈重新计算方案。

---

### **2. 数据流示例**

1. 用户在 HITL-Agent 输入需求 → HITL-Agent 将输入转发给 user-shopping-requirement-agent 解析 → user-shopping-requirement-agent 输出结构化结果与状态 → shopping-plan-agent 使用需求结果与用户附加输入生成搜索指令 → 各电商代理根据搜索指令返回产品数据 → shopping-solution-agent 整合电商数据并生成最终方案 → HITL-Agent 接收方案和状态后向用户展示。

---

## **四、工作流程示例**

**情境**：用户想购买一款适合家庭影院环境的投影仪，预算5000元。

1. **用户输入**：  
   在 HITL-Agent 中输入：“我想买一台预算5000元的投影仪，用来在家看电影。”

2. **需求解析**：  
   user-shopping-requirement-agent 从输入中提取“预算：5000元、产品类型：投影仪、使用场景：家庭影院”。

3. **任务规划**：  
   shopping-plan-agent 接收需求解析结果，根据预设的电商平台，生成 `amazon_search`、`worldmarket_search` 等指令（如搜索关键词“home theater projector”、价格范围0-5000元）。

4. **平台查询**：  
   amazon-agent、worldmarket-agent 等收到各自的搜索指令并查询数据源，返回相应的投影仪产品数据（价格、品牌、分辨率、用户评价）。

5. **方案生成**：  
   shopping-solution-agent 收集各平台结果，对比价格、性能和用户评价，生成2-3个备选方案供用户选择，并返回给 HITL-Agent。

6. **用户反馈**：  
   若用户对方案不满意，可以在 HITL-Agent 输入反馈（如“我希望分辨率更高一点，预算增加到6000元”），系统将再次进行规划与查询，直至用户满意。

---



## **五、总结**

该智能购物代理系统在模块化和可扩展性方面具备显著优势：  
- 用户输入 → 需求解析 → 方案规划 → 多平台查询 → 方案整合 → 用户反馈的流程清晰且易于扩展。  
- 引入多电商代理使数据来源更加多元，提高推荐可信度和多样性。  
- 系统可根据用户反馈快速迭代推荐方案，提高用户满意度。  
- 通过状态输出与监控机制，可持续优化系统性能与稳定性。


## **六、运行程序**

1. 首先进入到 `python/berkeley-hackathon/shopping_agents` 目录下 
2. 在当前目录下创建一个文件 名字叫做`.env.secret`,结构如下
~~~
API_KEY=
~~~
3. 在当前目录下运行命令 `dora up && dora build shopping_dataflow.yml && dora start shopping_dataflow.yml --attach`
4. 在另外一个命令端下面运行 `hitl-agent`
5. 开启另外一个命令端,在命令行中使用`cd /mofa_berkeley_hackathon/python/berkeley-hackathon/ui && streamlit run socket_client.py` 可以看到你的页面打开了。 保证你的端口12345没有被占用，如果被占用了，使用`lsof -i :12345`来查看被占用的进程号，使用  kill -9 删除它

