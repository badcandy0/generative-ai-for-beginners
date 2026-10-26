import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE_URL")
)

filter = input("请输入您想要的菜谱类型（例如：中餐、西餐、素食等）：")

no_filter = input("不太想要这些食材吗？请输入您不想要的食材（例如：牛肉、鱼、辣椒等），如果没有请直接按回车键：")

prompt = f"请给我展示5个{filter}菜谱：鸡肉、土豆和胡萝卜。每个菜谱列出所有所用食材。不想要的食材：{no_filter}。"

response = client.responses.create(
    model="deepseek-flash",  # 这是您的模型部署名称
    input=prompt,
    temperature=0.7,
    store=False,
)
print(response.output_text)