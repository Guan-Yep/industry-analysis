#!/usr/bin/env python3
"""
报告定制化模块
支持报告裁剪、风格转换、摘要生成、亮点提取
"""

import json
import sys
import os
import re
from typing import Dict, Any, List, Optional
from datetime import datetime


class ReportCustomizer:
    """报告定制化处理器"""
    
    # 报告模块定义
    MODULES = {
        "overview": {
            "name": "行业概览",
            "sections": ["行业定义", "市场规模", "发展阶段", "产业链"],
            "weight": 1.0
        },
        "pest": {
            "name": "PEST分析",
            "sections": ["政治环境", "经济环境", "社会环境", "技术环境"],
            "weight": 0.8
        },
        "bcg": {
            "name": "BCG矩阵",
            "sections": ["明星业务", "现金牛", "问题业务", "瘦狗业务"],
            "weight": 0.7
        },
        "swot": {
            "name": "SWOT分析",
            "sections": ["优势", "劣势", "机会", "威胁", "战略建议"],
            "weight": 0.9
        },
        "competition": {
            "name": "竞争格局",
            "sections": ["市场份额", "头部企业", "竞争态势"],
            "weight": 0.8
        },
        "trend": {
            "name": "趋势展望",
            "sections": ["发展趋势", "机会预测", "风险预警"],
            "weight": 0.7
        }
    }
    
    # 报告类型预设
    REPORT_TYPES = {
        "full": {
            "name": "完整版",
            "modules": ["overview", "pest", "bcg", "swot", "competition", "trend"],
            "detail_level": "high",
            "description": "包含所有分析模块的完整报告"
        },
        "brief": {
            "name": "精简版",
            "modules": ["overview", "swot", "competition"],
            "detail_level": "medium",
            "description": "聚焦核心内容的精简报告"
        },
        "executive": {
            "name": "汇报版",
            "modules": ["overview", "swot"],
            "detail_level": "low",
            "description": "适合高层汇报的精华版本"
        },
        "pest_only": {
            "name": "PEST专题",
            "modules": ["overview", "pest"],
            "detail_level": "high",
            "description": "聚焦宏观环境分析"
        },
        "swot_only": {
            "name": "SWOT专题",
            "modules": ["overview", "swot"],
            "detail_level": "high",
            "description": "聚焦战略分析"
        },
        "competition_only": {
            "name": "竞争专题",
            "modules": ["overview", "competition", "bcg"],
            "detail_level": "high",
            "description": "聚焦竞争格局分析"
        }
    }
    
    # 输出风格定义
    STYLES = {
        "formal": {
            "name": "正式风格",
            "tone": "专业、严谨、客观",
            "sentence_style": "长句、复杂结构",
            "vocabulary": "专业术语丰富",
            "example_prefix": "根据行业研究数据显示，",
            "example_suffix": "，这一趋势值得持续关注。"
        },
        "concise": {
            "name": "简洁风格",
            "tone": "直接、清晰、高效",
            "sentence_style": "短句、简单结构",
            "vocabulary": "通俗易懂",
            "example_prefix": "",
            "example_suffix": "。"
        },
        "data_driven": {
            "name": "数据驱动风格",
            "tone": "量化、精确、证据导向",
            "sentence_style": "数据+结论结构",
            "vocabulary": "数字和百分比优先",
            "example_prefix": "数据显示：",
            "example_suffix": "（数据来源：XX）"
        }
    }
    
    def __init__(self, report_data: Dict[str, Any] = None):
        """
        初始化报告定制器
        
        Args:
            report_data: 完整报告数据
        """
        self.report_data = report_data or {}
        self.selected_modules: List[str] = []
        self.selected_style: str = "formal"
        self.detail_level: str = "high"
    
    def set_report_type(self, report_type: str) -> "ReportCustomizer":
        """设置报告类型"""
        if report_type in self.REPORT_TYPES:
            config = self.REPORT_TYPES[report_type]
            self.selected_modules = config["modules"]
            self.detail_level = config["detail_level"]
        return self
    
    def set_modules(self, modules: List[str]) -> "ReportCustomizer":
        """自定义选择模块"""
        valid_modules = [m for m in modules if m in self.MODULES]
        self.selected_modules = valid_modules
        return self
    
    def set_style(self, style: str) -> "ReportCustomizer":
        """设置输出风格"""
        if style in self.STYLES:
            self.selected_style = style
        return self
    
    def get_available_types(self) -> str:
        """获取可用的报告类型"""
        lines = []
        lines.append("## 可用报告类型")
        lines.append("")
        lines.append("| 类型代码 | 名称 | 包含模块 | 说明 |")
        lines.append("|----------|------|----------|------|")
        for code, config in self.REPORT_TYPES.items():
            modules = ", ".join([self.MODULES[m]["name"] for m in config["modules"]])
            lines.append(f"| `{code}` | {config['name']} | {modules} | {config['description']} |")
        return "\n".join(lines)
    
    def get_available_modules(self) -> str:
        """获取可用的模块"""
        lines = []
        lines.append("## 可用分析模块")
        lines.append("")
        lines.append("| 模块代码 | 名称 | 包含内容 |")
        lines.append("|----------|------|----------|")
        for code, config in self.MODULES.items():
            sections = ", ".join(config["sections"])
            lines.append(f"| `{code}` | {config['name']} | {sections} |")
        return "\n".join(lines)
    
    def get_available_styles(self) -> str:
        """获取可用的风格"""
        lines = []
        lines.append("## 可用输出风格")
        lines.append("")
        lines.append("| 风格代码 | 名称 | 特点 |")
        lines.append("|----------|------|------|")
        for code, config in self.STYLES.items():
            lines.append(f"| `{code}` | {config['name']} | {config['tone']} |")
        return "\n".join(lines)
    
    def generate_config_prompt(self) -> str:
        """生成配置说明提示词"""
        lines = []
        lines.append("# 报告定制化配置")
        lines.append("")
        lines.append(self.get_available_types())
        lines.append("")
        lines.append(self.get_available_modules())
        lines.append("")
        lines.append(self.get_available_styles())
        lines.append("")
        lines.append("## 使用示例")
        lines.append("")
        lines.append("```bash")
        lines.append("# 生成精简版报告")
        lines.append('python report_customizer.py trim brief')
        lines.append("")
        lines.append("# 只生成PEST和SWOT模块")
        lines.append('python report_customizer.py trim custom pest,swot')
        lines.append("")
        lines.append("# 使用数据驱动风格")
        lines.append('python report_customizer.py style data_driven')
        lines.append("```")
        return "\n".join(lines)


