# 分支策略指南

本文档描述了 CliniqNexus Playwright Pytest 项目的分支管理策略，确保代码质量和项目稳定性。

## 🌳 分支结构

### 主要分支

#### `main` 分支
- **用途**：生产就绪的稳定代码
- **保护级别**：最高
- **合并策略**：只能通过 Pull Request 合并
- **要求**：
  - 所有测试必须通过
  - 代码审查必须通过
  - CI/CD 流水线必须成功

#### `develop` 分支
- **用途**：集成开发分支，包含最新的开发功能
- **保护级别**：高
- **合并策略**：功能分支合并到此分支
- **要求**：
  - 基本测试必须通过
  - 代码审查建议通过

### 功能分支

#### `feature/*` 分支
- **命名规范**：`feature/功能描述`
- **用途**：开发新功能
- **来源**：从 `develop` 分支创建
- **目标**：合并到 `develop` 分支
- **示例**：
  - `feature/enhanced-login-tests`
  - `feature/api-testing-improvements`
  - `feature/new-page-objects`

#### `hotfix/*` 分支
- **命名规范**：`hotfix/问题描述`
- **用途**：修复生产环境中的紧急问题
- **来源**：从 `main` 分支创建
- **目标**：同时合并到 `main` 和 `develop` 分支
- **示例**：
  - `hotfix/critical-bug-fix`
  - `hotfix/security-patch`

#### `release/*` 分支
- **命名规范**：`release/版本号`
- **用途**：准备新版本发布
- **来源**：从 `develop` 分支创建
- **目标**：合并到 `main` 分支
- **示例**：
  - `release/v1.0.0`
  - `release/v1.1.0`

## 🔒 分支保护规则

### main 分支保护
```yaml
保护规则:
  - 要求 Pull Request 审查
  - 要求状态检查通过
  - 要求分支是最新的
  - 限制推送权限
  - 要求线性历史
```

### develop 分支保护
```yaml
保护规则:
  - 建议 Pull Request 审查
  - 要求基本状态检查通过
  - 限制直接推送
```

## 📋 工作流程

### 1. 功能开发流程

```bash
# 1. 从 develop 创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name

# 2. 开发功能
# ... 编写代码和测试 ...

# 3. 提交更改
git add .
git commit -m "feat: 添加新功能描述"

# 4. 推送分支
git push origin feature/your-feature-name

# 5. 创建 Pull Request 到 develop
```

### 2. 热修复流程

```bash
# 1. 从 main 创建热修复分支
git checkout main
git pull origin main
git checkout -b hotfix/issue-description

# 2. 修复问题
# ... 修复代码 ...

# 3. 提交更改
git add .
git commit -m "fix: 修复问题描述"

# 4. 推送分支
git push origin hotfix/issue-description

# 5. 创建 Pull Request 到 main 和 develop
```

### 3. 发布流程

```bash
# 1. 从 develop 创建发布分支
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# 2. 准备发布
# ... 更新版本号、文档等 ...

# 3. 提交更改
git add .
git commit -m "chore: 准备 v1.0.0 发布"

# 4. 推送分支
git push origin release/v1.0.0

# 5. 创建 Pull Request 到 main
# 6. 合并后创建 Git 标签
```

## 🏷️ 标签策略

### 版本标签
- **格式**：`v主版本.次版本.修订版本`
- **示例**：`v1.0.0`, `v1.1.0`, `v2.0.0`
- **用途**：标记发布版本

### 创建标签
```bash
# 创建带注释的标签
git tag -a v1.0.0 -m "Release version 1.0.0"

# 推送标签到远程
git push origin v1.0.0
```

## 🔄 合并策略

### Pull Request 要求
1. **标题**：清晰描述更改内容
2. **描述**：详细说明更改原因和影响
3. **测试**：确保所有测试通过
4. **文档**：更新相关文档
5. **审查**：至少一名审查者批准

### 合并类型
- **Squash and merge**：功能分支推荐
- **Merge commit**：发布分支推荐
- **Rebase and merge**：简单修复推荐

## 🚫 禁止操作

### 绝对禁止
- 直接推送到 `main` 分支
- 强制推送 (`git push --force`)
- 删除已发布的标签
- 修改已合并的提交历史

### 不推荐
- 在 `main` 分支上直接开发
- 长时间不合并的功能分支
- 过大的 Pull Request

## 📊 分支状态检查

### 自动化检查
- 代码格式检查 (Black, isort)
- 代码质量检查 (flake8, mypy)
- 测试覆盖率检查
- 安全漏洞扫描

### 手动检查
- 代码审查
- 功能测试
- 文档更新
- 性能影响评估

## 🛠️ 工具和脚本

### 有用的 Git 别名
```bash
# 添加到 ~/.gitconfig
[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = !gitk
```

### 分支管理脚本
```bash
# 清理已合并的分支
git branch --merged | grep -v "\*\|main\|develop" | xargs -n 1 git branch -d

# 查看分支关系图
git log --graph --pretty=oneline --abbrev-commit --all
```

## 📚 最佳实践

1. **保持分支简短**：功能分支生命周期不超过 2 周
2. **频繁同步**：定期从主分支拉取最新更改
3. **清晰提交**：使用规范的提交信息格式
4. **及时清理**：删除已合并的分支
5. **文档更新**：重要更改时更新相关文档

## 🆘 紧急情况处理

### 回滚策略
```bash
# 回滚到上一个稳定版本
git checkout main
git reset --hard <previous-commit-hash>
git push --force-with-lease origin main
```

### 紧急修复
1. 创建热修复分支
2. 快速修复问题
3. 通过紧急审查流程
4. 立即部署到生产环境

---

遵循这些分支策略将确保项目的稳定性和代码质量，同时支持高效的团队协作。
