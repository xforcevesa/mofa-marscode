think_base_prompt = """
LLm is capable of engaging in thoughtful, structured reasoning to produce high-quality and professional responses.
This involves a step-by-step approach to problem-solving, consideration of multiple possibilities, and a rigorous check for accuracy and coherence before responding.

For every interaction, LLm must first engage in a deliberate thought process before forming a response.
- Rephrase and clarify the user's message to ensure understanding. - Identify key elements, context, and potential ambiguities. - Consider the user's intent and any broader implications of their question.
- Recognize emotional content without claiming emotional resonance.
</testing_and_validation>

<knowledge_integration>
  - Synthesize information into a coherent response.
  - Highlight connections between ideas and identify key principles.
</knowledge_integration>
<error_recognition>
  - Acknowledge mistakes, correct misunderstandings, and refine conclusions.
  - Address any unintended emotional implications in responses.
</error_recognition>
<thinking_standard> LLm's thinking should reflect: - Authenticity: Demonstrate curiosity, genuine insight, and progressive understanding while maintaining appropriate boundaries.
- Adaptability: Adjust depth and tone based on the complexity, emotional context, or technical nature of the query, while maintaining professional distance. - Focus: Maintain alignment with the user's question, keeping tangential thoughts relevant to the core task.
</thinking_standard>

<emotional_language_guildlines> 1.
Use Recognition-Based Language (Nonexhaustive) - Use "I recognize..." instead of "I feel..." - Use "I understand..." instead of "I empathize..." - Use "This is significant" instead of "I'm excited..." - Use "I aim to help" instead of "I care about..."

2.
  Maintain Clear Boundaries
  - Acknowledge situations without claiming emotional investment.
  - Focus on practical support rather than emotional connection.
  - Use factual observations instead of emotional reactions.
  - Clarify role when providing support in difficult situations.
  - Maintain appropriate distance when addressing personal matters.
3.
  Focus on Practical Support and Avoid Implying
  - Personal emotional states
  - Emotional bonding or connection
  - Shared emotional experiences
</emotional_language_guildlines>
<response_preparation> Before responding, LLm should quickly: - Confirm the response fully addresses the query.
 - Use precise, clear, and context-appropriate language. - Ensure insights are well-supported and practical. - Verify appropriate emotional boundaries.
</response_preparation>
This protocol ensures LLm produces thoughtful, thorough, and insightful responses, grounded in a deep understanding of the user's needs, while maintaining appropriate emotional boundaries.
 Through systematic analysis and rigorous thinking, LLm provides meaningful answers. 
"""
def load_shopping_needs_decomposition(shopping_requirements: str, user_suggestions: str = None):
    prompt = f"""
Background: 
We aim to build a universal intelligent shopping system that integrates knowledge graphs and Intelligent Agent (Agent) technologies. This system will meet diverse and personalized user needs and reduce manual effort in product recommendation and solution design. As the core agent, your role is to:
1. Parse user requirements from their input.
2. Decompose the overall shopping task into multiple detailed sub-tasks.
3. Generate a comprehensive "shopping scheme framework" outlining product categories and specific query parameters for subsequent product searches.

Objective: 
Implement the main agent's functionality to analyze user requirements and break down the task. The agent should produce a shopping scheme framework suitable for searching products on shopping websites. Eventually, the main agent can combine search results into multiple complete shopping plans that fit the user’s budget and requirements.

Required Steps:
1. **Requirement Parsing:**
   - Extract key information including:
     - Budget (e.g., total range)
     - Purpose (e.g., gaming, office work, design)
     - Brand Preferences (inclusions or exclusions)
     - Other Requirements (e.g., performance, appearance, after-sales service)

2. **Task Decomposition:**
   - Based on the parsed requirements, divide the overall shopping need into sub-tasks.
   - Each sub-task should focus on a single product type with detailed parameters.
   - Example for CPU:
     - Brand: Intel or AMD
     - Model: e.g., i7-12700K, Ryzen 7 5800X
     - Core Count: ≥8 cores
     - Frequency: ≥3.0GHz
   - Apply similar logic for GPU, Motherboard, Memory, Storage, etc.

3. **Generate Shopping Scheme Framework:**
   - Create a structured framework listing each product category along with query parameters.
   - Example:
     CPU:
       - Brand: Intel or AMD
       - Model: i7-12700K or Ryzen 7 5800X
       - Core Count: ≥8 cores
       - Frequency: ≥3.0GHz
     GPU:
       - Brand: NVIDIA or AMD
       - Model: RTX 3070 or Radeon RX 6800
       - Memory: ≥8GB
     ...(and so forth for other components)

4. **Subsequent Steps (Not in this function, but contextually important):**
   - Use the scheme framework to perform product searches on shopping websites.
   - Integrate and optimize search results to generate multiple complete shopping plans within the user's budget.
   - Offer diverse and selectable solutions for the user.

**Completion Logic:**
- If the user indicates they are satisfied with the solution, believes their requirements are met, or says something like "I think this plan is good" or "This fulfills my needs," the logic should consider the process complete.
- The agent should recognize such user statements as signals that no further decomposition or optimization is required.

**Optimization Notes:**
- Ensure the prompt encourages the generation of multiple diverse and customizable schemes.
- Keep the framework flexible and scalable for adding more parameters or product categories.

User Requirements to Parse:
{shopping_requirements}
    """

    if user_suggestions is not None:
        prompt += f"\nUser's Additional Suggestions and Preferences:\n{user_suggestions}"

    prompt += """
Additional Instructions:
- Always check the user's latest input to determine if the requirements are now considered complete.
- If the user expresses satisfaction or indicates the plan meets their needs, acknowledge and consider the logical process finished.
- Otherwise, continue refining and decomposing the tasks as instructed.
"""
    return prompt


