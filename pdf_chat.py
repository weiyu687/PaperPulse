from pathlib import Path
from openai import OpenAI


PROMPT_PATH = './prompt.txt'

with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
    PROMPT = f.read()

def process_file_and_query(api_key, file_path, query, model="moonshot-v1-32k", temperature=0.3):
    """
    处理文件并根据用户查询获取模型的回答。

    参数:
        api_key (str): Moonshot API Key。
        file_path (str): 要上传和处理的文件路径。
        query (str): 用户的问题或查询内容。
        model (str): 使用的模型名称，默认为 "moonshot-v1-32k"。
        temperature (float): 控制生成文本的随机性，默认为 0.3。

    返回:
        str: 模型返回的回答内容。
    """
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.moonshot.cn/v1",
    )

    try:
        file_object = client.files.create(file=Path(file_path), purpose="file-extract")

        file_content = client.files.content(file_id=file_object.id).text

        messages = [
            {
                "role": "system",
                "content": PROMPT,
            },
            {
                "role": "system",
                "content": file_content,
            },
            {"role": "user", "content": query},
        ]

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"发生错误: {str(e)}"


if __name__ == "__main__":
    api_key = "Your api key."
    file_path = "./test/example.pdf"
    query = "请按要求分析该论文"

    result = process_file_and_query(api_key, file_path, query)
    print(result)