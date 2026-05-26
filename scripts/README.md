# 行业分析技能 - 脚本工具

本目录包含行业分析技能的辅助脚本，用于提升分析效率和输出质量。

## 脚本列表

| 脚本 | 功能 | 依赖 |
|------|------|------|
| `keyword_expander.py` | 关键词扩充 | 无 |
| `search_organizer.py` | 搜索结果整理 | 无 |
| `mermaid_generator.py` | Mermaid图表生成 | 无（ASCII模式需ascii_charts.py） |
| `ascii_charts.py` | ASCII图表生成（兼容性强） | 无 |
| `report_generator.py` | 分析报告生成 | 无 |
| `ppt_prompter.py` | PPT提示词生成 | 无 |
| `quick_card_generator.py` | 行业速查卡生成 | 无 |
| `competitor_matrix.py` | 竞品分析矩阵生成 | 无 |

所有脚本使用Python 3.7+，无需额外依赖。

---

## 1. keyword_expander.py - 关键词扩充

根据行业名称自动生成多维度搜索关键词。

### 用法

```bash
# 输出Markdown格式
python keyword_expander.py "新能源汽车"

# 输出JSON格式
python keyword_expander.py "GUI Agent" --json
```

### 输出示例

```
# 新能源汽车行业分析 - 搜索关键词

## 推荐搜索查询（按优先级排序）

1. `新能源汽车 行业概况 2024`
2. `新能源汽车 行业定义 分类`
3. `新能源汽车 市场规模 2024`
...
```

### 扩充维度

- 行业概况
- 市场规模
- 产业链
- 竞争格局
- 政策法规
- 技术趋势
- 商业模式
- 痛点挑战
- 投融资
- 消费趋势

---

## 2. search_organizer.py - 搜索结果整理

对联网搜索获取的信息进行自动分类和整理。

### 用法

```bash
# 输出摘要
python search_organizer.py "新能源汽车" summary

# 导出分析数据JSON
python search_organizer.py "新能源汽车" export

# 输出Markdown格式
python search_organizer.py "新能源汽车" markdown
```

### 分类维度

- 行业概况
- 市场数据
- 产业链
- 竞争格局
- 政策法规
- 技术趋势
- 商业模式
- 痛点挑战
- 投融资
- 消费趋势

---

## 3. mermaid_generator.py - Mermaid图表生成

根据分析数据生成各类Mermaid图表代码。

### 用法

```bash
# 生成产业链图
python mermaid_generator.py chain '{"upstream":["供应商A","供应商B"],"midstream":["核心企业"],"downstream":["客户A","客户B"]}'

# 生成PEST思维导图
python mermaid_generator.py pest '{"political":["政策1","政策2"],"economic":["经济1"],"social":["社会1"],"technological":["技术1"]}'

# 生成BCG矩阵
python mermaid_generator.py bcg '{"companies":[{"name":"企业A","market_share":0.7,"growth_rate":0.8},{"name":"企业B","market_share":0.3,"growth_rate":0.6}]}'

# 生成SWOT思维导图
python mermaid_generator.py swot '{"strengths":["优势1"],"weaknesses":["劣势1"],"opportunities":["机会1"],"threats":["威胁1"]}'

# 生成市场份额饼图
python mermaid_generator.py pie '{"companies":[{"name":"企业A","share":35},{"name":"企业B","share":25},{"name":"其他","share":40}]}'

# 生成增长趋势图
python mermaid_generator.py trend '{"years":["2020","2021","2022","2023","2024"],"values":[100,150,200,280,350]}'

# 生成波特五力分析
python mermaid_generator.py porter '{"rivalry":"高","new_entrants":"中","substitutes":"低","supplier_power":"中","buyer_power":"高"}'
```

### 支持的图表类型

