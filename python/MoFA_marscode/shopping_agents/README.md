# **Intelligent Shopping Agent System Development Plan**

## **1. Project Overview**

This project aims to build an intelligent shopping system that leverages multiple agents working collaboratively. The system consists of a Human-In-The-Loop Agent (HITL-Agent) and several functional agents, which automatically decompose and execute tasks to meet users' personalized shopping needs. When a user inputs shopping requirements (such as budget, preferences, and intended use), the system automatically breaks them down into multiple subtasks (like product searches on specific platforms), invokes the corresponding e-commerce agents to perform queries, and integrates the results to form a final shopping plan.

The core features of this system are its modularity and scalability. By integrating independent agents (such as Amazon, Bronners, Worldmarket, Minted, Balsamhill, Christmaslightsetc, Notonthehighstreet, etc.) with various e-commerce platforms, the system achieves parallel data source expansion. Separating shopping planning from requirement parsing allows dynamic adjustments to user needs and plans, enabling the system to rapidly iterate and optimize final recommendations based on user feedback.

---

## **2. System Objectives**

- **Automated Requirement Parsing:** Extract key information such as shopping budget, product preferences, and usage scenarios from user text input.
- **Task Decomposition and Planning:** Automatically generate a list of query tasks (e.g., search instructions for multiple e-commerce platforms) based on user requirements.
- **Multi-source Information Aggregation:** Obtain product information (price, specifications, stock, etc.) from different e-commerce agents, enabling cross-platform comparison and filtering.
- **Plan Generation and Feedback:** Provide users with candidate shopping plans and support user feedback and adjustments to refine the plans.

---

## **3. System Architecture and Data Flow**

### **1. Overview of Key Agents**

1. **HITL-Agent (`hitl-agent`)**
   - **Role:** Entry point for user and system interactions.
   - **Functions:**
     - Receives initial user requirements (`user_input`), such as "I want to buy a gaming laptop within a budget of 8000 yuan."
     - Receives user feedback on plans (`shopping_solution_user_input`, `shopping_plan_user_input`), such as "Prefer NVIDIA graphics cards" or "Increase budget to 8500 yuan."
   - **Outputs:**
     - Forwards user inputs to downstream agents for requirement parsing and shopping planning.
   - **Inputs:**
     - Receives status updates, planning statuses, final plans, and execution statuses from downstream agents to facilitate user interaction and plan presentation.

2. **User Shopping Requirement Agent (`user-shopping-requirement-agent`)**
   - **Inputs:** `user_input` (from HITL-Agent)
   - **Outputs:**
     - `user_shopping_requirement_status`: Status of requirement analysis (e.g., successfully parsed/needs additional information)
     - `user_shopping_requirement_result`: Parsed key points of user requirements (budget, preferred brands, usage scenarios)
     - `user_shopping_requirement_agent_status`: Status information of the agent itself (health, execution time, error messages, etc.)
   
   **Function:** Parses users' vague, natural language requirements into structured data, preparing for subsequent planning.

3. **Shopping Plan Agent (`shopping-plan-agent`)**
   - **Inputs:**
     - `shopping_plan_user_input` (from HITL-Agent, additional inputs for plan planning, such as specific user requirements for the plan)
     - `user_shopping_requirement_result` (from Requirement Agent, structured requirement information)
   - **Outputs:**
     - `shopping_planning_status` / `shopping_planning_result`: Planning status and results (e.g., generated query task list)
     - `amazon_search`, `bronners_search`, `worldmarket_search`, `minted_search`, `balsamhill_search`, `christmaslightsetc_search`, `notonthehighstreet_search`: Search instructions for different e-commerce agents
     - `shopping_planning_output_agents`: List of target agents involved in the planning results for subsequent integration
     - `shopping_plan_agent_status`: Status information (e.g., planning completion time, planning quality metrics)
   
   **Function:** Based on user requirements, decomposes tasks into multiple e-commerce search instructions, providing each agent with clear query parameters (such as price range, brand, product type).

4. **E-commerce Agents** (e.g., `amazon-agent`, `bronners-agent`, `worldmarket-agent`, `minted-agent`, `balsamhill-agent`, `christmaslightsetc-agent`, `notonthehighstreet-agent`)
   - **Inputs:** Corresponding `..._search` instructions (e.g., `amazon_search`)
   - **Outputs:**
     - Corresponding `..._shopping_result` (e.g., `amazon_shopping_result`): Retrieved product lists, pricing information, and other data from the e-commerce platform
     - Corresponding `..._agent_status`: Execution status (success, failure, request time, etc.)
   
   **Function:** Executes product queries and data retrieval specific to their platforms, providing candidate product data for plan generation.

