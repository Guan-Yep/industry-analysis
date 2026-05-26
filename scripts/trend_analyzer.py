#!/usr/bin/env python3
"""
趋势洞察模块
支持Hype Cycle、趋势预测、时机矩阵、风险预警
"""

import json
import sys
import os
from typing import Dict, Any, List, Optional
from datetime import datetime


class HypeCycleGenerator:
    """Gartner技术成熟度曲线生成器"""
    
    # Hype Cycle阶段定义
    PHASES = {
        "trigger": {
            "name": "技术萌芽期",
            "name_en": "Innovation Trigger",
            "position": 0.1,
            "height": 0.2,
            "description": "技术突破启动，早期概念验证和媒体关注",
            "characteristics": ["概念验证", "早期投资", "媒体炒作开始"],
            "strategy": "关注技术动态，评估技术可行性"
        },
        "peak": {
            "name": "期望膨胀期",
            "name_en": "Peak of Inflated Expectations",
            "position": 0.25,
            "height": 1.0,
            "description": "过度热情和不切实际的期望",
            "characteristics": ["大量投资涌入", "媒体热炒", "泡沫形成"],
            "strategy": "谨慎评估，避免盲目跟风"
        },
        "trough": {
            "name": "泡沫破裂期",
            "name_en": "Trough of Disillusionment",
            "position": 0.45,
            "height": 0.15,
            "description": "实验失败，兴趣减退",
            "characteristics": ["投资减少", "负面报道", "企业退出"],
            "strategy": "逆向布局，寻找被低估的机会"
        },
        "slope": {
            "name": "稳步爬升期",
            "name_en": "Slope of Enlightenment",
            "position": 0.7,
            "height": 0.5,
            "description": "技术优势逐渐清晰，商业模式成熟",
            "characteristics": ["第二代产品", "最佳实践形成", "商业化加速"],
            "strategy": "积极布局，建立竞争壁垒"
        },
        "plateau": {
            "name": "生产成熟期",
            "name_en": "Plateau of Productivity",
            "position": 0.9,
            "height": 0.6,
            "description": "主流采用开始，技术价值被广泛认可",
            "characteristics": ["规模化应用", "市场成熟", "标准化"],
            "strategy": "优化运营，追求规模效益"
        }
    }
    
    def __init__(self, technologies: List[Dict[str, Any]] = None):
        """
        初始化Hype Cycle生成器
        
        Args:
            technologies: 技术列表，每项包含name和phase
        """
        self.technologies = technologies or []
    
    def add_technology(self, name: str, phase: str, description: str = "") -> None:
        """添加技术到曲线"""
        if phase in self.PHASES:
            self.technologies.append({
                "name": name,
                "phase": phase,
                "description": description
            })
    
    def generate_ascii_curve(self) -> str:
        """生成ASCII版本的Hype Cycle曲线"""
        width = 70
        height = 15
        
        # 创建画布
        canvas = [[' ' for _ in range(width)] for _ in range(height)]
        
        # 绘制曲线（简化版）
        curve_points = [
            (5, 12),   # 起点
            (10, 8),   # 上升
            (15, 2),   # 峰值
            (20, 4),   # 下降
            (30, 13),  # 谷底
            (45, 8),   # 爬升
            (55, 6),   # 稳定
            (65, 6),   # 终点
        ]
        
        # 连接曲线点
        for i in range(len(curve_points) - 1):
            x1, y1 = curve_points[i]
            x2, y2 = curve_points[i + 1]
            
            # 简单线性插值
            steps = abs(x2 - x1)
            for step in range(steps + 1):
                x = x1 + step
                y = int(y1 + (y2 - y1) * step / steps) if steps > 0 else y1
                if 0 <= x < width and 0 <= y < height:
                    canvas[y][x] = '─' if abs(y2 - y1) < abs(x2 - x1) else '│'
        
        # 标记关键点
        markers = [
            (10, 8, "①"),
            (15, 2, "②"),
            (30, 13, "③"),
            (45, 8, "④"),
            (60, 6, "⑤"),
        ]
        for x, y, marker in markers:
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = marker
        
        # 添加技术标注
        tech_positions = {
            "trigger": (8, 10),
            "peak": (13, 0),
            "trough": (28, 14),
            "slope": (43, 10),
            "plateau": (58, 8),
        }
        
        for tech in self.technologies[:5]:  # 最多标注5个技术
            phase = tech["phase"]
            if phase in tech_positions:
                x, y = tech_positions[phase]
                name = tech["name"][:8]  # 截断名称
                for i, char in enumerate(name):
                    if x + i < width:
                        canvas[y][x + i] = char
        
        lines = []
        lines.append("  Gartner技术成熟度曲线 (Hype Cycle)")
        lines.append("")
        lines.append("  期望值")
        lines.append("    ↑")
        
        for row in canvas:
            lines.append("    " + "".join(row))
        
        lines.append("    " + "─" * width + "→ 时间")
        lines.append("")
        lines.append("  阶段说明:")
        lines.append("  ① 技术萌芽期  ② 期望膨胀期  ③ 泡沫破裂期  ④ 稳步爬升期  ⑤ 生产成熟期")
        
        return "\n".join(lines)
    
    def generate_mermaid_quadrant(self) -> str:
        """生成Mermaid象限图表示Hype Cycle位置"""
        lines = []
        lines.append("```mermaid")
        lines.append("quadrantChart")
        lines.append("    title 技术成熟度分布")
        lines.append("    x-axis 成熟度低 --> 成熟度高")
        lines.append("    y-axis 期望值低 --> 期望值高")
        lines.append("    quadrant-1 期望膨胀期")
        lines.append("    quadrant-2 生产成熟期")
        lines.append("    quadrant-3 技术萌芽期")
        lines.append("    quadrant-4 稳步爬升期")
        
        for tech in self.technologies:
            phase = tech["phase"]
            phase_config = self.PHASES.get(phase, {})
            x = phase_config.get("position", 0.5)
            y = phase_config.get("height", 0.5)
            lines.append(f"    {tech['name']}: [{x:.2f}, {y:.2f}]")
        
        lines.append("```")
        return "\n".join(lines)
    
    def generate_analysis_report(self) -> str:
        """生成技术成熟度分析报告"""
        lines = []
        lines.append("# 技术成熟度分析报告")
        lines.append("")
        lines.append(self.generate_ascii_curve())
        lines.append("")
        
        # 按阶段分组
        by_phase = {phase: [] for phase in self.PHASES}
        for tech in self.technologies:
            if tech["phase"] in by_phase:
                by_phase[tech["phase"]].append(tech)
        
        lines.append("## 技术分布详情")
        lines.append("")
        
        for phase, config in self.PHASES.items():
            techs = by_phase[phase]
            lines.append(f"### {config['name']} ({config['name_en']})")
            lines.append("")
            lines.append(f"**特征**: {config['description']}")
            lines.append(f"**策略建议**: {config['strategy']}")
            lines.append("")
            
            if techs:
                lines.append("**相关技术**:")
                for tech in techs:
                    desc = f" - {tech['description']}" if tech.get('description') else ""
                    lines.append(f"- {tech['name']}{desc}")
            else:
                lines.append("*暂无技术处于此阶段*")
            lines.append("")
        
        return "\n".join(lines)
    
    def get_phase_template(self) -> str:
        """获取阶段判断模板"""
        lines = []
        lines.append("# 技术成熟度阶段判断指南")
        lines.append("")
        lines.append("请根据以下特征判断技术所处阶段：")
        lines.append("")
        
        for phase, config in self.PHASES.items():
            lines.append(f"## {config['name']} ({phase})")
            lines.append("")
            lines.append(f"**定义**: {config['description']}")
            lines.append("")
            lines.append("**判断特征**:")
            for char in config['characteristics']:
                lines.append(f"- {char}")
            lines.append("")
            lines.append(f"**建议策略**: {config['strategy']}")
            lines.append("")
        
        return "\n".join(lines)


