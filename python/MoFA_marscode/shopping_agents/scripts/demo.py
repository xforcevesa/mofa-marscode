# from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output, load_node_result
# from core.prompt import think_base_prompt,shopping_plan_validator_prompt
# from core.shopping_needs_analysis import analyze_shopping_needs,ShoppingPlanSolutions
# product_data = """
# ['{"chunks":[{"url":"/s?k=laptop+8000-15000","product_id":"B0CXKXNNPX","sku":"B0CXKXNNPX","model":"Microsoft Surface Pro","title":"Microsoft Surface Pro 2-in-1 Laptop/Tablet (2024), Windows 11 Copilot+ PC, 13\\" Touchscreen OLED Display, Snapdragon X Elite (12 Core), 16GB RAM, 256GB Storage, Black, Amazon Exclusive","description":"The most intelligent and versatile 2-in-1 laptop.","short_description":"","brand":"Microsoft","category":"Computers","category_hierarchy":["Electronics","Computers"],"price":899.0,"currency":"USD","original_price":1200.0,"discount_info":"Save 25%","availability":"In Stock","rating":3.9,"reviews_count":155,"reviews_breakdown":{"positive":80,"neutral":35,"negative":40},"seller_info":"","attributes":{"Display Size":"13 inches","Battery":"6000mAh"},"specifications":{"Processor":"Snapdragon X Elite (12 Core)","OS":"Windows 11"},"media":{"images":["https://m.media-amazon.com/images/I/61zRDADh+YS._AC_UY218_.jpg"],"videos":[]},"shipping_info":"Free delivery for Amazon Prime members","warranty_info":"1 Year Manufacturer Warranty","tags":["laptop","tablet","touchscreen"]},{"url":"/Dell-Inspiron-15-6-inch-i5-1135G7-Laptop/dp/B095RZ62BX","product_id":"B095RZ62BX","sku":"B095RZ62BX","model":"Dell Inspiron 15","title":"Dell Inspiron 15 3000 15.6-inch Full HD 11th Gen Intel Core i5-1135G7 12GB RAM 256GB SSD Laptop","description":"Check each product page for other buying options.","short_description":"","brand":"Dell","category":"Computers","category_hierarchy":["Electronics","Computers"],"price":407.0,"currency":"USD","original_price":500.0,"discount_info":"Save 5%","availability":"In Stock","rating":4.2,"reviews_count":528,"reviews_breakdown":{"positive":220,"neutral":200,"negative":100},"seller_info":"","attributes":{"Display Size":"15.6 inches","Disk Size":"256 GB","RAM":"12 GB","Operating System":"Windows 10"},"specifications":{"Processor":"Intel Core i5-1135G7","Graphics":"Intel Iris Xe"},"media":{"images":["https://m.media-amazon.com/images/I/61zRDADh+YS._AC_UY218_.jpg"],"videos":[]},"shipping_info":"Free shipping on orders over $25","warranty_info":"Limited 1 Year Warranty","tags":["laptop","Dell","Inspiron"]},{"url":"/LLSS-Inverter-Voltage-Converter-Connection/dp/B095RZ62BX","product_id":"B095RZ62BX","sku":"B095RZ62BX","model":"LLSS Inverter","title":"LLSS Pure Sine Wave Inverter 3200W,4000W,6000W,8000W,9000W,12000W,15000W Voltage Converter DC 12V 24V to AC 220V with Socket,USB Connection,LED Display,for Laptop,Travel","description":"Power inverter for laptops and other devices with high wattage needs.","short_description":"","brand":"LLSS","category":"Appliances","category_hierarchy":["Electronics","Home Appliances"],"price":593.8,"currency":"USD","original_price":650.0,"discount_info":"Save 10%","availability":"In Stock","rating":4.3,"reviews_count":411,"reviews_breakdown":{"positive":250,"neutral":100,"negative":61},"seller_info":"","attributes":{"Power Level":"3200W to 15000W","Socket Type":"Universal"},"specifications":{"Input Voltage":"12V/24V","Output Voltage":"220V"},"media":{"images":["https://m.media-amazon.com/images/I/613EMth3jjL._AC_UY218_.jpg"],"videos":[]},"shipping_info":"Free next day delivery available","warranty_info":"2 Year Warranty","tags":["inverter","power","electrical"]},{"url":"/Peak-Power-Detachable-Battery-Portable/dp/B0DPH6SBMT","product_id":"B0DPH6SBMT","sku":"B0DPH6SBMT","model":"Car Power Inverter","title":"Peak Power 7000W 8000W 9000W 10000W Car Power Pure Sine Wave Inverter 48V 60V 72V to 110V/220V","description":"Pure Sine Wave inverter designed for car and home.","short_description":"","brand":"None","category":"Tools","category_hierarchy":["Tools & Home Improvement"],"price":953.99,"currency":"USD","original_price":1.0,"discount_info":"Save more with coupon","availability":"Available Soon","rating":4.0,"reviews_count":219,"reviews_breakdown":{"positive":120,"neutral":57,"negative":42},"seller_info":"","attributes":{"Power Output":"10000W","Socket Type":"Universal"},"specifications":{"Input Voltage":"12V/24V","Output Voltage":"110V/220V"},"media":{"images":["https://m.media-amazon.com/images/I/71Qno9YXcyL._AC_UY218_.jpg"],"videos":[]},"shipping_info":"Delayed shipping expected","warranty_info":"3 Year Warranty","tags":["power inverter","peak power","inverter"]},{"url":"/HQCUZZY-Inverter-3200W-10000W/dp/B0DPHZMXFV","product_id":"B0DPHZMXFV","sku":"B0DPHZMXFV","model":"HQCUZZY Inverter","title":"Smart Power Inverter (3200W-15000W), DC(12V/24V) to Ac(220-240V)","description":"Power inverter with additional smart features for modern devices.","short_description":"","brand":"HQCUZZY","category":"Appliances","category_hierarchy":["Electronics","Home Appliances"],"price":304.99,"currency":"USD","original_price":319.99,"discount_info":"Save 4% at checkout","availability":"In Stock","rating":4.5,"reviews_count":162,"reviews_breakdown":{"positive":100,"neutral":30,"negative":32},"seller_info":"","attributes":{"Colors":"","Capacity":"3200W-15000W"},"specifications":{"Input Voltage":"12V/24V","Output Voltage":"220V AC"},"media":{"images":["https://m.media-amazon.com/images/I/71zR728x2wL._AC_UY218_.jpg"],"videos":[]},"shipping_info":"Arrives before Christmas","warranty_info":"","tags":["smart inverter","power inverter"]}]} ||| {"chunks":[{"url":"/Apple-2024-MacBook-15-inch-Laptop/dp/B0DLHN9WYG","product_id":"B0DLHN9WYG","sku":"","model":"","title":"Apple 2024 MacBook 15-inch Laptop","description":"","short_description":"3 capacities","brand":"Apple","category":"Laptops","category_hierarchy":["Computers & Tablets","Traditional Laptop Computers"],"price":1599.0,"currency":"USD","original_price":1699.0,"discount_info":"$99.01 off coupon applied","availability":"In Stock","rating":4.8,"reviews_count":367,"reviews_breakdown":{"positive":280,"neutral":50,"negative":37},"seller_info":"","attributes":{"Color":"Silver","Storage":"512GB"},"specifications":{"Display Size":"15.6 inches","RAM":"8GB"},"media":{"images":["https://m.media-amazon.com/images/I/81QIReOgqoL._AC_UY218_.jpg"],"videos":[]},"shipping_info":"Free delivery Thu, Dec 19","warranty_info":"","tags":["Laptop","Apple"]},{"url":"/Generac-7715-000-Watt-Gas-Powered-Generator/dp/B0CDMBYFR5","product_id":"B0CDMBYFR5","sku":"","model":"","title":"Generac 7715 GP8000E 8,000-Watt Gas-Powered Generator","description":"","short_description":"4.2 out of 5 stars","brand":"Generac","category":"Generators","category_hierarchy":["Tools & Home Improvement","Generators"],"price":1099.0,"currency":"USD","original_price":1219.0,"discount_info":"","availability":"Available","rating":4.2,"reviews_count":106,"reviews_breakdown":{"positive":70,"neutral":20,"negative":16},"seller_info":"","attributes":{"Color":"Orange","Size":"8000W"},"specifications":{"Display Size":"-","RAM":"-"},"media":{"images":["https://m.media-amazon.com/images/I/610Vs2dBajL._AC_UY218_.jpg"],"videos":[]},"shipping_info":"Free delivery Thu, Dec 19 on $35 of items shipped by Amazon","warranty_info":"","tags":["Generator","Power Supply"]},{"url":"/Intel-Celeron-N4020-14-Inch-Laptop/dp/B09YRY6QCX","product_id":"B09YRY6QCX","sku":"","model":"","title":"ASUS E410 Intel Celeron N4020 4GB 64GB 14-Inch HD LED Win 10 Laptop","description":"","short_description":"4.1 out of 5 stars","brand":"ASUS","category":"Laptops","category_hierarchy":["Computers & Tablets","Traditional Laptop Computers"],"price":135.0,"currency":"USD","original_price":146.97,"discount_info":"","availability":"In Stock","rating":4.1,"reviews_count":698,"reviews_breakdown":{"positive":456,"neutral":100,"negative":142},"seller_info":"","attributes":{"Color":"Black","Storage":"64GB"},"specifications":{"Display Size":"14 inches","RAM":"4 GB"},"media":{"images":["https://m.media-amazon.com/images/I/614Jk1dIoGL._AC_UY218_.jpg"],"videos":[]},"shipping_info":"Free delivery Fri, Dec 27","warranty_info":"","tags":["Laptop","ASUS"]}]}']
# """
# shopping_planning_result = "{'Laptop': ['Gaming laptop with NVIDIA graphics card, minimum 32GB RAM, price 8000-15000 RMB', '15-inch display gaming laptop with NVIDIA graphics card, minimum 32GB RAM, price 8000-15000 RMB']}"
# messages = [
#     {"role": "system",
#      "content": think_base_prompt},
#     {"role": "user",
#      "content": shopping_plan_validator_prompt(product_data=shopping_planning_result,
#                                                product_plan=product_data)}, ]
# result = analyze_shopping_needs(messages=messages, format_class=ShoppingPlanSolutions)
# print(result)
import random
shopping_data = {
    'Laptop': ['游戏笔记本 NVIDIA显卡 8000-15000元'],
    'Phone': ['苹果手机 5000-7000元', '安卓手机 2000-4000元'],

}

