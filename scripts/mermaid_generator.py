#!/usr/bin/env python3
"""
Mermaid图表生成脚本
根据分析数据生成各类Mermaid图表代码
支持Mermaid和ASCII两种输出格式
"""

import json
import sys
from typing import List, Dict, Any

# 导入ASCII图表生成器（可选）
try:
    from ascii_charts import ASCIICharts
    ASCII_AVAILABLE = True
except ImportError:
    ASCII_AVAILABLE = False


def generate_industry_chain(
    upstream: List[str],
    midstream: List[str],
    downstream: List[str],
    industry_name: str = "行业"
) -> str:
    """
    生成产业链流程图
    
    Args:
        upstream: 上游供应商列表
        midstream: 中游核心企业/业务列表
        downstream: 下游客户列表
        industry_name: 行业名称
        
    Returns:
        Mermaid flowchart代码
    """
    code = f"""```mermaid
%%{{init: {{'theme': 'base', 'themeVariables': {{ 'primaryColor': '#4A90D9'}}}}}}%%
flowchart TB
    subgraph 上游["上游供应商"]
"""
    
    for i, item in enumerate(upstream):
        code += f"        A{i+1}[{item}]\n"
    
    code += """    end
    
    subgraph 中游["{}核心"]
""".format(industry_name)
    
    for i, item in enumerate(midstream):
        code += f"        B{i+1}[{item}]\n"
    
    code += """    end
    
    subgraph 下游["下游客户"]
"""
    
    for i, item in enumerate(downstream):
        code += f"        C{i+1}[{item}]\n"
    
    code += "    end\n\n"
    
    # 添加连接线
    for i in range(len(upstream)):
        for j in range(len(midstream)):
            code += f"    A{i+1} --> B{j+1}\n"
    
    for i in range(len(midstream)):
        for j in range(len(downstream)):
            code += f"    B{i+1} --> C{j+1}\n"
    
    code += "```"
    return code


def generate_pest_mindmap(
    political: List[str],
    economic: List[str],
    social: List[str],
    technological: List[str]
) -> str:
    """
    生成PEST分析思维导图
    
    Args:
        political: 政治法规要点
        economic: 经济环境要点
        social: 社会文化要点
        technological: 技术环境要点
        
    Returns:
        Mermaid mindmap代码
    """
    code = """```mermaid
mindmap
  root((PEST分析))
    Political
"""
    for item in political:
        code += f"      {item}\n"
    
    code += "    Economic\n"
    for item in economic:
        code += f"      {item}\n"
    
    code += "    Social\n"
    for item in social:
        code += f"      {item}\n"
    
    code += "    Technological\n"
    for item in technological:
        code += f"      {item}\n"
    
    code += "```"
    return code


def generate_bcg_matrix(
    companies: List[Dict[str, Any]]
) -> str:
    """
    生成BCG矩阵图
    
    Args:
        companies: 公司列表，每个包含 name, market_share (0-1), growth_rate (0-1)
        
    Returns:
        Mermaid quadrantChart代码
    """
    code = """```mermaid
quadrantChart
    title BCG矩阵分析
    x-axis 低市场份额 --> 高市场份额
    y-axis 低增长率 --> 高增长率
    quadrant-1 明星业务
    quadrant-2 问题业务
    quadrant-3 瘦狗业务
    quadrant-4 现金牛业务
"""
    
    for company in companies:
        name = company.get("name", "企业")
        share = company.get("market_share", 0.5)
        growth = company.get("growth_rate", 0.5)
        code += f"    {name}: [{share}, {growth}]\n"
    
    code += "```"
    return code


def generate_swot_quadrant(
    strengths: List[str],
    weaknesses: List[str],
    opportunities: List[str],
    threats: List[str]
) -> str:
    """
    生成SWOT分析思维导图
    
    Args:
        strengths: 优势列表
        weaknesses: 劣势列表
        opportunities: 机会列表
        threats: 威胁列表
        
    Returns:
        Mermaid mindmap代码
    """
    code = """```mermaid
mindmap
  root((SWOT分析))
    Strengths 优势
"""
    for item in strengths:
        code += f"      {item}\n"
    
    code += "    Weaknesses 劣势\n"
    for item in weaknesses:
        code += f"      {item}\n"
    
    code += "    Opportunities 机会\n"
    for item in opportunities:
        code += f"      {item}\n"
    
    code += "    Threats 威胁\n"
    for item in threats:
        code += f"      {item}\n"
    
    code += "```"
    return code


