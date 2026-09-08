# Nutanix NCP-MCI 模拟考试系统

这是一个基于 Streamlit 的 Nutanix Certified Professional - Multicloud Infrastructure（NCP-MCI）备考模拟器。题库、答题逻辑、评分和页面界面集中在 `app.py` 中，适合本地运行和个人练习。

## 功能

- 内置 NCP-MCI v6.10 题库、答案和技术解析
- **章节练习模式**：逐题答题，提交后立即查看答案与解析
- **模拟考试模式**：完成整套题目后统一提交并查看得分与错题解析
- 支持随机抽题
- 支持按题号范围顺序练习
- 支持单选题和多选题
- 自动收集答错题目并保存在浏览器本地，可从主页进入错题专项练习
- 支持退出并重置当前练习

## 环境要求

- Python 3.11 或兼容版本
- pip

## 本地运行

在项目根目录执行：

```powershell
pip install -r requirements.txt
streamlit run app.py
```

启动后打开：<http://localhost:8501>

## 使用流程

1. 选择答题模式：章节练习或模拟考试。
2. 选择随机抽题，或关闭随机抽题后指定题号范围。
3. 点击“启动模拟系统”。
4. 按页面提示答题并提交。
5. 在章节练习模式中逐题查看解析；在模拟考试模式中完成后统一查看成绩和错题。
6. 答错的题目会写入当前浏览器的本地错题本。重新打开主页后，可以选择“练习错题”，也可以清空错题记录。

## 项目结构

```text
.
├── app.py                         # Streamlit 应用、题库和交互逻辑
├── requirements.txt               # Python 依赖
└── .devcontainer/devcontainer.json # Python 3.11 开发容器配置
```

## 维护题库

题库定义在 `app.py` 顶部的 `QUESTIONS` 列表中。每道题通常包含以下字段：

- `num`：题号
- `question`：题目内容
- `options`：选项列表，选项首字母用于记录答案
- `answer`：展示用答案
- `explanation`：技术解析
- `answer_clean`：用于判分的答案字母列表
- `is_multi`：是否为多选题

新增或修改题目时，请保持字段名称和答案格式一致。多选题的 `answer_clean` 应包含所有正确选项，`is_multi` 应设为 `True`。

## 验证

Python 代码修改后，先运行语法检查：

```powershell
python -c "import ast; from pathlib import Path; ast.parse(Path('app.py').read_text(encoding='utf-8')); print('app.py AST parse: OK')"
```

涉及页面或答题流程的修改，还应启动应用并手动验证：

- 章节练习的答题、提交和解析展示
- 模拟考试的统一提交、评分和错题展示
- 退出并重置后能重新开始
- 默认 Streamlit 窗口尺寸下页面可用

## 本地数据说明

顺序练习进度和错题本均保存在浏览器 `localStorage` 中，不会上传到服务器，也不会跨浏览器或设备同步。清理浏览器站点数据会同时清除这些记录。

## Dev Container

项目提供 `.devcontainer/devcontainer.json`，使用 Python 3.11 容器并转发 Streamlit 默认端口 `8501`。在容器中安装依赖后，可使用同样的启动命令运行应用。

## 免责声明

本项目用于个人学习和练习。请以 Nutanix 官方文档、培训材料和正式考试要求为准。