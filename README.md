<div align="center">

# ContextForge

**Lightweight LLM Context Intelligent Compression Engine**
轻量级 LLM 上下文智能压缩引擎

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)](https://github.com/gitstq/ContextForge/releases)

[**简体中文**](#简体中文) | [**繁體中文**](#繁體中文) | [**English**](#english)

</div>

---

<!-- ============================================================ -->
<!-- 简体中文 -->
<!-- ============================================================ -->

<a id="简体中文"></a>

## 简体中文

> 🦞 ContextForge 是一个零核心依赖、跨平台的 Python 库，用于智能压缩 LLM 输入内容——包括工具输出、日志、文件和 RAG 分块。在保持语义完整性的前提下，实现 **50-90% 的 Token 压缩率**。

### 📑 目录

- [🎉 项目介绍](#-项目介绍)
- [✨ 核心特性](#-核心特性)
- [🚀 快速开始](#-快速开始)
- [📖 详细使用指南](#-详细使用指南)
  - [内容类型指定](#内容类型指定)
  - [压缩强度选择](#压缩强度选择)
  - [文件压缩](#文件压缩)
  - [批量处理](#批量处理)
  - [自定义模式](#自定义模式)
  - [CLI 命令](#cli-命令)
  - [配置选项](#配置选项)
- [💡 设计思路与迭代规划](#-设计思路与迭代规划)
- [📦 打包与部署指南](#-打包与部署指南)
- [🤝 贡献指南](#-贡献指南)
- [📄 开源协议](#-开源协议)

---

### 🎉 项目介绍

**ContextForge** 是一款专为 LLM（大语言模型）场景设计的轻量级上下文智能压缩引擎。它能够智能地压缩发送给 LLM 的输入内容，包括但不限于：

- **工具输出**（Tool Outputs）
- **应用日志**（Application Logs）
- **源代码文件**（Source Code Files）
- **RAG 检索分块**（RAG Chunks）
- **对话历史**（Conversation History）

#### 核心价值

| 指标 | 说明 |
|------|------|
| **Token 压缩率** | 50% - 90% 的 Token 数量削减 |
| **语义保真度** | 压缩后保留原始文本的核心语义信息 |
| **零核心依赖** | 纯 Python 标准库实现，无需安装任何第三方包 |
| **跨平台兼容** | 完美支持 Windows、macOS、Linux |

#### 解决的痛点

1. **Token 成本高昂** —— LLM API 按 Token 计费，冗长的日志和工具输出会大幅增加调用成本
2. **上下文窗口有限** —— 模型的上下文窗口大小固定，冗余内容挤占了有效信息的空间
3. **工具输出冗长** —— 开发工具、调试器、构建系统等产生的输出往往包含大量重复和无用信息
4. **RAG 分块效率低** —— 检索到的文档片段可能包含大量与问题无关的内容

#### 与同类工具的差异化优势

| 特性 | ContextForge | 其他工具 |
|------|-------------|---------|
| 核心依赖 | **零依赖** | 通常需要多个第三方库 |
| 压缩策略 | **5 种策略组合** | 通常只有 1-2 种 |
| 内容检测 | **自动检测 11+ 种类型** | 需手动指定 |
| 使用方式 | **Python SDK + CLI 双模式** | 通常只支持其中一种 |
| 扩展性 | **自定义正则模式** | 固定模式，难以扩展 |

#### 灵感来源

本项目灵感来源于 GitHub 上热门的 LLM 上下文优化项目（如 headroom 等），旨在为开发者提供一个轻量、高效、易用的 LLM 上下文压缩解决方案，帮助降低 Token 消耗、提升模型推理效率。

---

### ✨ 核心特性

- 🧠 **智能内容检测** —— 自动识别 11+ 种内容类型（日志、JSON、代码、Markdown、XML、HTML、CSV、对话、工具输出、RAG 分块等），无需手动指定
- 📊 **5 种压缩策略** —— 语义压缩（Semantic）、结构压缩（Structural）、模板压缩（Template）、正则压缩（Regex）、去重压缩（Deduplication），多策略协同工作
- ⚡ **零核心依赖** —— 纯 Python 实现，仅使用标准库（`re`、`json`、`dataclasses`、`abc`、`enum`、`time`），无需安装任何第三方包
- 🎯 **3 级压缩强度** —— 轻度（Light, 30-50%）、均衡（Balanced, 50-70%）、激进（Aggressive, 70-90%），灵活适配不同场景
- 🔒 **敏感信息保护** —— 自动检测并脱敏 API Key、密码、Token、Secret 等敏感信息，防止泄露
- 📈 **详细压缩统计** —— 提供原始/压缩后的字符数、Token 数、压缩率、处理时间、使用策略等完整统计信息
- 🖥️ **CLI + Python SDK** —— 既可在终端通过命令行使用，也可作为 Python 库集成到项目中
- 🌍 **跨平台支持** —— 支持 Windows、macOS、Linux，无平台限制
- 🔄 **批量处理** —— 支持一次调用压缩多个文本，提升处理效率
- 📝 **可扩展模式** —— 支持自定义正则表达式模式，满足特定领域的压缩需求

---

### 🚀 快速开始

#### 环境要求

- Python 3.9 及以上版本

#### 安装

```bash
pip install contextforge
```

#### Python SDK 基本用法

```python
from contextforge import ContextCompressor

compressor = ContextCompressor()
result = compressor.compress("""
[2024-01-15 10:23:45] DEBUG: Starting application...
[2024-01-15 10:23:45] DEBUG: Loading config from /app/config.yaml
[2024-01-15 10:23:46] DEBUG: Connecting to database...
[2024-01-15 10:23:46] INFO: Database connected successfully
[2024-01-15 10:23:47] DEBUG: Running migrations...
[2024-01-15 10:23:48] INFO: Migrations completed
[2024-01-15 10:23:48] DEBUG: Starting HTTP server on port 8080
[2024-01-15 10:23:49] INFO: Server started successfully
""")

print(f"压缩率: {result.stats.compression_ratio:.1%}")
print(f"节省 Token: {result.stats.tokens_saved}")
print(result.compressed_text)
```

#### CLI 基本用法

```bash
# 压缩日志文件
contextforge compress app.log --type log --level aggressive

# 从 stdin 读取并压缩
cat output.json | contextforge compress - --type json

# 检测文件内容类型
contextforge detect myfile.txt

# 估算 Token 数量
contextforge tokens myfile.txt

# 查看压缩统计信息
contextforge compress data.json --stats

# 输出 JSON 格式结果
contextforge compress data.json --json
```

---

### 📖 详细使用指南

#### 内容类型指定

ContextForge 支持自动检测以下 11 种内容类型，也可手动指定：

| 类型 | 值 | 说明 |
|------|-----|------|
| 自动检测 | `auto` | 默认模式，自动识别内容类型 |
| 日志 | `log` | 应用日志、系统日志、访问日志 |
| JSON | `json` | JSON 格式数据 |
| 代码 | `code` | 源代码文件 |
| XML | `xml` | XML 格式数据 |
| Markdown | `markdown` | Markdown 文档 |
| 纯文本 | `text` | 普通文本 |
| 工具输出 | `tool_output` | 工具/命令执行输出 |
| RAG 分块 | `rag_chunks` | RAG 检索结果片段 |
| 对话 | `conversation` | 多轮对话记录 |
| HTML | `html` | HTML 网页内容 |
| CSV | `csv` | 逗号分隔值数据 |

```python
from contextforge import ContextCompressor

compressor = ContextCompressor()

# 自动检测内容类型
result = compressor.compress(text)

# 手动指定内容类型
result = compressor.compress(text, content_type="log")
result = compressor.compress(text, content_type="json")
```

#### 压缩强度选择

提供 3 种预设压缩强度，适配不同场景需求：

| 强度 | 值 | 压缩率 | 适用场景 |
|------|-----|--------|---------|
| 轻度 | `light` | 30-50% | 需要保留尽可能多细节的场景 |
| 均衡 | `balanced` | 50-70% | 大多数场景的推荐选择（默认） |
| 激进 | `aggressive` | 70-90% | Token 预算紧张、需要最大压缩的场景 |

```python
from contextforge import ContextCompressor, CompressionLevel

# 使用预设强度
compressor = ContextCompressor()
result = compressor.compress(text, level="light")
result = compressor.compress(text, level="balanced")
result = compressor.compress(text, level="aggressive")

# 使用 CompressionLevel 枚举
result = compressor.compress(text, level=CompressionLevel.AGGRESSIVE)
```

#### 文件压缩

支持直接压缩文件内容：

```python
from contextforge import ContextCompressor

compressor = ContextCompressor()

# 压缩单个文件
result = compressor.compress_file("app.log")
print(f"压缩率: {result.stats.compression_ratio:.1%}")
print(result.compressed_text)

# 指定文件编码
result = compressor.compress_file("data.txt", encoding="gbk")
```

#### 批量处理

支持一次调用压缩多个文本：

```python
from contextforge import ContextCompressor

compressor = ContextCompressor()

texts = [
    open("log1.txt").read(),
    open("log2.txt").read(),
    open("log3.txt").read(),
]

results = compressor.compress_batch(texts)

for i, result in enumerate(results):
    print(f"文件 {i+1}: 压缩率 {result.stats.compression_ratio:.1%}")
```

#### 自定义模式

支持添加自定义正则表达式模式，用于特定领域的压缩需求：

```python
from contextforge import ContextCompressor, CompressionConfig

config = CompressionConfig(
    custom_patterns=[
        {"pattern": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', "replacement": "<IP>"},
        {"pattern": r'order_id=\w+', "replacement": "order_id=<ID>"},
    ]
)

compressor = ContextCompressor(config=config)
result = compressor.compress(text)
```

#### CLI 命令

ContextForge 提供三个核心 CLI 命令：

**compress** —— 压缩文本或文件内容

```bash
# 基本压缩
contextforge compress <input_file>

# 指定内容类型和压缩强度
contextforge compress <input_file> --type log --level aggressive

# 从 stdin 读取
cat file.txt | contextforge compress -

# 输出到文件
contextforge compress input.txt -o output.txt

# 显示统计信息
contextforge compress input.txt --stats

# JSON 格式输出
contextforge compress input.txt --json

# 限制最大输出 Token 数
contextforge compress input.txt --max-tokens 1000

# 保留行号
contextforge compress input.txt --preserve-lines
```

**detect** —— 检测文件内容类型

```bash
contextforge detect <input_file>
# 输出示例：
# Content Type: log
# Confidence: 85.0%
```

**tokens** —— 估算 Token 数量

```bash
contextforge tokens <input_file>
# 输出示例：
# Estimated tokens: 1234
```

#### 配置选项

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `level` | `CompressionLevel` | `balanced` | 压缩强度：`light` / `balanced` / `aggressive` / `custom` |
| `content_type` | `ContentType` | `auto` | 内容类型：`auto` / `log` / `json` / `code` 等 |
| `preserve_line_numbers` | `bool` | `False` | 是否保留行号 |
| `preserve_code_blocks` | `bool` | `True` | 是否保留代码块结构 |
| `preserve_json_structure` | `bool` | `True` | 是否保留 JSON 结构 |
| `max_output_tokens` | `int` | `None` | 最大输出 Token 数限制 |
| `min_compression_ratio` | `float` | `0.1` | 最小压缩率阈值（低于此值不压缩） |
| `enable_semantic` | `bool` | `True` | 启用语义压缩策略 |
| `enable_structural` | `bool` | `True` | 启用结构压缩策略 |
| `enable_regex` | `bool` | `True` | 启用正则压缩策略 |
| `enable_dedup` | `bool` | `True` | 启用去重压缩策略 |
| `enable_template` | `bool` | `True` | 启用模板压缩策略 |
| `custom_patterns` | `list` | `[]` | 自定义正则压缩模式 |
| `sensitive_patterns` | `list` | 预设模式 | 敏感信息检测正则模式 |
| `language_hints` | `list` | `[]` | 语言提示信息 |

```python
from contextforge import ContextCompressor, CompressionConfig, CompressionLevel

config = CompressionConfig(
    level=CompressionLevel.AGGRESSIVE,
    preserve_code_blocks=False,
    max_output_tokens=2000,
    enable_semantic=True,
    enable_structural=True,
    enable_regex=True,
    enable_dedup=True,
    enable_template=True,
)

compressor = ContextCompressor(config=config)
result = compressor.compress(text)
```

---

### 💡 设计思路与迭代规划

#### 设计理念

1. **零依赖原则** —— 核心功能完全基于 Python 标准库实现，降低安装复杂度，提升兼容性
2. **语义保真** —— 压缩的核心目标是减少 Token 数量，同时最大程度保留原始文本的语义信息
3. **可扩展架构** —— 基于策略模式（Strategy Pattern）设计，每种压缩策略独立实现，可灵活组合和扩展
4. **自动化优先** —— 自动检测内容类型、自动选择最优策略组合，降低使用门槛

#### 技术栈

| 模块 | 技术 | 说明 |
|------|------|------|
| 正则引擎 | `re` | 正则表达式匹配与替换 |
| 数据模型 | `dataclasses` | 结构化数据模型定义 |
| 抽象基类 | `abc` | 策略接口抽象定义 |
| 枚举类型 | `enum` | 内容类型、压缩级别枚举 |
| 时间计量 | `time` | 性能计时统计 |
| JSON 处理 | `json` | JSON 解析与序列化 |
| CLI 框架 | `argparse` | 命令行参数解析 |

#### 迭代规划

| 版本 | 主题 | 核心功能 |
|------|------|---------|
| **v1.0** | 基础引擎 | 5 种压缩策略、11+ 内容类型检测、CLI + SDK 双模式 |
| **v1.1** | AI 驱动压缩 | 集成 LLM 进行语义理解和智能摘要，进一步提升压缩质量 |
| **v1.2** | MCP Server | 实现 Model Context Protocol 服务器，支持 MCP 客户端直接调用 |
| **v1.3** | Web Dashboard | 提供可视化 Web 管理界面，支持在线压缩、统计分析和配置管理 |
| **v2.0** | 插件生态 | 构建插件系统，支持社区贡献自定义压缩策略和内容类型检测器 |

---

### 📦 打包与部署指南

#### 通过 pip 安装

```bash
# 从 PyPI 安装（推荐）
pip install contextforge

# 升级到最新版本
pip install --upgrade contextforge
```

#### 从源码构建

```bash
# 克隆仓库
git clone https://github.com/gitstq/ContextForge.git
cd ContextForge

# 安装构建依赖
pip install setuptools wheel

# 构建 wheel 包
python -m build

# 安装构建产物
pip install dist/contextforge-*.whl
```

#### 作为 CLI 工具使用

安装完成后，`contextforge` 命令将自动注册到系统 PATH 中：

```bash
# 验证安装
contextforge --version

# 直接使用
contextforge compress myfile.log --type log --level aggressive
```

#### 作为 Python 库集成

```python
# 在项目中导入
from contextforge import ContextCompressor, CompressionLevel, CompressionConfig

# 创建压缩器实例
compressor = ContextCompressor()

# 压缩文本
result = compressor.compress(text, level=CompressionLevel.BALANCED)

# 获取统计信息
print(f"压缩率: {result.stats.compression_ratio:.1%}")
print(f"原始 Token: {result.stats.original_tokens}")
print(f"压缩后 Token: {result.stats.compressed_tokens}")
print(f"节省 Token: {result.stats.tokens_saved}")
print(f"处理时间: {result.stats.processing_time_ms:.2f}ms")
print(f"使用策略: {', '.join(result.stats.strategies_used)}")
```

---

### 🤝 贡献指南

我们欢迎并感谢所有形式的贡献！在提交贡献之前，请阅读以下指南。

#### 提交 Pull Request

1. **Fork** 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature-name`
3. 提交更改：`git commit -m 'feat: add your feature description'`
4. 推送分支：`git push origin feature/your-feature-name`
5. 提交 **Pull Request**

**PR 规范：**
- 遵循现有代码风格（PEP 8）
- 为新功能编写对应的单元测试
- 确保所有现有测试通过：`pytest tests/`
- PR 描述中清晰说明更改内容和动机

#### 提交 Issue

- **Bug 报告**：请包含复现步骤、预期行为、实际行为以及运行环境信息
- **功能建议**：请详细描述使用场景和期望的行为
- **问题咨询**：请在 Issue 中提供足够的上下文信息

#### 开发环境搭建

```bash
# 克隆仓库
git clone https://github.com/gitstq/ContextForge.git
cd ContextForge

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/

# 运行测试并生成覆盖率报告
pytest tests/ --cov=contextforge --cov-report=html
```

---

### 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。

```
MIT License

Copyright (c) 2024 ContextForge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<!-- ============================================================ -->
<!-- 繁體中文 -->
<!-- ============================================================ -->

<a id="繁體中文"></a>

## 繁體中文

> 🦞 ContextForge 是一個零核心依賴、跨平台的 Python 函式庫，用於智慧壓縮 LLM 輸入內容——包括工具輸出、日誌、檔案和 RAG 分塊。在保持語意完整性的前提下，實現 **50-90% 的 Token 壓縮率**。

### 📑 目錄

- [🎉 專案介紹](#-專案介紹-1)
- [✨ 核心特性](#-核心特性-1)
- [🚀 快速開始](#-快速開始-1)
- [📖 詳細使用指南](#-詳細使用指南-1)
  - [內容類型指定](#內容類型指定-1)
  - [壓縮強度選擇](#壓縮強度選擇-1)
  - [檔案壓縮](#檔案壓縮-1)
  - [批次處理](#批次處理-1)
  - [自訂模式](#自訂模式-1)
  - [CLI 命令](#cli-命令-1)
  - [設定選項](#設定選項-1)
- [💡 設計思路與迭代規劃](#-設計思路與迭代規劃-1)
- [📦 打包與部署指南](#-打包與部署指南-1)
- [🤝 貢獻指南](#-貢獻指南-1)
- [📄 開源協議](#-開源協議-1)

---

### 🎉 專案介紹

**ContextForge** 是一款專為 LLM（大型語言模型）場景設計的輕量級上下文智慧壓縮引擎。它能夠智慧地壓縮發送給 LLM 的輸入內容，包括但不限於：

- **工具輸出**（Tool Outputs）
- **應用程式日誌**（Application Logs）
- **原始碼檔案**（Source Code Files）
- **RAG 檢索分塊**（RAG Chunks）
- **對話歷史**（Conversation History）

#### 核心價值

| 指標 | 說明 |
|------|------|
| **Token 壓縮率** | 50% - 90% 的 Token 數量削減 |
| **語意保真度** | 壓縮後保留原始文本的核心語意資訊 |
| **零核心依賴** | 純 Python 標準函式庫實現，無需安裝任何第三方套件 |
| **跨平台相容** | 完美支援 Windows、macOS、Linux |

#### 解決的痛點

1. **Token 成本高昂** —— LLM API 按 Token 計費，冗長的日誌和工具輸出會大幅增加呼叫成本
2. **上下文視窗有限** —— 模型的上下文視窗大小固定，冗餘內容擠占了有效資訊的空間
3. **工具輸出冗長** —— 開發工具、除錯器、建置系統等產生的輸出往往包含大量重複和無用資訊
4. **RAG 分塊效率低** —— 檢索到的文件片段可能包含大量與問題無關的內容

#### 與同類工具的差異化優勢

| 特性 | ContextForge | 其他工具 |
|------|-------------|---------|
| 核心依賴 | **零依賴** | 通常需要多個第三方函式庫 |
| 壓縮策略 | **5 種策略組合** | 通常只有 1-2 種 |
| 內容偵測 | **自動偵測 11+ 種類型** | 需手動指定 |
| 使用方式 | **Python SDK + CLI 雙模式** | 通常只支援其中一種 |
| 擴展性 | **自訂正則模式** | 固定模式，難以擴展 |

#### 靈感來源

本專案靈感來源於 GitHub 上熱門的 LLM 上下文最佳化專案（如 headroom 等），旨在為開發者提供一個輕量、高效、易用的 LLM 上下文壓縮解決方案，幫助降低 Token 消耗、提升模型推理效率。

---

### ✨ 核心特性

- 🧠 **智慧內容偵測** —— 自動識別 11+ 種內容類型（日誌、JSON、程式碼、Markdown、XML、HTML、CSV、對話、工具輸出、RAG 分塊等），無需手動指定
- 📊 **5 種壓縮策略** —— 語意壓縮（Semantic）、結構壓縮（Structural）、模板壓縮（Template）、正則壓縮（Regex）、去重壓縮（Deduplication），多策略協同工作
- ⚡ **零核心依賴** —— 純 Python 實現，僅使用標準函式庫（`re`、`json`、`dataclasses`、`abc`、`enum`、`time`），無需安裝任何第三方套件
- 🎯 **3 級壓縮強度** —— 輕度（Light, 30-50%）、均衡（Balanced, 50-70%）、激進（Aggressive, 70-90%），靈活適配不同場景
- 🔒 **敏感資訊保護** —— 自動偵測並脫敏 API Key、密碼、Token、Secret 等敏感資訊，防止洩露
- 📈 **詳細壓縮統計** —— 提供原始/壓縮後的字元數、Token 數、壓縮率、處理時間、使用策略等完整統計資訊
- 🖥️ **CLI + Python SDK** —— 既可在終端透過命令列使用，也可作為 Python 函式庫整合到專案中
- 🌍 **跨平台支援** —— 支援 Windows、macOS、Linux，無平台限制
- 🔄 **批次處理** —— 支援一次呼叫壓縮多個文本，提升處理效率
- 📝 **可擴展模式** —— 支援自訂正則表示式模式，滿足特定領域的壓縮需求

---

### 🚀 快速開始

#### 環境要求

- Python 3.9 及以上版本

#### 安裝

```bash
pip install contextforge
```

#### Python SDK 基本用法

```python
from contextforge import ContextCompressor

compressor = ContextCompressor()
result = compressor.compress("""
[2024-01-15 10:23:45] DEBUG: Starting application...
[2024-01-15 10:23:45] DEBUG: Loading config from /app/config.yaml
[2024-01-15 10:23:46] DEBUG: Connecting to database...
[2024-01-15 10:23:46] INFO: Database connected successfully
[2024-01-15 10:23:47] DEBUG: Running migrations...
[2024-01-15 10:23:48] INFO: Migrations completed
[2024-01-15 10:23:48] DEBUG: Starting HTTP server on port 8080
[2024-01-15 10:23:49] INFO: Server started successfully
""")

print(f"壓縮率: {result.stats.compression_ratio:.1%}")
print(f"節省 Token: {result.stats.tokens_saved}")
print(result.compressed_text)
```

#### CLI 基本用法

```bash
# 壓縮日誌檔案
contextforge compress app.log --type log --level aggressive

# 從 stdin 讀取並壓縮
cat output.json | contextforge compress - --type json

# 偵測檔案內容類型
contextforge detect myfile.txt

# 估算 Token 數量
contextforge tokens myfile.txt

# 查看壓縮統計資訊
contextforge compress data.json --stats

# 輸出 JSON 格式結果
contextforge compress data.json --json
```

---

### 📖 詳細使用指南

#### 內容類型指定

ContextForge 支援自動偵測以下 11 種內容類型，也可手動指定：

| 類型 | 值 | 說明 |
|------|-----|------|
| 自動偵測 | `auto` | 預設模式，自動識別內容類型 |
| 日誌 | `log` | 應用程式日誌、系統日誌、存取日誌 |
| JSON | `json` | JSON 格式資料 |
| 程式碼 | `code` | 原始碼檔案 |
| XML | `xml` | XML 格式資料 |
| Markdown | `markdown` | Markdown 文件 |
| 純文本 | `text` | 普通文本 |
| 工具輸出 | `tool_output` | 工具/命令執行輸出 |
| RAG 分塊 | `rag_chunks` | RAG 檢索結果片段 |
| 對話 | `conversation` | 多輪對話記錄 |
| HTML | `html` | HTML 網頁內容 |
| CSV | `csv` | 逗號分隔值資料 |

```python
from contextforge import ContextCompressor

compressor = ContextCompressor()

# 自動偵測內容類型
result = compressor.compress(text)

# 手動指定內容類型
result = compressor.compress(text, content_type="log")
result = compressor.compress(text, content_type="json")
```

#### 壓縮強度選擇

提供 3 種預設壓縮強度，適配不同場景需求：

| 強度 | 值 | 壓縮率 | 適用場景 |
|------|-----|--------|---------|
| 輕度 | `light` | 30-50% | 需要保留盡可能多細節的場景 |
| 均衡 | `balanced` | 50-70% | 大多數場景的推薦選擇（預設） |
| 激進 | `aggressive` | 70-90% | Token 預算緊張、需要最大壓縮的場景 |

```python
from contextforge import ContextCompressor, CompressionLevel

# 使用預設強度
compressor = ContextCompressor()
result = compressor.compress(text, level="light")
result = compressor.compress(text, level="balanced")
result = compressor.compress(text, level="aggressive")

# 使用 CompressionLevel 列舉
result = compressor.compress(text, level=CompressionLevel.AGGRESSIVE)
```

#### 檔案壓縮

支援直接壓縮檔案內容：

```python
from contextforge import ContextCompressor

compressor = ContextCompressor()

# 壓縮單一檔案
result = compressor.compress_file("app.log")
print(f"壓縮率: {result.stats.compression_ratio:.1%}")
print(result.compressed_text)

# 指定檔案編碼
result = compressor.compress_file("data.txt", encoding="big5")
```

#### 批次處理

支援一次呼叫壓縮多個文本：

```python
from contextforge import ContextCompressor

compressor = ContextCompressor()

texts = [
    open("log1.txt").read(),
    open("log2.txt").read(),
    open("log3.txt").read(),
]

results = compressor.compress_batch(texts)

for i, result in enumerate(results):
    print(f"檔案 {i+1}: 壓縮率 {result.stats.compression_ratio:.1%}")
```

#### 自訂模式

支援新增自訂正則表示式模式，用於特定領域的壓縮需求：

```python
from contextforge import ContextCompressor, CompressionConfig

config = CompressionConfig(
    custom_patterns=[
        {"pattern": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', "replacement": "<IP>"},
        {"pattern": r'order_id=\w+', "replacement": "order_id=<ID>"},
    ]
)

compressor = ContextCompressor(config=config)
result = compressor.compress(text)
```

#### CLI 命令

ContextForge 提供三個核心 CLI 命令：

**compress** —— 壓縮文本或檔案內容

```bash
# 基本壓縮
contextforge compress <input_file>

# 指定內容類型和壓縮強度
contextforge compress <input_file> --type log --level aggressive

# 從 stdin 讀取
cat file.txt | contextforge compress -

# 輸出到檔案
contextforge compress input.txt -o output.txt

# 顯示統計資訊
contextforge compress input.txt --stats

# JSON 格式輸出
contextforge compress input.txt --json

# 限制最大輸出 Token 數
contextforge compress input.txt --max-tokens 1000

# 保留行號
contextforge compress input.txt --preserve-lines
```

**detect** —— 偵測檔案內容類型

```bash
contextforge detect <input_file>
# 輸出範例：
# Content Type: log
# Confidence: 85.0%
```

**tokens** —— 估算 Token 數量

```bash
contextforge tokens <input_file>
# 輸出範例：
# Estimated tokens: 1234
```

#### 設定選項

| 設定項 | 類型 | 預設值 | 說明 |
|--------|------|--------|------|
| `level` | `CompressionLevel` | `balanced` | 壓縮強度：`light` / `balanced` / `aggressive` / `custom` |
| `content_type` | `ContentType` | `auto` | 內容類型：`auto` / `log` / `json` / `code` 等 |
| `preserve_line_numbers` | `bool` | `False` | 是否保留行號 |
| `preserve_code_blocks` | `bool` | `True` | 是否保留程式碼區塊結構 |
| `preserve_json_structure` | `bool` | `True` | 是否保留 JSON 結構 |
| `max_output_tokens` | `int` | `None` | 最大輸出 Token 數限制 |
| `min_compression_ratio` | `float` | `0.1` | 最小壓縮率閾值（低於此值不壓縮） |
| `enable_semantic` | `bool` | `True` | 啟用語意壓縮策略 |
| `enable_structural` | `bool` | `True` | 啟用結構壓縮策略 |
| `enable_regex` | `bool` | `True` | 啟用正則壓縮策略 |
| `enable_dedup` | `bool` | `True` | 啟用去重壓縮策略 |
| `enable_template` | `bool` | `True` | 啟用模板壓縮策略 |
| `custom_patterns` | `list` | `[]` | 自訂正則壓縮模式 |
| `sensitive_patterns` | `list` | 預設模式 | 敏感資訊偵測正則模式 |
| `language_hints` | `list` | `[]` | 語言提示資訊 |

```python
from contextforge import ContextCompressor, CompressionConfig, CompressionLevel

config = CompressionConfig(
    level=CompressionLevel.AGGRESSIVE,
    preserve_code_blocks=False,
    max_output_tokens=2000,
    enable_semantic=True,
    enable_structural=True,
    enable_regex=True,
    enable_dedup=True,
    enable_template=True,
)

compressor = ContextCompressor(config=config)
result = compressor.compress(text)
```

---

### 💡 設計思路與迭代規劃

#### 設計理念

1. **零依賴原則** —— 核心功能完全基於 Python 標準函式庫實現，降低安裝複雜度，提升相容性
2. **語意保真** —— 壓縮的核心目標是減少 Token 數量，同時最大程度保留原始文本的語意資訊
3. **可擴展架構** —— 基於策略模式（Strategy Pattern）設計，每種壓縮策略獨立實現，可靈活組合和擴展
4. **自動化優先** —— 自動偵測內容類型、自動選擇最優策略組合，降低使用門檻

#### 技術棧

| 模組 | 技術 | 說明 |
|------|------|------|
| 正則引擎 | `re` | 正則表示式比對與替換 |
| 資料模型 | `dataclasses` | 結構化資料模型定義 |
| 抽象基類 | `abc` | 策略介面抽象定義 |
| 列舉類型 | `enum` | 內容類型、壓縮級別列舉 |
| 時間計量 | `time` | 效能計時統計 |
| JSON 處理 | `json` | JSON 解析與序列化 |
| CLI 框架 | `argparse` | 命令列參數解析 |

#### 迭代規劃

| 版本 | 主題 | 核心功能 |
|------|------|---------|
| **v1.0** | 基礎引擎 | 5 種壓縮策略、11+ 內容類型偵測、CLI + SDK 雙模式 |
| **v1.1** | AI 驅動壓縮 | 整合 LLM 進行語意理解和智慧摘要，進一步提升壓縮品質 |
| **v1.2** | MCP Server | 實作 Model Context Protocol 伺服器，支援 MCP 客戶端直接呼叫 |
| **v1.3** | Web Dashboard | 提供視覺化 Web 管理介面，支援線上壓縮、統計分析和設定管理 |
| **v2.0** | 外掛生態 | 建構外掛系統，支援社群貢獻自訂壓縮策略和內容類型偵測器 |

---

### 📦 打包與部署指南

#### 透過 pip 安裝

```bash
# 從 PyPI 安裝（推薦）
pip install contextforge

# 升級到最新版本
pip install --upgrade contextforge
```

#### 從原始碼建置

```bash
# 複製倉庫
git clone https://github.com/gitstq/ContextForge.git
cd ContextForge

# 安裝建置依賴
pip install setuptools wheel

# 建置 wheel 套件
python -m build

# 安裝建置產物
pip install dist/contextforge-*.whl
```

#### 作為 CLI 工具使用

安裝完成後，`contextforge` 命令將自動註冊到系統 PATH 中：

```bash
# 驗證安裝
contextforge --version

# 直接使用
contextforge compress myfile.log --type log --level aggressive
```

#### 作為 Python 函式庫整合

```python
# 在專案中匯入
from contextforge import ContextCompressor, CompressionLevel, CompressionConfig

# 建立壓縮器實例
compressor = ContextCompressor()

# 壓縮文本
result = compressor.compress(text, level=CompressionLevel.BALANCED)

# 取得統計資訊
print(f"壓縮率: {result.stats.compression_ratio:.1%}")
print(f"原始 Token: {result.stats.original_tokens}")
print(f"壓縮後 Token: {result.stats.compressed_tokens}")
print(f"節省 Token: {result.stats.tokens_saved}")
print(f"處理時間: {result.stats.processing_time_ms:.2f}ms")
print(f"使用策略: {', '.join(result.stats.strategies_used)}")
```

---

### 🤝 貢獻指南

我們歡迎並感謝所有形式的貢獻！在提交貢獻之前，請閱讀以下指南。

#### 提交 Pull Request

1. **Fork** 本倉庫
2. 建立特性分支：`git checkout -b feature/your-feature-name`
3. 提交變更：`git commit -m 'feat: add your feature description'`
4. 推送分支：`git push origin feature/your-feature-name`
5. 提交 **Pull Request**

**PR 規範：**
- 遵循現有程式碼風格（PEP 8）
- 為新功能撰寫對應的單元測試
- 確保所有現有測試通過：`pytest tests/`
- PR 描述中清晰說明變更內容和動機

#### 提交 Issue

- **Bug 回報**：請包含重現步驟、預期行為、實際行為以及執行環境資訊
- **功能建議**：請詳細描述使用場景和期望的行為
- **問題諮詢**：請在 Issue 中提供足夠的上下文資訊

#### 開發環境搭建

```bash
# 複製倉庫
git clone https://github.com/gitstq/ContextForge.git
cd ContextForge

# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
pytest tests/

# 執行測試並產生覆蓋率報告
pytest tests/ --cov=contextforge --cov-report=html
```

---

### 📄 開源協議

本專案基於 [MIT License](LICENSE) 開源。

```
MIT License

Copyright (c) 2024 ContextForge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<!-- ============================================================ -->
<!-- English -->
<!-- ============================================================ -->

<a id="english"></a>

## English

> 🦞 ContextForge is a zero-dependency, cross-platform Python library for intelligently compressing LLM inputs — tool outputs, logs, files, and RAG chunks. Achieves **50-90% token reduction** while preserving semantic integrity.

### 📑 Table of Contents

- [🎉 Project Introduction](#-project-introduction)
- [✨ Core Features](#-core-features-2)
- [🚀 Quick Start](#-quick-start-2)
- [📖 Detailed Usage Guide](#-detailed-usage-guide-2)
  - [Content Type Specification](#content-type-specification)
  - [Compression Level Selection](#compression-level-selection)
  - [File Compression](#file-compression)
  - [Batch Processing](#batch-processing)
  - [Custom Patterns](#custom-patterns)
  - [CLI Commands](#cli-commands)
  - [Configuration Options](#configuration-options)
- [💡 Design Philosophy & Roadmap](#-design-philosophy--roadmap)
- [📦 Packaging & Deployment](#-packaging--deployment)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

### 🎉 Project Introduction

**ContextForge** is a lightweight context intelligent compression engine designed specifically for LLM (Large Language Model) scenarios. It intelligently compresses inputs sent to LLMs, including but not limited to:

- **Tool Outputs**
- **Application Logs**
- **Source Code Files**
- **RAG Chunks**
- **Conversation History**

#### Core Value

| Metric | Description |
|--------|-------------|
| **Token Reduction** | 50% - 90% token count reduction |
| **Semantic Fidelity** | Preserves core semantic information of the original text |
| **Zero Core Dependencies** | Pure Python standard library implementation, no third-party packages needed |
| **Cross-Platform** | Full support for Windows, macOS, Linux |

#### Pain Points Solved

1. **High Token Costs** —— LLM APIs charge per token; verbose logs and tool outputs significantly increase costs
2. **Context Window Limitations** —— Model context windows have fixed sizes; redundant content crowds out useful information
3. **Verbose Tool Outputs** —— Development tools, debuggers, and build systems often produce outputs with large amounts of redundant and useless information
4. **Low RAG Chunk Efficiency** —— Retrieved document fragments may contain substantial content irrelevant to the query

#### Differentiation from Similar Tools

| Feature | ContextForge | Other Tools |
|---------|-------------|-------------|
| Core Dependencies | **Zero dependencies** | Usually require multiple third-party libraries |
| Compression Strategies | **5 strategy combinations** | Typically only 1-2 |
| Content Detection | **Auto-detect 11+ types** | Manual specification required |
| Usage Mode | **Python SDK + CLI dual mode** | Usually only one of the two |
| Extensibility | **Custom regex patterns** | Fixed patterns, hard to extend |

#### Inspiration

This project is inspired by trending GitHub projects focused on LLM context optimization (such as headroom), aiming to provide developers with a lightweight, efficient, and easy-to-use LLM context compression solution that helps reduce token consumption and improve model inference efficiency.

---

### ✨ Core Features

- 🧠 **Smart Content Detection** —— Automatically identifies 11+ content types (logs, JSON, code, Markdown, XML, HTML, CSV, conversations, tool outputs, RAG chunks, etc.) without manual specification
- 📊 **5 Compression Strategies** —— Semantic, Structural, Template, Regex, and Deduplication compression, working together in a multi-strategy pipeline
- ⚡ **Zero Core Dependencies** —— Pure Python implementation using only the standard library (`re`, `json`, `dataclasses`, `abc`, `enum`, `time`), no third-party packages required
- 🎯 **3 Compression Levels** —— Light (30-50%), Balanced (50-70%), Aggressive (70-90%), flexibly adaptable to different scenarios
- 🔒 **Sensitive Information Protection** —— Automatically detects and redacts API keys, passwords, tokens, secrets, and other sensitive information to prevent leaks
- 📈 **Detailed Compression Statistics** —— Provides comprehensive statistics including original/compressed character count, token count, compression ratio, processing time, and strategies used
- 🖥️ **CLI + Python SDK** —— Use from the terminal via command line or integrate as a Python library in your projects
- 🌍 **Cross-Platform Support** —— Works on Windows, macOS, and Linux with no platform restrictions
- 🔄 **Batch Processing** —— Compress multiple texts in a single call for improved efficiency
- 📝 **Extensible Patterns** —— Support for custom regex patterns to meet domain-specific compression needs

---

### 🚀 Quick Start

#### Requirements

- Python 3.9 or higher

#### Installation

```bash
pip install contextforge
```

#### Python SDK Basic Usage

```python
from contextforge import ContextCompressor

compressor = ContextCompressor()
result = compressor.compress("""
[2024-01-15 10:23:45] DEBUG: Starting application...
[2024-01-15 10:23:45] DEBUG: Loading config from /app/config.yaml
[2024-01-15 10:23:46] DEBUG: Connecting to database...
[2024-01-15 10:23:46] INFO: Database connected successfully
[2024-01-15 10:23:47] DEBUG: Running migrations...
[2024-01-15 10:23:48] INFO: Migrations completed
[2024-01-15 10:23:48] DEBUG: Starting HTTP server on port 8080
[2024-01-15 10:23:49] INFO: Server started successfully
""")

print(f"Compression: {result.stats.compression_ratio:.1%}")
print(f"Tokens saved: {result.stats.tokens_saved}")
print(result.compressed_text)
```

#### CLI Basic Usage

```bash
# Compress a log file
contextforge compress app.log --type log --level aggressive

# Read from stdin and compress
cat output.json | contextforge compress - --type json

# Detect content type
contextforge detect myfile.txt

# Estimate token count
contextforge tokens myfile.txt

# Show compression statistics
contextforge compress data.json --stats

# Output as JSON
contextforge compress data.json --json
```

---

### 📖 Detailed Usage Guide

#### Content Type Specification

ContextForge supports automatic detection of 11 content types, or you can specify them manually:

| Type | Value | Description |
|------|-------|-------------|
| Auto-detect | `auto` | Default mode, automatically identifies content type |
| Log | `log` | Application logs, system logs, access logs |
| JSON | `json` | JSON format data |
| Code | `code` | Source code files |
| XML | `xml` | XML format data |
| Markdown | `markdown` | Markdown documents |
| Plain text | `text` | Regular text |
| Tool output | `tool_output` | Tool/command execution output |
| RAG chunks | `rag_chunks` | RAG retrieval result fragments |
| Conversation | `conversation` | Multi-turn conversation records |
| HTML | `html` | HTML web content |
| CSV | `csv` | Comma-separated values data |

```python
from contextforge import ContextCompressor

compressor = ContextCompressor()

# Auto-detect content type
result = compressor.compress(text)

# Manually specify content type
result = compressor.compress(text, content_type="log")
result = compressor.compress(text, content_type="json")
```

#### Compression Level Selection

Three preset compression levels are available for different scenarios:

| Level | Value | Reduction | Use Case |
|-------|-------|-----------|----------|
| Light | `light` | 30-50% | Scenarios requiring maximum detail preservation |
| Balanced | `balanced` | 50-70% | Recommended for most scenarios (default) |
| Aggressive | `aggressive` | 70-90% | Tight token budgets requiring maximum compression |

```python
from contextforge import ContextCompressor, CompressionLevel

# Use preset levels
compressor = ContextCompressor()
result = compressor.compress(text, level="light")
result = compressor.compress(text, level="balanced")
result = compressor.compress(text, level="aggressive")

# Use CompressionLevel enum
result = compressor.compress(text, level=CompressionLevel.AGGRESSIVE)
```

#### File Compression

Supports direct file content compression:

```python
from contextforge import ContextCompressor

compressor = ContextCompressor()

# Compress a single file
result = compressor.compress_file("app.log")
print(f"Compression: {result.stats.compression_ratio:.1%}")
print(result.compressed_text)

# Specify file encoding
result = compressor.compress_file("data.txt", encoding="utf-8")
```

#### Batch Processing

Supports compressing multiple texts in a single call:

```python
from contextforge import ContextCompressor

compressor = ContextCompressor()

texts = [
    open("log1.txt").read(),
    open("log2.txt").read(),
    open("log3.txt").read(),
]

results = compressor.compress_batch(texts)

for i, result in enumerate(results):
    print(f"File {i+1}: {result.stats.compression_ratio:.1%} reduction")
```

#### Custom Patterns

Supports adding custom regex patterns for domain-specific compression needs:

```python
from contextforge import ContextCompressor, CompressionConfig

config = CompressionConfig(
    custom_patterns=[
        {"pattern": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', "replacement": "<IP>"},
        {"pattern": r'order_id=\w+', "replacement": "order_id=<ID>"},
    ]
)

compressor = ContextCompressor(config=config)
result = compressor.compress(text)
```

#### CLI Commands

ContextForge provides three core CLI commands:

**compress** —— Compress text or file content

```bash
# Basic compression
contextforge compress <input_file>

# Specify content type and compression level
contextforge compress <input_file> --type log --level aggressive

# Read from stdin
cat file.txt | contextforge compress -

# Output to file
contextforge compress input.txt -o output.txt

# Show statistics
contextforge compress input.txt --stats

# JSON format output
contextforge compress input.txt --json

# Limit maximum output tokens
contextforge compress input.txt --max-tokens 1000

# Preserve line numbers
contextforge compress input.txt --preserve-lines
```

**detect** —— Detect file content type

```bash
contextforge detect <input_file>
# Example output:
# Content Type: log
# Confidence: 85.0%
```

**tokens** —— Estimate token count

```bash
contextforge tokens <input_file>
# Example output:
# Estimated tokens: 1234
```

#### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `level` | `CompressionLevel` | `balanced` | Compression level: `light` / `balanced` / `aggressive` / `custom` |
| `content_type` | `ContentType` | `auto` | Content type: `auto` / `log` / `json` / `code` etc. |
| `preserve_line_numbers` | `bool` | `False` | Whether to preserve line numbers |
| `preserve_code_blocks` | `bool` | `True` | Whether to preserve code block structure |
| `preserve_json_structure` | `bool` | `True` | Whether to preserve JSON structure |
| `max_output_tokens` | `int` | `None` | Maximum output token count limit |
| `min_compression_ratio` | `float` | `0.1` | Minimum compression ratio threshold |
| `enable_semantic` | `bool` | `True` | Enable semantic compression strategy |
| `enable_structural` | `bool` | `True` | Enable structural compression strategy |
| `enable_regex` | `bool` | `True` | Enable regex compression strategy |
| `enable_dedup` | `bool` | `True` | Enable deduplication compression strategy |
| `enable_template` | `bool` | `True` | Enable template compression strategy |
| `custom_patterns` | `list` | `[]` | Custom regex compression patterns |
| `sensitive_patterns` | `list` | Preset patterns | Sensitive information detection regex patterns |
| `language_hints` | `list` | `[]` | Language hint information |

```python
from contextforge import ContextCompressor, CompressionConfig, CompressionLevel

config = CompressionConfig(
    level=CompressionLevel.AGGRESSIVE,
    preserve_code_blocks=False,
    max_output_tokens=2000,
    enable_semantic=True,
    enable_structural=True,
    enable_regex=True,
    enable_dedup=True,
    enable_template=True,
)

compressor = ContextCompressor(config=config)
result = compressor.compress(text)
```

---

### 💡 Design Philosophy & Roadmap

#### Design Philosophy

1. **Zero Dependencies** —— Core functionality is built entirely on the Python standard library, reducing installation complexity and improving compatibility
2. **Semantic Preservation** —— The core goal of compression is to reduce token count while maximizing preservation of the original text's semantic information
3. **Extensible Architecture** —— Built on the Strategy Pattern, each compression strategy is independently implemented and can be flexibly combined and extended
4. **Automation First** —— Automatic content type detection and optimal strategy selection lower the barrier to entry

#### Tech Stack

| Module | Technology | Description |
|--------|-----------|-------------|
| Regex Engine | `re` | Regex pattern matching and replacement |
| Data Models | `dataclasses` | Structured data model definitions |
| Abstract Base Class | `abc` | Strategy interface abstraction |
| Enum Types | `enum` | Content type and compression level enumerations |
| Time Measurement | `time` | Performance timing statistics |
| JSON Processing | `json` | JSON parsing and serialization |
| CLI Framework | `argparse` | Command-line argument parsing |

#### Roadmap

| Version | Theme | Core Features |
|---------|-------|---------------|
| **v1.0** | Foundation Engine | 5 compression strategies, 11+ content type detection, CLI + SDK dual mode |
| **v1.1** | AI-Powered Compression | Integrate LLM for semantic understanding and intelligent summarization |
| **v1.2** | MCP Server | Implement Model Context Protocol server for direct MCP client invocation |
| **v1.3** | Web Dashboard | Visual web management interface with online compression, analytics, and configuration |
| **v2.0** | Plugin Ecosystem | Build a plugin system for community-contributed compression strategies and detectors |

---

### 📦 Packaging & Deployment

#### Install via pip

```bash
# Install from PyPI (recommended)
pip install contextforge

# Upgrade to latest version
pip install --upgrade contextforge
```

#### Build from Source

```bash
# Clone the repository
git clone https://github.com/gitstq/ContextForge.git
cd ContextForge

# Install build dependencies
pip install setuptools wheel

# Build wheel package
python -m build

# Install the built package
pip install dist/contextforge-*.whl
```

#### Use as a CLI Tool

After installation, the `contextforge` command is automatically registered in your system PATH:

```bash
# Verify installation
contextforge --version

# Direct usage
contextforge compress myfile.log --type log --level aggressive
```

#### Integrate as a Python Library

```python
# Import in your project
from contextforge import ContextCompressor, CompressionLevel, CompressionConfig

# Create compressor instance
compressor = ContextCompressor()

# Compress text
result = compressor.compress(text, level=CompressionLevel.BALANCED)

# Get statistics
print(f"Compression: {result.stats.compression_ratio:.1%}")
print(f"Original tokens: {result.stats.original_tokens}")
print(f"Compressed tokens: {result.stats.compressed_tokens}")
print(f"Tokens saved: {result.stats.tokens_saved}")
print(f"Processing time: {result.stats.processing_time_ms:.2f}ms")
print(f"Strategies used: {', '.join(result.stats.strategies_used)}")
```

---

### 🤝 Contributing

We welcome and appreciate contributions of all forms! Please read the following guidelines before submitting.

#### Submitting a Pull Request

1. **Fork** this repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'feat: add your feature description'`
4. Push the branch: `git push origin feature/your-feature-name`
5. Submit a **Pull Request**

**PR Guidelines:**
- Follow existing code style (PEP 8)
- Write corresponding unit tests for new features
- Ensure all existing tests pass: `pytest tests/`
- Clearly describe the changes and motivation in the PR description

#### Submitting an Issue

- **Bug Reports**: Include reproduction steps, expected behavior, actual behavior, and runtime environment information
- **Feature Requests**: Describe the use case and expected behavior in detail
- **Questions**: Provide sufficient context in the Issue

#### Development Setup

```bash
# Clone the repository
git clone https://github.com/gitstq/ContextForge.git
cd ContextForge

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run tests with coverage report
pytest tests/ --cov=contextforge --cov-report=html
```

---

### 📄 License

This project is licensed under the [MIT License](LICENSE).

```
MIT License

Copyright (c) 2024 ContextForge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**Built with ❤️ by the ContextForge Team**

[**简体中文**](#简体中文) | [**繁體中文**](#繁體中文) | [**English**](#english)

</div>
