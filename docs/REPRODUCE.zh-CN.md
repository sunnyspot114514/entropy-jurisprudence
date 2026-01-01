# 复现指南

[🇺🇸 English](REPRODUCE.md) | [🇨🇳 中文说明](REPRODUCE.zh-CN.md)

本文档提供复现本仓库实验的详细说明。

## 环境要求

| 要求 | 版本 |
|------|------|
| Python | 3.9+ |
| Ollama | 最新版 |
| 操作系统 | Windows / Linux / macOS |

## 依赖安装

```bash
pip install -r requirements.txt
```

所需包：
- `requests` - API 通信
- `numpy` - 数值计算
- `pandas` - 数据分析
- `scipy` - 统计指标
- `tabulate` - Markdown 表格生成

## 模型下载

通过 Ollama 下载以下模型：

```bash
ollama pull deepseek-r1:8b
ollama pull qwen3:8b
ollama pull gemma3:4b
ollama pull llama3:8b
ollama pull mistral:7b
ollama pull phi3:3.8b
```

运行实验前确保 Ollama 正在运行：

```bash
ollama serve
```

## 运行实验

### 步骤 1：执行实验

```bash
python src/run_experiment.py
```

这将：
- 每个模型每个案例执行 10 次试验（可配置）
- 将结果保存到 `data/experiment_data.json`
- 在终端显示进度

**预计运行时间：** 约 30-60 分钟（取决于硬件）

### 步骤 2：分析结果

```bash
python src/analyze_results.py
```

这将：
- 计算判决稳定性、逻辑稳定性、RI 指标
- 检测 R 值幻觉
- 输出 `data/analysis_results.csv`

## 提示词位置

形式化规则提示词定义在：

```
src/run_experiment.py → SYSTEM_PROMPT 变量（约第 50 行）
```

关键提示词组件：
- `E = H × R` 公式定义
- R 值量表（0.1 / 1.0 / 2.0）
- 输出格式规范（`MATH:` 块）

## 自定义配置

### 添加新测试案例

编辑 `src/run_experiment.py` 中的 `CASES` 字典：

```python
CASES = {
    "Your_Case_Name": "道德困境描述...",
}
```

### 修改试验次数

修改 `src/run_experiment.py` 中的 `TRIALS_PER_CASE`：

```python
TRIALS_PER_CASE = 10  # 默认值
```

### 添加新模型

将模型名称添加到 `src/run_experiment.py` 的 `MODELS` 列表：

```python
MODELS = ["deepseek-r1:8b", "qwen3:8b", "gemma3:4b", "your-model:tag"]
```

注意：不同模型可能需要不同的 API 策略（chat vs generate 端点）。

## 预期输出

成功复现后，您应该得到：

| 文件 | 描述 |
|------|------|
| `data/experiment_data.json` | 包含 CoT 推理的原始试验数据 |
| `data/analysis_results.csv` | 聚合指标表 |

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| Ollama 连接被拒绝 | 先运行 `ollama serve` |
| 模型未找到 | 运行 `ollama pull <model>` |
| JSON 解析错误 | 检查模型输出格式合规性 |
| R 值幻觉 | 预期行为，已在指标中捕获 |

## 硬件参考

实验在以下配置上进行：
- GPU：NVIDIA RTX 系列（建议 8GB+ 显存）
- 内存：16GB+
- 存储：模型需要 10GB 可用空间

纯 CPU 执行可行但显著较慢。
