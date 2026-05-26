# 数据增强模块使用指南

本文档说明如何使用数据增强模块提升报告的数据密度和可信度。

## 一、模块概览

| 功能 | 脚本 | 说明 |
|------|------|------|
| 数据提取 | `data_extractor.py extract` | 从文本中提取关键数据点 |
| 数据校验 | `data_extractor.py validate` | 检查数据合理性 |
| 来源追踪 | `data_extractor.py track` | 管理和标注数据来源 |

## 二、数据提取器

### 2.1 支持提取的数据类型

| 数据类型 | 说明 | 示例模式 |
|----------|------|----------|
| market_size | 市场规模 | "市场规模达到1000亿元" |
| growth_rate | 增长率 | "年增长率25%" |
| penetration_rate | 渗透率 | "渗透率达到35%" |
| market_share | 市场份额 | "市场份额占35%" |
| user_count | 用户规模 | "用户数达到5亿" |
| revenue | 营收 | "营收500亿元" |
| profit | 利润 | "净利润50亿元" |
| investment | 投融资 | "融资10亿美元" |
| company_count | 企业数量 | "企业数量超过1000家" |

### 2.2 使用方法

```bash
# 从文本文件提取数据
python data_extractor.py extract report.txt

# 输出JSON格式
python data_extractor.py extract report.txt json

# 输出可用于分析框架的格式
python data_extractor.py extract report.txt analysis
```

### 2.3 输出示例

```markdown
# 数据提取报告

- **数据来源**: industry_report.pdf
- **提取时间**: 2025-01-15 10:30

## 提取的关键数据

### 市场规模

| 数值 | 单位 | 上下文 |
|------|------|--------|
| 8000 | 亿元 | ...2024年新能源汽车市场规模达到8000亿元... |

### 增长率

| 数值 | 单位 | 上下文 |
|------|------|--------|
| 35 | % | ...同比增长35%，保持高速发展态势... |
```

## 三、数据校验器

### 3.1 校验规则

| 数据类型 | 合理范围 | 警告范围 |
|----------|----------|----------|
| 增长率 | -50% ~ 200% | -20% ~ 100% |
| 渗透率 | 0% ~ 100% | 0% ~ 100% |
| 市场份额 | 0% ~ 100% | 0% ~ 100% |
| 市场规模 | 0 ~ 100万亿 | 0.1亿 ~ 10万亿 |

### 3.2 使用方法

```bash
# 校验提取的数据
python data_extractor.py validate extracted_data.json

# 输出JSON格式
python data_extractor.py validate extracted_data.json json
```

### 3.3 校验结果示例

```markdown
# 数据校验报告

**校验结果**: ⚠️ 数据基本合理，2项需要关注

## ❌ 异常数据

- 增长率 250 超出合理范围 [-50, 200]

## ⚠️ 需要关注

- 增长率 120 可能需要核实（通常范围 [-20, 100]）

## ✅ 校验通过

- 市场规模 8000 在合理范围内
- 渗透率 35 在合理范围内
```

## 四、来源追踪器

### 4.1 来源类型

| 类型代码 | 说明 | 可信度建议 |
|----------|------|------------|
| official | 官方数据（政府、企业财报） | high |
| research | 研究报告（券商、咨询机构） | high/medium |
| report | 行业报告 | medium |
| news | 新闻资讯 | medium/low |

### 4.2 使用方法

```bash
# 生成来源追踪报告
python data_extractor.py track sources.json

# 生成引用格式
python data_extractor.py track sources.json citations
```

### 4.3 来源JSON格式

```json
[
  {
    "name": "中国汽车工业协会2024年报",
    "type": "official",
    "reliability": "high",
    "data_points": ["market_size", "growth_rate"]
  },
  {
    "name": "艾瑞咨询新能源汽车报告",
    "type": "research",
    "reliability": "medium",
    "data_points": ["penetration_rate", "market_share"]
  }
]
```

### 4.4 输出示例

```markdown
# 数据来源追踪

**总来源数**: 5

## 来源类型分布

- 官方数据: 2个
- 研究报告: 2个
- 新闻资讯: 1个

## 可信度分布

- 🟢 high: 2个
- 🟡 medium: 2个
- 🔴 low: 1个

## 来源详情

| 来源名称 | 类型 | 可信度 | 数据点数 |
|----------|------|--------|----------|
| 中国汽车工业协会2024年报 | 官方数据 | high | 2 |
| 艾瑞咨询新能源汽车报告 | 研究报告 | medium | 2 |
```

## 五、工作流程

### 5.1 标准数据增强流程

```
用户上传文本/报告
       ↓
  数据提取器提取关键数据
       ↓
  数据校验器检查合理性
       ↓
  修正异常数据（人工确认）
       ↓
  来源追踪器记录来源
       ↓
  数据填充到分析框架
       ↓
  生成带来源标注的报告
```

### 5.2 与报告生成集成

提取的数据可直接用于报告生成：

```bash
# 1. 提取数据
python data_extractor.py extract report.txt analysis > extracted.json

# 2. 校验数据
python data_extractor.py validate extracted.json

# 3. 生成报告（使用提取的数据）
python report_generator.py "新能源汽车" extracted.json
```

## 六、最佳实践

### 6.1 数据质量保障

1. **多源交叉验证**: 同一数据点尽量从多个来源获取
2. **时效性检查**: 优先使用最近1-2年的数据
3. **来源可信度**: 官方数据 > 研究报告 > 新闻资讯
4. **异常值复核**: 校验器标记的异常值需人工确认

### 6.2 来源标注规范

```markdown
## 市场规模

2024年中国新能源汽车市场规模达到**8000亿元**[1]，同比增长**35%**[2]。

---
**数据来源**:
[1] 中国汽车工业协会2024年报 (★★★)
[2] 艾瑞咨询新能源汽车行业报告 (★★☆)
```
