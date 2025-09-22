# 🔒 SSL证书问题解决方案

## 问题描述

在使用pip安装Python包时，可能会遇到以下SSL证书验证错误：

```
SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1028)'))
```

## 解决方案

### 方案1：自动配置（推荐）

运行我们提供的SSL配置脚本：

```bash
python scripts/setup_pip_ssl.py
```

这个脚本会：
- 创建pip配置文件
- 设置受信任的主机
- 配置环境变量
- 测试配置是否生效

### 方案2：手动配置

#### 2.1 创建pip配置文件

**Linux/macOS:**
```bash
mkdir -p ~/.config/pip
cat > ~/.config/pip/pip.conf << EOF
[global]
trusted-host = pypi.org
               pypi.python.org
               files.pythonhosted.org
EOF
```

**Windows:**
```cmd
mkdir %APPDATA%\pip
echo [global] > %APPDATA%\pip\pip.conf
echo trusted-host = pypi.org >> %APPDATA%\pip\pip.conf
echo                pypi.python.org >> %APPDATA%\pip\pip.conf
echo                files.pythonhosted.org >> %APPDATA%\pip\pip.conf
```

#### 2.2 使用命令行参数

在每次安装时添加受信任主机参数：

```bash
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org <package_name>
```

#### 2.3 设置环境变量

```bash
export PIP_TRUSTED_HOST="pypi.org pypi.python.org files.pythonhosted.org"
```

## 验证解决方案

运行以下命令验证配置是否生效：

```bash
pip --version
pip install --upgrade pip
```

如果命令执行成功且没有SSL错误，说明问题已解决。

## 常见问题

### Q: 为什么会出现SSL证书问题？

A: 这通常发生在以下情况：
- 企业网络环境
- 代理服务器配置
- 防火墙设置
- 系统时间不正确
- 证书链不完整

### Q: 设置受信任主机是否安全？

A: 对于开发和测试环境，这是安全的。对于生产环境，建议：
- 使用企业内部的PyPI镜像
- 配置正确的证书链
- 使用虚拟专用网络(VPN)

### Q: 如何恢复默认设置？

A: 删除pip配置文件即可：

**Linux/macOS:**
```bash
rm ~/.config/pip/pip.conf
```

**Windows:**
```cmd
del %APPDATA%\pip\pip.conf
```

## 替代方案

### 使用国内镜像源

如果SSL问题持续存在，可以使用国内镜像源：

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ <package_name>
```

### 使用conda

如果pip问题无法解决，可以考虑使用conda：

```bash
conda install <package_name>
```

## 项目特定配置

本项目已包含SSL配置脚本，位于：
- `scripts/setup_pip_ssl.py` - 自动配置脚本
- `pip.conf` - 项目级配置文件

运行以下命令即可解决SSL问题：

```bash
python scripts/setup_pip_ssl.py
```

## 联系支持

如果问题仍然存在，请：
1. 检查网络连接
2. 验证系统时间
3. 联系网络管理员
4. 提交Issue到项目仓库
