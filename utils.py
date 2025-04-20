import json

def add_item_to_json(file_path, new_item):
    """
    读取 JSON 文件（假设其本身是一个列表），添加新项，并保存更新后的 JSON 数据。

    参数:
        file_path (str): JSON 文件的路径。
        new_item (any): 要添加到列表中的新项。

    返回:
        bool: 操作是否成功。
    """
    try:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"警告: 文件 '{file_path}' 未找到，将创建一个新文件并初始化为空列表。")
            data = []

        if not isinstance(data, list):
            raise ValueError("错误: 文件内容不是一个有效的列表。")

        data.append(new_item)

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("操作成功：新项已添加并保存。")
        return True

    except json.JSONDecodeError:
        print("错误: 文件内容不是有效的 JSON 格式。")
        return False
    except Exception as e:
        print(f"发生未知错误: {e}")
        return False

def remove_duplicates_by_field(file_path, field_name):
    """
    删除 JSON 文件中字典列表中指定字段值重复的项，仅保留第一次出现的项。

    参数:
        file_path (str): JSON 文件的路径。
        field_name (str): 用于判断重复的字段名。

    返回:
        bool: 操作是否成功。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("错误: 文件内容不是一个列表。")

        seen_values = set()
        unique_data = []

        for item in data:
            if not isinstance(item, dict):
                raise ValueError("错误: 列表中的元素不是字典。")

            if field_name not in item:
                print(f"警告: 字段 '{field_name}' 不在某些字典中，跳过该项：{item}")
                continue

            field_value = item[field_name]

            if field_value not in seen_values:
                seen_values.add(field_value)
                unique_data.append(item)
            else:
                print(f"已删除重复项: {item}")

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(unique_data, file, ensure_ascii=False, indent=4)

        print("操作成功：重复项已删除并保存。")
        return True

    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 未找到。")
        return False
    except json.JSONDecodeError:
        print("错误: 文件内容不是有效的 JSON 格式。")
        return False
    except Exception as e:
        print(f"发生未知错误: {e}")
        return False