class TrendPredictor:
    """趋势预测器 - 技术/市场/政策三维度"""
    
    DIMENSIONS = {
        "technology": {
            "name": "技术趋势",
            "icon": "🔬",
            "factors": [
                "核心技术突破",
                "技术成本下降",
                "技术标准化进程",
                "专利布局变化",
                "研发投入趋势"
            ]
        },
        "market": {
            "name": "市场趋势",
            "icon": "📈",
            "factors": [
                "市场规模增长",
                "用户需求变化",
                "竞争格局演变",
                "商业模式创新",
                "价格走势"
            ]
        },
        "policy": {
            "name": "政策趋势",
            "icon": "🏛️",
            "factors": [
                "产业政策方向",
                "监管政策变化",
                "补贴政策调整",
                "国际贸易政策",
                "环保政策要求"
            ]
        }
    }
    
    def __init__(self, industry: str = "行业"):
        """
        初始化趋势预测器
        
        Args:
            industry: 行业名称
        """
        self.industry = industry
        self.predictions: Dict[str, List[Dict]] = {
            "technology": [],
            "market": [],
            "policy": []
        }
    
    def add_prediction(self, dimension: str, prediction: str, 
                       timeframe: str = "1-3年", confidence: str = "medium") -> None:
        """
        添加趋势预测
        
        Args:
            dimension: 维度 (technology/market/policy)
            prediction: 预测内容
            timeframe: 时间范围
            confidence: 置信度 (high/medium/low)
        """
        if dimension in self.predictions:
            self.predictions[dimension].append({
                "content": prediction,
                "timeframe": timeframe,
                "confidence": confidence
            })
    
    def generate_prediction_template(self) -> str:
        """生成趋势预测模板"""
        lines = []
        lines.append(f"# {self.industry}趋势预测模板")
        lines.append("")
        lines.append("请根据以下框架进行未来3年趋势预测：")
        lines.append("")
        
        for dim, config in self.DIMENSIONS.items():
            lines.append(f"## {config['icon']} {config['name']}")
            lines.append("")
            lines.append("### 分析要点")
            for factor in config['factors']:
                lines.append(f"- {factor}")
            lines.append("")
            lines.append("### 预测模板")
            lines.append("")
            lines.append("| 时间范围 | 预测内容 | 置信度 | 依据 |")
            lines.append("|----------|----------|--------|------|")
            lines.append("| 1年内 | [预测1] | 高/中/低 | [数据/趋势] |")
            lines.append("| 1-3年 | [预测2] | 高/中/低 | [数据/趋势] |")
            lines.append("| 3-5年 | [预测3] | 高/中/低 | [数据/趋势] |")
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_prediction_report(self) -> str:
        """生成趋势预测报告"""
        lines = []
        lines.append(f"# {self.industry}趋势预测报告")
        lines.append("")
        lines.append(f"*生成时间: {datetime.now().strftime('%Y-%m-%d')}*")
        lines.append("")
        
        confidence_icons = {"high": "🟢", "medium": "🟡", "low": "🔴"}
        
        for dim, config in self.DIMENSIONS.items():
            preds = self.predictions[dim]
            lines.append(f"## {config['icon']} {config['name']}")
            lines.append("")
            
            if preds:
                lines.append("| 预测内容 | 时间范围 | 置信度 |")
                lines.append("|----------|----------|--------|")
                for pred in preds:
                    icon = confidence_icons.get(pred['confidence'], '⚪')
                    lines.append(f"| {pred['content']} | {pred['timeframe']} | {icon} {pred['confidence']} |")
            else:
                lines.append("*暂无预测数据，请使用模板填充*")
            lines.append("")
        
        return "\n".join(lines)


