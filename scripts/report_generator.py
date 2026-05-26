#!/usr/bin/env python3
"""
行业分析报告生成脚本
根据收集的数据生成结构化的行业分析报告
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional, Union


class IndustryReportGenerator:
    """行业分析报告生成器"""
    
    def __init__(self, industry: str, data: Dict[str, Any]):
        """
        初始化报告生成器
        
        Args:
            industry: 行业名称
            data: 分析数据字典
        """
        self.industry = industry
        self.data = data
        self.report_date = datetime.now().strftime("%Y年%m月")
    
    def generate_cover(self) -> str:
        """生成报告封面"""
        return f"""# {self.industry}行业分析报告

**报告日期**：{self.report_date}
**分析周期**：{self.data.get('period', '2024-2025年')}
**报告版本**：V1.0

---

"""
    
    def generate_toc(self) -> str:
        """生成目录"""
        return """## 目录

- [一、行业概览](#一行业概览)
  - [1.1 行业概况](#11-行业概况)
  - [1.2 行业基本数据](#12-行业基本数据)
  - [1.3 行业痛点](#13-行业痛点)
  - [1.4 商业模式](#14-商业模式)
  - [1.5 产业链位置](#15-产业链位置)
- [二、PEST环境分析](#二pest环境分析)
  - [2.1 政治法规环境](#21-政治法规环境)
  - [2.2 经济环境](#22-经济环境)
  - [2.3 社会文化环境](#23-社会文化环境)
  - [2.4 技术环境](#24-技术环境)
- [三、BCG矩阵分析](#三bcg矩阵分析)
- [四、SWOT战略分析](#四swot战略分析)
- [五、总结与建议](#五总结与建议)

---

"""
    
    def generate_overview_section(self) -> str:
        """生成行业概览章节"""
        overview = self.data.get('overview', {})
        
        section = f"""## 一、行业概览

### 1.1 行业概况

#### 行业定义

{overview.get('definition', f'{self.industry}是指...')}

#### 发展历程

{overview.get('history', '行业发展历程...')}

#### 当前发展阶段

{overview.get('stage', '当前处于成长期/成熟期...')}

#### 核心特征

{self._format_list(overview.get('characteristics', ['特征1', '特征2', '特征3']))}

### 1.2 行业基本数据

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| 全球市场规模 | {overview.get('global_market_size', 'X亿美元')} | {overview.get('data_source', '行业报告')} |
| 中国市场规模 | {overview.get('china_market_size', 'X亿元')} | {overview.get('data_source', '行业报告')} |
| 同比增长率 | {overview.get('growth_rate', 'X%')} | {overview.get('data_source', '行业报告')} |
| 预测CAGR | {overview.get('cagr', 'X%')} | {overview.get('data_source', '行业报告')} |

### 1.3 行业痛点

{self._format_pain_points(overview.get('pain_points', {}))}

### 1.4 商业模式

{overview.get('business_model', '主要商业模式描述...')}

### 1.5 产业链位置

{overview.get('industry_chain', '产业链描述...')}

{self._generate_chain_mermaid(overview.get('chain_data', {}))}

---

"""
        return section
    
    def generate_pest_section(self) -> str:
        """生成PEST分析章节"""
        pest = self.data.get('pest', {})
        
        section = f"""## 二、PEST环境分析

### 2.1 政治法规环境 (Political)

{pest.get('political', '政治法规环境分析...')}

### 2.2 经济环境 (Economic)

{pest.get('economic', '经济环境分析...')}

### 2.3 社会文化环境 (Social)

{pest.get('social', '社会文化环境分析...')}

### 2.4 技术环境 (Technological)

{pest.get('technological', '技术环境分析...')}

### 2.5 PEST综合评估

| 维度 | 机会 | 威胁 | 影响程度 |
|------|------|------|----------|
| Political | {pest.get('p_opportunity', '-')} | {pest.get('p_threat', '-')} | {pest.get('p_impact', '中')} |
| Economic | {pest.get('e_opportunity', '-')} | {pest.get('e_threat', '-')} | {pest.get('e_impact', '中')} |
| Social | {pest.get('s_opportunity', '-')} | {pest.get('s_threat', '-')} | {pest.get('s_impact', '中')} |
| Technological | {pest.get('t_opportunity', '-')} | {pest.get('t_threat', '-')} | {pest.get('t_impact', '中')} |

{self._generate_pest_mermaid(pest)}

---

"""
        return section
    
    def generate_bcg_section(self) -> str:
        """生成BCG矩阵分析章节"""
        bcg = self.data.get('bcg', {})
        
        section = f"""## 三、BCG矩阵分析

### 3.1 市场定位分析

{bcg.get('analysis', 'BCG矩阵分析...')}

### 3.2 各象限企业/业务

#### 明星业务 (Stars)
{bcg.get('stars', '- 高增长、高份额的业务/企业')}

#### 现金牛业务 (Cash Cows)
{bcg.get('cash_cows', '- 低增长、高份额的业务/企业')}

#### 问题业务 (Question Marks)
{bcg.get('question_marks', '- 高增长、低份额的业务/企业')}

#### 瘦狗业务 (Dogs)
{bcg.get('dogs', '- 低增长、低份额的业务/企业')}

### 3.3 战略建议

{bcg.get('strategy', 'BCG战略建议...')}

{self._generate_bcg_mermaid(bcg.get('companies', []))}

---

"""
        return section
    
    def generate_swot_section(self) -> str:
        """生成SWOT分析章节"""
        swot = self.data.get('swot', {})
        
        section = f"""## 四、SWOT战略分析

### 4.1 优势分析 (Strengths)

{self._format_list(swot.get('strengths', ['优势1', '优势2', '优势3']))}

### 4.2 劣势分析 (Weaknesses)

{self._format_list(swot.get('weaknesses', ['劣势1', '劣势2', '劣势3']))}

### 4.3 机会分析 (Opportunities)

{self._format_list(swot.get('opportunities', ['机会1', '机会2', '机会3']))}

### 4.4 威胁分析 (Threats)

{self._format_list(swot.get('threats', ['威胁1', '威胁2', '威胁3']))}

### 4.5 交叉策略分析

#### 优势-机会 (SO) 策略

{swot.get('so_strategy', 'SO策略分析...')}

#### 劣势-机会 (WO) 策略

{swot.get('wo_strategy', 'WO策略分析...')}

#### 优势-威胁 (ST) 策略

{swot.get('st_strategy', 'ST策略分析...')}

#### 劣势-威胁 (WT) 策略

{swot.get('wt_strategy', 'WT策略分析...')}

### 4.6 综合战略建议

{swot.get('overall_strategy', '综合战略建议...')}

{self._generate_swot_mermaid(swot)}

---

"""
        return section
    
    def generate_conclusion_section(self) -> str:
        """生成总结与建议章节"""
        conclusion = self.data.get('conclusion', {})
        
        section = f"""## 五、总结与建议

### 5.1 关键洞察

{self._format_numbered_list(conclusion.get('insights', ['洞察1', '洞察2', '洞察3', '洞察4']))}

### 5.2 战略建议

#### 短期建议（1年内）

{self._format_list(conclusion.get('short_term', ['短期建议1', '短期建议2']))}

#### 中期建议（1-3年）

{self._format_list(conclusion.get('mid_term', ['中期建议1', '中期建议2']))}

#### 长期建议（3年以上）

{self._format_list(conclusion.get('long_term', ['长期建议1', '长期建议2']))}

### 5.3 风险提示

| 风险类型 | 风险描述 | 发生概率 | 影响程度 | 应对措施 |
|----------|----------|----------|----------|----------|
{self._format_risk_table(conclusion.get('risks', []))}

---

## 附录

### 数据来源

{self._format_list(self.data.get('sources', ['公开资料整理', '行业研究报告']))}

### 免责声明

本报告基于公开信息和数据分析编制，仅供参考。报告中的观点和结论不构成任何投资建议。

"""
        return section
    
    def generate_full_report(self) -> str:
        """生成完整报告"""
        report = ""
        report += self.generate_cover()
        report += self.generate_toc()
        report += self.generate_overview_section()
        report += self.generate_pest_section()
        report += self.generate_bcg_section()
        report += self.generate_swot_section()
        report += self.generate_conclusion_section()
        return report
    
    # 辅助方法
    def _format_list(self, items: List[str]) -> str:
        """格式化无序列表"""
        return "\n".join(f"- {item}" for item in items)
    
    def _format_numbered_list(self, items: List[Any]) -> str:
        """格式化有序列表"""
        result = []
        for i, item in enumerate(items):
            if isinstance(item, dict):
                # 处理字典格式的洞察
                title = item.get('title', f'洞察{i+1}')
                content = item.get('content', '')
                result.append(f"{i+1}. **{title}**：{content}")
            else:
                result.append(f"{i+1}. {item}")
        return "\n".join(result)
    
    def _format_pain_points(self, pain_points: Dict[str, List[str]]) -> str:
        """格式化痛点分析"""
        result = ""
        categories = {
            'technical': '#### 技术层面痛点',
            'business': '#### 商业层面痛点',
            'user': '#### 用户层面痛点',
            'regulatory': '#### 监管层面痛点'
        }
        for key, title in categories.items():
            points = pain_points.get(key, [])
            if points:
                result += f"\n{title}\n\n"
                result += self._format_list(points) + "\n"
        return result if result else "暂无痛点分析数据"
    
    def _format_risk_table(self, risks: List[Dict[str, str]]) -> str:
        """格式化风险表格"""
        if not risks:
            return "| - | - | - | - | - |"
        rows = []
        for risk in risks:
            rows.append(
                f"| {risk.get('type', '-')} | {risk.get('description', '-')} | "
                f"{risk.get('probability', '-')} | {risk.get('impact', '-')} | "
                f"{risk.get('mitigation', '-')} |"
            )
        return "\n".join(rows)
    
    def _generate_chain_mermaid(self, chain_data: Dict) -> str:
        """生成产业链Mermaid图"""
        upstream = chain_data.get('upstream', ['原材料', '技术', '设备'])
        midstream = chain_data.get('midstream', ['核心企业'])
        downstream = chain_data.get('downstream', ['企业客户', '个人消费者'])
        
        code = f"""
```mermaid
%%{{init: {{'theme': 'base', 'themeVariables': {{ 'primaryColor': '#4A90D9'}}}}}}%%
flowchart TB
    subgraph 上游["上游供应商"]
"""
        for i, item in enumerate(upstream):
            code += f"        A{i+1}[{item}]\n"
        
        code += f"""    end
    
    subgraph 中游["{self.industry}核心"]
"""
        for i, item in enumerate(midstream):
            code += f"        B{i+1}[{item}]\n"
        
        code += """    end
    
    subgraph 下游["下游客户"]
"""
        for i, item in enumerate(downstream):
            code += f"        C{i+1}[{item}]\n"
        
        code += "    end\n\n"
        
        for i in range(len(upstream)):
            for j in range(len(midstream)):
                code += f"    A{i+1} --> B{j+1}\n"
        
        for i in range(len(midstream)):
            for j in range(len(downstream)):
                code += f"    B{i+1} --> C{j+1}\n"
        
        code += "```\n"
        return code
    
    def _generate_pest_mermaid(self, pest: Dict) -> str:
        """生成PEST思维导图"""
        return f"""
```mermaid
mindmap
  root((PEST分析))
    Political
      {pest.get('p_key1', '政策法规')}
      {pest.get('p_key2', '监管要求')}
      {pest.get('p_key3', '行业标准')}
    Economic
      {pest.get('e_key1', '市场规模')}
      {pest.get('e_key2', '消费能力')}
      {pest.get('e_key3', '投融资')}
    Social
      {pest.get('s_key1', '消费观念')}
      {pest.get('s_key2', '生活方式')}
      {pest.get('s_key3', '人口结构')}
    Technological
      {pest.get('t_key1', '核心技术')}
      {pest.get('t_key2', '数字化')}
      {pest.get('t_key3', '新兴技术')}
```
"""
    
    def _generate_bcg_mermaid(self, companies: List[Dict]) -> str:
        """生成BCG矩阵图"""
        if not companies:
            companies = [
                {"name": "企业A", "market_share": 0.7, "growth_rate": 0.8},
                {"name": "企业B", "market_share": 0.3, "growth_rate": 0.7},
                {"name": "企业C", "market_share": 0.8, "growth_rate": 0.3},
                {"name": "企业D", "market_share": 0.2, "growth_rate": 0.2},
            ]
        
        code = """
```mermaid
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
            code += f"    {company['name']}: [{company['market_share']}, {company['growth_rate']}]\n"
        
        code += "```\n"
        return code
    
    def _generate_swot_mermaid(self, swot: Dict) -> str:
        """生成SWOT思维导图"""
        strengths = swot.get('strengths', ['优势1', '优势2'])[:3]
        weaknesses = swot.get('weaknesses', ['劣势1', '劣势2'])[:3]
        opportunities = swot.get('opportunities', ['机会1', '机会2'])[:3]
        threats = swot.get('threats', ['威胁1', '威胁2'])[:3]
        
        code = """
```mermaid
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
        
        code += "```\n"
        return code


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python report_generator.py <行业名称> [数据JSON文件]")
        print()
        print("示例:")
        print("  python report_generator.py \"新能源汽车\"")
        print("  python report_generator.py \"GUI Agent\" data.json")
        print()
        print("如果不提供数据文件，将生成模板报告")
        sys.exit(1)
    
    industry = sys.argv[1]
    
    # 加载数据
    if len(sys.argv) > 2:
        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        # 使用空数据生成模板
        data = {}
    
    # 生成报告
    generator = IndustryReportGenerator(industry, data)
    report = generator.generate_full_report()
    
    print(report)


if __name__ == "__main__":
    main()
