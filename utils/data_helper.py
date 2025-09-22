"""
数据助手工具类
"""
import json
import yaml
import os
from typing import Dict, List, Any


class DataHelper:
    """数据助手类，用于处理测试数据"""
    
    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        """加载JSON文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"文件未找到: {file_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return {}
    
    @staticmethod
    def load_yaml(file_path: str) -> Dict[str, Any]:
        """加载YAML文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"文件未找到: {file_path}")
            return {}
        except yaml.YAMLError as e:
            print(f"YAML解析错误: {e}")
            return {}
    
    @staticmethod
    def save_json(data: Dict[str, Any], file_path: str) -> None:
        """保存数据到JSON文件"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    
    @staticmethod
    def save_yaml(data: Dict[str, Any], file_path: str) -> None:
        """保存数据到YAML文件"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True)
    
    @staticmethod
    def get_test_data(data_type: str) -> Dict[str, Any]:
        """获取测试数据"""
        data_file = f"data/test_data.json"
        test_data = DataHelper.load_json(data_file)
        return test_data.get(data_type, {})
    
    @staticmethod
    def get_user_data(user_type: str = "default") -> Dict[str, Any]:
        """获取用户数据"""
        users_file = "data/users.yaml"
        users_data = DataHelper.load_yaml(users_file)
        return users_data.get(user_type, {})
    
    @staticmethod
    def generate_random_email() -> str:
        """生成随机邮箱"""
        import random
        import string
        
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        domain = random.choice(['gmail.com', 'yahoo.com', 'hotmail.com'])
        return f"{username}@{domain}"