| 类型 | 说明 | Mermaid图表类型 |
|------|------|-----------------|
| chain | 产业链图 | flowchart |
| pest | PEST分析 | mindmap |
| bcg | BCG矩阵 | quadrantChart |
| swot | SWOT分析 | mindmap |
| pie | 市场份额饼图 | pie |
| cost_pie | 成本结构饼图 | pie |
| trend | 增长趋势（柱状+折线） | xychart-beta |
| bar | 柱状图 | xychart-beta |
| line | 折线图 | xychart-beta |
| multi_line | 多系列折线图 | xychart-beta |
| porter | 波特五力 | flowchart |
| timeline | 时间线图 | timeline |
| quadrant | 竞争定位象限图 | quadrantChart |
| journey | 用户旅程图 | flowchart |
| gantt | 甘特图 | gantt |

### 新增图表示例

```bash
# 生成柱状图
python mermaid_generator.py bar '{"labels":["Q1","Q2","Q3","Q4"],"values":[100,150,200,250],"title":"季度营收(亿元)"}'

# 生成折线图
python mermaid_generator.py line '{"labels":["1月","2月","3月","4月","5月","6月"],"values":[100,120,150,180,220,260],"title":"用户增长趋势"}'

# 生成多系列折线图
python mermaid_generator.py multi_line '{"labels":["2020","2021","2022","2023"],"series":[{"name":"企业A","values":[100,150,200,250]},{"name":"企业B","values":[80,120,180,240]}]}'

# 生成时间线图
python mermaid_generator.py timeline '{"events":[{"year":"2020","event":"产品发布"},{"year":"2022","event":"市场扩张"},{"year":"2024","event":"行业领先"}],"title":"发展历程"}'

# 生成成本结构饼图
python mermaid_generator.py cost_pie '{"items":[{"name":"原材料","percent":45},{"name":"人工成本","percent":25},{"name":"研发投入","percent":15},{"name":"其他","percent":15}]}'

# 生成竞争定位象限图
python mermaid_generator.py quadrant '{"companies":[{"name":"品牌A","x":0.8,"y":0.85},{"name":"品牌B","x":0.3,"y":0.7}],"title":"竞争定位分析"}'

# 生成用户旅程图
python mermaid_generator.py journey '{"stages":[{"name":"认知","action":"广告触达"},{"name":"兴趣","action":"内容种草"},{"name":"购买","action":"下单"}]}'

# 生成甘特图
python mermaid_generator.py gantt '{"tasks":[{"section":"第一阶段","name":"需求分析","start":"2024","end":"2025"},{"section":"第二阶段","name":"开发测试","start":"2025","end":"2026"}]}'
```

### ASCII模式（解决Mermaid兼容性问题）

当目标平台不支持Mermaid渲染时，可以使用 `--ascii` 选项生成ASCII图表：

```bash
# ASCII产业链图
python mermaid_generator.py --ascii chain '{"upstream":["供应商A"],"midstream":["核心企业"],"downstream":["客户A"]}'

# ASCII PEST分析
python mermaid_generator.py --ascii pest '{"political":["政策1"],"economic":["经济1"],"social":["社会1"],"technological":["技术1"]}'

# ASCII BCG矩阵
python mermaid_generator.py --ascii bcg '{"stars":["比亚迪"],"cash_cows":["特斯拉"],"question_marks":["蔚来"],"dogs":["其他"]}'

# ASCII SWOT分析
python mermaid_generator.py --ascii swot '{"strengths":["优势1"],"weaknesses":["劣势1"],"opportunities":["机会1"],"threats":["威胁1"]}'

# ASCII饼图/占比图
python mermaid_generator.py --ascii pie '{"companies":[{"name":"企业A","share":35},{"name":"企业B","share":25}]}'
```

---

## 3.5 ascii_charts.py - ASCII图表生成

生成跨平台兼容的ASCII艺术图表，适用于不支持Mermaid的环境。

### 用法

