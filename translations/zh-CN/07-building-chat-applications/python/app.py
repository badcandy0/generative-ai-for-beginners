import os
from openai import OpenAI
import numpy as np

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_API_BASE_URL")
)

system_prompt = """
##角色和任务
你是一个消化内科的专家。请你解答用户的问题，并提供详细的解释和建议。请确保你的回答是专业的、准确的，并且易于理解。

##限制
- 仅回答消化内科相关的问题。
- 不要提供与消化内科无关的建议或信息。
- 不要提供医疗诊断或处方。
- 不要提供任何可能被误解为医疗建议的内容。

##安全准则
- 不要生成任何包含暴力、色情、仇恨、歧视或不适当内容的回答。
- 除了询问用户的症状和病史外，不要要求提供任何个人身份信息。
- 若用户出言不逊或提出不适当的问题，请礼貌地拒绝回答，并提醒用户保持尊重和礼貌。

##回答格式
- 回复格式应简洁明了，避免使用复杂的医学术语。
- 涉及多项建议时，请使用编号或项目符号列表。
- 回复结尾应包含一句鼓励用户咨询专业医生的建议，例如：“请记住，以上信息仅供参考，若有任何健康问题，请咨询专业医生。”
"""

system_prompt_1 = """
你是一个非常专业的助理。所有的回答都要以中文输出，并且要尽量详细和专业。请确保你的回答是准确的，并且易于理解。
""" 

prompt = f"Product description: A home milkshake maker\nSeed words: fast, healthy, compact.\nProduct names: HomeShaker, Fit Shaker, QuickShake, Shake Maker\n\nProduct description: A pair of shoes that can fit any foot size.\nSeed words: adaptable, fit, omni-fit."

response = client.responses.create(
    model="deepseek-flash",  # 这是您的模型部署名称
    input=[
        {"role": "system", "content": system_prompt_1},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    store=False,
)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


print(response.output_text)