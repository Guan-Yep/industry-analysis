#!/usr/bin/env python3
"""
行业速查卡生成脚本
生成1页精华的行业速查卡，适合快速了解一个行业
"""

import json
import sys
from typing import Dict, Any, List
from datetime import datetime


class QuickCardGenerator:
    """行业速查卡生成器"""
    
    # 发展阶段映射
    STAGE_ICONS = {
        "萌芽期": "🌱",
        "成长期": "📈",
        "快速成长期": "🚀",
        "成熟期": "🏢",
        "衰退期": "📉",
    }
    
    # 趋势判断映射
    TREND_ICONS = {
        "看多": "📈",
        "看平": "➡️",
        "看空": "📉",
        "谨慎": "⚠️",
    }
    
    def __init__(self, industry: str, data: Dict[str, Any] = None):
        """
        初始化速查卡生成器
        
        Args:
            industry: 行业名称
            data: 行业数据（可选）
        """
        self.industry = industry
        self.data = data or {}
        self.report_date = datetime.now().strftime("%Y-%m-%d")
    
    def _get_stage_icon(self, stage: str) -> str:
        """获取发展阶段图标"""
        for key, icon in self.STAGE_ICONS.items():
            if key in stage:
                return icon
        return "📊"
    
    def _get_trend_icon(self, trend: str) -> str:
        """获取趋势判断图标"""
        for key, icon in self.TREND_ICONS.items():
            if key in trend:
                return icon
        return "📊"
    
    def _format_number(self, value: str) -> str:
        """格式化数字显示"""
        # 保持原有格式，确保对齐
        return value.ljust(12)
    
    def generate_ascii_card(self) -> str:
        """生成ASCII格式的速查卡"""
        overview = self.data.get('overview', {})
        competition = self.data.get('competition', {})
        trends = self.data.get('trends', {})
        
        # 提取数据
        market_size = overview.get('china_market_size', 'N/A')
        growth_rate = overview.get('growth_rate', 'N/A')
        stage = overview.get('stage', '成长期')
        penetration = overview.get('penetration', 'N/A')
        
        # 头部玩家
        top_players = competition.get('top_players', [])
        if not top_players:
            top_players = [
                {'name': '企业A', 'share': '30%'},
                {'name': '企业B', 'share': '20%'},
                {'name': '企业C', 'share': '15%'},
            ]
        players_str = " > ".join([f"{p['name']}({p['share']})" for p in top_players[:3]])
        
        # 核心驱动和风险
        drivers = trends.get('drivers', ['技术创新', '政策支持', '需求增长'])
        risks = trends.get('risks', ['竞争加剧', '成本上升', '监管趋严'])
        drivers_str = " + ".join(drivers[:3])
        risks_str = " + ".join(risks[:3])
        
        # 趋势判断
        trend_judgment = trends.get('judgment', '看多')
        trend_advice = trends.get('advice', '关注头部企业')
        trend_icon = self._get_trend_icon(trend_judgment)
        stage_icon = self._get_stage_icon(stage)
        
        # 生成卡片
        card = f"""
╔══════════════════════════════════════════════════════════════════╗
║                 🔍 {self.industry}行业速查卡                      
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  ┌─────────────────┬─────────────────────────────────────────┐  ║
║  │ 📊 市场规模     │ {market_size.ljust(40)}│  ║
║  │ 📈 增长率       │ {growth_rate.ljust(40)}│  ║
║  │ {stage_icon} 发展阶段     │ {stage.ljust(40)}│  ║
║  │ 📍 渗透率       │ {penetration.ljust(40)}│  ║
║  └─────────────────┴─────────────────────────────────────────┘  ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  🏆 头部玩家                                                     ║
║  {players_str.ljust(64)}║
╠══════════════════════════════════════════════════════════════════╣
║  ✅ 核心驱动                                                     ║
║  {drivers_str.ljust(64)}║
║                                                                  ║
║  ⚠️ 主要风险                                                     ║
║  {risks_str.ljust(64)}║
╠══════════════════════════════════════════════════════════════════╣
║  {trend_icon} 趋势判断: {trend_judgment.ljust(8)} │ 💡 {trend_advice.ljust(38)}║
╠══════════════════════════════════════════════════════════════════╣
║  📅 更新时间: {self.report_date}                                         ║
╚══════════════════════════════════════════════════════════════════╝
"""
        return card
    
    def generate_markdown_card(self) -> str:
        """生成Markdown格式的速查卡"""
        overview = self.data.get('overview', {})
        competition = self.data.get('competition', {})
        trends = self.data.get('trends', {})
        
        # 提取数据
        market_size = overview.get('china_market_size', 'N/A')
        growth_rate = overview.get('growth_rate', 'N/A')
        stage = overview.get('stage', '成长期')
        penetration = overview.get('penetration', 'N/A')
        stage_icon = self._get_stage_icon(stage)
        
        # 头部玩家
        top_players = competition.get('top_players', [])
        if not top_players:
            top_players = [
                {'name': '企业A', 'share': '30%'},
                {'name': '企业B', 'share': '20%'},
                {'name': '企业C', 'share': '15%'},
            ]
        
        # 核心驱动和风险
        drivers = trends.get('drivers', ['技术创新', '政策支持', '需求增长'])
        risks = trends.get('risks', ['竞争加剧', '成本上升', '监管趋严'])
        
        # 趋势判断
        trend_judgment = trends.get('judgment', '看多')
        trend_advice = trends.get('advice', '关注头部企业')
        trend_icon = self._get_trend_icon(trend_judgment)
        
        card = f"""# 🔍 {self.industry}行业速查卡

> 📅 更新时间：{self.report_date}

---

## 📊 核心数据

| 指标 | 数值 |
|------|------|
| 市场规模 | {market_size} |
| 增长率 | {growth_rate} |
| 发展阶段 | {stage_icon} {stage} |
| 渗透率 | {penetration} |

---

## 🏆 头部玩家

| 排名 | 企业 | 市场份额 |
|------|------|----------|
"""
        for i, player in enumerate(top_players[:5]):
            card += f"| {i+1} | {player['name']} | {player['share']} |\n"
        
        card += f"""
---

## ✅ 核心驱动因素

"""
        for i, driver in enumerate(drivers[:5]):
            card += f"{i+1}. {driver}\n"
        
        card += f"""
---

## ⚠️ 主要风险

"""
        for i, risk in enumerate(risks[:5]):
            card += f"{i+1}. {risk}\n"
        
        card += f"""
---

## {trend_icon} 趋势判断

- **整体判断**：{trend_judgment}
- **投资建议**：{trend_advice}

---

## 💡 一句话总结

> {overview.get('summary', f'{self.industry}市场处于{stage}，建议持续关注行业动态。')}
"""
        return card
    
    def generate_json_card(self) -> Dict[str, Any]:
        """生成JSON格式的速查卡数据"""
        overview = self.data.get('overview', {})
        competition = self.data.get('competition', {})
        trends = self.data.get('trends', {})
        
        return {
            "industry": self.industry,
            "update_date": self.report_date,
            "core_metrics": {
                "market_size": overview.get('china_market_size', 'N/A'),
                "growth_rate": overview.get('growth_rate', 'N/A'),
                "stage": overview.get('stage', '成长期'),
                "penetration": overview.get('penetration', 'N/A'),
            },
            "top_players": competition.get('top_players', []),
            "drivers": trends.get('drivers', []),
            "risks": trends.get('risks', []),
            "trend": {
                "judgment": trends.get('judgment', '看多'),
                "advice": trends.get('advice', '关注头部企业'),
            },
            "summary": overview.get('summary', ''),
        }


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python quick_card_generator.py <行业名称> [数据JSON文件] [--format=ascii|markdown|json]")
        print()
        print("示例:")
        print('  python quick_card_generator.py "新能源汽车"')
        print('  python quick_card_generator.py "新能源汽车" data.json')
        print('  python quick_card_generator.py "新能源汽车" data.json --format=markdown')
        print('  python quick_card_generator.py "新能源汽车" --format=json')
        print()
        print("输出格式:")
        print("  ascii    - ASCII艺术卡片（默认）")
        print("  markdown - Markdown格式")
        print("  json     - JSON数据格式")
        sys.exit(1)
    
    industry = sys.argv[1]
    
    # 解析参数
    data = {}
    output_format = "ascii"
    
    for arg in sys.argv[2:]:
        if arg.startswith("--format="):
            output_format = arg.split("=")[1]
        elif arg.endswith('.json'):
            with open(arg, 'r', encoding='utf-8') as f:
                data = json.load(f)
    
    # 生成速查卡
    generator = QuickCardGenerator(industry, data)
    
    if output_format == "markdown":
        print(generator.generate_markdown_card())
    elif output_format == "json":
        print(json.dumps(generator.generate_json_card(), ensure_ascii=False, indent=2))
    else:
        print(generator.generate_ascii_card())


if __name__ == "__main__":
    main()
