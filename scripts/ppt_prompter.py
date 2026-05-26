#!/usr/bin/env python3
"""
PPT提示词生成脚本
根据行业分析数据生成用于GenerateImage工具的PPT页面提示词
"""

import json
import sys
from typing import Dict, Any, List
from datetime import datetime


class PPTPrompter:
    """PPT提示词生成器"""
    
    # PPT尺寸常量
    PPT_WIDTH = 2560
    PPT_HEIGHT = 1440
    PPT_SIZE = f"图片尺寸：宽度{PPT_WIDTH}px，高度{PPT_HEIGHT}px，16:9比例。"
    
    # 视觉风格常量
    STYLE_BASE = f"""图片尺寸：宽度2560px，高度1440px，16:9比例。
视觉风格：线性扁平风格，白色工程图纸感的背景，整体呈浅蓝-白色调。
标题的字号小，正文的字号非常小，保持留白充足，适当搭配少量扁平的图解元素。
不要出现人像。"""
    
    COVER_STYLE = """图片尺寸：宽度2560px，高度1440px，16:9比例。
线性扁平风格，浅蓝灰色调的背景，带有淡淡的工程图纸网格纹理，极简几何线条装饰。"""
    
    def __init__(self, industry: str, data: Dict[str, Any]):
        """
        初始化PPT提示词生成器
        
        Args:
            industry: 行业名称
            data: 分析数据
        """
        self.industry = industry
        self.data = data
        self.report_date = datetime.now().strftime("%Y年%m月")
    
    def generate_page1_cover(self) -> Dict[str, str]:
        """生成封面页提示词"""
        subtitle = self.data.get('subtitle', f'{datetime.now().year}年度分析')
        author = self.data.get('author', '行业研究团队')
        
        prompt = f"""生成一张PPT封面页。

{self.COVER_STYLE}

页面中央位置展示主标题「{self.industry}行业分析报告」，深蓝色粗体，字号小，单行展示。
主标题下方展示副标题「{subtitle}」，灰色，字号更小。
页面底部小字显示「{author} · {self.report_date}」

整体留白充足，聚焦标题。"""
        
        return {
            "page_id": 1,
            "title": "封面页",
            "prompt": prompt,
            "filename": "ppt-page-1-cover.png"
        }
    
    def generate_page2_overview(self) -> Dict[str, str]:
        """生成行业概览页提示词"""
        overview = self.data.get('overview', {})
        
        market_size = overview.get('china_market_size', 'X亿元')
        growth_rate = overview.get('growth_rate', 'X%')
        players = overview.get('main_players', 'X家')
        segments = overview.get('segments', 'X个')
        stage = overview.get('stage', '成长期')
        driver = overview.get('growth_driver', '技术创新与需求增长')
        feature = overview.get('core_feature', '快速迭代、竞争激烈')
        summary = overview.get('summary', f'{self.industry}市场快速发展，潜力巨大')
        
        prompt = f"""生成一张信息图海报。

{self.STYLE_BASE}

标题「行业概览」位于页面左上角，黑色粗体。

页面分为左右两个区域：

左侧区域展示核心数据：
- "市场规模：{market_size}" 大号字
- "增长率：{growth_rate}" 中号字
- "主要玩家：{players}" 中号字
- "细分领域：{segments}" 中号字

右侧区域展示发展趋势：
- "行业阶段：{stage}"
- "增长驱动：{driver}"
- "核心特征：{feature}"

底部总结区域：「{summary}」"""
        
        return {
            "page_id": 2,
            "title": "行业概览",
            "prompt": prompt,
            "filename": "ppt-page-2-overview.png"
        }
    
    def generate_page3_market(self) -> Dict[str, str]:
        """生成市场规模与增长页提示词"""
        market = self.data.get('market', {})
        
        global_current = market.get('global_current', 'X亿美元')
        global_forecast = market.get('global_forecast', 'X亿美元')
        global_cagr = market.get('global_cagr', 'X%')
        china_current = market.get('china_current', 'X亿元')
        china_forecast = market.get('china_forecast', 'X亿元')
        china_cagr = market.get('china_cagr', 'X%')
        
        segments = market.get('segments', [
            {'name': '细分市场A', 'share': 'X%'},
            {'name': '细分市场B', 'share': 'X%'},
            {'name': '细分市场C', 'share': 'X%'},
        ])
        
        summary = market.get('summary', '市场持续增长，中国市场增速领先全球')
        
        segments_text = "\n".join([f"- {s['name']}：{s['share']}" for s in segments[:3]])
        
        prompt = f"""生成一张信息图海报。

{self.STYLE_BASE}

标题「市场规模与增长趋势」位于页面左上角，黑色粗体。

页面展示市场规模数据：

全球市场：
- 当前：{global_current}
- 预计2027年：{global_forecast}
- CAGR：{global_cagr}

中国市场：
- 当前：{china_current}
- 预计2027年：{china_forecast}
- CAGR：{china_cagr}

细分市场占比：
{segments_text}

底部总结：「{summary}」"""
        
        return {
            "page_id": 3,
            "title": "市场规模与增长",
            "prompt": prompt,
            "filename": "ppt-page-3-market.png"
        }
    
    def generate_page4_chain(self) -> Dict[str, str]:
        """生成产业链分析页提示词"""
        chain = self.data.get('chain', {})
        
        upstream = chain.get('upstream', ['原材料供应商', '技术提供商', '设备供应商'])
        midstream = chain.get('midstream', ['核心产品/服务提供商'])
        downstream = chain.get('downstream', ['企业客户', '个人消费者'])
        
        upstream_power = chain.get('upstream_power', '中')
        downstream_power = chain.get('downstream_power', '中')
        value_share = chain.get('value_share', 'X%')
        
        summary = chain.get('summary', '产业链完整，中游环节价值集中')
        
        upstream_text = "\n".join([f"- {item}" for item in upstream[:3]])
        downstream_text = "\n".join([f"- {item}" for item in downstream[:2]])
        
        prompt = f"""生成一张信息图海报。

{self.STYLE_BASE}

标题「产业链分析」位于页面左上角，黑色粗体。

页面采用从左到右的流程布局，展示产业链三个环节：

左侧区域「上游」：
{upstream_text}
- 议价能力：{upstream_power}

中间区域「中游」：
- {midstream[0] if midstream else '核心企业'}
- 价值占比：{value_share}

右侧区域「下游」：
{downstream_text}
- 议价能力：{downstream_power}

底部总结：「{summary}」"""
        
        return {
            "page_id": 4,
            "title": "产业链分析",
            "prompt": prompt,
            "filename": "ppt-page-4-chain.png"
        }
    
    def generate_page5_pest(self) -> Dict[str, str]:
        """生成PEST分析页提示词"""
        pest = self.data.get('pest', {})
        
        political = pest.get('political_points', ['政策支持', '监管规范'])
        economic = pest.get('economic_points', ['市场增长', '消费升级'])
        social = pest.get('social_points', ['需求变化', '观念转变'])
        technological = pest.get('technological_points', ['技术创新', '数字化'])
        
        p_impact = pest.get('p_impact', '利好')
        e_impact = pest.get('e_impact', '利好')
        s_impact = pest.get('s_impact', '利好')
        t_impact = pest.get('t_impact', '利好')
        
        summary = pest.get('summary', '宏观环境整体有利于行业发展')
        
        prompt = f"""生成一张信息图海报。

{self.STYLE_BASE}

标题「PEST环境分析」位于页面左上角，黑色粗体。

页面采用四象限布局：

左上区域「Political 政治法规」：
- {political[0] if len(political) > 0 else '政策支持'}
- {political[1] if len(political) > 1 else '监管规范'}
- 影响：{p_impact}

右上区域「Economic 经济环境」：
- {economic[0] if len(economic) > 0 else '市场增长'}
- {economic[1] if len(economic) > 1 else '消费升级'}
- 影响：{e_impact}

左下区域「Social 社会文化」：
- {social[0] if len(social) > 0 else '需求变化'}
- {social[1] if len(social) > 1 else '观念转变'}
- 影响：{s_impact}

右下区域「Technological 技术环境」：
- {technological[0] if len(technological) > 0 else '技术创新'}
- {technological[1] if len(technological) > 1 else '数字化'}
- 影响：{t_impact}

底部总结：「{summary}」"""
        
        return {
            "page_id": 5,
            "title": "PEST分析",
            "prompt": prompt,
            "filename": "ppt-page-5-pest.png"
        }
    
    def generate_page6_bcg(self) -> Dict[str, str]:
        """生成BCG矩阵页提示词"""
        bcg = self.data.get('bcg', {})
        
        # 处理字符串或列表格式
        stars = bcg.get('stars', '头部企业A')
        if isinstance(stars, list):
            stars = stars[0] if stars else '头部企业'
        
        cash_cows = bcg.get('cash_cows', '成熟企业B')
        if isinstance(cash_cows, list):
            cash_cows = cash_cows[0] if cash_cows else '成熟企业'
            
        question_marks = bcg.get('question_marks', '新兴企业C')
        if isinstance(question_marks, list):
            question_marks = question_marks[0] if question_marks else '新兴企业'
            
        dogs = bcg.get('dogs', '边缘企业D')
        if isinstance(dogs, list):
            dogs = dogs[0] if dogs else '边缘企业'
        
        summary = bcg.get('summary', '行业格局分化明显，头部效应显著')
        
        prompt = f"""生成一张信息图海报。

{self.STYLE_BASE}

标题「BCG矩阵分析」位于页面左上角，黑色粗体。

页面采用四象限矩阵布局：

左上区域「问题业务」（高增长/低份额）：
- {question_marks}
- 策略：选择性投资

右上区域「明星业务」（高增长/高份额）：
- {stars}
- 策略：加大投资

左下区域「瘦狗业务」（低增长/低份额）：
- {dogs}
- 策略：收缩或退出

右下区域「现金牛业务」（低增长/高份额）：
- {cash_cows}
- 策略：维持收割

底部总结：「{summary}」"""
        
        return {
            "page_id": 6,
            "title": "BCG矩阵",
            "prompt": prompt,
            "filename": "ppt-page-6-bcg.png"
        }
    
    def generate_page7_swot(self) -> Dict[str, str]:
        """生成SWOT分析页提示词"""
        swot = self.data.get('swot', {})
        
        strengths = swot.get('strengths', ['优势1', '优势2', '优势3'])
        weaknesses = swot.get('weaknesses', ['劣势1', '劣势2', '劣势3'])
        opportunities = swot.get('opportunities', ['机会1', '机会2', '机会3'])
        threats = swot.get('threats', ['威胁1', '威胁2', '威胁3'])
        
        summary = swot.get('summary', '把握机会、发挥优势、规避风险')
        
        s_text = "\n".join([f"- {s}" for s in strengths[:3]])
        w_text = "\n".join([f"- {w}" for w in weaknesses[:3]])
        o_text = "\n".join([f"- {o}" for o in opportunities[:3]])
        t_text = "\n".join([f"- {t}" for t in threats[:3]])
        
        prompt = f"""生成一张信息图海报。

{self.STYLE_BASE}

标题「SWOT战略分析」位于页面左上角，黑色粗体。

页面采用四象限布局：

左上区域「Strengths 优势」：
{s_text}

右上区域「Weaknesses 劣势」：
{w_text}

左下区域「Opportunities 机会」：
{o_text}

右下区域「Threats 威胁」：
{t_text}

底部总结：「{summary}」"""
        
        return {
            "page_id": 7,
            "title": "SWOT分析",
            "prompt": prompt,
            "filename": "ppt-page-7-swot.png"
        }
    
    def generate_page8_insights(self) -> Dict[str, str]:
        """生成关键洞察与建议页提示词"""
        insights = self.data.get('insights', {})
        
        insight_list = insights.get('key_insights', [
            {'title': '洞察一', 'content': '关键发现1'},
            {'title': '洞察二', 'content': '关键发现2'},
            {'title': '洞察三', 'content': '关键发现3'},
            {'title': '洞察四', 'content': '关键发现4'},
        ])
        
        short_term = insights.get('short_term', '短期建议')
        mid_term = insights.get('mid_term', '中期建议')
        long_term = insights.get('long_term', '长期建议')
        
        summary = insights.get('summary', '把握趋势、稳步发展')
        
        insights_text = ""
        for i, insight in enumerate(insight_list[:4]):
            insights_text += f"\n洞察{['一', '二', '三', '四'][i]}：「{insight.get('title', f'洞察{i+1}')}」\n{insight.get('content', '描述')}\n"
        
        prompt = f"""生成一张信息图海报。

{self.STYLE_BASE}

标题「关键洞察与建议」位于页面左上角，黑色粗体。

页面展示四个关键洞察：
{insights_text}

战略建议区域：
短期：{short_term}
中期：{mid_term}
长期：{long_term}

底部总结：「{summary}」"""
        
        return {
            "page_id": 8,
            "title": "关键洞察与建议",
            "prompt": prompt,
            "filename": "ppt-page-8-insights.png"
        }
    
    def generate_page9_ending(self) -> Dict[str, str]:
        """生成结尾页提示词"""
        author = self.data.get('author', '行业研究团队')
        
        prompt = f"""生成一张PPT结尾页。

{self.COVER_STYLE}

页面中央显示「感谢阅读」，深蓝色大号字。
下方显示「{author} · {self.report_date}」，灰色小号字。

整体简洁，大量留白。"""
        
        return {
            "page_id": 9,
            "title": "结尾页",
            "prompt": prompt,
            "filename": "ppt-page-9-ending.png"
        }
    
    def generate_all_prompts(self) -> List[Dict[str, str]]:
        """生成所有9页PPT的提示词"""
        return [
            self.generate_page1_cover(),
            self.generate_page2_overview(),
            self.generate_page3_market(),
            self.generate_page4_chain(),
            self.generate_page5_pest(),
            self.generate_page6_bcg(),
            self.generate_page7_swot(),
            self.generate_page8_insights(),
            self.generate_page9_ending(),
        ]
    
    def generate_ppt_json(self) -> Dict[str, Any]:
        """生成PPT JSON配置"""
        pages = self.generate_all_prompts()
        
        return {
            "ppt_title": f"{self.industry}行业分析报告",
            "global_style": self.STYLE_BASE,
            "template_prompt": "",
            "ppt_content": [
                {
                    "page_id": page["page_id"],
                    "prompt": page["prompt"],
                    "ref_images": []
                }
                for page in pages
            ]
        }


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python ppt_prompter.py <行业名称> [数据JSON文件] [--json]")
        print()
        print("示例:")
        print("  python ppt_prompter.py \"新能源汽车\"")
        print("  python ppt_prompter.py \"GUI Agent\" data.json")
        print("  python ppt_prompter.py \"AI芯片\" data.json --json")
        print()
        print("输出:")
        print("  默认输出每页PPT的提示词")
        print("  --json 输出完整的PPT JSON配置")
        sys.exit(1)
    
    industry = sys.argv[1]
    
    # 加载数据
    data = {}
    for arg in sys.argv[2:]:
        if arg.endswith('.json'):
            with open(arg, 'r', encoding='utf-8') as f:
                data = json.load(f)
            break
    
    # 生成提示词
    prompter = PPTPrompter(industry, data)
    
    if '--json' in sys.argv:
        # 输出JSON格式
        output = prompter.generate_ppt_json()
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        # 输出每页提示词
        pages = prompter.generate_all_prompts()
        for page in pages:
            print(f"\n{'='*60}")
            print(f"## 第{page['page_id']}页：{page['title']}")
            print(f"文件名：{page['filename']}")
            print(f"{'='*60}")
            print(page['prompt'])
            print()


if __name__ == "__main__":
    main()