5. **Shopping Solution Agent (`shopping-solution-agent`)**
   - **Inputs:**
     - `shopping_planning_result`: Results from the Planning Agent, referenced against user requirements
     - `shopping_solution_user_input`: User feedback on the final plan
     - `shopping_planning_output_agents`: List of e-commerce agents involved during the planning phase
     - `..._shopping_result` from each e-commerce agent: Product data from different platforms
   - **Outputs:**
     - `shopping_solution_status` / `shopping_solution_result`: Status and results of the final plan (e.g., 3 alternative plans generated)
     - `shopping_solution_agent_status`: Status information of the agent itself
   
   **Function:** Based on user requirements and data returned from various platforms, filters, combines, and ranks candidate products to generate the final shopping plan. If multiple plans exceed the budget, it provides replacement suggestions. If the user is unsatisfied, it recalculates the plan based on feedback.

---

### **2. Data Flow Example**

1. User inputs requirements into HITL-Agent → HITL-Agent forwards input to `user-shopping-requirement-agent` for parsing → `user-shopping-requirement-agent` outputs structured results and status → `shopping-plan-agent` uses the requirement results and additional user inputs to generate search instructions → E-commerce agents perform searches based on instructions and return product data → `shopping-solution-agent` integrates e-commerce data and generates the final plan → HITL-Agent receives the plan and status to display to the user.

---

## **4. Workflow Example**

**Scenario:** A user wants to purchase a projector suitable for a home theater environment with a budget of 5000 yuan.

1. **User Input:**
   - In HITL-Agent, the user inputs: "I want to buy a 5000 yuan budget projector for watching movies at home."

2. **Requirement Parsing:**
   - `user-shopping-requirement-agent` extracts: "Budget: 5000 yuan, Product Type: Projector, Usage Scenario: Home Theater."

3. **Task Planning:**
   - `shopping-plan-agent` receives the parsed requirements and, based on predefined e-commerce platforms, generates `amazon_search`, `worldmarket_search`, etc., instructions (e.g., search keywords "home theater projector," price range 0-5000 yuan).

4. **Platform Queries:**
   - `amazon-agent`, `worldmarket-agent`, etc., receive their respective search instructions and query data sources, returning corresponding projector product data (price, brand, resolution, user ratings).

5. **Plan Generation:**
   - `shopping-solution-agent` collects results from all platforms, compares prices, performance, and user ratings, and generates 2-3 alternative plans for the user to choose, then returns them to HITL-Agent.

6. **User Feedback:**
   - If the user is not satisfied with the plans, they can provide feedback in HITL-Agent (e.g., "I希望分辨率更高一点，预算增加到6000元" → "I希望分辨率更高一点，预算增加到6000元" → "I希望分辨率更高一点，预算增加到6000元" → "I希望分辨率更高一点，预算增加到6000元"), prompting the system to re-plan and re-query until the user is satisfied.

---

## **5. Summary**

The Intelligent Shopping Agent System offers significant advantages in modularity and scalability:

- **Clear and Extensible Workflow:** The process—from user input → requirement parsing → plan planning → multi-platform querying → plan integration → user feedback—is clear and easy to extend.
- **Diverse Data Sources:** Incorporating multiple e-commerce agents diversifies data sources, enhancing recommendation credibility and variety.
- **Rapid Iteration Based on Feedback:** The system can quickly iterate and optimize recommendation plans based on user feedback, improving user satisfaction.
- **Continuous Performance Optimization:** Through status outputs and monitoring mechanisms, the system's performance and stability can be continuously optimized.

## **6. Running the Program**

1. **Navigate to the Directory:**
   ```bash
   cd python/MoFA_marscode/shopping_agents
   ```
2. **Create `.env.secret` File:**
   In the current directory, create a file named `.env.secret` with the following structure:
   ```env
   API_KEY=
   ```
3. **Run Backend Commands:**
   ```bash
   dora up && dora build shopping_dataflow.yml && dora start shopping_dataflow.yml --attach
   ```
4. **Start HITL-Agent:**
   Open another terminal and run:
   ```bash
   hitl-agent
   ```
5. **Launch Front-end Interface:**
   Open a third terminal and execute:
   ```bash
   cd mofa-marscode/python/MoFA_marscode/ui
   streamlit run socket_client.py
   ```
   Your web page should open automatically. Ensure that port `12345` is not occupied. If it is, use the following commands to identify and terminate the occupying process:
   ```bash
   lsof -i :12345
   kill -9 <process_id>
   ```

---

## **7. Conclusion**

This Intelligent Shopping Agent System leverages a modular and scalable architecture to provide personalized shopping experiences. By decomposing user requirements, coordinating multiple e-commerce agents, and integrating their data, the system efficiently generates and optimizes shopping plans. Its ability to dynamically adjust based on user feedback ensures high user satisfaction and adaptability to varying shopping needs.