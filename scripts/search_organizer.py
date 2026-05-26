#!/usr/bin/env python3
"""
搜索结果整理脚本
帮助整理和分类联网搜索获取的信息
"""

import json
import sys
from typing import Dict, List, Any
from datetime import datetime


class SearchOrganizer:
    """搜索结果整理器"""
    
    # 信息分类维度
    CATEGORIES = {
        "overview": {
            "name": "行业概况",
            "keywords": ["概况", "定义", "分类", "发展历程", "特征", "现状"]
        },
        "market": {
            "name": "市场数据",
            "keywords": ["市场规模", "增长率", "CAGR", "市场份额", "细分市场"]
        },
        "chain": {
            "name": "产业链",
            "keywords": ["产业链", "上游", "下游", "供应商", "客户", "价值链"]
        },
        "competition": {
            "name": "竞争格局",
            "keywords": ["竞争", "企业", "玩家", "市场份额", "排名", "头部"]
        },
        "policy": {
            "name": "政策法规",
            "keywords": ["政策", "法规", "监管", "标准", "合规", "规范"]
        },
        "technology": {
            "name": "技术趋势",
            "keywords": ["技术", "创新", "研发", "AI", "数字化", "专利"]
        },
        "business": {
            "name": "商业模式",
            "keywords": ["商业模式", "盈利", "收入", "成本", "定价"]
        },
        "pain_points": {
            "name": "痛点挑战",
            "keywords": ["痛点", "挑战", "问题", "瓶颈", "风险", "障碍"]
        },
        "investment": {
            "name": "投融资",
            "keywords": ["融资", "投资", "估值", "IPO", "并购"]
        },
        "consumer": {
            "name": "消费趋势",
            "keywords": ["消费", "用户", "需求", "行为", "画像"]
        }
    }
    
    def __init__(self, industry: str):
        """
        初始化整理器
        
        Args:
            industry: 行业名称
        """
        self.industry = industry
        self.results: Dict[str, List[Dict]] = {cat: [] for cat in self.CATEGORIES}
        self.unclassified: List[Dict] = []
    
    def add_result(self, title: str, content: str, source: str, url: str = "") -> str:
        """
        添加搜索结果并自动分类
        
        Args:
            title: 标题
            content: 内容摘要
            source: 来源
            url: 链接
            
        Returns:
            分类结果
        """
        result = {
            "title": title,
            "content": content,
            "source": source,
            "url": url,
            "added_at": datetime.now().isoformat()
        }
        
        # 自动分类
        category = self._classify(title, content)
        
        if category:
            self.results[category].append(result)
            return self.CATEGORIES[category]["name"]
        else:
            self.unclassified.append(result)
            return "未分类"
    
    def _classify(self, title: str, content: str) -> str:
        """
        根据标题和内容自动分类
        
        Args:
            title: 标题
            content: 内容
            
        Returns:
            分类ID或空字符串
        """
        text = (title + " " + content).lower()
        
        # 计算每个分类的匹配得分
        scores = {}
        for cat_id, cat_info in self.CATEGORIES.items():
            score = sum(1 for kw in cat_info["keywords"] if kw in text)
            if score > 0:
                scores[cat_id] = score
        
        # 返回得分最高的分类
        if scores:
            return max(scores, key=scores.get)
        return ""
    
    def get_summary(self) -> Dict[str, Any]:
        """
        获取整理结果摘要
        
        Returns:
            摘要字典
        """
        summary = {
            "industry": self.industry,
            "total_results": sum(len(v) for v in self.results.values()) + len(self.unclassified),
            "by_category": {},
            "unclassified_count": len(self.unclassified)
        }
        
        for cat_id, results in self.results.items():
            if results:
                summary["by_category"][self.CATEGORIES[cat_id]["name"]] = len(results)
        
        return summary
    
    def get_category_results(self, category: str) -> List[Dict]:
        """
        获取指定分类的结果
        
        Args:
            category: 分类ID
            
        Returns:
            结果列表
        """
        return self.results.get(category, [])
    
    def export_for_analysis(self) -> Dict[str, Any]:
        """
        导出用于分析的结构化数据
        
        Returns:
            结构化数据字典
        """
        export_data = {
            "industry": self.industry,
            "generated_at": datetime.now().isoformat(),
            "overview": self._extract_overview_data(),
            "market": self._extract_market_data(),
            "chain": self._extract_chain_data(),
            "pest": self._extract_pest_data(),
            "bcg": self._extract_bcg_data(),
            "swot": self._extract_swot_data(),
            "conclusion": self._extract_conclusion_data(),
            "sources": self._get_all_sources()
        }
        return export_data
    
    def _extract_overview_data(self) -> Dict:
        """提取行业概况数据"""
        overview_results = self.results.get("overview", [])
        market_results = self.results.get("market", [])
        pain_results = self.results.get("pain_points", [])
        business_results = self.results.get("business", [])
        chain_results = self.results.get("chain", [])
        
        return {
            "definition": self._find_content(overview_results, ["定义", "是指"]),
            "history": self._find_content(overview_results, ["发展历程", "发展阶段"]),
            "stage": self._find_content(overview_results, ["当前", "阶段", "现状"]),
            "characteristics": self._extract_list(overview_results, ["特征", "特点"]),
            "global_market_size": self._find_number(market_results, ["全球", "市场规模"]),
            "china_market_size": self._find_number(market_results, ["中国", "市场规模"]),
            "growth_rate": self._find_number(market_results, ["增长率", "增速"]),
            "cagr": self._find_number(market_results, ["CAGR", "复合增长"]),
            "pain_points": {
                "technical": self._extract_list(pain_results, ["技术"]),
                "business": self._extract_list(pain_results, ["商业", "盈利"]),
                "user": self._extract_list(pain_results, ["用户", "客户"]),
                "regulatory": self._extract_list(pain_results, ["监管", "合规"])
            },
            "business_model": self._find_content(business_results, ["商业模式", "盈利模式"]),
            "industry_chain": self._find_content(chain_results, ["产业链"])
        }
    
    def _extract_market_data(self) -> Dict:
        """提取市场数据"""
        market_results = self.results.get("market", [])
        
        return {
            "global_current": self._find_number(market_results, ["全球", "当前", "2024"]),
            "global_forecast": self._find_number(market_results, ["全球", "预计", "预测"]),
            "global_cagr": self._find_number(market_results, ["全球", "CAGR"]),
            "china_current": self._find_number(market_results, ["中国", "当前", "2024"]),
            "china_forecast": self._find_number(market_results, ["中国", "预计", "预测"]),
            "china_cagr": self._find_number(market_results, ["中国", "CAGR"]),
            "segments": self._extract_segments(market_results)
        }
    
    def _extract_chain_data(self) -> Dict:
        """提取产业链数据"""
        chain_results = self.results.get("chain", [])
        
        return {
            "upstream": self._extract_list(chain_results, ["上游", "供应商"]),
            "midstream": self._extract_list(chain_results, ["中游", "核心"]),
            "downstream": self._extract_list(chain_results, ["下游", "客户"]),
            "upstream_power": self._find_content(chain_results, ["上游", "议价"]),
            "downstream_power": self._find_content(chain_results, ["下游", "议价"])
        }
    
    def _extract_pest_data(self) -> Dict:
        """提取PEST分析数据"""
        policy_results = self.results.get("policy", [])
        market_results = self.results.get("market", [])
        consumer_results = self.results.get("consumer", [])
        tech_results = self.results.get("technology", [])
        
        return {
            "political": self._find_content(policy_results, ["政策", "法规"]),
            "economic": self._find_content(market_results, ["经济", "消费"]),
            "social": self._find_content(consumer_results, ["社会", "消费观念"]),
            "technological": self._find_content(tech_results, ["技术", "创新"]),
            "political_points": self._extract_list(policy_results, ["政策"]),
            "economic_points": self._extract_list(market_results, ["经济"]),
            "social_points": self._extract_list(consumer_results, ["社会", "消费"]),
            "technological_points": self._extract_list(tech_results, ["技术"])
        }
    
    def _extract_bcg_data(self) -> Dict:
        """提取BCG矩阵数据"""
        competition_results = self.results.get("competition", [])
        
        return {
            "analysis": self._find_content(competition_results, ["竞争", "格局"]),
            "companies": self._extract_companies(competition_results)
        }
    
    def _extract_swot_data(self) -> Dict:
        """提取SWOT分析数据"""
        all_results = []
        for results in self.results.values():
            all_results.extend(results)
        
        return {
            "strengths": self._extract_list(all_results, ["优势", "领先", "强"]),
            "weaknesses": self._extract_list(all_results, ["劣势", "不足", "弱"]),
            "opportunities": self._extract_list(all_results, ["机会", "机遇", "增长"]),
            "threats": self._extract_list(all_results, ["威胁", "风险", "挑战"])
        }
    
    def _extract_conclusion_data(self) -> Dict:
        """提取结论数据"""
        return {
            "insights": [],
            "short_term": [],
            "mid_term": [],
            "long_term": [],
            "risks": []
        }
    
    def _get_all_sources(self) -> List[str]:
        """获取所有来源"""
        sources = set()
        for results in self.results.values():
            for result in results:
                if result.get("source"):
                    sources.add(result["source"])
        for result in self.unclassified:
            if result.get("source"):
                sources.add(result["source"])
        return list(sources)
    
    # 辅助方法
    def _find_content(self, results: List[Dict], keywords: List[str]) -> str:
        """在结果中查找包含关键词的内容"""
        for result in results:
            content = result.get("content", "")
            if any(kw in content for kw in keywords):
                return content[:200] + "..." if len(content) > 200 else content
        return ""
    
    def _find_number(self, results: List[Dict], keywords: List[str]) -> str:
        """在结果中查找数字"""
        import re
        for result in results:
            content = result.get("content", "") + result.get("title", "")
            if any(kw in content for kw in keywords):
                # 查找数字模式
                numbers = re.findall(r'[\d,]+\.?\d*\s*[亿万%]', content)
                if numbers:
                    return numbers[0]
        return ""
    
    def _extract_list(self, results: List[Dict], keywords: List[str]) -> List[str]:
        """提取列表项"""
        items = []
        for result in results:
            content = result.get("content", "")
            if any(kw in content for kw in keywords):
                # 简单提取：按句号分割取前几项
                sentences = content.split("。")[:3]
                items.extend([s.strip() for s in sentences if s.strip()])
        return items[:5]  # 最多返回5项
    
    def _extract_segments(self, results: List[Dict]) -> List[Dict]:
        """提取细分市场数据"""
        # 简化实现，返回占位数据
        return [
            {"name": "细分市场A", "share": "X%"},
            {"name": "细分市场B", "share": "X%"},
            {"name": "其他", "share": "X%"}
        ]
    
    def _extract_companies(self, results: List[Dict]) -> List[Dict]:
        """提取公司数据"""
        # 简化实现，返回占位数据
        return [
            {"name": "企业A", "market_share": 0.7, "growth_rate": 0.8},
            {"name": "企业B", "market_share": 0.5, "growth_rate": 0.6},
            {"name": "企业C", "market_share": 0.3, "growth_rate": 0.4}
        ]
    
    def to_markdown(self) -> str:
        """输出Markdown格式的整理结果"""
        output = f"# {self.industry}行业 - 搜索结果整理\n\n"
        output += f"整理时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        summary = self.get_summary()
        output += f"## 摘要\n\n"
        output += f"- 总结果数：{summary['total_results']}\n"
        output += f"- 未分类数：{summary['unclassified_count']}\n\n"
        
        output += "### 分类统计\n\n"
        for cat_name, count in summary['by_category'].items():
            output += f"- {cat_name}：{count}条\n"
        
        output += "\n---\n\n"
        
        for cat_id, cat_info in self.CATEGORIES.items():
            results = self.results[cat_id]
            if results:
                output += f"## {cat_info['name']}\n\n"
                for i, result in enumerate(results, 1):
                    output += f"### {i}. {result['title']}\n\n"
                    output += f"**来源**：{result['source']}\n\n"
                    output += f"{result['content']}\n\n"
                    if result.get('url'):
                        output += f"[链接]({result['url']})\n\n"
                output += "---\n\n"
        
        if self.unclassified:
            output += "## 未分类\n\n"
            for i, result in enumerate(self.unclassified, 1):
                output += f"### {i}. {result['title']}\n\n"
                output += f"**来源**：{result['source']}\n\n"
                output += f"{result['content']}\n\n"
        
        return output


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python search_organizer.py <行业名称> [操作]")
        print()
        print("操作:")
        print("  summary    - 输出摘要")
        print("  export     - 导出分析数据JSON")
        print("  markdown   - 输出Markdown格式")
        print()
        print("示例:")
        print("  python search_organizer.py \"新能源汽车\" summary")
        sys.exit(1)
    
    industry = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else "summary"
    
    # 创建整理器（演示用）
    organizer = SearchOrganizer(industry)
    
    # 添加一些示例数据
    organizer.add_result(
        "行业概况：市场规模达千亿",
        f"{industry}行业2024年市场规模达到1000亿元，同比增长25%",
        "行业研究报告"
    )
    organizer.add_result(
        "政策利好：国家出台支持政策",
        f"国家发改委发布{industry}产业发展指导意见，明确支持方向",
        "政府网站"
    )
    
    if action == "summary":
        summary = organizer.get_summary()
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    elif action == "export":
        data = organizer.export_for_analysis()
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif action == "markdown":
        print(organizer.to_markdown())
    else:
        print(f"未知操作: {action}")
        sys.exit(1)


if __name__ == "__main__":
    main()