class ReportTrimmer:
    """报告裁剪器 - 按需组合模块"""
    
    def __init__(self, full_report: str):
        """
        初始化裁剪器
        
        Args:
            full_report: 完整报告的Markdown文本
        """
        self.full_report = full_report
        self.sections = self._parse_sections()
    
    def _parse_sections(self) -> Dict[str, str]:
        """解析报告章节"""
        sections = {}
        current_section = "header"
        current_content = []
        
        for line in self.full_report.split("\n"):
            # 检测一级或二级标题
            if line.startswith("# ") or line.startswith("## "):
                if current_content:
                    sections[current_section] = "\n".join(current_content)
                current_section = line.lstrip("#").strip().lower()
                current_content = [line]
            else:
                current_content.append(line)
        
        if current_content:
            sections[current_section] = "\n".join(current_content)
        
        return sections
    
    def trim(self, keep_sections: List[str]) -> str:
        """
        裁剪报告，只保留指定章节
        
        Args:
            keep_sections: 要保留的章节关键词列表
        """
        result = []
        
        # 始终保留header
        if "header" in self.sections:
            result.append(self.sections["header"])
        
        for section_key, content in self.sections.items():
            if section_key == "header":
                continue
            
            # 检查是否匹配任何保留关键词
            for keep in keep_sections:
                if keep.lower() in section_key or section_key in keep.lower():
                    result.append(content)
                    break
        
        return "\n\n".join(result)
    
    def get_section_list(self) -> List[str]:
        """获取所有章节列表"""
        return list(self.sections.keys())