shopping_agents = {
    'amazon_agent': {'inputs': 'amazon_search', 'outputs': 'amazon_shopping_result'},
    'bronners_agent': {'inputs': 'bronners_search', 'outputs': 'bronners_shopping_result'},
    'worldmarket_agent': {'inputs': 'worldmarket_search', 'outputs': 'worldmarket_shopping_result'},
    'minted_agent': {'inputs': 'minted_search', 'outputs': 'minted_shopping_result'},
    'balsamhill_agent': {'inputs': 'balsamhill_search', 'outputs': 'balsamhill_shopping_result'}
}

# 1. 将所有查询扁平化为 (category, query) 的列表
all_queries = []
for category, queries_list in shopping_data.items():
    for q in queries_list:
        all_queries.append((category, q))

agents = list(shopping_agents.keys())
agent_count = len(agents)
total_queries = len(all_queries)

# 2. 分配查询给agents
assignment = {agent: [] for agent in agents}

if total_queries > agent_count:
    # 查询数 > agent数, 随机打乱并循环分配
    random.shuffle(all_queries)
    for i, query in enumerate(all_queries):
        agent_name = agents[i % agent_count]
        assignment[agent_name].append(query)
else:
    # 查询数 <= agent数，一对一分配，其余agent没有查询
    for i, query in enumerate(all_queries):
        assignment[agents[i]].append(query)

# 3. 构建最终数据结构
final_result = []
for agent in agents:
    queries = assignment[agent]
    # 按category分组
    web_search_data = {}
    for category, q in queries:
        if category not in web_search_data:
            web_search_data[category] = []
        web_search_data[category].append(q)

    result_item = {
        'agent_name': agent,
        'agent_output_name': shopping_agents[agent]['outputs'],
        'web_search_data': web_search_data
    }

    final_result.append(result_item)

print(final_result)