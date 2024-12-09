from typing import List

from mofa.utils.ai.conn import create_openai_client, generate_json_from_llm
from pydantic import BaseModel,Field
from .prompt import think_base_prompt,load_shopping_needs_decomposition

class SingleShoppingTypeNeed(BaseModel):
    Price_Range:str = Field(description="Price Range")
    # Brand:str = Field(description="Under a product, there should be only one brand included.")
    Specifications:str = Field(description='Product Specifications')
    Web_Shopping_Search_Text:str = Field(description="Shopping Website Search Content")
    Product_Model:str = Field(description="Product Model")

class SingleShoppingTypeNeeds(BaseModel):
    Product_Type:str = Field(description="Types of Products")
    Product_Infos:List[SingleShoppingTypeNeed] = Field(description="Under a product, there should be one or more brands included.")

class ShoppingPlan(BaseModel):
    Shopping_Needs:List[SingleShoppingTypeNeeds]


def analyze_shopping_needs(shopping_requirements:str,model_name:str='gpt-4o'):
    # shopping_task = "我想要一个编程的电脑,我希望这个电脑功耗比较低.然后我的预算不是特别多,并且我在上面不会跑llm相关的内容. 然后我的手机是iphone的。是否苹果相关的产品会适合我?"
    messages = [
        {"role": "system",
         "content": think_base_prompt},
        {"role": "user",
         "content": load_shopping_needs_decomposition(shopping_requirements=shopping_requirements)},]
    llm_client = create_openai_client()
    result = generate_json_from_llm(client=llm_client, format_class=ShoppingPlan, messages=messages,model_name=model_name)
    return result