class StyleConverter:
    """风格转换器 - 转换报告语言风格"""
    
    STYLE_TEMPLATES = {
        "formal": {
            "intro_phrases": [
                "根据行业研究数据显示，",
                "从市场分析角度来看，",
                "综合各方面因素考量，",
                "基于当前市场态势分析，"
            ],
            "transition_phrases": [
                "与此同时，",
                "值得注意的是，",
                "进一步分析表明，",
                "从长远发展角度，"
            ],
            "conclusion_phrases": [
                "综上所述，",
                "总体而言，",
                "基于以上分析，"
            ]
        },
        "concise": {
            "intro_phrases": [""],
            "transition_phrases": ["此外，", "同时，", "另外，"],
            "conclusion_phrases": ["总结：", "结论："]
        },
        "data_driven": {
            "intro_phrases": [
                "数据显示：",
                "根据统计：",
                "量化分析表明："
            ],
            "transition_phrases": [
                "进一步数据表明，",
                "从数据维度看，"
            ],
            "conclusion_phrases": [
                "数据结论：",
                "量化总结："
            ]
        }
    }
    
    def __init__(self, target_style: str = "formal"):
        """
        初始化风格转换器
        
        Args:
            target_style: 目标风格
        """
        self.target_style = target_style
        self.template = self.STYLE_TEMPLATES.get(target_style, self.STYLE_TEMPLATES["formal"])
    
    def get_style_guide(self) -> str:
        """获取风格指南提示词"""
        style_config = ReportCustomizer.STYLES.get(self.target_style, {})
        
        lines = []
        lines.append(f"## {style_config.get('name', '默认风格')}写作指南")
        lines.append("")
        lines.append(f"**语气**: {style_config.get('tone', '专业客观')}")
        lines.append(f"**句式**: {style_config.get('sentence_style', '标准句式')}")
        lines.append(f"**用词**: {style_config.get('vocabulary', '专业术语')}")
        lines.append("")
        lines.append("### 开头短语示例")
        for phrase in self.template["intro_phrases"][:3]:
            if phrase:
                lines.append(f"- {phrase}")
        lines.append("")
        lines.append("### 过渡短语示例")
        for phrase in self.template["transition_phrases"][:3]:
            lines.append(f"- {phrase}")
        lines.append("")
        lines.append("### 总结短语示例")
        for phrase in self.template["conclusion_phrases"]:
            lines.append(f"- {phrase}")
        
        return "\n".join(lines)


