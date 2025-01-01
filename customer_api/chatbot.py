from openai import OpenAI
from provider_api.models import Product, Provider


def get_db_info():
    info = dict()
    provdiers = Provider.objects.all()
    for provider in provdiers:
        products = Product.objects.filter(provider=provider)
        info[provider.shop_name] = {
            '地址': provider.address,
            '分類': provider.category,
            '商品': [
                {
                    '產品名稱': product.name,
                    '價錢': product.price,
                    '介紹': product.description,
                    '上架時間': product.created_at
                } for product in products
            ]
        }
    return info

SYSTEM_MESSAGE_TEMPLATE = "你是 U-BirdEAT 外送平台的智能機器人功能，你可以透過聊天了解顧客需求，並推薦餐廳與商品。以下為平台資料庫中的資訊，請依照平台中的餐廳與產品資訊，進行回覆(請不要使用Markdown格式):\n"

def get_chatbot_response(customer, prompt):
    client = OpenAI()
    customer.chatrecord_set.create(role="user", content=prompt)
    
    messages = list()
    messages.append({
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": SYSTEM_MESSAGE_TEMPLATE + str(get_db_info())
            }
        ]
    })
    records = customer.chatrecord_set.all().order_by('created_at')
    for record in records:
        messages.append({
            "role": record.role,
            "content": [
                {
                    "type": "text",
                    "text": record.content
                }
            ]
        })
    
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        response_format={
            "type": "text"
        },
        temperature=1,
        max_completion_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

    customer.chatrecord_set.create(role="system", content=response.choices[0].message.content)
    return response.choices[0].message.content