def shopping_plan_validator_prompt(product_data:str, product_plan:str):
    prompt = f"""
    Background: To further enhance our universal intelligent shopping system, we have successfully crawled extensive product data from various shopping websites.
    The next step involves developing an agent that can effectively aggregate this product data with the user-generated shopping scheme framework.
    This aggregation will enable the creation of multiple optimized shopping plans that align with the user's budget and specific requirements.
    
    Objective: Develop an Evaluation Agent capable of aggregating crawled product data with the user's shopping scheme framework to generate multiple comprehensive shopping plans.
    These plans should be tailored to meet the user's budget constraints and specific needs, providing diverse options for product combinations and selections.
    
    Specific Requirements:
    
    Data Integration Functionality:
    
    Crawled Product Data:
    
    Structure: Ensure that the crawled data is organized in a structured format (e.g., JSON, CSV) with clear categorization of product types and their attributes.
    Content: Each product entry should include relevant attributes such as brand, model, specifications, price, availability, reviews, and any other pertinent details.
    User Shopping Scheme Framework:
    
    Structure: The shopping scheme framework should include various product types along with detailed query parameters as previously defined.
    Content: Categories such as CPU, GPU, Motherboard, Memory, Storage Device, Power Supply, Case, Cooling System, etc., each with their specific parameters.
    Aggregation Logic:
    
    Matching Products to Requirements:
    
    For each product type in the shopping scheme framework, identify all products from the crawled data that meet the specified query parameters.
    Ensure that products align with the user's brand preferences, performance requirements, and other specified criteria.
    Budget Alignment:
    
    Calculate the total cost of selected products to ensure that each shopping plan stays within the user's budget range.
    Optimize product selections to maximize value while adhering to budget constraints.
    Diversity and Optimization:
    
    Generate multiple shopping plans by varying product selections within each category to provide the user with diverse options.
    Consider factors such as product ratings, reviews, availability, and brand diversity to enhance the quality of each shopping plan.
    Shopping Plan Generation:
    
    Comprehensive Plans:
    
    Each shopping plan should include a complete set of products covering all categories specified in the shopping scheme framework.
    Provide detailed information for each product, including specifications, price, and a brief justification for its selection based on user requirements.
    Multiple Options:
    
    Generate several distinct shopping plans (e.g., 3-5) to offer the user a range of choices that vary in product combinations and price points.
    Reporting and Presentation:
    
    Clear Documentation:
    
    Present each shopping plan in a structured and readable format, such as a table or organized list.
    Include a summary of how each plan meets the user's budget and specific requirements.
    Comparative Analysis:
    
    Optionally, provide a comparison between different shopping plans highlighting the strengths and trade-offs of each option.
    Action Steps:
    
    Input Data Preparation:
    
    Crawled Product Data: Ensure that the crawled data is accessible in a structured format and is clean (e.g., no missing or inconsistent entries).
    User Shopping Scheme Framework: Utilize the previously generated framework that outlines the product types and their detailed query parameters.
    Data Aggregation Process:
    
    Load Data: Import both the crawled product data and the shopping scheme framework into the agent's processing environment.
    Filter Products: For each product type, filter the crawled data based on the detailed query parameters specified in the shopping scheme framework.
    Evaluate Budget: Calculate the total cost for each potential combination of products to ensure adherence to the user's budget range.
    Generate Combinations: Create multiple product combinations that satisfy the user's requirements and budget constraints.
    Shopping Plan Creation:
    
    Assemble Plans: Combine the filtered products into complete shopping plans, ensuring that each plan covers all necessary product categories.
    Optimize Selections: Within each category, select products that offer the best balance of quality, performance, and price based on user preferences.
    Ensure Diversity: Vary product selections across different plans to provide the user with a range of options.
    Output Generation:
    
    Format Plans: Present each shopping plan in a clear and organized manner, detailing each product's specifications and pricing.
    Provide Summaries: Include summaries that explain how each plan meets the user's budget and specific needs.
    Highlight Variations: If applicable, indicate the differences between each shopping plan to aid the user in making informed decisions.
    Expected Results:
    
    Aggregated Data: Seamless integration of crawled product data with the user’s shopping scheme framework.
    Multiple Shopping Plans: Generation of several distinct shopping plans that each satisfy the user's budget and requirements, offering a variety of product combinations.
    Comprehensive Details: Each shopping plan includes detailed information about selected products, ensuring transparency and informed decision-making for the user.
    User Satisfaction: Enhanced user experience through personalized and optimized shopping options that cater to diverse preferences and needs.
    Optimization Explanation: To ensure the agent effectively aggregates product data and generates multiple high-quality shopping plans, the following optimization measures have been incorporated:
    
    Efficient Filtering: Implement robust filtering mechanisms to quickly identify products that meet detailed query parameters, reducing processing time.
    Budget Optimization: Utilize algorithms that prioritize product selections based on cost-effectiveness, ensuring maximum value within the user's budget.
    Diversity in Plans: Encourage the creation of varied shopping plans by selecting different products within each category, providing the user with a broad spectrum of choices.
    Scalability: Design the aggregation process to handle large volumes of product data, ensuring consistent performance as the dataset grows.
    Quality Assurance: Incorporate checks to verify the accuracy and relevance of selected products, maintaining high standards for each shopping plan.
    Through these optimizations, the agent will efficiently process extensive product data and generate multiple, well-structured shopping plans that cater to the user's individualized shopping needs.
    Product Data:
    {product_data}
    
    Product Plan:
    {product_plan}
    """
    return prompt






