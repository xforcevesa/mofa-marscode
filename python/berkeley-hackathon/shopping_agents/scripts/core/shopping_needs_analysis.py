from typing import List, Optional, Dict

from mofa.utils.ai.conn import create_openai_client, generate_json_from_llm
from pydantic import BaseModel,Field, HttpUrl
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




class ShippingOption(BaseModel):
    Method: str = Field(description="Shipping method (e.g., Standard, Express)")
    Cost: float = Field(description="Shipping cost in ¥")
    Estimated_Delivery_Time: str = Field(description="Estimated delivery time (e.g., 3-5 business days)")
    Carrier: str = Field(description="Shipping carrier (e.g., DHL, FedEx)")


class SellerInfo(BaseModel):
    Seller_Name: str = Field(description="Name of the seller or store")
    Seller_Rating: float = Field(description="Seller rating out of 5")
    Seller_Location: str = Field(description="Location of the seller")
    Seller_Store_Link: Optional[HttpUrl] = Field( description="URL to the seller's store or profile")


class WarrantyInfo(BaseModel):
    Duration: str = Field(description="Warranty duration (e.g., 2 years)")
    Coverage: str = Field(description="Warranty coverage details (e.g., parts and labor)")
    Provider: str = Field(description="Warranty provider (e.g., manufacturer, third-party)")


class ReturnPolicy(BaseModel):
    Policy_Details: str = Field(description="Details of the return policy")
    Return_Window: str = Field(description="Timeframe for returns (e.g., 30 days)")
    Conditions: str = Field(description="Conditions for returns (e.g., unopened, original packaging)")


class UserReview(BaseModel):
    Reviewer_Name: str = Field(description="Name or alias of the reviewer")
    Rating: float = Field(description="Rating out of 5")
    Comment: str = Field(description="Review comment")
    Review_Date: str = Field(description="Date of the review")


class SingleProductDetail(BaseModel):
    Product_Type: str = Field(description="Type of Product (e.g., CPU, GPU, Motherboard)")
    Brand: str = Field(description="Brand of the product (e.g., Intel, AMD)")
    Model: str = Field(description="Model of the product (e.g., i7-12700K, Ryzen 7 5800X)")
    Product_Name: str = Field(description="Full name of the product")
    Specifications: str = Field(description="Detailed specifications of the product")
    Price: float = Field(description="Price of the product in ¥")
    Currency: str = Field( description="Currency of the price")
    Availability: str = Field(description="Availability status (e.g., 'In Stock', 'Out of Stock')")
    Product_Link: HttpUrl = Field(description="Direct URL to purchase the product")
    Seller: SellerInfo = Field(description="Information about the seller")
    Shipping_Options: List[ShippingOption] = Field(description="Available shipping options for the product")
    Warranty: WarrantyInfo = Field(description="Warranty details for the product")
    Return_Policy: ReturnPolicy = Field(description="Return policy for the product")
    Reviews: List[UserReview] = Field(description="List of user reviews and ratings")
    Images: List[HttpUrl] = Field(description="URLs to product images")
    Discounts: Optional[str] = Field( description="Any applicable discounts or promotions")
    Energy_Efficiency_Rating: Optional[str] = Field( description="Energy efficiency rating (e.g., 80 Plus Gold)")
    Aesthetic_Details: Optional[str] = Field( description="Design and aesthetic details (e.g., RGB lighting)")
    Justification: Optional[str] = Field( description="Reason for selecting this product based on user requirements")


class ValidationIssue(BaseModel):
    Issue_Type: str = Field(description="Type of Issue (e.g., Budget Exceeded, Compatibility Problem)")
    Description: str = Field(description="Detailed description of the issue.")
    Recommendation: str = Field(description="Suggested action to resolve the issue.")


class ShoppingPlanEvaluation(BaseModel):
    Validation_Status: str = Field(description="Overall validation status (e.g., 'Valid', 'Issues Detected')")
    Issues: Optional[List[ValidationIssue]] = Field( description="List of detected issues, if any.")
    Recommendations: Optional[List[str]] = Field( description="List of recommendations to optimize the plan.")


class ShoppingPlanSolution(BaseModel):
    Plan_ID: str = Field(description="Unique identifier for the shopping plan (e.g., 'Plan 1')")
    Products: List[SingleProductDetail] = Field(description="List of all selected products in the plan.")
    Total_Cost: float = Field(description="Total cost of all products in the plan.")
    Shopping_Plan_Evaluation: ShoppingPlanEvaluation = Field(description="Validation results and recommendations for the plan.")


class ShoppingPlanSolutions(BaseModel):
    Plans: List[ShoppingPlanSolution] = Field(description="List of all generated shopping plans.")


def extract_web_search_text_by_product_type(shopping_plan: ShoppingPlan) -> Dict[str, List[str]]:
    result = {}

    # 遍历每个ShoppingTypeNeed和其ProductInfos
    for shopping_type in shopping_plan.Shopping_Needs:
        for product in shopping_type.Product_Infos:
            # 如果Product_Type已经是字典中的键，添加Web_Shopping_Search_Text到该键的列表
            if shopping_type.Product_Type not in result:
                result[shopping_type.Product_Type] = []
            result[shopping_type.Product_Type].append(product.Web_Shopping_Search_Text)

    return result

def analyze_shopping_needs(shopping_requirements:str=None,format_class=ShoppingPlan,messages:List[dict]=None,user_suggestions:str=None,model_name:str='gpt-4o',):
    if messages is None:

        messages = [
        {"role": "system",
         "content": think_base_prompt},
        {"role": "user",
         "content": load_shopping_needs_decomposition(shopping_requirements=shopping_requirements,user_suggestions=user_suggestions)},]
    llm_client = create_openai_client()
    result = generate_json_from_llm(client=llm_client, format_class=format_class, messages=messages,model_name=model_name)
    return result

