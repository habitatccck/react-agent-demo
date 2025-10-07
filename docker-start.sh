#!/bin/bash
# Docker 快速启动脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
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

# 检查 Docker 和 Docker Compose
check_dependencies() {
    print_info "检查依赖..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi
    
    print_success "依赖检查通过"
}

# 检查环境变量文件
check_env() {
    print_info "检查环境变量..."
    
    if [ ! -f ".env" ]; then
        print_warning "未找到 .env 文件，正在创建..."
        cp env.docker.example .env
        print_warning "请编辑 .env 文件，填入真实的 API 密钥"
        print_info "编辑命令: nano .env"
        read -p "按 Enter 继续..."
    fi
    
    print_success "环境变量检查完成"
}

# 构建和启动服务
start_services() {
    local mode=${1:-dev}
    
    print_info "启动服务 (模式: $mode)..."
    
    case $mode in
        "dev")
            docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
            ;;
        "prod")
            docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
            ;;
        "api")
            docker-compose up api --build
            ;;
        "langgraph")
            docker-compose up langgraph --build
            ;;
        *)
            docker-compose up --build
            ;;
    esac
    
    print_success "服务启动完成"
}

# 检查服务状态
check_services() {
    print_info "检查服务状态..."
    
    # 等待服务启动
    sleep 10
    
    # 检查 HTTP API 服务
    if curl -f http://localhost:8000/health &> /dev/null; then
        print_success "HTTP API 服务运行正常 (http://localhost:8000)"
    else
        print_error "HTTP API 服务启动失败"
    fi
    
    # 检查 LangGraph 服务
    if curl -f http://localhost:2024/health &> /dev/null; then
        print_success "LangGraph 服务运行正常 (http://localhost:2024)"
    else
        print_error "LangGraph 服务启动失败"
    fi
    
    print_info "服务状态检查完成"
}

# 显示服务信息
show_info() {
    print_info "服务信息:"
    echo "  - HTTP API: http://localhost:8000"
    echo "  - API 文档: http://localhost:8000/docs"
    echo "  - LangGraph: http://localhost:2024"
    echo "  - 健康检查: http://localhost:8000/health"
    echo ""
    print_info "管理命令:"
    echo "  - 查看日志: docker-compose logs -f"
    echo "  - 停止服务: docker-compose down"
    echo "  - 重启服务: docker-compose restart"
    echo "  - 查看状态: docker-compose ps"
}

# 主函数
main() {
    echo "🐳 LangGraph Docker 部署脚本"
    echo "================================"
    
    # 解析参数
    MODE="dev"
    if [ $# -gt 0 ]; then
        MODE=$1
    fi
    
    # 执行步骤
    check_dependencies
    check_env
    start_services $MODE
    
    if [ "$MODE" = "prod" ]; then
        check_services
    fi
    
    show_info
}

# 运行主函数
main "$@"