class TimingMatrix:
    """时机矩阵 - 进入时机评估"""
    
    # 时机评估维度
    DIMENSIONS = {
        "market_maturity": {
            "name": "市场成熟度",
            "levels": {
                "early": {"name": "早期", "score": 1, "risk": "高", "opportunity": "高"},
                "growth": {"name": "成长期", "score": 2, "risk": "中", "opportunity": "高"},
                "mature": {"name": "成熟期", "score": 3, "risk": "低", "opportunity": "中"},
                "decline": {"name": "衰退期", "score": 4, "risk": "中", "opportunity": "低"}
            }
        },
        "competition": {
            "name": "竞争强度",
            "levels": {
                "low": {"name": "低", "score": 1, "entry_barrier": "低"},
                "medium": {"name": "中", "score": 2, "entry_barrier": "中"},
                "high": {"name": "高", "score": 3, "entry_barrier": "高"},
                "extreme": {"name": "极高", "score": 4, "entry_barrier": "极高"}
            }
        },
        "technology_readiness": {
            "name": "技术成熟度",
            "levels": {
                "experimental": {"name": "实验阶段", "score": 1},
                "pilot": {"name": "试点阶段", "score": 2},
                "commercial": {"name": "商业化", "score": 3},
                "mainstream": {"name": "主流应用", "score": 4}
            }
        },
        "resource_requirement": {
            "name": "资源要求",
            "levels": {
                "low": {"name": "低", "score": 1},
                "medium": {"name": "中", "score": 2},
                "high": {"name": "高", "score": 3},
                "extreme": {"name": "极高", "score": 4}
            }
        }
    }
    
    # 进入时机建议
    TIMING_RECOMMENDATIONS = {
        "now": {
            "name": "立即进入",
            "icon": "🟢",
            "description": "市场窗口期，建议立即行动",
            "conditions": "市场成长期 + 竞争强度低/中 + 技术商业化"
        },
        "prepare": {
            "name": "积极准备",
            "icon": "🟡",
            "description": "做好准备，等待合适时机",
            "conditions": "市场早期 + 技术试点阶段"
        },
        "wait": {
            "name": "观望等待",
            "icon": "🟠",
            "description": "持续关注，暂不投入大量资源",
            "conditions": "竞争极高 或 技术实验阶段"
        },
        "avoid": {
            "name": "暂不建议",
            "icon": "🔴",
            "description": "当前不是好的进入时机",
            "conditions": "市场衰退期 或 资源要求极高"
        }
    }
    
    def __init__(self, industry: str = "行业"):
        """
        初始化时机矩阵
        
        Args:
            industry: 行业名称
        """
        self.industry = industry
        self.assessments: Dict[str, str] = {}
    
    def set_assessment(self, dimension: str, level: str) -> None:
        """设置评估结果"""
        if dimension in self.DIMENSIONS:
            if level in self.DIMENSIONS[dimension]["levels"]:
                self.assessments[dimension] = level
    
    def calculate_timing(self) -> Dict[str, Any]:
        """计算进入时机建议"""
        if not self.assessments:
            return {"recommendation": "unknown", "reason": "缺少评估数据"}
        
        # 简单评分逻辑
        total_score = 0
        for dim, level in self.assessments.items():
            if dim in self.DIMENSIONS and level in self.DIMENSIONS[dim]["levels"]:
                total_score += self.DIMENSIONS[dim]["levels"][level]["score"]
        
        avg_score = total_score / len(self.assessments) if self.assessments else 0
        
        # 特殊条件检查
        market = self.assessments.get("market_maturity", "")
        competition = self.assessments.get("competition", "")
        tech = self.assessments.get("technology_readiness", "")
        
        if market == "decline":
            return {"recommendation": "avoid", "reason": "市场处于衰退期"}
        
        if competition == "extreme" and tech in ["experimental", "pilot"]:
            return {"recommendation": "wait", "reason": "竞争激烈且技术不成熟"}
        
        if market in ["growth"] and competition in ["low", "medium"] and tech in ["commercial", "mainstream"]:
            return {"recommendation": "now", "reason": "市场成长期，竞争适中，技术成熟"}
        
        if market == "early" or tech in ["experimental", "pilot"]:
            return {"recommendation": "prepare", "reason": "市场或技术尚在早期"}
        
        if avg_score <= 2:
            return {"recommendation": "now", "reason": "综合评估适合进入"}
        elif avg_score <= 2.5:
            return {"recommendation": "prepare", "reason": "建议做好准备"}
        elif avg_score <= 3:
            return {"recommendation": "wait", "reason": "建议观望"}
        else:
            return {"recommendation": "avoid", "reason": "当前不建议进入"}
    
    def generate_matrix_template(self) -> str:
        """生成时机评估模板"""
        lines = []
        lines.append(f"# {self.industry}进入时机评估")
        lines.append("")
        lines.append("请对以下维度进行评估：")
        lines.append("")
        
        for dim, config in self.DIMENSIONS.items():
            lines.append(f"## {config['name']}")
            lines.append("")
            lines.append("| 等级 | 说明 |")
            lines.append("|------|------|")
            for level, level_config in config['levels'].items():
                lines.append(f"| `{level}` | {level_config['name']} |")
            lines.append("")
        
        lines.append("## 时机建议说明")
        lines.append("")
        for rec, config in self.TIMING_RECOMMENDATIONS.items():
            lines.append(f"- {config['icon']} **{config['name']}**: {config['description']}")
        lines.append("")
        
        return "\n".join(lines)
    
    def generate_assessment_report(self) -> str:
        """生成时机评估报告"""
        timing = self.calculate_timing()
        rec_config = self.TIMING_RECOMMENDATIONS.get(timing["recommendation"], {})
        
        lines = []
        lines.append(f"# {self.industry}进入时机评估报告")
        lines.append("")
        
        # 评估结果
        lines.append("## 📊 评估结果")
        lines.append("")
        lines.append(f"**建议**: {rec_config.get('icon', '⚪')} {rec_config.get('name', '未知')}")
        lines.append(f"**原因**: {timing['reason']}")
        lines.append("")
        
        # 各维度评估
        lines.append("## 📋 各维度评估")
        lines.append("")
        lines.append("| 维度 | 评估结果 |")
        lines.append("|------|----------|")
        
        for dim, config in self.DIMENSIONS.items():
            level = self.assessments.get(dim, "未评估")
            if level in config["levels"]:
                level_name = config["levels"][level]["name"]
            else:
                level_name = level
            lines.append(f"| {config['name']} | {level_name} |")
        lines.append("")
        
        # 建议说明
        lines.append("## 💡 建议说明")
        lines.append("")
        lines.append(rec_config.get("description", ""))
        lines.append("")
        lines.append(f"**适用条件**: {rec_config.get('conditions', '')}")
        
        return "\n".join(lines)