def generate_market_share_pie(
    companies: List[Dict[str, Any]],
    title: str = "市场份额分布"
) -> str:
    """
    生成市场份额饼图
    
    Args:
        companies: 公司列表，每个包含 name 和 share
        title: 图表标题
        
    Returns:
        Mermaid pie代码
    """
    code = f"""```mermaid
pie title {title}
"""
    for company in companies:
        name = company.get("name", "企业")
        share = company.get("share", 10)
        code += f'    "{name}" : {share}\n'
    
    code += "```"
    return code


def generate_growth_trend(
    years: List[str],
    values: List[float],
    title: str = "市场规模增长趋势",
    y_label: str = "市场规模(亿元)",
    y_max: int = 1000
) -> str:
    """
    生成增长趋势图
    
    Args:
        years: 年份列表
        values: 对应的数值列表
        title: 图表标题
        y_label: Y轴标签
        y_max: Y轴最大值
        
    Returns:
        Mermaid xychart-beta代码
    """
    years_str = ", ".join(years)
    values_str = ", ".join(str(v) for v in values)
    
    code = f"""```mermaid
xychart-beta
    title "{title}"
    x-axis [{years_str}]
    y-axis "{y_label}" 0 --> {y_max}
    bar [{values_str}]
    line [{values_str}]
```"""
    return code


def generate_porter_five_forces(
    rivalry: str = "中",
    new_entrants: str = "中",
    substitutes: str = "中",
    supplier_power: str = "中",
    buyer_power: str = "中"
) -> str:
    """
    生成波特五力分析图
    
    Args:
        rivalry: 现有竞争强度 (高/中/低)
        new_entrants: 新进入者威胁 (高/中/低)
        substitutes: 替代品威胁 (高/中/低)
        supplier_power: 供应商议价能力 (高/中/低)
        buyer_power: 购买者议价能力 (高/中/低)
        
    Returns:
        Mermaid flowchart代码
    """
    code = f"""```mermaid
flowchart TB
    subgraph 波特五力分析
        A["潜在进入者威胁<br/>({new_entrants})"] --> C["行业竞争强度<br/>({rivalry})"]
        B["替代品威胁<br/>({substitutes})"] --> C
        D["供应商议价能力<br/>({supplier_power})"] --> C
        E["购买者议价能力<br/>({buyer_power})"] --> C
    end
    
    C --> F[行业吸引力评估]
```"""
    return code


def generate_bar_chart(
    labels: List[str],
    values: List[float],
    title: str = "数据对比",
    y_label: str = "数值",
    y_max: int = None
) -> str:
    """
    生成柱状图
    
    Args:
        labels: X轴标签列表
        values: 对应的数值列表
        title: 图表标题
        y_label: Y轴标签
        y_max: Y轴最大值（可选，自动计算）
        
    Returns:
        Mermaid xychart-beta代码
    """
    if y_max is None:
        y_max = int(max(values) * 1.2)
    
    labels_str = ", ".join(labels)
    values_str = ", ".join(str(v) for v in values)
    
    code = f"""```mermaid
xychart-beta
    title "{title}"
    x-axis [{labels_str}]
    y-axis "{y_label}" 0 --> {y_max}
    bar [{values_str}]
```"""
    return code