```bash
# 柱状图
python ascii_charts.py bar '{"data":[{"label":"Q1","value":100},{"label":"Q2","value":150}],"title":"季度营收"}'

# 占比图（饼图替代）
python ascii_charts.py pie '{"data":[{"label":"企业A","value":35},{"label":"企业B","value":25}],"title":"市场份额"}'

# SWOT矩阵
python ascii_charts.py swot '{"strengths":["优势1","优势2"],"weaknesses":["劣势1"],"opportunities":["机会1"],"threats":["威胁1"]}'

# BCG矩阵
python ascii_charts.py bcg '{"stars":["比亚迪"],"cash_cows":["特斯拉"],"question_marks":["蔚来"],"dogs":["其他"]}'

# PEST分析
python ascii_charts.py pest '{"political":["政策1"],"economic":["经济1"],"social":["社会1"],"technological":["技术1"]}'

# 产业链图
python ascii_charts.py chain '{"upstream":["供应商A"],"midstream":["制造商"],"downstream":["客户A"]}'

# 流程图（水平）
python ascii_charts.py flow '{"stages":["需求分析","方案设计","开发实施","测试上线"]}'

# 对比表格
python ascii_charts.py table '{"headers":["指标","企业A","企业B"],"rows":[["市场份额","35%","25%"],["增长率","45%","30%"]]}'

# 评分卡
python ascii_charts.py score '{"items":[{"name":"产品力","score":5},{"name":"品牌力","score":4}],"title":"能力评估"}'
```

### 支持的图表类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| bar | 柱状图 | 数据对比、趋势展示 |
| pie | 占比图（饼图替代） | 市场份额、成本结构 |
| trend | 趋势图 | 时间序列数据 |
| quadrant | 四象限图 | BCG矩阵、定位分析 |
| flow | 水平流程图 | 简单流程展示 |
| vflow | 垂直流程图 | 复杂流程展示 |
| table | 对比表格 | 多维度对比 |
| swot | SWOT矩阵 | SWOT分析 |
| bcg | BCG矩阵 | BCG分析 |
| pest | PEST分析图 | PEST分析 |
| chain | 产业链图 | 产业链分析 |
| score | 评分卡 | 能力评估 |

### 输出示例

**柱状图：**
```
  季度营收对比
  ────────────────────────────────────────────────────────
  Q1     │████████████████████░░░░░░░░░░░░░░░░░░░░│ 100
  Q2     │██████████████████████████████░░░░░░░░░░│ 150
  Q3     │████████████████████████████████████░░░░│ 180
  Q4     │████████████████████████████████████████│ 200
  ────────────────────────────────────────────────────────
```

**SWOT矩阵：**
```
  ┌───────────────────────────────────┬───────────────────────────────────┐
  │      ✅ Strengths 优势             │      ❌ Weaknesses 劣势            │
  ├───────────────────────────────────┼───────────────────────────────────┤
  │• 产业链完整                        │• 品牌溢价能力不足                   │
  │• 市场规模全球第一                   │• 核心芯片依赖进口                   │
  ├───────────────────────────────────┼───────────────────────────────────┤
  │      🎯 Opportunities 机会         │      ⚠️ Threats 威胁               │
  ├───────────────────────────────────┼───────────────────────────────────┤
  │• 海外市场拓展空间大                 │• 欧美贸易壁垒加剧                   │
  └───────────────────────────────────┴───────────────────────────────────┘
```

---

## 4. report_generator.py - 分析报告生成

根据收集的数据生成结构化的行业分析报告。

### 用法

```bash
# 生成模板报告
python report_generator.py "新能源汽车"

# 使用数据文件生成报告
python report_generator.py "新能源汽车" data.json
```

### 数据文件格式

