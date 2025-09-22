"""
环境配置管理
"""
import os
from typing import Dict, Any


class EnvironmentConfig:
    """环境配置类"""
    
    def __init__(self, environment: str = None):
        self.environment = environment or os.getenv('TEST_ENV', 'dev')
        self.config = self._load_environment_config()
    
    def _load_environment_config(self) -> Dict[str, Any]:
        """加载环境配置"""
        configs = {
            'dev': {
                'base_url': 'http://localhost:3000',
                'api_url': 'http://localhost:8000/api',
                'database_url': 'sqlite:///dev.db',
                'debug': True,
                'timeout': 30000,
                'headless': False
            },
            'staging': {
                'base_url': 'https://staging.example.com',
                'api_url': 'https://staging-api.example.com/api',
                'database_url': 'postgresql://staging:password@staging-db:5432/staging',
                'debug': False,
                'timeout': 60000,
                'headless': True
            },
            'production': {
                'base_url': 'https://example.com',
                'api_url': 'https://api.example.com/api',
                'database_url': 'postgresql://prod:password@prod-db:5432/production',
                'debug': False,
                'timeout': 60000,
                'headless': True
            }
        }
        
        return configs.get(self.environment, configs['dev'])
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self.config.get(key, default)
    
    def get_base_url(self) -> str:
        """获取基础URL"""
        return self.get('base_url')
    
    def get_api_url(self) -> str:
        """获取API URL"""
        return self.get('api_url')
    
    def is_debug(self) -> bool:
        """是否调试模式"""
        return self.get('debug', False)
    
    def get_timeout(self) -> int:
        """获取超时时间"""
        return self.get('timeout', 30000)
    
    def is_headless(self) -> bool:
        """是否无头模式"""
        return self.get('headless', True)


# 全局环境配置实例
env_config = EnvironmentConfig()
