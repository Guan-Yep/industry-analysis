#!/usr/bin/env python3
"""
数据提取器
从用户上传的文本/报告中提取关键数据点
"""

import json
import sys
import re
import os
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime


class DataExtractor:
    """从文本中提取行业分析关键数据"""
    
    # 数据类型定义
    DATA_PATTERNS = {
        "market_size": {
            "name": "市场规模",
            "patterns": [
                r"市场规模[约为达到]*[：:]*\s*(\d+(?:\.\d+)?)\s*(万亿|亿|百万|千万|万)?(?:元|美元|人民币)?",
                r"规模[约为达到]*[：:]*\s*(\d+(?:\.\d+)?)\s*(万亿|亿|百万|千万|万)?",
                r"(\d+(?:\.\d+)?)\s*(万亿|亿|百万|千万|万)?(?:元|美元)?(?:的)?市场",
                r"市场(?:总)?(?:体)?规模.*?(\d+(?:\.\d+)?)\s*(万亿|亿|百万|千万|万)?",
            ],
            "unit": "亿元"
        },
        "growth_rate": {
            "name": "增长率",
            "patterns": [
                r"(?:年均|年)?增长率[约为达到]*[：:]*\s*(\d+(?:\.\d+)?)\s*%",
                r"(?:同比|环比)?增长[约]*\s*(\d+(?:\.\d+)?)\s*%",
                r"CAGR[约为]*[：:]*\s*(\d+(?:\.\d+)?)\s*%",
                r"复合增长率[约为]*[：:]*\s*(\d+(?:\.\d+)?)\s*%",
                r"(\d+(?:\.\d+)?)\s*%\s*(?:的)?(?:年均)?增长",
            ],
            "unit": "%"
        },
        "penetration_rate": {
            "name": "渗透率",
            "patterns": [
                r"渗透率[约为达到]*[：:]*\s*(\d+(?:\.\d+)?)\s*%",
                r"渗透率.*?(\d+(?:\.\d+)?)\s*%",
                r"(\d+(?:\.\d+)?)\s*%\s*(?:的)?渗透率",
            ],
            "unit": "%"
        },
        "market_share": {
            "name": "市场份额",
            "patterns": [
                r"(?:市场)?份额[约为达到]*[：:]*\s*(\d+(?:\.\d+)?)\s*%",
                r"占(?:据)?(?:市场)?[约]*\s*(\d+(?:\.\d+)?)\s*%",
                r"市占率[约为]*[：:]*\s*(\d+(?:\.\d+)?)\s*%",
                r"(\d+(?:\.\d+)?)\s*%\s*(?:的)?(?:市场)?份额",
            ],
            "unit": "%"
        },
        "user_count": {
            "name": "用户规模",
            "patterns": [
                r"用户[数量规模]*[约为达到]*[：:]*\s*(\d+(?:\.\d+)?)\s*(亿|万|千万|百万)?(?:人|户)?",
                r"(\d+(?:\.\d+)?)\s*(亿|万|千万|百万)?(?:用户|人|户)",
                r"活跃用户.*?(\d+(?:\.\d+)?)\s*(亿|万|千万|百万)?",
            ],
            "unit": "万"
        },
        "revenue": {
            "name": "营收",
            "patterns": [
                r"营[业收]*[收入额]*[约为达到]*[：:]*\s*(\d+(?:\.\d+)?)\s*(万亿|亿|百万|千万|万)?(?:元|美元)?",
                r"收入[约为达到]*[：:]*\s*(\d+(?:\.\d+)?)\s*(万亿|亿|百万|千万|万)?(?:元|美元)?",
                r"销售额[约为达到]*[：:]*\s*(\d+(?:\.\d+)?)\s*(万亿|亿|百万|千万|万)?",
            ],
            "unit": "亿元"
        },
        "profit": {
            "name": "利润",
            "patterns": [
                r"(?:净)?利润[约为达到]*[：:]*\s*(\d+(?:\.\d+)?)\s*(万亿|亿|百万|千万|万)?(?:元|美元)?",
                r"利润率[约为达到]*[：:]*\s*(\d+(?:\.\d+)?)\s*%",
            ],
            "unit": "亿元"
        },
        "investment": {
            "name": "投融资",
            "patterns": [
                r"融资[金额总额]*[约为达到]*[：:]*\s*(\d+(?:\.\d+)?)\s*(万亿|亿|百万|千万|万)?(?:元|美元)?",
                r"投资[金额总额]*[约为达到]*[：:]*\s*(\d+(?:\.\d+)?)\s*(万亿|亿|百万|千万|万)?(?:元|美元)?",
                r"获得.*?(\d+(?:\.\d+)?)\s*(万亿|亿|百万|千万|万)?(?:元|美元)?(?:融资|投资)",
            ],
            "unit": "亿元"
        },
        "company_count": {
            "name": "企业数量",
            "patterns": [
                r"企业[数量]*[约为达到]*[：:]*\s*(\d+(?:\.\d+)?)\s*(万|千|百)?(?:家|个)?",
                r"(\d+(?:\.\d+)?)\s*(万|千|百)?(?:家|个)?企业",
                r"玩家[数量]*[约为达到]*[：:]*\s*(\d+(?:\.\d+)?)\s*(万|千|百)?",
            ],
            "unit": "家"
        },
        "year": {
            "name": "年份",
            "patterns": [
                r"(20\d{2})\s*年",
                r"(20\d{2})(?:年度|财年)?",
            ],
            "unit": "年"
        }
    }
    
    # 公司名称模式
    COMPANY_PATTERNS = [
        r"([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)",  # 英文公司名
        r"([\u4e00-\u9fa5]{2,}(?:集团|公司|科技|汽车|电子|网络|互联|控股|股份))",  # 中文公司名
        r"(比亚迪|特斯拉|蔚来|理想|小鹏|华为|腾讯|阿里|百度|字节|美团|京东|拼多多|宁德时代)",  # 知名公司
    ]
    
    def __init__(self, text: str, source: str = "用户上传"):
        """
        初始化数据提取器
        
        Args:
            text: 待提取的文本内容
            source: 数据来源标注
        """
        self.text = text
        self.source = source
        self.extracted_data: Dict[str, List[Dict]] = {}
        self.companies: List[str] = []
        self.extraction_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    def extract_all(self) -> Dict[str, Any]:
        """提取所有类型的数据"""
        result = {
            "source": self.source,
            "extraction_time": self.extraction_time,
            "data": {},
            "companies": [],
            "raw_matches": []
        }
        
        # 提取各类数据
        for data_type, config in self.DATA_PATTERNS.items():
            matches = self._extract_by_patterns(config["patterns"], config.get("unit", ""))
            if matches:
                result["data"][data_type] = {
                    "name": config["name"],
                    "values": matches,
                    "unit": config.get("unit", "")
                }
                result["raw_matches"].extend([
                    {"type": data_type, "match": m} for m in matches
                ])
        
        # 提取公司名称
        result["companies"] = self._extract_companies()
        
        return result
    
    def _extract_by_patterns(self, patterns: List[str], unit: str) -> List[Dict]:
        """根据模式列表提取数据"""
        matches = []
        seen_values = set()
        
        for pattern in patterns:
            for match in re.finditer(pattern, self.text):
                groups = match.groups()
                value = groups[0] if groups else None
                
                if value and value not in seen_values:
                    seen_values.add(value)
                    
                    # 获取上下文
                    start = max(0, match.start() - 50)
                    end = min(len(self.text), match.end() + 50)
                    context = self.text[start:end].replace("\n", " ").strip()
                    
                    # 提取单位（如果有）
                    extracted_unit = groups[1] if len(groups) > 1 and groups[1] else unit
                    
                    matches.append({
                        "value": float(value),
                        "unit": extracted_unit,
                        "context": f"...{context}...",
                        "source": self.source
                    })
        
        return matches
    
    def _extract_companies(self) -> List[str]:
        """提取公司名称"""
        companies = set()
        
        for pattern in self.COMPANY_PATTERNS:
            for match in re.finditer(pattern, self.text):
                company = match.group(1).strip()
                if len(company) >= 2:
                    companies.add(company)
        
        return list(companies)[:20]  # 最多返回20个
    
    def extract_market_data(self) -> Dict[str, Any]:
        """提取市场相关数据（市场规模、增长率、渗透率）"""
        return {
            "market_size": self._extract_by_patterns(
                self.DATA_PATTERNS["market_size"]["patterns"],
                self.DATA_PATTERNS["market_size"]["unit"]
            ),
            "growth_rate": self._extract_by_patterns(
                self.DATA_PATTERNS["growth_rate"]["patterns"],
                self.DATA_PATTERNS["growth_rate"]["unit"]
            ),
            "penetration_rate": self._extract_by_patterns(
                self.DATA_PATTERNS["penetration_rate"]["patterns"],
                self.DATA_PATTERNS["penetration_rate"]["unit"]
            )
        }
    
    def extract_competition_data(self) -> Dict[str, Any]:
        """提取竞争相关数据（市场份额、企业数量）"""
        return {
            "market_share": self._extract_by_patterns(
                self.DATA_PATTERNS["market_share"]["patterns"],
                self.DATA_PATTERNS["market_share"]["unit"]
            ),
            "company_count": self._extract_by_patterns(
                self.DATA_PATTERNS["company_count"]["patterns"],
                self.DATA_PATTERNS["company_count"]["unit"]
            ),
            "companies": self._extract_companies()
        }
    
    def extract_financial_data(self) -> Dict[str, Any]:
        """提取财务相关数据（营收、利润、投融资）"""
        return {
            "revenue": self._extract_by_patterns(
                self.DATA_PATTERNS["revenue"]["patterns"],
                self.DATA_PATTERNS["revenue"]["unit"]
            ),
            "profit": self._extract_by_patterns(
                self.DATA_PATTERNS["profit"]["patterns"],
                self.DATA_PATTERNS["profit"]["unit"]
            ),
            "investment": self._extract_by_patterns(
                self.DATA_PATTERNS["investment"]["patterns"],
                self.DATA_PATTERNS["investment"]["unit"]
            )
        }
    
    def to_markdown(self) -> str:
        """输出Markdown格式的提取结果"""
        data = self.extract_all()
        
        lines = []
        lines.append(f"# 数据提取报告")
        lines.append(f"")
        lines.append(f"- **数据来源**: {data['source']}")
        lines.append(f"- **提取时间**: {data['extraction_time']}")
        lines.append(f"")
        
        # 提取的数据
        lines.append(f"## 提取的关键数据")
        lines.append(f"")
        
        if not data["data"]:
            lines.append("未提取到结构化数据。")
        else:
            for data_type, info in data["data"].items():
                if info["values"]:
                    lines.append(f"### {info['name']}")
                    lines.append(f"")
                    lines.append(f"| 数值 | 单位 | 上下文 |")
                    lines.append(f"|------|------|--------|")
                    for v in info["values"][:5]:  # 最多显示5条
                        context = v["context"][:60] + "..." if len(v["context"]) > 60 else v["context"]
                        lines.append(f"| {v['value']} | {v['unit']} | {context} |")
                    lines.append(f"")
        
        # 识别的公司
        if data["companies"]:
            lines.append(f"## 识别的公司/品牌")
            lines.append(f"")
            lines.append(", ".join(data["companies"]))
            lines.append(f"")
        
        return "\n".join(lines)
    
    def to_analysis_json(self) -> Dict[str, Any]:
        """输出可直接用于分析框架的JSON格式"""
        data = self.extract_all()
        
        # 转换为分析框架可用的格式
        analysis_data = {
            "source": data["source"],
            "extraction_time": data["extraction_time"],
            "overview": {},
            "competition": {
                "companies": data["companies"]
            }
        }
        
        # 市场数据
        if "market_size" in data["data"] and data["data"]["market_size"]["values"]:
            analysis_data["overview"]["market_size"] = data["data"]["market_size"]["values"][0]
        
        if "growth_rate" in data["data"] and data["data"]["growth_rate"]["values"]:
            analysis_data["overview"]["growth_rate"] = data["data"]["growth_rate"]["values"][0]
        
        if "penetration_rate" in data["data"] and data["data"]["penetration_rate"]["values"]:
            analysis_data["overview"]["penetration_rate"] = data["data"]["penetration_rate"]["values"][0]
        
        # 竞争数据
        if "market_share" in data["data"] and data["data"]["market_share"]["values"]:
            analysis_data["competition"]["market_shares"] = data["data"]["market_share"]["values"]
        
        return analysis_data