```json
{
  "period": "2024-2025年",
  "overview": {
    "definition": "行业定义...",
    "global_market_size": "1000亿美元",
    "china_market_size": "5000亿元",
    "growth_rate": "25%"
  },
  "pest": {
    "political": "政策分析...",
    "economic": "经济分析..."
  },
  "bcg": {
    "stars": "明星企业...",
    "cash_cows": "现金牛企业..."
  },
  "swot": {
    "strengths": ["优势1", "优势2"],
    "weaknesses": ["劣势1", "劣势2"],
    "opportunities": ["机会1", "机会2"],
    "threats": ["威胁1", "威胁2"]
  },
  "conclusion": {
    "insights": ["洞察1", "洞察2"],
    "short_term": ["短期建议1"],
    "mid_term": ["中期建议1"],
    "long_term": ["长期建议1"]
  }
}
```

### 报告结构

1. 封面
2. 目录
3. 行业概览
4. PEST环境分析
5. BCG矩阵分析
6. SWOT战略分析
7. 总结与建议
8. 附录

---

## 5. ppt_prompter.py - PPT提示词生成

根据分析数据生成用于GenerateImage工具的PPT页面提示词。

### 用法

```bash
# 生成每页PPT提示词
python ppt_prompter.py "新能源汽车"

# 使用数据文件生成
python ppt_prompter.py "新能源汽车" data.json

# 输出PPT JSON配置
python ppt_prompter.py "新能源汽车" data.json --json
```

### PPT页面结构

| 页码 | 内容 | 文件名 |
|------|------|--------|
| 1 | 封面页 | ppt-page-1-cover.png |
| 2 | 行业概览 | ppt-page-2-overview.png |
| 3 | 市场规模与增长 | ppt-page-3-market.png |
| 4 | 产业链分析 | ppt-page-4-chain.png |
| 5 | PEST分析 | ppt-page-5-pest.png |
| 6 | BCG矩阵 | ppt-page-6-bcg.png |
| 7 | SWOT分析 | ppt-page-7-swot.png |
| 8 | 关键洞察与建议 | ppt-page-8-insights.png |
| 9 | 结尾页 | ppt-page-9-ending.png |

### 数据文件格式

与report_generator.py相同，额外支持以下字段：

```json
{
  "subtitle": "2024年度分析",
  "author": "行业研究团队",
  "insights": {
    "key_insights": [
      {"title": "洞察一", "content": "关键发现1"},
      {"title": "洞察二", "content": "关键发现2"}
    ],
    "short_term": "短期建议",
    "mid_term": "中期建议",
    "long_term": "长期建议"
  }
}
```

---

## 工作流示例

完整的行业分析工作流：

```bash
# 1. 生成搜索关键词
python keyword_expander.py "新能源汽车" > keywords.md

# 2. 执行联网搜索（使用WebSearch工具）
# ...

# 3. 整理搜索结果
python search_organizer.py "新能源汽车" export > data.json

# 4. 生成Mermaid图表
python mermaid_generator.py chain '{"upstream":["电池","电机"],"midstream":["整车制造"],"downstream":["消费者"]}' > chain.md

# 5. 生成分析报告
python report_generator.py "新能源汽车" data.json > report.md

# 6. 生成PPT提示词
python ppt_prompter.py "新能源汽车" data.json > ppt_prompts.md

# 7. 使用GenerateImage工具生成PPT图片
# ...
```

---

## 6. quick_card_generator.py - 行业速查卡生成

生成1页精华的行业速查卡，适合快速了解一个行业。

### 用法

```bash
# ASCII格式（终端显示）
python quick_card_generator.py "新能源汽车"

# Markdown格式
python quick_card_generator.py "新能源汽车" --format=markdown

# JSON格式
python quick_card_generator.py "新能源汽车" --format=json

# 使用数据文件
python quick_card_generator.py "新能源汽车" data.json --format=markdown
```

### 输出格式

| 格式 | 说明 |
|------|------|
| ascii | ASCII艺术卡片，适合终端显示（默认） |
| markdown | Markdown格式，适合文档 |
| json | JSON数据格式，适合程序处理 |

### 数据JSON格式