class RiskWarning:
    """风险预警清单生成器"""
    
    # 风险类型定义
    RISK_TYPES = {
        "market": {
            "name": "市场风险",
            "icon": "📉",
            "common_risks": [
                "市场需求不及预期",
                "市场增速放缓",
                "价格战导致利润下滑",
                "替代品威胁"
            ]
        },
        "technology": {
            "name": "技术风险",
            "icon": "⚙️",
            "common_risks": [
                "技术路线变更",
                "核心技术突破不及预期",
                "技术标准不确定",
                "知识产权纠纷"
            ]
        },
        "policy": {
            "name": "政策风险",
            "icon": "📜",
            "common_risks": [
                "补贴政策退坡",
                "监管政策收紧",
                "贸易政策变化",
                "环保要求提高"
            ]
        },
        "competition": {
            "name": "竞争风险",
            "icon": "⚔️",
            "common_risks": [
                "巨头入场",
                "行业整合加速",
                "人才竞争加剧",
                "供应链被卡脖子"
            ]
        },
        "operation": {
            "name": "运营风险",
            "icon": "🔧",
            "common_risks": [
                "供应链中断",
                "成本上涨",
                "人才流失",
                "现金流压力"
            ]
        }
    }
    
    # 风险等级
    RISK_LEVELS = {
        "critical": {"name": "严重", "icon": "🔴", "action": "立即应对"},
        "high": {"name": "高", "icon": "🟠", "action": "重点关注"},
        "medium": {"name": "中", "icon": "🟡", "action": "持续监控"},
        "low": {"name": "低", "icon": "🟢", "action": "定期检查"}
    }
    
    def __init__(self, industry: str = "行业"):
        """
        初始化风险预警器
        
        Args:
            industry: 行业名称
        """
        self.industry = industry
        self.risks: List[Dict] = []
    
    def add_risk(self, risk_type: str, description: str, 
                 level: str = "medium", mitigation: str = "") -> None:
        """
        添加风险项
        
        Args:
            risk_type: 风险类型
            description: 风险描述
            level: 风险等级
            mitigation: 应对措施
        """
        self.risks.append({
            "type": risk_type,
            "description": description,
            "level": level,
            "mitigation": mitigation
        })
    
    def generate_risk_template(self) -> str:
        """生成风险评估模板"""
        lines = []
        lines.append(f"# {self.industry}风险评估模板")
        lines.append("")
        lines.append("请对以下风险类型进行评估：")
        lines.append("")
        
        for risk_type, config in self.RISK_TYPES.items():
            lines.append(f"## {config['icon']} {config['name']}")
            lines.append("")
            lines.append("**常见风险点**:")
            for risk in config['common_risks']:
                lines.append(f"- {risk}")
            lines.append("")
            lines.append("**评估模板**:")
            lines.append("")
            lines.append("| 风险描述 | 等级 | 应对措施 |")
            lines.append("|----------|------|----------|")
            lines.append("| [具体风险] | 严重/高/中/低 | [应对措施] |")
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_warning_report(self) -> str:
        """生成风险预警报告"""
        lines = []
        lines.append(f"# {self.industry}风险预警清单")
        lines.append("")
        lines.append(f"*更新时间: {datetime.now().strftime('%Y-%m-%d')}*")
        lines.append("")
        
        # 按等级分组
        by_level = {level: [] for level in self.RISK_LEVELS}
        for risk in self.risks:
            level = risk.get("level", "medium")
            if level in by_level:
                by_level[level].append(risk)
        
        # 风险汇总
        lines.append("## 📊 风险汇总")
        lines.append("")
        total = len(self.risks)
        for level, config in self.RISK_LEVELS.items():
            count = len(by_level[level])
            lines.append(f"- {config['icon']} {config['name']}风险: {count}项")
        lines.append(f"- **总计**: {total}项")
        lines.append("")
        
        # 详细清单
        lines.append("## 📋 详细清单")
        lines.append("")
        
        for level, config in self.RISK_LEVELS.items():
            risks = by_level[level]
            if risks:
                lines.append(f"### {config['icon']} {config['name']}风险 ({config['action']})")
                lines.append("")
                lines.append("| 类型 | 风险描述 | 应对措施 |")
                lines.append("|------|----------|----------|")
                for risk in risks:
                    type_name = self.RISK_TYPES.get(risk['type'], {}).get('name', risk['type'])
                    mitigation = risk.get('mitigation', '待制定')
                    lines.append(f"| {type_name} | {risk['description']} | {mitigation} |")
                lines.append("")
        
        return "\n".join(lines)
    
    def generate_ascii_matrix(self) -> str:
        """生成ASCII风险矩阵"""
        lines = []
        lines.append("  风险矩阵")
        lines.append("")
        lines.append("  影响程度")
        lines.append("    高 │ ⚠️ 中风险  │ 🔴 高风险  │ 🔴 严重风险")
        lines.append("       │           │           │")
        lines.append("    中 │ 🟢 低风险  │ ⚠️ 中风险  │ 🔴 高风险")
        lines.append("       │           │           │")
        lines.append("    低 │ 🟢 可接受  │ 🟢 低风险  │ ⚠️ 中风险")
        lines.append("       └───────────┴───────────┴───────────→")
        lines.append("              低         中         高")
        lines.append("                    发生概率")
        
        return "\n".join(lines)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python trend_analyzer.py <命令> [参数]")
        print()
        print("命令:")
        print("  hype [技术JSON]        - 生成Hype Cycle分析")
        print("  predict [行业名称]     - 生成趋势预测模板")
        print("  timing [行业名称]      - 生成时机评估模板")
        print("  risk [行业名称]        - 生成风险预警模板")
        print()
        print("示例:")
        print("  python trend_analyzer.py hype techs.json")
        print('  python trend_analyzer.py predict "新能源汽车"')
        print('  python trend_analyzer.py timing "新能源汽车"')
        print('  python trend_analyzer.py risk "新能源汽车"')
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "hype":
        tech_file = sys.argv[2] if len(sys.argv) > 2 else None
        
        generator = HypeCycleGenerator()
        
        if tech_file and os.path.exists(tech_file):
            with open(tech_file, 'r', encoding='utf-8') as f:
                techs = json.load(f)
            for tech in techs:
                generator.add_technology(
                    tech.get("name", ""),
                    tech.get("phase", "trigger"),
                    tech.get("description", "")
                )
            print(generator.generate_analysis_report())
        else:
            print(generator.get_phase_template())
    
    elif command == "predict":
        industry = sys.argv[2] if len(sys.argv) > 2 else "行业"
        predictor = TrendPredictor(industry)
        print(predictor.generate_prediction_template())
    
    elif command == "timing":
        industry = sys.argv[2] if len(sys.argv) > 2 else "行业"
        
        if len(sys.argv) > 3 and os.path.exists(sys.argv[3]):
            with open(sys.argv[3], 'r', encoding='utf-8') as f:
                assessments = json.load(f)
            matrix = TimingMatrix(industry)
            for dim, level in assessments.items():
                matrix.set_assessment(dim, level)
            print(matrix.generate_assessment_report())
        else:
            matrix = TimingMatrix(industry)
            print(matrix.generate_matrix_template())
    
    elif command == "risk":
        industry = sys.argv[2] if len(sys.argv) > 2 else "行业"
        
        if len(sys.argv) > 3 and os.path.exists(sys.argv[3]):
            with open(sys.argv[3], 'r', encoding='utf-8') as f:
                risks = json.load(f)
            warning = RiskWarning(industry)
            for risk in risks:
                warning.add_risk(
                    risk.get("type", "market"),
                    risk.get("description", ""),
                    risk.get("level", "medium"),
                    risk.get("mitigation", "")
                )
            print(warning.generate_warning_report())
        else:
            warning = RiskWarning(industry)
            print(warning.generate_risk_template())
            print()
            print(warning.generate_ascii_matrix())
    
    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