class DataValidator:
    """数据校验器 - 检查提取数据的合理性"""
    
    # 合理性范围定义
    VALIDATION_RULES = {
        "growth_rate": {
            "min": -50,
            "max": 200,
            "warning_min": -20,
            "warning_max": 100,
            "description": "增长率"
        },
        "penetration_rate": {
            "min": 0,
            "max": 100,
            "warning_min": 0,
            "warning_max": 100,
            "description": "渗透率"
        },
        "market_share": {
            "min": 0,
            "max": 100,
            "warning_min": 0,
            "warning_max": 100,
            "description": "市场份额"
        },
        "market_size": {
            "min": 0,
            "max": 1000000,  # 100万亿
            "warning_min": 0.1,
            "warning_max": 100000,
            "description": "市场规模"
        }
    }
    
    def __init__(self, extracted_data: Dict[str, Any]):
        """
        初始化校验器
        
        Args:
            extracted_data: DataExtractor提取的数据
        """
        self.data = extracted_data
        self.validation_results: List[Dict] = []
    
    def validate_all(self) -> Dict[str, Any]:
        """执行全部校验"""
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "passed": [],
            "summary": ""
        }
        
        data_section = self.data.get("data", {})
        
        for data_type, rule in self.VALIDATION_RULES.items():
            if data_type in data_section:
                for item in data_section[data_type].get("values", []):
                    value = item.get("value", 0)
                    check_result = self._check_value(value, rule, data_type)
                    
                    if check_result["status"] == "error":
                        results["valid"] = False
                        results["errors"].append(check_result)
                    elif check_result["status"] == "warning":
                        results["warnings"].append(check_result)
                    else:
                        results["passed"].append(check_result)
        
        # 生成摘要
        error_count = len(results["errors"])
        warning_count = len(results["warnings"])
        passed_count = len(results["passed"])
        
        if error_count == 0 and warning_count == 0:
            results["summary"] = f"✅ 数据校验通过，共{passed_count}项数据均在合理范围内"
        elif error_count == 0:
            results["summary"] = f"⚠️ 数据基本合理，{warning_count}项需要关注"
        else:
            results["summary"] = f"❌ 发现{error_count}项异常数据，{warning_count}项警告"
        
        return results
    
    def _check_value(self, value: float, rule: Dict, data_type: str) -> Dict:
        """检查单个数值"""
        result = {
            "data_type": data_type,
            "description": rule["description"],
            "value": value,
            "status": "passed",
            "message": ""
        }
        
        if value < rule["min"] or value > rule["max"]:
            result["status"] = "error"
            result["message"] = f"{rule['description']} {value} 超出合理范围 [{rule['min']}, {rule['max']}]"
        elif value < rule["warning_min"] or value > rule["warning_max"]:
            result["status"] = "warning"
            result["message"] = f"{rule['description']} {value} 可能需要核实（通常范围 [{rule['warning_min']}, {rule['warning_max']}]）"
        else:
            result["message"] = f"{rule['description']} {value} 在合理范围内"
        
        return result
    
    def to_markdown(self) -> str:
        """输出Markdown格式的校验报告"""
        results = self.validate_all()
        
        lines = []
        lines.append("# 数据校验报告")
        lines.append("")
        lines.append(f"**校验结果**: {results['summary']}")
        lines.append("")
        
        if results["errors"]:
            lines.append("## ❌ 异常数据")
            lines.append("")
            for err in results["errors"]:
                lines.append(f"- {err['message']}")
            lines.append("")
        
        if results["warnings"]:
            lines.append("## ⚠️ 需要关注")
            lines.append("")
            for warn in results["warnings"]:
                lines.append(f"- {warn['message']}")
            lines.append("")
        
        if results["passed"]:
            lines.append("## ✅ 校验通过")
            lines.append("")
            for p in results["passed"][:10]:
                lines.append(f"- {p['message']}")
            lines.append("")
        
        return "\n".join(lines)


