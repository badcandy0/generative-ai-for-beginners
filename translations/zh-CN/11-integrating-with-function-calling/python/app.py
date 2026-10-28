import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import requests
load_dotenv()
endpoint = os.environ['OPENAI_API_BASE_URL']
client = OpenAI(
api_key=os.environ['OPENAI_API_KEY'],
base_url=endpoint
)

deployment=os.environ['AZURE_OPENAI_DEPLOYMENT']


student_1_description="Emily Johnson is a sophomore majoring in computer science at Duke University. She has a 3.7 GPA. Emily is an active member of the university's Chess Club and Debate Team. She hopes to pursue a career in software engineering after graduating."

student_2_description = "Michael Lee is a sophomore majoring in computer science at Stanford University. He has a 3.8 GPA. Michael is known for his programming skills and is an active member of the university's Robotics Club. He hopes to pursue a career in artificial intelligence after finishing his studies."


prompt1 = f'''
Please extract the following information from the given text and return it as a JSON object:

name
major
school
grades
club

This is the body of text to extract the information from:
{student_1_description}
'''

prompt2 = f'''
Please extract the following information from the given text and return it as a JSON object:

name
major
school
grades
club

This is the body of text to extract the information from:
{student_2_description}
'''

# 来自提示一的响应
# openai_response1 = client.responses.create(
# model=deployment,
# input = [{'role': 'user', 'content': prompt1}],
# store=False,
# )
# openai_response1.output_text

# 来自提示二的响应
# openai_response2 = client.responses.create(
# model=deployment,
# input = [{'role': 'user', 'content': prompt2}],
# store=False,
# )
# openai_response2.output_text

messages= [ {"role": "user", "content": "Find me a good course for a beginner student to learn Azure."} ]

functions = [
   {
      "type":"function",
      "name":"search_courses",
      "description":"Retrieves courses from the search index based on the parameters provided",
      "parameters":{
         "type":"object",
         "properties":{
            "role":{
               "type":"string",
               "description":"The role of the learner (i.e. developer, data scientist, student, etc.)"
            },
            "product":{
               "type":"string",
               "description":"The product that the lesson is covering (i.e. Azure, Power BI, etc.)"
            },
            "level":{
               "type":"string",
               "description":"The level of experience the learner has prior to taking the course (i.e. beginner, intermediate, advanced)"
            }
         },
         "required":[
            "role"
         ]
      }
   }
]

response = client.responses.create(model=deployment,
                                        input=messages,
                                        tools=functions,
                                        tool_choice="auto",
                                        store=False)

response_items = response.output
tool_calls = [item for item in response_items if item.type == "function_call"]

def search_courses(role, product, level):
  url = "https://learn.microsoft.com/api/catalog/"
  params = {
     "role": role,
     "product": product,
     "level": level
  }
  response = requests.get(url, params=params)
  modules = response.json()["modules"]
  results = []
  for module in modules[:5]:
     title = module["title"]
     url = module["url"]
     results.append({"title": title, "url": url})
  return str(results)

# 检查模型是否想调用一个函数
if tool_calls:
 for tool_call in tool_calls:
  print("Recommended Function call:")
  print(tool_call.name)
  print()

  # 调用该函数。
  function_name = tool_call.name

  available_functions = {
          "search_courses": search_courses,
  }
  function_to_call = available_functions[function_name]

  function_args = json.loads(tool_call.arguments)
  function_response = function_to_call(**function_args)

  print("Output of function call:")
  print(function_response)
  print(type(function_response))

  # 将函数调用及其结果添加回对话中。
  # 模型的 function_call 项必须附加在其输出之前。
  messages.append(tool_call)  # 助手的 function_call 项
  messages.append( # 函数结果
      {
          "type": "function_call_output",
          "call_id": tool_call.call_id,
          "output": function_response,
      }
  )

function_to_call = available_functions[function_name]

function_args = json.loads(tool_call.arguments)
function_response = function_to_call(**function_args)
print("Messages in next request:")
print(messages)
print()

second_response = client.responses.create(
   input=messages,
   model=deployment,
   tool_choice="auto",
   tools=functions,
   temperature=0,
   store=False,
      )  # 从模型获取一个新的响应，其中它可以看到函数的响应


print(second_response.output_text)