def generate_line_chart(
    labels: List[str],
    values: List[float],
    title: str = "趋势变化",
    y_label: str = "数值",
    y_max: int = None
) -> str:
    """
    生成折线图
    
    Args:
        labels: X轴标签列表
        values: 对应的数值列表
        title: 图表标题
        y_label: Y轴标签
        y_max: Y轴最大值（可选，自动计算）
        
    Returns:
        Mermaid xychart-beta代码
    """
    if y_max is None:
        y_max = int(max(values) * 1.2)
    
    labels_str = ", ".join(labels)
    values_str = ", ".join(str(v) for v in values)
    
    code = f"""```mermaid
xychart-beta
    title "{title}"
    x-axis [{labels_str}]
    y-axis "{y_label}" 0 --> {y_max}
    line [{values_str}]
```"""
    return code


def generate_multi_line_chart(
    labels: List[str],
    series: List[Dict[str, Any]],
    title: str = "多系列对比",
    y_label: str = "数值",
    y_max: int = None
) -> str:
    """
    生成多系列折线图
    
    Args:
        labels: X轴标签列表
        series: 系列数据列表，每项包含 name 和 values
        title: 图表标题
        y_label: Y轴标签
        y_max: Y轴最大值（可选，自动计算）
        
    Returns:
        Mermaid xychart-beta代码
    """
    all_values = []
    for s in series:
        all_values.extend(s.get("values", []))
    
    if y_max is None and all_values:
        y_max = int(max(all_values) * 1.2)
    elif y_max is None:
        y_max = 100
    
    labels_str = ", ".join(labels)
    
    code = f"""```mermaid
xychart-beta
    title "{title}"
    x-axis [{labels_str}]
    y-axis "{y_label}" 0 --> {y_max}
"""
    
    for s in series:
        name = s.get("name", "系列")
        values_str = ", ".join(str(v) for v in s.get("values", []))
        code += f'    line "{name}" [{values_str}]\n'
    
    code += "```"
    return code


def generate_timeline(
    events: List[Dict[str, str]],
    title: str = "发展历程"
) -> str:
    """
    生成时间线图
    
    Args:
        events: 事件列表，每项包含 year 和 event
        title: 图表标题
        
    Returns:
        Mermaid timeline代码
    """
    code = f"""```mermaid
timeline
    title {title}
"""
    
    for event in events:
        year = event.get("year", "")
        desc = event.get("event", "")
        code += f"    {year} : {desc}\n"
    
    code += "```"
    return code


def generate_cost_pie(
    items: List[Dict[str, Any]],
    title: str = "成本结构分析"
) -> str:
    """
    生成成本结构饼图
    
    Args:
        items: 成本项列表，每项包含 name 和 percent
        title: 图表标题
        
    Returns:
        Mermaid pie代码
    """
    code = f"""```mermaid
pie showData
    title {title}
"""
    for item in items:
        name = item.get("name", "项目")
        percent = item.get("percent", 10)
        code += f'    "{name}" : {percent}\n'
    
    code += "```"
    return code


def generate_competition_quadrant(
    companies: List[Dict[str, Any]],
    title: str = "竞争定位分析",
    x_axis: str = "低价格 --> 高价格",
    y_axis: str = "低品质 --> 高品质",
    q1: str = "高端市场",
    q2: str = "性价比市场",
    q3: str = "低端市场",
    q4: str = "溢价市场"
) -> str:
    """
    生成竞争定位象限图
    
    Args:
        companies: 企业列表，每项包含 name, x, y 坐标
        title: 图表标题
        x_axis/y_axis: 坐标轴标签
        q1-q4: 四个象限名称
        
    Returns:
        Mermaid quadrantChart代码
    """
    code = f"""```mermaid
quadrantChart
    title {title}
    x-axis {x_axis}
    y-axis {y_axis}
    quadrant-1 {q1}
    quadrant-2 {q2}
    quadrant-3 {q3}
    quadrant-4 {q4}
"""
    
    for company in companies:
        name = company.get("name", "企业")
        x = company.get("x", 0.5)
        y = company.get("y", 0.5)
        code += f"    {name}: [{x}, {y}]\n"
    
    code += "```"
    return code


