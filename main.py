import os
import json

from pdf_chat import process_file_and_query
from utils import add_item_to_json, remove_duplicates_by_field

PDF_FOLDER = './paper'
PAPER_JSON = './paper.json'
API_KEY = 'Your api key.'

pdf_list = os.listdir(PDF_FOLDER)

for pdf_name in pdf_list:
    pdf_path = os.path.join(PDF_FOLDER, pdf_name)
    try:
        result = process_file_and_query(API_KEY, pdf_path, '请按照论文要求分析该论文')
        result_dict = json.loads(result)
        add_item_to_json(PAPER_JSON, result_dict)

        os.remove(pdf_path)

    except Exception as e:
        print('---------------------------------------------------')
        print(f'{pdf_name}读取失败')
        print(f'报错：{e}')

    finally:
        continue

remove_duplicates_by_field(PAPER_JSON, 'paper_title')
