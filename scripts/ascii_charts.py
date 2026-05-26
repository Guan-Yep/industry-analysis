#!/usr/bin/env python3
"""
ASCII图表生成脚本
生成兼容性强的ASCII艺术图表，适用于所有平台
"""

import json
import sys
import os
from typing import Dict, Any, List, Tuple
from math import ceil


class ASCIICharts:
    """ASCII图表生成器"""
    
    # 柱状图字符
    BAR_FULL = "█"
    BAR_HALF = "▌"
    BAR_EMPTY = "░"
    
    # 线条字符
    LINE_H = "─"
    LINE_V = "│"
    CORNER_TL = "┌"
    CORNER_TR = "┐"
    CORNER_BL = "└"
    CORNER_BR = "┘"
    T_DOWN = "┬"
    T_UP = "┴"
    T_RIGHT = "├"
    T_LEFT = "┤"
    CROSS = "┼"
    
    # 箭头
    ARROW_RIGHT = "→"
    ARROW_LEFT = "←"
    ARROW_UP = "↑"
    ARROW_DOWN = "↓"
    
    @staticmethod
    def bar_chart(
        data: List[Dict[str, Any]],
        title: str = "柱状图",
        max_width: int = 40,
        show_values: bool = True
    ) -> str:
        """
        生成ASCII柱状图
        
        Args:
            data: 数据列表，每项包含 label 和 value
            title: 图表标题
            max_width: 最大柱宽
            show_values: 是否显示数值
            
        Returns:
            ASCII柱状图字符串
        """
        if not data:
            return "暂无数据"
        
        # 计算最大值和标签宽度
        max_value = max(item.get('value', 0) for item in data)
        max_label_len = max(len(str(item.get('label', ''))) for item in data)
        
        if max_value == 0:
            max_value = 1
        
        lines = []
        lines.append(f"  {title}")
        lines.append(f"  {'─' * (max_width + max_label_len + 10)}")
        
        for item in data:
            label = str(item.get('label', '')).ljust(max_label_len)
            value = item.get('value', 0)
            
            # 计算柱宽
            bar_width = int((value / max_value) * max_width)
            bar = ASCIICharts.BAR_FULL * bar_width + ASCIICharts.BAR_EMPTY * (max_width - bar_width)
            
            if show_values:
                lines.append(f"  {label} │{bar}│ {value}")
            else:
                lines.append(f"  {label} │{bar}│")
        
        lines.append(f"  {'─' * (max_width + max_label_len + 10)}")
        
        return "\n".join(lines)
    
    @staticmethod
    def horizontal_bar_chart(
        data: List[Dict[str, Any]],
        title: str = "数据对比",
        max_width: int = 30
    ) -> str:
        """
        生成水平柱状对比图
        
        Args:
            data: 数据列表
            title: 标题
            max_width: 最大宽度
            
        Returns:
            ASCII图表
        """
        if not data:
            return "暂无数据"
        
        max_value = max(item.get('value', 0) for item in data)
        if max_value == 0:
            max_value = 1
        
        lines = []
        lines.append(f"┌{'─' * (max_width + 20)}┐")
        lines.append(f"│  {title.center(max_width + 16)}│")
        lines.append(f"├{'─' * (max_width + 20)}┤")
        
        for item in data:
            label = str(item.get('label', ''))[:10].ljust(10)
            value = item.get('value', 0)
            percent = (value / max_value) * 100
            
            bar_len = int((value / max_value) * max_width)
            bar = "█" * bar_len + "░" * (max_width - bar_len)
            
            lines.append(f"│ {label} {bar} {value:>6} ({percent:>5.1f}%)│")
        
        lines.append(f"└{'─' * (max_width + 20)}┘")
        
        return "\n".join(lines)
    
    @staticmethod
    def pie_chart_text(
        data: List[Dict[str, Any]],
        title: str = "占比分布"
    ) -> str:
        """
        生成饼图的文本表示（条形占比图）
        
        Args:
            data: 数据列表，每项包含 label 和 value/percent
            title: 标题
            
        Returns:
            ASCII占比图
        """
        if not data:
            return "暂无数据"
        
        # 计算总和和百分比
        total = sum(item.get('value', item.get('percent', 0)) for item in data)
        if total == 0:
            total = 100
        
        lines = []
        lines.append(f"┌{'─' * 50}┐")
        lines.append(f"│  {title.center(46)}│")
        lines.append(f"├{'─' * 50}┤")
        
        bar_total_width = 30
        
        for item in data:
            label = str(item.get('label', ''))[:12].ljust(12)
            value = item.get('value', item.get('percent', 0))
            percent = (value / total) * 100 if total > 0 else 0
            
            bar_len = int((percent / 100) * bar_total_width)
            bar = "█" * bar_len + "░" * (bar_total_width - bar_len)
            
            lines.append(f"│ {label} {bar} {percent:>5.1f}% │")
        
        lines.append(f"├{'─' * 50}┤")
        lines.append(f"│  {'总计'.ljust(10)} {' ' * 30} 100.0% │")
        lines.append(f"└{'─' * 50}┘")
        
        return "\n".join(lines)
    
    @staticmethod
    def trend_chart(
        labels: List[str],
        values: List[float],
        title: str = "趋势图",
        height: int = 10,
        width: int = 50
    ) -> str:
        """
        生成ASCII趋势图（折线图效果）
        
        Args:
            labels: X轴标签
            values: 数值列表
            title: 标题
            height: 图表高度
            width: 图表宽度
            
        Returns:
            ASCII趋势图
        """
        if not values:
            return "暂无数据"
        
        min_val = min(values)
        max_val = max(values)
        if max_val == min_val:
            max_val = min_val + 1
        
        # 归一化到高度范围
        normalized = [int((v - min_val) / (max_val - min_val) * (height - 1)) for v in values]
        
        # 计算每个数据点的X位置
        step = max(1, (width - 10) // len(values))
        
        lines = []
        lines.append(f"  {title}")
        lines.append("")
        
        # 绘制图表
        for row in range(height - 1, -1, -1):
            # Y轴标签
            if row == height - 1:
                y_label = f"{max_val:>8.0f}"
            elif row == 0:
                y_label = f"{min_val:>8.0f}"
            else:
                y_label = " " * 8
            
            line = f"{y_label} │"
            
            for i, n in enumerate(normalized):
                if n == row:
                    line += "●"
                elif n > row and i > 0 and normalized[i-1] < row:
                    line += "/"
                elif n < row and i > 0 and normalized[i-1] > row:
                    line += "\\"
                else:
                    line += " "
                line += " " * (step - 1)
            
            lines.append(line)
        
        # X轴
        lines.append(f"{'─' * 9}┼{'─' * (len(values) * step + 5)}")
        
        # X轴标签
        x_labels = "          "
        for i, label in enumerate(labels):
            x_labels += str(label)[:step].ljust(step)
        lines.append(x_labels)
        
        return "\n".join(lines)
    
    @staticmethod
    def quadrant_chart(
        items: List[Dict[str, Any]],
        title: str = "四象限图",
        q1_name: str = "象限一",
        q2_name: str = "象限二",
        q3_name: str = "象限三",
        q4_name: str = "象限四",
        x_label: str = "X轴",
        y_label: str = "Y轴"
    ) -> str:
        """
        生成ASCII四象限图
        
        Args:
            items: 数据点列表，每项包含 name, x, y (0-1范围)
            title: 标题
            q1-q4_name: 四个象限的名称
            x_label, y_label: 坐标轴标签
            
        Returns:
            ASCII四象限图
        """
        width = 60
        height = 20
        half_w = width // 2
        half_h = height // 2
        
        # 创建画布
        canvas = [[' ' for _ in range(width)] for _ in range(height)]
        
        # 绘制坐标轴
        for i in range(width):
            canvas[half_h][i] = '─'
        for i in range(height):
            canvas[i][half_w] = '│'
        canvas[half_h][half_w] = '┼'
        
        # 放置数据点
        for item in items:
            x = item.get('x', 0.5)
            y = item.get('y', 0.5)
            name = item.get('name', '?')[:3]
            
            # 转换坐标
            px = int(x * (width - 4)) + 2
            py = int((1 - y) * (height - 2)) + 1
            
            px = max(2, min(width - 4, px))
            py = max(1, min(height - 2, py))
            
            # 放置名称
            for i, c in enumerate(name):
                if 0 <= px + i < width:
                    canvas[py][px + i] = c
        
        lines = []
        lines.append(f"  {title.center(width)}")
        lines.append("")
        lines.append(f"  {y_label}")
        lines.append(f"  ↑")
        
        # 象限标签
        canvas[2][5:5+len(q2_name)] = list(q2_name[:10])
        canvas[2][half_w+5:half_w+5+len(q1_name)] = list(q1_name[:10])
        canvas[half_h+2][5:5+len(q3_name)] = list(q3_name[:10])
        canvas[half_h+2][half_w+5:half_w+5+len(q4_name)] = list(q4_name[:10])
        
        for row in canvas:
            lines.append("  " + "".join(row))
        
        lines.append(f"  {' ' * half_w}{x_label} →")
        
        return "\n".join(lines)
    
    @staticmethod
    def flow_chart(
        stages: List[str],
        title: str = "流程图"
    ) -> str:
        """
        生成ASCII流程图（水平）
        
        Args:
            stages: 流程阶段列表
            title: 标题
            
        Returns:
            ASCII流程图
        """
        if not stages:
            return "暂无数据"
        
        lines = []
        lines.append(f"  {title}")
        lines.append("")
        
        # 计算框宽度
        max_len = max(len(s) for s in stages)
        box_width = max(max_len + 4, 12)
        
        # 顶部边框
        top_line = "  "
        for i, stage in enumerate(stages):
            top_line += "┌" + "─" * box_width + "┐"
            if i < len(stages) - 1:
                top_line += "    "
        lines.append(top_line)
        
        # 内容行
        content_line = "  "
        for i, stage in enumerate(stages):
            content_line += "│" + stage.center(box_width) + "│"
            if i < len(stages) - 1:
                content_line += " ──→ "
        lines.append(content_line)
        
        # 底部边框
        bottom_line = "  "
        for i, stage in enumerate(stages):
            bottom_line += "└" + "─" * box_width + "┘"
            if i < len(stages) - 1:
                bottom_line += "    "
        lines.append(bottom_line)
        
        return "\n".join(lines)
    
    @staticmethod
    def vertical_flow_chart(
        stages: List[Dict[str, Any]],
        title: str = "流程图"
    ) -> str:
        """
        生成垂直ASCII流程图
        
        Args:
            stages: 流程阶段列表，每项包含 name 和可选的 items
            title: 标题
            
        Returns:
            ASCII流程图
        """
        if not stages:
            return "暂无数据"
        
        box_width = 40
        
        lines = []
        lines.append(f"  {title}")
        lines.append("")
        
        for i, stage in enumerate(stages):
            name = stage if isinstance(stage, str) else stage.get('name', '')
            items = [] if isinstance(stage, str) else stage.get('items', [])
            
            # 顶部
            lines.append(f"  ┌{'─' * box_width}┐")
            lines.append(f"  │{name.center(box_width)}│")
            
            if items:
                lines.append(f"  │{' ' * box_width}│")
                for item in items[:3]:  # 最多3项
                    lines.append(f"  │  • {item[:box_width-4].ljust(box_width-4)}│")
            
            lines.append(f"  └{'─' * box_width}┘")
            
            # 箭头（除了最后一个）
            if i < len(stages) - 1:
                lines.append(f"  {' ' * (box_width // 2)}│")
                lines.append(f"  {' ' * (box_width // 2)}▼")
        
        return "\n".join(lines)
    
    @staticmethod
    def comparison_table(
        headers: List[str],
        rows: List[List[str]],
        title: str = "对比表格"
    ) -> str:
        """
        生成ASCII对比表格
        
        Args:
            headers: 表头列表
            rows: 数据行列表
            title: 标题
            
        Returns:
            ASCII表格
        """
        if not headers or not rows:
            return "暂无数据"
        
        # 计算列宽
        col_widths = []
        for i, header in enumerate(headers):
            max_width = len(header)
            for row in rows:
                if i < len(row):
                    max_width = max(max_width, len(str(row[i])))
            col_widths.append(min(max_width + 2, 20))  # 最大20字符
        
        total_width = sum(col_widths) + len(headers) + 1
        
        lines = []
        lines.append(f"  {title}")
        lines.append("")
        
        # 顶部边框
        top = "  ┌"
        for i, w in enumerate(col_widths):
            top += "─" * w
            top += "┬" if i < len(col_widths) - 1 else "┐"
        lines.append(top)
        
        # 表头
        header_line = "  │"
        for i, (header, w) in enumerate(zip(headers, col_widths)):
            header_line += header[:w-1].center(w) + "│"
        lines.append(header_line)
        
        # 分隔线
        sep = "  ├"
        for i, w in enumerate(col_widths):
            sep += "─" * w
            sep += "┼" if i < len(col_widths) - 1 else "┤"
        lines.append(sep)
        
        # 数据行
        for row in rows:
            row_line = "  │"
            for i, w in enumerate(col_widths):
                cell = str(row[i]) if i < len(row) else ""
                row_line += cell[:w-1].center(w) + "│"
            lines.append(row_line)
        
        # 底部边框
        bottom = "  └"
        for i, w in enumerate(col_widths):
            bottom += "─" * w
            bottom += "┴" if i < len(col_widths) - 1 else "┘"
        lines.append(bottom)
        
        return "\n".join(lines)
    
    @staticmethod
    def swot_matrix(
        strengths: List[str],
        weaknesses: List[str],
        opportunities: List[str],
        threats: List[str],
        title: str = "SWOT分析"
    ) -> str:
        """
        生成ASCII SWOT矩阵
        
        Args:
            strengths: 优势列表
            weaknesses: 劣势列表
            opportunities: 机会列表
            threats: 威胁列表
            title: 标题
            
        Returns:
            ASCII SWOT矩阵
        """
        box_width = 35
        
        def format_items(items: List[str], max_items: int = 4) -> List[str]:
            result = []
            for item in items[:max_items]:
                result.append(f"• {item[:box_width-4]}")
            return result
        
        s_items = format_items(strengths)
        w_items = format_items(weaknesses)
        o_items = format_items(opportunities)
        t_items = format_items(threats)
        
        max_rows = max(len(s_items), len(w_items), len(o_items), len(t_items), 3)
        
        lines = []
        lines.append(f"  {title.center(box_width * 2 + 5)}")
        lines.append("")
        
        # 顶部
        lines.append(f"  ┌{'─' * box_width}┬{'─' * box_width}┐")
        lines.append(f"  │{'✅ Strengths 优势'.center(box_width)}│{'❌ Weaknesses 劣势'.center(box_width)}│")
        lines.append(f"  ├{'─' * box_width}┼{'─' * box_width}┤")
        
        # S和W内容
        for i in range(max_rows):
            s_text = s_items[i] if i < len(s_items) else ""
            w_text = w_items[i] if i < len(w_items) else ""
            lines.append(f"  │{s_text.ljust(box_width)}│{w_text.ljust(box_width)}│")
        
        # 中间分隔
        lines.append(f"  ├{'─' * box_width}┼{'─' * box_width}┤")
        lines.append(f"  │{'🎯 Opportunities 机会'.center(box_width)}│{'⚠️ Threats 威胁'.center(box_width)}│")
        lines.append(f"  ├{'─' * box_width}┼{'─' * box_width}┤")
        
        # O和T内容
        for i in range(max_rows):
            o_text = o_items[i] if i < len(o_items) else ""
            t_text = t_items[i] if i < len(t_items) else ""
            lines.append(f"  │{o_text.ljust(box_width)}│{t_text.ljust(box_width)}│")
        
        # 底部
        lines.append(f"  └{'─' * box_width}┴{'─' * box_width}┘")
        
        return "\n".join(lines)
    
    @staticmethod
    def bcg_matrix(
        stars: List[str],
        cash_cows: List[str],
        question_marks: List[str],
        dogs: List[str],
        title: str = "BCG矩阵"
    ) -> str:
        """
        生成ASCII BCG矩阵
        
        Args:
            stars: 明星业务列表
            cash_cows: 现金牛列表
            question_marks: 问题业务列表
            dogs: 瘦狗业务列表
            title: 标题
            
        Returns:
            ASCII BCG矩阵
        """
        box_width = 30
        
        def format_items(items: List[str], max_items: int = 3) -> List[str]:
            result = []
            for item in items[:max_items]:
                result.append(f"• {item[:box_width-4]}")
            return result
        
        s_items = format_items(stars)
        c_items = format_items(cash_cows)
        q_items = format_items(question_marks)
        d_items = format_items(dogs)
        
        max_rows = max(len(s_items), len(c_items), len(q_items), len(d_items), 2)
        
        lines = []
        lines.append(f"  {title.center(box_width * 2 + 10)}")
        lines.append("")
        lines.append(f"  {'市场增长率 ↑'.ljust(15)}")
        lines.append(f"  {'高'.ljust(5)}")
        
        # 顶部
        lines.append(f"  ┌{'─' * box_width}┬{'─' * box_width}┐")
        lines.append(f"  │{'❓ 问题业务'.center(box_width)}│{'⭐ 明星业务'.center(box_width)}│")
        lines.append(f"  │{'(高增长/低份额)'.center(box_width)}│{'(高增长/高份额)'.center(box_width)}│")
        lines.append(f"  ├{'─' * box_width}┼{'─' * box_width}┤")
        
        for i in range(max_rows):
            q_text = q_items[i] if i < len(q_items) else ""
            s_text = s_items[i] if i < len(s_items) else ""
            lines.append(f"  │{q_text.ljust(box_width)}│{s_text.ljust(box_width)}│")
        
        lines.append(f"  ├{'─' * box_width}┼{'─' * box_width}┤")
        lines.append(f"  │{'🐕 瘦狗业务'.center(box_width)}│{'🐄 现金牛业务'.center(box_width)}│")
        lines.append(f"  │{'(低增长/低份额)'.center(box_width)}│{'(低增长/高份额)'.center(box_width)}│")
        lines.append(f"  ├{'─' * box_width}┼{'─' * box_width}┤")
        
        for i in range(max_rows):
            d_text = d_items[i] if i < len(d_items) else ""
            c_text = c_items[i] if i < len(c_items) else ""
            lines.append(f"  │{d_text.ljust(box_width)}│{c_text.ljust(box_width)}│")
        
        lines.append(f"  └{'─' * box_width}┴{'─' * box_width}┘")
        lines.append(f"  {'低'.ljust(5)}{' ' * (box_width - 5)}{'低'.center(10)}{'高'.rjust(box_width - 5)}")
        lines.append(f"  {' ' * 20}{'相对市场份额 →'.center(30)}")
        
        return "\n".join(lines)
    
    @staticmethod
    def pest_diagram(
        political: List[str],
        economic: List[str],
        social: List[str],
        technological: List[str],
        title: str = "PEST分析"
    ) -> str:
        """
        生成ASCII PEST分析图
        
        Args:
            political: 政治因素
            economic: 经济因素
            social: 社会因素
            technological: 技术因素
            title: 标题
            
        Returns:
            ASCII PEST图
        """
        box_width = 30
        
        def format_items(items: List[str], max_items: int = 3) -> List[str]:
            result = []
            for item in items[:max_items]:
                result.append(f"• {item[:box_width-4]}")
            return result
        
        p_items = format_items(political)
        e_items = format_items(economic)
        s_items = format_items(social)
        t_items = format_items(technological)
        
        max_rows = max(len(p_items), len(e_items), len(s_items), len(t_items), 2)
        
        lines = []
        lines.append(f"  {title.center(box_width * 2 + 5)}")
        lines.append("")
        
        # P和E
        lines.append(f"  ┌{'─' * box_width}┬{'─' * box_width}┐")
        lines.append(f"  │{'🏛️ Political 政治法规'.center(box_width)}│{'💰 Economic 经济环境'.center(box_width)}│")
        lines.append(f"  ├{'─' * box_width}┼{'─' * box_width}┤")
        
        for i in range(max_rows):
            p_text = p_items[i] if i < len(p_items) else ""
            e_text = e_items[i] if i < len(e_items) else ""
            lines.append(f"  │{p_text.ljust(box_width)}│{e_text.ljust(box_width)}│")
        
        # S和T
        lines.append(f"  ├{'─' * box_width}┼{'─' * box_width}┤")
        lines.append(f"  │{'👥 Social 社会文化'.center(box_width)}│{'🔧 Technological 技术环境'.center(box_width)}│")
        lines.append(f"  ├{'─' * box_width}┼{'─' * box_width}┤")
        
        for i in range(max_rows):
            s_text = s_items[i] if i < len(s_items) else ""
            t_text = t_items[i] if i < len(t_items) else ""
            lines.append(f"  │{s_text.ljust(box_width)}│{t_text.ljust(box_width)}│")
        
        lines.append(f"  └{'─' * box_width}┴{'─' * box_width}┘")
        
        return "\n".join(lines)
    
    @staticmethod
    def industry_chain(
        upstream: List[str],
        midstream: List[str],
        downstream: List[str],
        title: str = "产业链图"
    ) -> str:
        """
        生成ASCII产业链图
        
        Args:
            upstream: 上游环节
            midstream: 中游环节
            downstream: 下游环节
            title: 标题
            
        Returns:
            ASCII产业链图
        """
        box_width = 20
        
        lines = []
        lines.append(f"  {title}")
        lines.append("")
        
        # 上游
        lines.append(f"  ┌{'─' * (box_width * 3 + 10)}┐")
        lines.append(f"  │{'📦 上游供应'.center(box_width * 3 + 8)}│")
        lines.append(f"  ├{'─' * (box_width * 3 + 10)}┤")
        
        up_line = "  │ "
        for item in upstream[:3]:
            up_line += f"[{item[:box_width-4].center(box_width-4)}] "
        up_line = up_line.ljust(box_width * 3 + 11) + "│"
        lines.append(up_line)
        
        lines.append(f"  └{'─' * (box_width * 3 + 10)}┘")
        lines.append(f"  {' ' * ((box_width * 3 + 10) // 2)}│")
        lines.append(f"  {' ' * ((box_width * 3 + 10) // 2)}▼")
        
        # 中游
        lines.append(f"  ┌{'─' * (box_width * 3 + 10)}┐")
        lines.append(f"  │{'🏭 中游制造'.center(box_width * 3 + 8)}│")
        lines.append(f"  ├{'─' * (box_width * 3 + 10)}┤")
        
        mid_line = "  │ "
        for item in midstream[:3]:
            mid_line += f"[{item[:box_width-4].center(box_width-4)}] "
        mid_line = mid_line.ljust(box_width * 3 + 11) + "│"
        lines.append(mid_line)
        
        lines.append(f"  └{'─' * (box_width * 3 + 10)}┘")
        lines.append(f"  {' ' * ((box_width * 3 + 10) // 2)}│")
        lines.append(f"  {' ' * ((box_width * 3 + 10) // 2)}▼")
        
        # 下游
        lines.append(f"  ┌{'─' * (box_width * 3 + 10)}┐")
        lines.append(f"  │{'🛒 下游客户'.center(box_width * 3 + 8)}│")
        lines.append(f"  ├{'─' * (box_width * 3 + 10)}┤")
        
        down_line = "  │ "
        for item in downstream[:3]:
            down_line += f"[{item[:box_width-4].center(box_width-4)}] "
        down_line = down_line.ljust(box_width * 3 + 11) + "│"
        lines.append(down_line)
        
        lines.append(f"  └{'─' * (box_width * 3 + 10)}┘")
        
        return "\n".join(lines)
    
    @staticmethod
    def score_card(
        items: List[Dict[str, Any]],
        title: str = "评分卡",
        max_score: int = 5
    ) -> str:
        """
        生成ASCII评分卡
        
        Args:
            items: 评分项列表，每项包含 name 和 score
            title: 标题
            max_score: 最高分
            
        Returns:
            ASCII评分卡
        """
        if not items:
            return "暂无数据"
        
        box_width = 50
        
        lines = []
        lines.append(f"  ┌{'─' * box_width}┐")
        lines.append(f"  │{title.center(box_width)}│")
        lines.append(f"  ├{'─' * box_width}┤")
        
        for item in items:
            name = str(item.get('name', ''))[:15].ljust(15)
            score = min(max_score, max(0, item.get('score', 0)))
            
            stars = "★" * score + "☆" * (max_score - score)
            bar_len = int((score / max_score) * 20)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            
            lines.append(f"  │ {name} {stars} {bar} {score}/{max_score} │")
        
        lines.append(f"  └{'─' * box_width}┘")
        
        return "\n".join(lines)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python ascii_charts.py <图表类型> [参数JSON或JSON文件路径]")
        print()
        print("支持的图表类型:")
        print("  bar          - 柱状图")
        print("  pie          - 占比图（饼图替代）")
        print("  trend        - 趋势图")
        print("  quadrant     - 四象限图")
        print("  flow         - 流程图（水平）")
        print("  vflow        - 流程图（垂直）")
        print("  table        - 对比表格")
        print("  swot         - SWOT矩阵")
        print("  bcg          - BCG矩阵")
        print("  pest         - PEST分析图")
        print("  chain        - 产业链图")
        print("  score        - 评分卡")
        print()
        print("示例:")
        print('  python ascii_charts.py bar data.json')
        print('  python ascii_charts.py swot params.json')
        sys.exit(1)
    
    chart_type = sys.argv[1]
    
    # 支持从JSON文件读取参数
    params = {}
    if len(sys.argv) > 2:
        arg = sys.argv[2]
        if arg.endswith('.json') and os.path.exists(arg):
            with open(arg, 'r', encoding='utf-8') as f:
                params = json.load(f)
        else:
            try:
                params = json.loads(arg)
            except json.JSONDecodeError:
                print(f"错误: 无法解析参数。请提供有效的JSON字符串或JSON文件路径。")
                sys.exit(1)
    
    if chart_type == "bar":
        print(ASCIICharts.bar_chart(
            params.get("data", [{"label": "A", "value": 50}, {"label": "B", "value": 80}]),
            params.get("title", "柱状图")
        ))
    elif chart_type == "pie":
        print(ASCIICharts.pie_chart_text(
            params.get("data", [{"label": "A", "value": 60}, {"label": "B", "value": 40}]),
            params.get("title", "占比分布")
        ))
    elif chart_type == "trend":
        print(ASCIICharts.trend_chart(
            params.get("labels", ["2020", "2021", "2022", "2023", "2024"]),
            params.get("values", [100, 150, 200, 280, 350]),
            params.get("title", "趋势图")
        ))
    elif chart_type == "quadrant":
        print(ASCIICharts.quadrant_chart(
            params.get("items", []),
            params.get("title", "四象限图"),
            params.get("q1", "象限一"),
            params.get("q2", "象限二"),
            params.get("q3", "象限三"),
            params.get("q4", "象限四")
        ))
    elif chart_type == "flow":
        print(ASCIICharts.flow_chart(
            params.get("stages", ["阶段1", "阶段2", "阶段3"]),
            params.get("title", "流程图")
        ))
    elif chart_type == "vflow":
        print(ASCIICharts.vertical_flow_chart(
            params.get("stages", [{"name": "阶段1"}, {"name": "阶段2"}]),
            params.get("title", "流程图")
        ))
    elif chart_type == "table":
        print(ASCIICharts.comparison_table(
            params.get("headers", ["列1", "列2", "列3"]),
            params.get("rows", [["A", "B", "C"], ["D", "E", "F"]]),
            params.get("title", "对比表格")
        ))
    elif chart_type == "swot":
        print(ASCIICharts.swot_matrix(
            params.get("strengths", ["优势1", "优势2"]),
            params.get("weaknesses", ["劣势1", "劣势2"]),
            params.get("opportunities", ["机会1", "机会2"]),
            params.get("threats", ["威胁1", "威胁2"]),
            params.get("title", "SWOT分析")
        ))
    elif chart_type == "bcg":
        print(ASCIICharts.bcg_matrix(
            params.get("stars", ["明星企业"]),
            params.get("cash_cows", ["现金牛企业"]),
            params.get("question_marks", ["问题企业"]),
            params.get("dogs", ["瘦狗企业"]),
            params.get("title", "BCG矩阵")
        ))
    elif chart_type == "pest":
        print(ASCIICharts.pest_diagram(
            params.get("political", ["政策1", "政策2"]),
            params.get("economic", ["经济1", "经济2"]),
            params.get("social", ["社会1", "社会2"]),
            params.get("technological", ["技术1", "技术2"]),
            params.get("title", "PEST分析")
        ))
    elif chart_type == "chain":
        print(ASCIICharts.industry_chain(
            params.get("upstream", ["供应商A", "供应商B"]),
            params.get("midstream", ["制造商"]),
            params.get("downstream", ["客户A", "客户B"]),
            params.get("title", "产业链图")
        ))
    elif chart_type == "score":
        print(ASCIICharts.score_card(
            params.get("items", [{"name": "指标A", "score": 4}, {"name": "指标B", "score": 3}]),
            params.get("title", "评分卡")
        ))
    else:
        print(f"未知的图表类型: {chart_type}")
        sys.exit(1)


if __name__ == "__main__":
    main()