def generate_user_journey(
    stages: List[Dict[str, str]],
    title: str = "用户旅程"
) -> str:
    """
    生成用户旅程流程图
    
    Args:
        stages: 阶段列表，每项包含 name 和 action
        title: 图表标题
        
    Returns:
        Mermaid flowchart代码
    """
    code = f"""```mermaid
flowchart LR
"""
    
    # 生成节点
    for i, stage in enumerate(stages):
        name = stage.get("name", f"阶段{i+1}")
        code += f"    S{i}[{name}]\n"
    
    # 生成连接
    for i in range(len(stages) - 1):
        action = stages[i].get("action", "")
        if action:
            code += f"    S{i} -.-> |{action}| S{i+1}\n"
        else:
            code += f"    S{i} --> S{i+1}\n"
    
    code += "```"
    return code


def generate_gantt_chart(
    tasks: List[Dict[str, str]],
    title: str = "项目规划"
) -> str:
    """
    生成甘特图
    
    Args:
        tasks: 任务列表，每项包含 section, name, start, end
        title: 图表标题
        
    Returns:
        Mermaid gantt代码
    """
    code = f"""```mermaid
gantt
    title {title}
    dateFormat YYYY
"""
    
    current_section = None
    for task in tasks:
        section = task.get("section", "")
        if section and section != current_section:
            code += f"    section {section}\n"
            current_section = section
        
        name = task.get("name", "任务")
        start = task.get("start", "2024")
        end = task.get("end", "2025")
        code += f"        {name}           :{start}, {end}\n"
    
    code += "```"
    return code