class SummaryGenerator:
    """摘要生成器 - 生成执行摘要"""
    
    def __init__(self, report_data: Dict[str, Any] = None):
        """
        初始化摘要生成器
        
        Args:
            report_data: 报告数据
        """
        self.report_data = report_data or {}
    
    def generate_executive_summary(self, industry: str = "行业") -> str:
        """生成1页执行摘要"""
        data = self.report_data
        
        lines = []
        lines.append(f"# {industry}分析 - 执行摘要")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # 核心发现
        lines.append("## 📊 核心发现")
        lines.append("")
        
        overview = data.get("overview", {})
        if overview:
            lines.append(f"- **市场规模**: {overview.get('market_size', '待补充')}")
            lines.append(f"- **增长率**: {overview.get('growth_rate', '待补充')}")
            lines.append(f"- **发展阶段**: {overview.get('stage', '待补充')}")
        else:
            lines.append("- 市场规模：[待补充]")
            lines.append("- 增长率：[待补充]")
            lines.append("- 发展阶段：[待补充]")
        lines.append("")
        
        # 竞争态势
        lines.append("## 🏆 竞争态势")
        lines.append("")
        competition = data.get("competition", {})
        if competition.get("top_players"):
            for player in competition["top_players"][:3]:
                lines.append(f"- {player}")
        else:
            lines.append("- TOP1：[待补充]")
            lines.append("- TOP2：[待补充]")
            lines.append("- TOP3：[待补充]")
        lines.append("")
        
        # SWOT精华
        lines.append("## 💡 战略要点")
        lines.append("")
        swot = data.get("swot", {})
        lines.append(f"- **核心优势**: {swot.get('top_strength', '[待补充]')}")
        lines.append(f"- **主要风险**: {swot.get('top_threat', '[待补充]')}")
        lines.append(f"- **关键机会**: {swot.get('top_opportunity', '[待补充]')}")
        lines.append("")
        
        # 行动建议
        lines.append("## 🎯 行动建议")
        lines.append("")
        recommendations = data.get("recommendations", [])
        if recommendations:
            for i, rec in enumerate(recommendations[:3], 1):
                lines.append(f"{i}. {rec}")
        else:
            lines.append("1. [待补充]")
            lines.append("2. [待补充]")
            lines.append("3. [待补充]")
        lines.append("")
        
        lines.append("---")
        lines.append(f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d')}*")
        
        return "\n".join(lines)
    
    def generate_summary_template(self) -> str:
        """生成摘要模板（供大模型填充）"""
        lines = []
        lines.append("# 执行摘要模板")
        lines.append("")
        lines.append("请根据完整报告内容，填充以下摘要模板：")
        lines.append("")
        lines.append("## 一句话总结")
        lines.append("[用一句话概括行业现状和趋势]")
        lines.append("")
        lines.append("## 三个核心数据")
        lines.append("1. 市场规模：[X亿元]")
        lines.append("2. 增长率：[X%]")
        lines.append("3. 渗透率/集中度：[X%]")
        lines.append("")
        lines.append("## 三个关键洞察")
        lines.append("1. [洞察1]")
        lines.append("2. [洞察2]")
        lines.append("3. [洞察3]")
        lines.append("")
        lines.append("## 三个行动建议")
        lines.append("1. [建议1]")
        lines.append("2. [建议2]")
        lines.append("3. [建议3]")
        lines.append("")
        lines.append("## 风险提示")
        lines.append("[主要风险点]")
        
        return "\n".join(lines)


class InsightExtractor:
    """亮点提取器 - 提取核心洞察"""
    
    # 洞察类型定义
    INSIGHT_TYPES = {
        "market": {
            "name": "市场洞察",
            "keywords": ["市场规模", "增长", "份额", "渗透率", "需求"],
            "icon": "📈"
        },
        "competition": {
            "name": "竞争洞察",
            "keywords": ["竞争", "份额", "头部", "格局", "集中度"],
            "icon": "🏆"
        },
        "technology": {
            "name": "技术洞察",
            "keywords": ["技术", "创新", "研发", "专利", "突破"],
            "icon": "🔬"
        },
        "risk": {
            "name": "风险洞察",
            "keywords": ["风险", "挑战", "威胁", "不确定", "压力"],
            "icon": "⚠️"
        },
        "opportunity": {
            "name": "机会洞察",
            "keywords": ["机会", "机遇", "潜力", "空间", "增长点"],
            "icon": "🎯"
        }
    }
    
    def __init__(self, report_text: str = ""):
        """
        初始化亮点提取器
        
        Args:
            report_text: 报告文本
        """
        self.report_text = report_text
    
    def extract_insights(self, max_insights: int = 5) -> List[Dict]:
        """
        提取核心洞察
        
        Args:
            max_insights: 最大洞察数量
        """
        insights = []
        
        # 按段落分析
        paragraphs = self.report_text.split("\n\n")
        
        for para in paragraphs:
            if len(para) < 50:  # 跳过太短的段落
                continue
            
            # 检测洞察类型
            for insight_type, config in self.INSIGHT_TYPES.items():
                score = sum(1 for kw in config["keywords"] if kw in para)
                if score >= 2:  # 至少匹配2个关键词
                    insights.append({
                        "type": insight_type,
                        "type_name": config["name"],
                        "icon": config["icon"],
                        "content": para[:200] + "..." if len(para) > 200 else para,
                        "score": score
                    })
                    break
        
        # 按分数排序，取前N个
        insights.sort(key=lambda x: x["score"], reverse=True)
        return insights[:max_insights]
    
    def generate_insight_template(self) -> str:
        """生成洞察提取模板"""
        lines = []
        lines.append("# 核心洞察提取指南")
        lines.append("")
        lines.append("请从报告中提取3-5个最重要的洞察，按以下格式输出：")
        lines.append("")
        lines.append("## 洞察类型")
        lines.append("")
        for code, config in self.INSIGHT_TYPES.items():
            lines.append(f"- {config['icon']} **{config['name']}**: {', '.join(config['keywords'][:3])}相关")
        lines.append("")
        lines.append("## 输出格式")
        lines.append("")
        lines.append("```")
        lines.append("### 洞察1: [标题]")
        lines.append("**类型**: [市场/竞争/技术/风险/机会]")
        lines.append("**内容**: [一句话描述]")
        lines.append("**数据支撑**: [相关数据]")
        lines.append("**启示**: [对决策的意义]")
        lines.append("```")
        lines.append("")
        lines.append("## 提取原则")
        lines.append("")
        lines.append("1. **数据优先**: 有数据支撑的洞察优先")
        lines.append("2. **差异化**: 避免重复，覆盖不同维度")
        lines.append("3. **可行动**: 洞察应能指导决策")
        lines.append("4. **时效性**: 优先提取最新趋势")
        
        return "\n".join(lines)
    
    def to_markdown(self, insights: List[Dict] = None) -> str:
        """输出Markdown格式的洞察列表"""
        if insights is None:
            insights = self.extract_insights()
        
        lines = []
        lines.append("# 核心洞察")
        lines.append("")
        
        if not insights:
            lines.append("暂无提取到的洞察。请使用模板手动提取。")
            lines.append("")
            lines.append(self.generate_insight_template())
        else:
            for i, insight in enumerate(insights, 1):
                lines.append(f"## {insight['icon']} 洞察{i}: {insight['type_name']}")
                lines.append("")
                lines.append(insight["content"])
                lines.append("")
        
        return "\n".join(lines)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python report_customizer.py <命令> [参数]")
        print()
        print("命令:")
        print("  config                  - 显示配置选项")
        print("  trim <类型> [报告文件]  - 裁剪报告")
        print("  style <风格>            - 获取风格指南")
        print("  summary [数据文件]      - 生成执行摘要")
        print("  insights [报告文件]     - 提取核心洞察")
        print()
        print("报告类型: full, brief, executive, pest_only, swot_only, competition_only")
        print("风格: formal, concise, data_driven")
        print()
        print("示例:")
        print("  python report_customizer.py config")
        print("  python report_customizer.py trim brief report.md")
        print("  python report_customizer.py style data_driven")
        print("  python report_customizer.py summary data.json")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "config":
        customizer = ReportCustomizer()
        print(customizer.generate_config_prompt())
    
    elif command == "trim":
        report_type = sys.argv[2] if len(sys.argv) > 2 else "brief"
        report_file = sys.argv[3] if len(sys.argv) > 3 else None
        
        if report_file and os.path.exists(report_file):
            with open(report_file, 'r', encoding='utf-8') as f:
                report_text = f.read()
            
            # 根据类型获取要保留的模块
            customizer = ReportCustomizer()
            if report_type in customizer.REPORT_TYPES:
                modules = customizer.REPORT_TYPES[report_type]["modules"]
                keep_sections = [customizer.MODULES[m]["name"] for m in modules]
            else:
                # 自定义模块列表
                keep_sections = report_type.split(",")
            
            trimmer = ReportTrimmer(report_text)
            print(trimmer.trim(keep_sections))
        else:
            # 输出可用的裁剪选项
            customizer = ReportCustomizer()
            print(customizer.get_available_types())
    
    elif command == "style":
        style = sys.argv[2] if len(sys.argv) > 2 else "formal"
        converter = StyleConverter(style)
        print(converter.get_style_guide())
    
    elif command == "summary":
        data_file = sys.argv[2] if len(sys.argv) > 2 else None
        industry = sys.argv[3] if len(sys.argv) > 3 else "行业"
        
        if data_file and os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            generator = SummaryGenerator(data)
            print(generator.generate_executive_summary(industry))
        else:
            generator = SummaryGenerator()
            print(generator.generate_summary_template())
    
    elif command == "insights":
        report_file = sys.argv[2] if len(sys.argv) > 2 else None
        
        if report_file and os.path.exists(report_file):
            with open(report_file, 'r', encoding='utf-8') as f:
                report_text = f.read()
            extractor = InsightExtractor(report_text)
            print(extractor.to_markdown())
        else:
            extractor = InsightExtractor()
            print(extractor.generate_insight_template())
    
    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
