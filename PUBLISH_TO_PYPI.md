# PyPI 发布教程（Windows 环境）

## 1. 注册 PyPI 账号

- 访问 <https://pypi.org/account/register/> 注册账号。

## 2. 检查项目结构

- 确保项目根目录下有 `setup.py`、`pyproject.toml`、`README.md` 等文件。
- 代码已提交到主分支，远程仓库地址已更新为新仓库名。

## 3. 安装打包和上传工具

```cmd
pip install build twine
```

## 4. 清理旧的构建文件（可选）

```cmd
rmdir /s /q build dist arxiv_search.egg-info
```

## 5. 构建分发包

```cmd
python -m build
```

- 构建完成后，会在 `dist/` 目录下生成 `.tar.gz` 和 `.whl` 文件。

## 6. 上传到 PyPI

```cmd
twine upload dist/*
```

- 系统会提示输入 PyPI 用户名和密码（或 token）。

## 7. 验证发布

- 发布成功后，可在 <https://pypi.org/project/arxiv-search-sdk/> 查看。

## 8. 安装测试

```cmd
pip install arxiv-search-sdk
```

---

### 常见问题

- 如果上传时报错“文件已存在”，请修改 `setup.py` 里的 `version` 字段，递增版本号后重新打包上传。
- 推荐使用 PyPI token 进行安全上传，详见 <https://pypi.org/help/#apitoken>

---

如需自动化发布，可考虑 GitHub Actions 等 CI 工具。