def main():
    """
    命令行入口
    """
    if len(sys.argv) < 2:
        print("用法: python mermaid_generator.py <图表类型> [参数JSON]")
        print()
        print("支持的图表类型:")
        print("  chain     - 产业链图")
        print("  pest      - PEST分析思维导图")
        print("  bcg       - BCG矩阵")
        print("  swot      - SWOT分析思维导图")
        print("  pie       - 市场份额饼图")
        print("  cost_pie  - 成本结构饼图")
        print("  trend     - 增长趋势图（柱状+折线）")
        print("  bar       - 柱状图")
        print("  line      - 折线图")
        print("  multi_line - 多系列折线图")
        print("  porter    - 波特五力分析")
        print("  timeline  - 时间线图")
        print("  quadrant  - 竞争定位象限图")
        print("  journey   - 用户旅程图")
        print("  gantt     - 甘特图")
        print()
        print("示例:")
        print('  python mermaid_generator.py chain \'{"upstream":["供应商A","供应商B"],"midstream":["核心企业"],"downstream":["客户A","客户B"]}\'')
        print('  python mermaid_generator.py bar \'{"labels":["Q1","Q2","Q3","Q4"],"values":[100,150,200,250],"title":"季度营收"}\'')
        print('  python mermaid_generator.py timeline \'{"events":[{"year":"2020","event":"产品发布"},{"year":"2022","event":"市场扩张"}]}\'')
        sys.exit(1)
    
    chart_type = sys.argv[1]
    params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    
    if chart_type == "chain":
        print(generate_industry_chain(
            params.get("upstream", ["原材料", "技术", "设备"]),
            params.get("midstream", ["核心企业"]),
            params.get("downstream", ["企业客户", "个人消费者"]),
            params.get("industry_name", "行业")
        ))
    elif chart_type == "pest":
        print(generate_pest_mindmap(
            params.get("political", ["政策法规", "监管要求"]),
            params.get("economic", ["市场规模", "消费能力"]),
            params.get("social", ["消费观念", "生活方式"]),
            params.get("technological", ["核心技术", "数字化"])
        ))
    elif chart_type == "bcg":
        print(generate_bcg_matrix(
            params.get("companies", [
                {"name": "企业A", "market_share": 0.7, "growth_rate": 0.8},
                {"name": "企业B", "market_share": 0.3, "growth_rate": 0.6},
            ])
        ))
    elif chart_type == "swot":
        print(generate_swot_quadrant(
            params.get("strengths", ["优势1", "优势2"]),
            params.get("weaknesses", ["劣势1", "劣势2"]),
            params.get("opportunities", ["机会1", "机会2"]),
            params.get("threats", ["威胁1", "威胁2"])
        ))
    elif chart_type == "pie":
        print(generate_market_share_pie(
            params.get("companies", [
                {"name": "企业A", "share": 35},
                {"name": "企业B", "share": 25},
                {"name": "其他", "share": 40},
            ]),
            params.get("title", "市场份额分布")
        ))
    elif chart_type == "cost_pie":
        print(generate_cost_pie(
            params.get("items", [
                {"name": "原材料", "percent": 45},
                {"name": "人工成本", "percent": 25},
                {"name": "其他", "percent": 30},
            ]),
            params.get("title", "成本结构分析")
        ))
    elif chart_type == "trend":
        print(generate_growth_trend(
            params.get("years", ["2020", "2021", "2022", "2023", "2024"]),
            params.get("values", [100, 150, 200, 280, 350]),
            params.get("title", "市场规模增长趋势"),
            params.get("y_label", "市场规模(亿元)"),
            params.get("y_max", 500)
        ))
    elif chart_type == "bar":
        print(generate_bar_chart(
            params.get("labels", ["Q1", "Q2", "Q3", "Q4"]),
            params.get("values", [100, 150, 200, 250]),
            params.get("title", "数据对比"),
            params.get("y_label", "数值"),
            params.get("y_max")
        ))
    elif chart_type == "line":
        print(generate_line_chart(
            params.get("labels", ["1月", "2月", "3月", "4月", "5月", "6月"]),
            params.get("values", [100, 120, 150, 180, 220, 260]),
            params.get("title", "趋势变化"),
            params.get("y_label", "数值"),
            params.get("y_max")
        ))
    elif chart_type == "multi_line":
        print(generate_multi_line_chart(
            params.get("labels", ["2020", "2021", "2022", "2023", "2024"]),
            params.get("series", [
                {"name": "系列A", "values": [100, 150, 200, 250, 300]},
                {"name": "系列B", "values": [80, 120, 180, 240, 320]},
            ]),
            params.get("title", "多系列对比"),
            params.get("y_label", "数值"),
            params.get("y_max")
        ))
    elif chart_type == "porter":
        print(generate_porter_five_forces(
            params.get("rivalry", "中"),
            params.get("new_entrants", "中"),
            params.get("substitutes", "中"),
            params.get("supplier_power", "中"),
            params.get("buyer_power", "中")
        ))
    elif chart_type == "timeline":
        print(generate_timeline(
            params.get("events", [
                {"year": "2020", "event": "产品发布"},
                {"year": "2022", "event": "市场扩张"},
                {"year": "2024", "event": "行业领先"},
            ]),
            params.get("title", "发展历程")
        ))
    elif chart_type == "quadrant":
        print(generate_competition_quadrant(
            params.get("companies", [
                {"name": "品牌A", "x": 0.8, "y": 0.85},
                {"name": "品牌B", "x": 0.3, "y": 0.7},
            ]),
            params.get("title", "竞争定位分析"),
            params.get("x_axis", "低价格 --> 高价格"),
            params.get("y_axis", "低品质 --> 高品质"),
            params.get("q1", "高端市场"),
            params.get("q2", "性价比市场"),
            params.get("q3", "低端市场"),
            params.get("q4", "溢价市场")
        ))
    elif chart_type == "journey":
        print(generate_user_journey(
            params.get("stages", [
                {"name": "认知", "action": "广告触达"},
                {"name": "兴趣", "action": "内容种草"},
                {"name": "购买", "action": "下单转化"},
                {"name": "使用", "action": ""},
            ]),
            params.get("title", "用户旅程")
        ))
    elif chart_type == "gantt":
        print(generate_gantt_chart(
            params.get("tasks", [
                {"section": "第一阶段", "name": "需求分析", "start": "2024", "end": "2025"},
                {"section": "第一阶段", "name": "产品设计", "start": "2025", "end": "2026"},
                {"section": "第二阶段", "name": "开发测试", "start": "2026", "end": "2027"},
            ]),
            params.get("title", "项目规划")
        ))
    else:
        print(f"未知的图表类型: {chart_type}")
        sys.exit(1)


