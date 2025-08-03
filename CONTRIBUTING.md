# 贡献指南

感谢您对 ArXiv Search SDK 的贡献兴趣！

## 如何贡献

### 1. 报告问题

如果您发现了 bug 或有功能建议，请：

1. 检查是否已有相关的 issue
2. 如果没有，请创建新的 issue
3. 提供详细的描述和复现步骤

### 2. 提交代码

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 3. 代码规范

- 使用 Black 格式化代码
- 遵循 PEP 8 代码风格
- 添加适当的文档字符串
- 为新功能添加测试

### 4. 测试

在提交代码前，请确保：

```bash
# 运行测试
pytest

# 代码格式检查
black --check .
flake8 .

# 类型检查
mypy .
```

### 5. 文档

- 为新功能添加文档
- 更新 README.md（如有必要）
- 添加示例代码

## 开发环境设置

1. 克隆仓库
```bash
git clone https://github.com/li-xiu-qi/arxiv-search-sdk.git
cd arxiv-search-sdk
```

2. 安装依赖
```bash
pip install -e .[dev]
```

3. 运行测试
```bash
pytest
```

感谢您的贡献！
