"""
用户API测试用例
"""
import pytest
import requests
from config.settings import API_BASE_URL


class TestUserAPI:
    """用户API测试类"""
    
    def test_get_user_list(self):
        """测试获取用户列表"""
        response = requests.get(f"{API_BASE_URL}/users")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_user(self):
        """测试创建用户"""
        user_data = {
            "name": "测试用户",
            "email": "test@example.com"
        }
        response = requests.post(f"{API_BASE_URL}/users", json=user_data)
        assert response.status_code == 201
        assert response.json()["name"] == user_data["name"]
    
    def test_get_user_by_id(self):
        """测试根据ID获取用户"""
        user_id = 1
        response = requests.get(f"{API_BASE_URL}/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["id"] == user_id
