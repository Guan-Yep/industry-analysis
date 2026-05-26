#!/usr/bin/env python3
"""
竞品分析矩阵生成脚本
生成竞品对比表格、定位分析、差异化洞察
"""

import json
import sys
from typing import Dict, Any, List
from datetime import datetime


class CompetitorMatrix:
    """竞品分析矩阵生成器"""
    
    # 评分等级
    SCORE_LEVELS = {
        5: "★★★★★",
        4: "★★★★☆",
        3: "★★★☆☆",
        2: "★★☆☆☆",
        1: "★☆☆☆☆",
        0: "☆☆☆☆☆",
    }
    
    # 默认对比维度
    DEFAULT_DIMENSIONS = [
        "产品力",
        "技术实力",
        "品牌影响力",
        "渠道能力",
        "价格竞争力",
        "服务质量",
        "市场份额",
        "增长势头",
    ]
    
    def __init__(self, industry: str, competitors: List[Dict[str, Any]] = None):
        """
        初始化竞品分析器
        
        Args:
            industry: 行业名称
            competitors: 竞品数据列表
        """
        self.industry = industry
        self.competitors = competitors or []
        self.report_date = datetime.now().strftime("%Y-%m-%d")
    
    def _get_score_stars(self, score: int) -> str:
        """将分数转换为星级显示"""
        score = max(0, min(5, score))
        return self.SCORE_LEVELS.get(score, "★★★☆☆")
    
    def _calculate_total_score(self, scores: Dict[str, int]) -> float:
        """计算综合得分"""
        if not scores:
            return 0
        return sum(scores.values()) / len(scores)
    
    def generate_comparison_table(self, dimensions: List[str] = None) -> str:
        """
        生成竞品对比表格（Markdown格式）
        
        Args:
            dimensions: 对比维度列表
            
        Returns:
            Markdown表格
        """
        dims = dimensions or self.DEFAULT_DIMENSIONS
        
        if not self.competitors:
            return "暂无竞品数据"
        
        # 表头
        header = "| 维度 |"
        separator = "|------|"
        for comp in self.competitors:
            header += f" {comp.get('name', '竞品')} |"
            separator += "------|"
        
        # 表格内容
        rows = []
        for dim in dims:
            row = f"| {dim} |"
            for comp in self.competitors:
                scores = comp.get('scores', {})
                score = scores.get(dim, 3)
                row += f" {self._get_score_stars(score)} |"
            rows.append(row)
        
        # 综合得分行
        total_row = "| **综合得分** |"
        for comp in self.competitors:
            scores = comp.get('scores', {})
            # 只计算实际有的维度
            relevant_scores = {k: v for k, v in scores.items() if k in dims}
            total = self._calculate_total_score(relevant_scores)
            total_row += f" **{total:.1f}/5** |"
        rows.append(total_row)
        
        return f"{header}\n{separator}\n" + "\n".join(rows)
    
    def generate_basic_info_table(self) -> str:
        """生成竞品基本信息表格"""
        if not self.competitors:
            return "暂无竞品数据"
        
        table = """| 企业 | 成立时间 | 融资阶段 | 估值/市值 | 员工规模 | 核心业务 |
|------|----------|----------|-----------|----------|----------|
"""
        for comp in self.competitors:
            info = comp.get('info', {})
            table += f"| {comp.get('name', 'N/A')} | {info.get('founded', 'N/A')} | {info.get('funding', 'N/A')} | {info.get('valuation', 'N/A')} | {info.get('employees', 'N/A')} | {info.get('core_business', 'N/A')} |\n"
        
        return table
    
    def generate_product_comparison(self) -> str:
        """生成产品对比表格"""
        if not self.competitors:
            return "暂无竞品数据"
        
        table = """| 企业 | 主要产品 | 定价区间 | 目标客户 | 核心卖点 |
|------|----------|----------|----------|----------|
"""
        for comp in self.competitors:
            product = comp.get('product', {})
            table += f"| {comp.get('name', 'N/A')} | {product.get('main_product', 'N/A')} | {product.get('price_range', 'N/A')} | {product.get('target_customer', 'N/A')} | {product.get('usp', 'N/A')} |\n"
        
        return table
    
    def generate_swot_comparison(self) -> str:
        """生成各竞品SWOT对比"""
        if not self.competitors:
            return "暂无竞品数据"
        
        result = ""
        for comp in self.competitors:
            swot = comp.get('swot', {})
            name = comp.get('name', '竞品')
            
            result += f"""
### {name} SWOT分析

| 优势 (Strengths) | 劣势 (Weaknesses) |
|------------------|-------------------|
"""
            strengths = swot.get('strengths', ['待分析'])
            weaknesses = swot.get('weaknesses', ['待分析'])
            max_len = max(len(strengths), len(weaknesses))
            
            for i in range(max_len):
                s = strengths[i] if i < len(strengths) else ""
                w = weaknesses[i] if i < len(weaknesses) else ""
                result += f"| {s} | {w} |\n"
            
            result += """
| 机会 (Opportunities) | 威胁 (Threats) |
|----------------------|----------------|
"""
            opportunities = swot.get('opportunities', ['待分析'])
            threats = swot.get('threats', ['待分析'])
            max_len = max(len(opportunities), len(threats))
            
            for i in range(max_len):
                o = opportunities[i] if i < len(opportunities) else ""
                t = threats[i] if i < len(threats) else ""
                result += f"| {o} | {t} |\n"
            
            result += "\n"
        
        return result
    
    def generate_positioning_quadrant(self) -> str:
        """生成竞争定位象限图（Mermaid）"""
        if not self.competitors:
            return "暂无竞品数据"
        
        code = """```mermaid
quadrantChart
    title 竞争定位矩阵
    x-axis 低价格 --> 高价格
    y-axis 低品质 --> 高品质
    quadrant-1 高端市场
    quadrant-2 性价比市场
    quadrant-3 低端市场
    quadrant-4 溢价市场
"""
        for comp in self.competitors:
            positioning = comp.get('positioning', {})
            x = positioning.get('price', 0.5)
            y = positioning.get('quality', 0.5)
            name = comp.get('name', '竞品')
            code += f"    {name}: [{x}, {y}]\n"
        
        code += "```"
        return code
    
    def generate_radar_description(self) -> str:
        """生成雷达图数据描述（供其他工具渲染）"""
        if not self.competitors:
            return "暂无竞品数据"
        
        result = "### 竞品能力雷达图数据\n\n"
        result += "| 企业 | " + " | ".join(self.DEFAULT_DIMENSIONS[:6]) + " |\n"
        result += "|------|" + "|".join(["------"] * 6) + "|\n"
        
        for comp in self.competitors:
            scores = comp.get('scores', {})
            row = f"| {comp.get('name', 'N/A')} |"
            for dim in self.DEFAULT_DIMENSIONS[:6]:
                score = scores.get(dim, 3)
                row += f" {score} |"
            result += row + "\n"
        
        return result
    
    def generate_differentiation_analysis(self) -> str:
        """生成差异化分析"""
        if not self.competitors:
            return "暂无竞品数据"
        
        result = """## 差异化分析

### 各竞品差异化定位

| 企业 | 差异化策略 | 核心优势 | 目标市场 |
|------|------------|----------|----------|
"""
        for comp in self.competitors:
            diff = comp.get('differentiation', {})
            result += f"| {comp.get('name', 'N/A')} | {diff.get('strategy', 'N/A')} | {diff.get('core_advantage', 'N/A')} | {diff.get('target_market', 'N/A')} |\n"
        
        result += """
### 竞争要点总结

"""
        # 找出各维度的领先者
        if len(self.competitors) >= 2:
            for dim in self.DEFAULT_DIMENSIONS[:5]:
                max_score = 0
                leader = ""
                for comp in self.competitors:
                    score = comp.get('scores', {}).get(dim, 0)
                    if score > max_score:
                        max_score = score
                        leader = comp.get('name', '')
                if leader:
                    result += f"- **{dim}领先者**：{leader}（{max_score}/5分）\n"
        
        return result
    
    def generate_strategy_recommendations(self) -> str:
        """生成竞争策略建议"""
        result = """## 竞争策略建议

### 市场进入策略

| 策略类型 | 适用情况 | 具体建议 |
|----------|----------|----------|
| 差异化竞争 | 市场存在未被满足的需求 | 聚焦特定细分市场，打造差异化产品 |
| 成本领先 | 具备规模或效率优势 | 通过降本增效获取价格竞争力 |
| 聚焦战略 | 资源有限但有独特能力 | 深耕垂直领域，建立专业壁垒 |
| 快速跟随 | 市场验证完成但未饱和 | 学习领先者经验，快速复制优化 |

### 针对主要竞品的应对策略

"""
        for comp in self.competitors:
            name = comp.get('name', '竞品')
            strategy = comp.get('counter_strategy', {})
            result += f"""#### 针对{name}

- **竞争要点**：{strategy.get('key_point', '待分析')}
- **应对策略**：{strategy.get('response', '待分析')}
- **注意事项**：{strategy.get('caution', '待分析')}

"""
        return result
    
    def generate_full_report(self) -> str:
        """生成完整的竞品分析报告"""
        report = f"""# {self.industry}行业竞品分析报告

> 📅 分析时间：{self.report_date}
> 📊 分析对象：{', '.join([c.get('name', '') for c in self.competitors])}

---

## 一、竞品概览

### 1.1 基本信息

{self.generate_basic_info_table()}

### 1.2 产品对比

{self.generate_product_comparison()}

---

## 二、能力对比分析

### 2.1 综合能力评分

{self.generate_comparison_table()}

### 2.2 能力雷达图数据

{self.generate_radar_description()}

---

## 三、竞争定位分析

### 3.1 市场定位矩阵

{self.generate_positioning_quadrant()}

{self.generate_differentiation_analysis()}

---

## 四、各竞品SWOT分析

{self.generate_swot_comparison()}

---

{self.generate_strategy_recommendations()}

---

## 五、关键洞察

### 5.1 竞争格局判断

- **市场集中度**：[高/中/低]
- **竞争激烈程度**：[激烈/一般/温和]
- **格局稳定性**：[稳定/变化中/动荡]

### 5.2 核心结论

1. [结论1]
2. [结论2]
3. [结论3]

### 5.3 行动建议

1. [建议1]
2. [建议2]
3. [建议3]

---

## 附录：数据来源

| 数据类型 | 来源 | 时间 |
|----------|------|------|
| 企业信息 | [来源] | {self.report_date} |
| 市场数据 | [来源] | {self.report_date} |
| 产品信息 | [来源] | {self.report_date} |
"""
        return report


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python competitor_matrix.py <行业名称> [数据JSON文件] [--output=full|table|positioning|swot]")
        print()
        print("示例:")
        print('  python competitor_matrix.py "新能源汽车"')
        print('  python competitor_matrix.py "新能源汽车" competitors.json')
        print('  python competitor_matrix.py "新能源汽车" competitors.json --output=table')
        print()
        print("输出类型:")
        print("  full        - 完整竞品分析报告（默认）")
        print("  table       - 仅输出对比表格")
        print("  positioning - 仅输出定位分析")
        print("  swot        - 仅输出SWOT对比")
        print()
        print("数据JSON格式示例:")
        print("""
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
        "strengths": ["垂直整合", "成本优势", "产能规模"],
        "weaknesses": ["品牌高端化不足", "智能化起步较晚"],
        "opportunities": ["海外市场", "高端市场"],
        "threats": ["价格战", "技术迭代"]
      },
      "differentiation": {
        "strategy": "成本领先+全产业链",
        "core_advantage": "电池自研自产",
        "target_market": "大众市场"
      },
      "counter_strategy": {
        "key_point": "规模优势难以复制",
        "response": "聚焦细分市场差异化",
        "caution": "避免正面价格战"
      }
    }
  ]
}
""")
        sys.exit(1)
    
    industry = sys.argv[1]
    
    # 解析参数
    competitors = []
    output_type = "full"
    
    for arg in sys.argv[2:]:
        if arg.startswith("--output="):
            output_type = arg.split("=")[1]
        elif arg.endswith('.json'):
            with open(arg, 'r', encoding='utf-8') as f:
                data = json.load(f)
                competitors = data.get('competitors', [])
    
    # 生成分析
    matrix = CompetitorMatrix(industry, competitors)
    
    if output_type == "table":
        print(matrix.generate_comparison_table())
    elif output_type == "positioning":
        print(matrix.generate_positioning_quadrant())
        print()
        print(matrix.generate_differentiation_analysis())
    elif output_type == "swot":
        print(matrix.generate_swot_comparison())
    else:
        print(matrix.generate_full_report())


if __name__ == "__main__":
    main()