```json
{
  "overview": {
    "china_market_size": "3.2万亿元",
    "growth_rate": "35%",
    "stage": "快速成长期",
    "penetration": "38%",
    "summary": "中国新能源汽车市场全球领先"
  },
  "competition": {
    "top_players": [
      {"name": "比亚迪", "share": "35%"},
      {"name": "特斯拉", "share": "18%"},
      {"name": "理想", "share": "12%"}
    ]
  },
  "trends": {
    "drivers": ["政策补贴", "电池降本", "消费升级"],
    "risks": ["补贴退坡", "产能过剩", "原材料波动"],
    "judgment": "看多",
    "advice": "关注智能化+出海赛道"
  }
}
```

---

## 7. competitor_matrix.py - 竞品分析矩阵生成

生成竞品对比表格、定位分析、差异化洞察。

### 用法

```bash
# 生成完整竞品分析报告
python competitor_matrix.py "新能源汽车" competitors.json

# 仅生成对比表格
python competitor_matrix.py "新能源汽车" competitors.json --output=table

# 仅生成定位分析
python competitor_matrix.py "新能源汽车" competitors.json --output=positioning

# 仅生成SWOT对比
python competitor_matrix.py "新能源汽车" competitors.json --output=swot
```

### 输出类型

| 类型 | 说明 |
|------|------|
| full | 完整竞品分析报告（默认） |
| table | 仅对比表格 |
| positioning | 仅定位分析 |
| swot | 仅SWOT对比 |

### 评分维度

| 维度 | 说明 |
|------|------|
| 产品力 | 功能完整性、用户体验、创新性 |
| 技术实力 | 核心技术、研发投入、专利储备 |
| 品牌影响力 | 知名度、美誉度、忠诚度 |
| 渠道能力 | 销售网络、获客能力 |
| 价格竞争力 | 定价策略、性价比 |
| 服务质量 | 客户服务、响应速度 |
| 市场份额 | 当前市场占有率 |
| 增长势头 | 增长速度、发展潜力 |

### 数据JSON格式

```json
{
  "competitors": [
    {
      "name": "比亚迪",
      "info": {
        "founded": "1995年",
        "funding": "上市",
        "valuation": "7000亿",
        "employees": "60万+",
        "core_business": "新能源汽车、电池"
      },
      "product": {
        "main_product": "王朝系列、海洋系列",
        "price_range": "10-50万",
        "target_customer": "大众消费者",
        "usp": "垂直整合、性价比"
      },
      "scores": {
        "产品力": 5,
        "技术实力": 5,
        "品牌影响力": 4,
        "渠道能力": 5,
        "价格竞争力": 5,
        "服务质量": 4,
        "市场份额": 5,
        "增长势头": 5
      },
      "positioning": {"price": 0.4, "quality": 0.8},
      "swot": {
        "strengths": ["垂直整合", "成本优势"],
        "weaknesses": ["品牌高端化不足"],
        "opportunities": ["海外市场"],
        "threats": ["价格战"]
      },
      "differentiation": {
        "strategy": "成本领先",
        "core_advantage": "电池自研",
        "target_market": "大众市场"
      },
      "counter_strategy": {
        "key_point": "规模优势难以复制",
        "response": "聚焦细分市场",
        "caution": "避免价格战"
      }
    }
  ]
}
```

---

## 8. data_extractor.py - 数据增强模块

从用户上传的文本/报告中提取关键数据点，并进行校验和来源追踪。

### 用法

```bash
# 从文本文件提取数据
python data_extractor.py extract report.txt

# 输出JSON格式
python data_extractor.py extract report.txt json

# 输出可用于分析框架的格式
python data_extractor.py extract report.txt analysis

# 校验提取的数据
python data_extractor.py validate extracted_data.json

# 生成来源追踪报告
python data_extractor.py track sources.json

# 生成引用格式
python data_extractor.py track sources.json citations
```

### 支持提取的数据类型

