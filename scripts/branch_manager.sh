#!/bin/bash

# 分支管理脚本
# 用于简化常见的分支操作

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示帮助信息
show_help() {
    echo "分支管理脚本"
    echo ""
    echo "用法: $0 [命令] [选项]"
    echo ""
    echo "命令:"
    echo "  create-feature <name>    创建功能分支"
    echo "  create-hotfix <name>     创建热修复分支"
    echo "  create-release <version> 创建发布分支"
    echo "  switch <branch>          切换到指定分支"
    echo "  sync                     同步当前分支"
    echo "  cleanup                  清理已合并的分支"
    echo "  status                   显示分支状态"
    echo "  help                     显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 create-feature new-login-tests"
    echo "  $0 create-hotfix critical-bug"
    echo "  $0 create-release v1.0.0"
    echo "  $0 switch develop"
    echo "  $0 sync"
    echo "  $0 cleanup"
}

# 检查是否在Git仓库中
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "当前目录不是Git仓库"
        exit 1
    fi
}

# 检查工作目录是否干净
check_clean_working_dir() {
    if ! git diff-index --quiet HEAD --; then
        print_error "工作目录不干净，请先提交或暂存更改"
        exit 1
    fi
}

# 创建功能分支
create_feature_branch() {
    local feature_name="$1"
    if [ -z "$feature_name" ]; then
        print_error "请提供功能分支名称"
        exit 1
    fi
    
    local branch_name="feature/$feature_name"
    
    print_info "创建功能分支: $branch_name"
    
    # 切换到develop分支
    git checkout develop
    git pull origin develop
    
    # 创建新分支
    git checkout -b "$branch_name"
    
    print_success "功能分支 '$branch_name' 创建成功"
    print_info "当前分支: $(git branch --show-current)"
}

# 创建热修复分支
create_hotfix_branch() {
    local hotfix_name="$1"
    if [ -z "$hotfix_name" ]; then
        print_error "请提供热修复分支名称"
        exit 1
    fi
    
    local branch_name="hotfix/$hotfix_name"
    
    print_info "创建热修复分支: $branch_name"
    
    # 切换到main分支
    git checkout main
    git pull origin main
    
    # 创建新分支
    git checkout -b "$branch_name"
    
    print_success "热修复分支 '$branch_name' 创建成功"
    print_info "当前分支: $(git branch --show-current)"
}

# 创建发布分支
create_release_branch() {
    local version="$1"
    if [ -z "$version" ]; then
        print_error "请提供版本号"
        exit 1
    fi
    
    local branch_name="release/$version"
    
    print_info "创建发布分支: $branch_name"
    
    # 切换到develop分支
    git checkout develop
    git pull origin develop
    
    # 创建新分支
    git checkout -b "$branch_name"
    
    print_success "发布分支 '$branch_name' 创建成功"
    print_info "当前分支: $(git branch --show-current)"
}

# 切换到指定分支
switch_branch() {
    local branch_name="$1"
    if [ -z "$branch_name" ]; then
        print_error "请提供分支名称"
        exit 1
    fi
    
    print_info "切换到分支: $branch_name"
    
    if git show-ref --verify --quiet "refs/heads/$branch_name"; then
        git checkout "$branch_name"
        print_success "已切换到分支: $branch_name"
    else
        print_error "分支 '$branch_name' 不存在"
        exit 1
    fi
}

# 同步当前分支
sync_branch() {
    local current_branch=$(git branch --show-current)
    print_info "同步分支: $current_branch"
    
    if [ "$current_branch" = "main" ]; then
        git pull origin main
    elif [ "$current_branch" = "develop" ]; then
        git pull origin develop
    else
        # 对于功能分支，先从develop拉取最新更改
        git fetch origin
        git rebase origin/develop
    fi
    
    print_success "分支 '$current_branch' 同步完成"
}

# 清理已合并的分支
cleanup_branches() {
    print_info "清理已合并的分支..."
    
    # 获取已合并的分支列表（排除main、develop和当前分支）
    local current_branch=$(git branch --show-current)
    local merged_branches=$(git branch --merged | grep -v "\*\|main\|develop\|$current_branch" | sed 's/^[ ]*//')
    
    if [ -z "$merged_branches" ]; then
        print_info "没有需要清理的已合并分支"
        return
    fi
    
    echo "以下分支已合并，将被删除："
    echo "$merged_branches"
    echo ""
    read -p "确认删除这些分支吗？(y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "$merged_branches" | xargs -n 1 git branch -d
        print_success "已删除已合并的分支"
    else
        print_info "取消删除操作"
    fi
}

# 显示分支状态
show_status() {
    print_info "分支状态信息："
    echo ""
    
    # 当前分支
    local current_branch=$(git branch --show-current)
    echo "当前分支: $current_branch"
    
    # 分支列表
    echo ""
    echo "本地分支:"
    git branch --format='%(refname:short) %(upstream:track)'
    
    echo ""
    echo "远程分支:"
    git branch -r --format='%(refname:short)'
    
    # 未推送的提交
    local unpushed_commits=$(git log --oneline origin/$(git branch --show-current)..HEAD 2>/dev/null | wc -l)
    if [ "$unpushed_commits" -gt 0 ]; then
        echo ""
        print_warning "有 $unpushed_commits 个未推送的提交"
    fi
    
    # 工作目录状态
    if ! git diff-index --quiet HEAD --; then
        echo ""
        print_warning "工作目录有未提交的更改"
    fi
}

# 主函数
main() {
    check_git_repo
    
    case "$1" in
        "create-feature")
            check_clean_working_dir
            create_feature_branch "$2"
            ;;
        "create-hotfix")
            check_clean_working_dir
            create_hotfix_branch "$2"
            ;;
        "create-release")
            check_clean_working_dir
            create_release_branch "$2"
            ;;
        "switch")
            switch_branch "$2"
            ;;
        "sync")
            sync_branch
            ;;
        "cleanup")
            cleanup_branches
            ;;
        "status")
            show_status
            ;;
        "help"|"--help"|"-h"|"")
            show_help
            ;;
        *)
            print_error "未知命令: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"