def main_ascii():
    """ASCII模式命令行入口"""
    import os
    
    if not ASCII_AVAILABLE:
        print("错误: ASCII图表模块不可用，请确保 ascii_charts.py 在同一目录")
        sys.exit(1)
    
    if len(sys.argv) < 3:
        print("用法: python mermaid_generator.py --ascii <图表类型> [参数JSON或JSON文件]")
        sys.exit(1)
    
    chart_type = sys.argv[2]
    
    # 支持从JSON文件读取参数
    params = {}
    if len(sys.argv) > 3:
        arg = sys.argv[3]
        if arg.endswith('.json') and os.path.exists(arg):
            with open(arg, 'r', encoding='utf-8') as f:
                params = json.load(f)
        else:
            try:
                params = json.loads(arg)
            except json.JSONDecodeError:
                print(f"错误: 无法解析参数。请提供有效的JSON字符串或JSON文件路径。")
                sys.exit(1)
    
    if chart_type == "chain":
        print(ASCIICharts.industry_chain(
            params.get("upstream", ["原材料", "技术", "设备"]),
            params.get("midstream", ["核心企业"]),
            params.get("downstream", ["企业客户", "个人消费者"]),
            params.get("title", "产业链图")
        ))
    elif chart_type == "pest":
        print(ASCIICharts.pest_diagram(
            params.get("political", ["政策法规", "监管要求"]),
            params.get("economic", ["市场规模", "消费能力"]),
            params.get("social", ["消费观念", "生活方式"]),
            params.get("technological", ["核心技术", "数字化"]),
            params.get("title", "PEST分析")
        ))
    elif chart_type == "bcg":
        print(ASCIICharts.bcg_matrix(
            params.get("stars", ["明星企业"]),
            params.get("cash_cows", ["现金牛企业"]),
            params.get("question_marks", ["问题企业"]),
            params.get("dogs", ["瘦狗企业"]),
            params.get("title", "BCG矩阵")
        ))
    elif chart_type == "swot":
        print(ASCIICharts.swot_matrix(
            params.get("strengths", ["优势1", "优势2"]),
            params.get("weaknesses", ["劣势1", "劣势2"]),
            params.get("opportunities", ["机会1", "机会2"]),
            params.get("threats", ["威胁1", "威胁2"]),
            params.get("title", "SWOT分析")
        ))
    elif chart_type == "pie":
        data = params.get("companies", [{"name": "A", "share": 60}, {"name": "B", "share": 40}])
        # 转换格式
        pie_data = [{"label": item.get("name", ""), "value": item.get("share", 0)} for item in data]
        print(ASCIICharts.pie_chart_text(pie_data, params.get("title", "市场份额分布")))
    elif chart_type == "trend" or chart_type == "bar":
        print(ASCIICharts.bar_chart(
            [{"label": l, "value": v} for l, v in zip(
                params.get("years", params.get("labels", ["2020", "2021", "2022"])),
                params.get("values", [100, 150, 200])
            )],
            params.get("title", "趋势图")
        ))
    elif chart_type == "flow":
        print(ASCIICharts.flow_chart(
            params.get("stages", ["阶段1", "阶段2", "阶段3"]),
            params.get("title", "流程图")
        ))
    elif chart_type == "score":
        print(ASCIICharts.score_card(
            params.get("items", [{"name": "指标A", "score": 4}]),
            params.get("title", "评分卡")
        ))
    elif chart_type == "table":
        print(ASCIICharts.comparison_table(
            params.get("headers", ["列1", "列2"]),
            params.get("rows", [["A", "B"]]),
            params.get("title", "对比表格")
        ))
    else:
        print(f"ASCII模式不支持的图表类型: {chart_type}")
        print("支持的类型: chain, pest, bcg, swot, pie, trend, bar, flow, score, table")
        sys.exit(1)


if __name__ == "__main__":
    # 检查是否使用ASCII模式
    if len(sys.argv) > 1 and sys.argv[1] == "--ascii":
        main_ascii()
    else:
        main()