| 类型 | 说明 | 示例 |
|------|------|------|
| market_size | 市场规模 | "市场规模达到1000亿元" |
| growth_rate | 增长率 | "年增长率25%" |
| penetration_rate | 渗透率 | "渗透率达到35%" |
| market_share | 市场份额 | "市场份额占35%" |
| user_count | 用户规模 | "用户数达到5亿" |
| revenue | 营收 | "营收500亿元" |
| investment | 投融资 | "融资10亿美元" |

### 来源JSON格式

```json
[
  {
    "name": "中国汽车工业协会2024年报",
    "type": "official",
    "reliability": "high",
    "data_points": ["market_size", "growth_rate"]
  }
]
```

---

## 9. report_customizer.py - 报告定制化模块

支持报告裁剪、风格转换、摘要生成、洞察提取。

### 用法

```bash
# 查看所有配置选项
python report_customizer.py config

# 生成精简版报告
python report_customizer.py trim brief full_report.md

# 自定义模块组合
python report_customizer.py trim pest,swot full_report.md

# 获取风格写作指南
python report_customizer.py style formal
python report_customizer.py style concise
python report_customizer.py style data_driven

# 生成执行摘要模板
python report_customizer.py summary

# 使用数据生成摘要
python report_customizer.py summary data.json "新能源汽车"

# 提取核心洞察
python report_customizer.py insights report.md
```

### 报告类型

| 类型代码 | 名称 | 包含模块 |
|----------|------|----------|
| full | 完整版 | 全部6个模块 |
| brief | 精简版 | 概览+SWOT+竞争 |
| executive | 汇报版 | 概览+SWOT |
| pest_only | PEST专题 | 概览+PEST |
| swot_only | SWOT专题 | 概览+SWOT |
| competition_only | 竞争专题 | 概览+竞争+BCG |

### 输出风格

| 风格代码 | 名称 | 特点 |
|----------|------|------|
| formal | 正式风格 | 专业、严谨、客观 |
| concise | 简洁风格 | 直接、清晰、高效 |
| data_driven | 数据驱动 | 量化、精确、证据导向 |

---

## 10. trend_analyzer.py - 趋势洞察模块

提供Hype Cycle、趋势预测、时机矩阵、风险预警功能。

### 用法

```bash
# 获取Hype Cycle阶段判断模板
python trend_analyzer.py hype

# 使用技术数据生成分析
python trend_analyzer.py hype techs.json

# 生成趋势预测模板
python trend_analyzer.py predict "新能源汽车"

# 获取时机评估模板
python trend_analyzer.py timing "新能源汽车"

# 使用评估数据生成报告
python trend_analyzer.py timing "新能源汽车" assessment.json

# 获取风险评估模板
python trend_analyzer.py risk "新能源汽车"

# 使用风险数据生成报告
python trend_analyzer.py risk "新能源汽车" risks.json
```

### Hype Cycle阶段

| 阶段代码 | 名称 | 说明 |
|----------|------|------|
| trigger | 技术萌芽期 | 概念验证、早期投资 |
| peak | 期望膨胀期 | 媒体热炒、泡沫形成 |
| trough | 泡沫破裂期 | 投资减少、企业退出 |
| slope | 稳步爬升期 | 商业化加速 |
| plateau | 生产成熟期 | 规模化应用 |

### 技术数据JSON格式

```json
[
  {
    "name": "固态电池",
    "phase": "slope",
    "description": "技术逐渐成熟，商业化加速"
  }
]
```

### 时机评估JSON格式

```json
{
  "market_maturity": "growth",
  "competition": "high",
  "technology_readiness": "commercial",
  "resource_requirement": "high"
}
```

### 风险数据JSON格式

```json
[
  {
    "type": "policy",
    "description": "补贴政策退坡",
    "level": "high",
    "mitigation": "提前布局成本优化"
  }
]
```

---

## 注意事项

1. 所有脚本使用UTF-8编码
2. JSON参数可以使用文件路径代替直接传参
3. 输出可直接重定向到文件
4. 脚本设计为无状态，可重复执行
5. Windows PowerShell中建议使用JSON文件而非命令行JSON字符串