class SourceTracker:
    """数据来源追踪器"""
    
    def __init__(self):
        self.sources: List[Dict] = []
    
    def add_source(self, 
                   source_name: str, 
                   source_type: str = "report",
                   data_points: List[Dict] = None,
                   reliability: str = "medium") -> None:
        """
        添加数据来源
        
        Args:
            source_name: 来源名称
            source_type: 来源类型 (report/news/official/research)
            data_points: 从该来源提取的数据点
            reliability: 可信度 (high/medium/low)
        """
        self.sources.append({
            "name": source_name,
            "type": source_type,
            "data_points": data_points or [],
            "reliability": reliability,
            "added_time": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
    
    def get_source_summary(self) -> Dict[str, Any]:
        """获取来源汇总"""
        summary = {
            "total_sources": len(self.sources),
            "by_type": {},
            "by_reliability": {},
            "sources": self.sources
        }
        
        for source in self.sources:
            # 按类型统计
            s_type = source["type"]
            summary["by_type"][s_type] = summary["by_type"].get(s_type, 0) + 1
            
            # 按可信度统计
            rel = source["reliability"]
            summary["by_reliability"][rel] = summary["by_reliability"].get(rel, 0) + 1
        
        return summary
    
    def to_markdown(self) -> str:
        """输出Markdown格式的来源列表"""
        summary = self.get_source_summary()
        
        lines = []
        lines.append("# 数据来源追踪")
        lines.append("")
        lines.append(f"**总来源数**: {summary['total_sources']}")
        lines.append("")
        
        # 按类型
        lines.append("## 来源类型分布")
        lines.append("")
        type_names = {
            "report": "行业报告",
            "news": "新闻资讯",
            "official": "官方数据",
            "research": "研究论文"
        }
        for t, count in summary["by_type"].items():
            lines.append(f"- {type_names.get(t, t)}: {count}个")
        lines.append("")
        
        # 按可信度
        lines.append("## 可信度分布")
        lines.append("")
        rel_icons = {"high": "🟢", "medium": "🟡", "low": "🔴"}
        for rel, count in summary["by_reliability"].items():
            lines.append(f"- {rel_icons.get(rel, '⚪')} {rel}: {count}个")
        lines.append("")
        
        # 详细列表
        lines.append("## 来源详情")
        lines.append("")
        lines.append("| 来源名称 | 类型 | 可信度 | 数据点数 |")
        lines.append("|----------|------|--------|----------|")
        for source in self.sources:
            lines.append(f"| {source['name']} | {type_names.get(source['type'], source['type'])} | {source['reliability']} | {len(source['data_points'])} |")
        lines.append("")
        
        return "\n".join(lines)
    
    def generate_citations(self) -> str:
        """生成引用格式的来源列表"""
        lines = []
        lines.append("## 数据来源")
        lines.append("")
        
        for i, source in enumerate(self.sources, 1):
            rel_icon = {"high": "★★★", "medium": "★★☆", "low": "★☆☆"}.get(source["reliability"], "★★☆")
            lines.append(f"[{i}] {source['name']} ({rel_icon})")
        
        lines.append("")
        lines.append("*可信度说明: ★★★高 ★★☆中 ★☆☆低*")
        
        return "\n".join(lines)


def main():
    """命令行入口"""
    if len(sys.argv) < 3:
        print("用法: python data_extractor.py <命令> <参数>")
        print()
        print("命令:")
        print("  extract <文本文件>     - 从文本文件提取数据")
        print("  validate <JSON文件>    - 校验提取的数据")
        print("  track <来源JSON文件>   - 生成来源追踪报告")
        print()
        print("示例:")
        print("  python data_extractor.py extract report.txt")
        print("  python data_extractor.py validate extracted_data.json")
        sys.exit(1)
    
    command = sys.argv[1]
    arg = sys.argv[2]
    
    if command == "extract":
        # 从文件读取文本
        if os.path.exists(arg):
            with open(arg, 'r', encoding='utf-8') as f:
                text = f.read()
            source = os.path.basename(arg)
        else:
            text = arg
            source = "命令行输入"
        
        extractor = DataExtractor(text, source)
        
        # 输出格式
        output_format = sys.argv[3] if len(sys.argv) > 3 else "markdown"
        
        if output_format == "json":
            print(json.dumps(extractor.extract_all(), ensure_ascii=False, indent=2))
        elif output_format == "analysis":
            print(json.dumps(extractor.to_analysis_json(), ensure_ascii=False, indent=2))
        else:
            print(extractor.to_markdown())
    
    elif command == "validate":
        # 从JSON文件读取数据
        if os.path.exists(arg):
            with open(arg, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = json.loads(arg)
        
        validator = DataValidator(data)
        
        output_format = sys.argv[3] if len(sys.argv) > 3 else "markdown"
        
        if output_format == "json":
            print(json.dumps(validator.validate_all(), ensure_ascii=False, indent=2))
        else:
            print(validator.to_markdown())
    
    elif command == "track":
        # 从JSON文件读取来源信息
        if os.path.exists(arg):
            with open(arg, 'r', encoding='utf-8') as f:
                sources = json.load(f)
        else:
            sources = json.loads(arg)
        
        tracker = SourceTracker()
        for source in sources:
            tracker.add_source(
                source.get("name", "未知来源"),
                source.get("type", "report"),
                source.get("data_points", []),
                source.get("reliability", "medium")
            )
        
        output_format = sys.argv[3] if len(sys.argv) > 3 else "markdown"
        
        if output_format == "json":
            print(json.dumps(tracker.get_source_summary(), ensure_ascii=False, indent=2))
        elif output_format == "citations":
            print(tracker.generate_citations())
        else:
            print(tracker.to_markdown())
    
    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
