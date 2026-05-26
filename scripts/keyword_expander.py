#!/usr/bin/env python3
"""
关键词扩充脚本
根据用户输入的行业关键词，自动生成多维度的搜索关键词组合
"""

import json
import sys
from typing import List, Dict
from datetime import datetime


def expand_keywords(industry: str) -> Dict[str, List[str]]:
    """
    根据行业关键词生成多维度搜索关键词
    
    Args:
        industry: 行业名称
        
    Returns:
        包含各维度搜索关键词的字典
    """
    current_year = datetime.now().year
    last_year = current_year - 1
    
    keywords = {
        "行业概况": [
            f"{industry} 行业概况 {current_year}",
            f"{industry} 行业定义 分类",
            f"{industry} 发展历程 阶段",
            f"{industry} 行业特征 现状",
        ],
        "市场规模": [
            f"{industry} 市场规模 {current_year}",
            f"{industry} 市场增长率 预测",
            f"{industry} 全球市场 中国市场",
            f"{industry} 细分市场 占比",
        ],
        "产业链": [
            f"{industry} 产业链分析",
            f"{industry} 上游供应商",
            f"{industry} 下游客户 应用场景",
            f"{industry} 价值链 利润分布",
        ],
        "竞争格局": [
            f"{industry} 竞争格局 {current_year}",
            f"{industry} 主要企业 市场份额",
            f"{industry} 头部公司 排名",
            f"{industry} 竞争态势 格局变化",
        ],
        "政策法规": [
            f"{industry} 政策法规 {current_year}",
            f"{industry} 监管要求 合规",
            f"{industry} 行业标准 规范",
            f"{industry} 产业政策 扶持",
        ],
        "技术趋势": [
            f"{industry} 技术趋势 {current_year}",
            f"{industry} 核心技术 创新",
            f"{industry} AI应用 数字化",
            f"{industry} 技术壁垒 研发",
        ],
        "商业模式": [
            f"{industry} 商业模式 盈利模式",
            f"{industry} 成本结构 收入来源",
            f"{industry} 定价策略 收费模式",
        ],
        "痛点挑战": [
            f"{industry} 行业痛点 挑战",
            f"{industry} 发展瓶颈 问题",
            f"{industry} 风险因素 障碍",
        ],
        "投融资": [
            f"{industry} 投融资 {current_year}",
            f"{industry} 融资事件 投资",
            f"{industry} 估值 资本市场",
        ],
        "消费趋势": [
            f"{industry} 消费趋势 用户需求",
            f"{industry} 用户画像 消费行为",
            f"{industry} 市场需求 增长驱动",
        ],
    }
    
    return keywords


def generate_search_queries(industry: str, max_queries: int = 20) -> List[str]:
    """
    生成优先级排序的搜索查询列表
    
    Args:
        industry: 行业名称
        max_queries: 最大查询数量
        
    Returns:
        搜索查询列表
    """
    keywords = expand_keywords(industry)
    
    # 按优先级排序的维度
    priority_order = [
        "行业概况",
        "市场规模",
        "竞争格局",
        "产业链",
        "技术趋势",
        "政策法规",
        "商业模式",
        "痛点挑战",
        "投融资",
        "消费趋势",
    ]
    
    queries = []
    for dimension in priority_order:
        if dimension in keywords:
            queries.extend(keywords[dimension][:2])  # 每个维度取前2个
            if len(queries) >= max_queries:
                break
    
    return queries[:max_queries]


def output_markdown(industry: str) -> str:
    """
    输出Markdown格式的关键词列表
    """
    keywords = expand_keywords(industry)
    queries = generate_search_queries(industry)
    
    output = f"# {industry}行业分析 - 搜索关键词\n\n"
    output += f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    
    output += "## 推荐搜索查询（按优先级排序）\n\n"
    for i, query in enumerate(queries, 1):
        output += f"{i}. `{query}`\n"
    
    output += "\n## 分维度关键词详情\n\n"
    for dimension, kws in keywords.items():
        output += f"### {dimension}\n"
        for kw in kws:
            output += f"- {kw}\n"
        output += "\n"
    
    return output


def output_json(industry: str) -> str:
    """
    输出JSON格式的关键词数据
    """
    data = {
        "industry": industry,
        "generated_at": datetime.now().isoformat(),
        "keywords_by_dimension": expand_keywords(industry),
        "search_queries": generate_search_queries(industry),
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def main():
    if len(sys.argv) < 2:
        print("用法: python keyword_expander.py <行业名称> [--json]")
        print("示例: python keyword_expander.py \"新能源汽车\"")
        print("      python keyword_expander.py \"GUI Agent\" --json")
        sys.exit(1)
    
    industry = sys.argv[1]
    output_format = "json" if "--json" in sys.argv else "markdown"
    
    if output_format == "json":
        print(output_json(industry))
    else:
        print(output_markdown(industry))


if __name__ == "__main__":
    main()
