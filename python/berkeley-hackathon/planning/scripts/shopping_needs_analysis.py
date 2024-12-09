from typing import List

from mofa.utils.ai.conn import create_openai_client, generate_json_from_llm
from pydantic import BaseModel,Field
from prompt import think_base_prompt,load_shopping_needs_decomposition

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


def analyze_shopping_needs(shopping_requirements:str,messages:List[dict]=None,user_suggestions:str=None,model_name:str='gpt-4o'):
    if messages is None:

        messages = [
        {"role": "system",
         "content": think_base_prompt},
        {"role": "user",
         "content": load_shopping_needs_decomposition(shopping_requirements=shopping_requirements,user_suggestions=user_suggestions)},]
    llm_client = create_openai_client()
    result = generate_json_from_llm(client=llm_client, format_class=ShoppingPlan, messages=messages,model_name=model_name)
    return result

