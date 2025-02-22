import requests
import datetime
from flask import Flask, request, jsonify, make_response, send_file, send_from_directory
from flask_cors import CORS

app = Flask(__name__)

# 添加静态文件路由
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

CORS(app, 
     resources={r"/*": {
         "origins": ["http://127.0.0.1:5000", "http://127.0.0.1:5500", "http://178.16.140.245:5000", "http://178.16.140.245"],
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": ["Content-Type"]
     }})

# ==================== 基础数据配置 ====================
TIANGAN_WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火',
    '戊': '土', '己': '土', '庚': '金', '辛': '金',
    '壬': '水', '癸': '水'
}

DIZHI_CANGGAN = {
    '子': ['癸'],
    '丑': ['己', '癸', '辛'],
    '寅': ['甲', '丙', '戊'],
    '卯': ['乙'],
    '辰': ['戊', '乙', '癸'],
    '巳': ['丙', '庚', '戊'],
    '午': ['丁', '己'],
    '未': ['己', '丁', '乙'],
    '申': ['庚', '壬', '戊'],
    '酉': ['辛'],
    '戌': ['戊', '辛', '丁'],
    '亥': ['壬', '甲']
}

WUXING_SHENGKE = {
    '木': {'生': '火', '克': '土', '被生': '水', '被克': '金'},
    '火': {'生': '土', '克': '金', '被生': '木', '被克': '水'},
    '土': {'生': '金', '克': '水', '被生': '火', '被克': '木'},
    '金': {'生': '水', '克': '木', '被生': '土', '被克': '火'},
    '水': {'生': '木', '克': '金', '被生': '土', '被克': '火'}
}

TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# ==================== 五行水晶推荐配置 ====================
crystals_by_wuxing = {
    "木": ["绿幽灵:促进事业发展与财富增长", "绿发晶:提升活力，增强免疫力，带来积极乐观的心态", "翡翠:调和情绪并创造和谐的环境"],
    "火": ["红玛瑙：增强活力，提升自信心，带来热情与积极的力量", "红碧玺：有提升创造力，激发灵感，带来丰富的人生体验", "粉水晶：温柔、爱与疗愈，能促进爱情和人际关系"],
    "土": ["黄水晶：招来财运，提升个人魅力，带来丰盛与富足", "虎眼石：增强自信心，提升决断力，带来清晰的思绪", "茶水晶：象征稳定与安全"],
    "金": ["白水晶：有效清理能量场中的负面能量，恢复平衡与和谐", "透明水晶：能够放大能量，提升其他水晶的疗愈功效", "白幽灵：清除负面能量，带来内心的平静与祥和"],
    "水": ["蓝宝石：舒缓情绪，促进内心的平静与宁静", "海蓝宝石：带来平静与明晰", "黑曜石：具有强大的保护作用，能有效抵御负能量"]
}

five_element_numbers = {
    '木': [3, 8],
    '火': [2, 7],
    '土': [5, 0],
    '金': [4, 9],
    '水': [1, 6]
}
# ==================== 色彩映射及五行调衡策略 ====================
# 天干对应色系：包括五行属性、主色（十干）
TIANGAN_COLOR = {
    '甲': {'wuxing': '木', 'color': '#0B6623'},   # 青碧（对应肝经528Hz）
    '乙': {'wuxing': '木', 'color': '#C9CC3F'},   # 柳黄（胆经492Hz）
    '丙': {'wuxing': '火', 'color': '#FF2400'},   # 赤红（心轮639Hz）
    '丁': {'wuxing': '火', 'color': '#8A2BE2'},   # 绛紫（心包587Hz）
    '戊': {'wuxing': '土', 'color': '#CC7722'},   # 赭石（脾胃432Hz）
    '己': {'wuxing': '土', 'color': '#6F4E37'},   # 棕褐（胰腺396Hz）
    '庚': {'wuxing': '金', 'color': '#EDE6D3'},   # 银白（肺经741Hz）
    '辛': {'wuxing': '金', 'color': '#E5E4E2'},   # 铂金（皮肤852Hz）
    '壬': {'wuxing': '水', 'color': '#000000'},   # 玄墨（肾经396Hz）
    '癸': {'wuxing': '水', 'color': '#000080'}    # 藏青（膀胱528Hz）
}

# 地支对应色系（取藏干组合中的主色）
DIZHI_COLOR = {
    '子': {'wuxing': '水', 'color': '#000080'},     # 子夜墨蓝
    '丑': {'wuxing': '土', 'color': '#8B4513'},     # 冻土棕
    '寅': {'wuxing': '木', 'color': '#01796F'},     # 松柏绿
    '卯': {'wuxing': '木', 'color': '#34C2A7'},     # 翡翠潮
    '辰': {'wuxing': '土', 'color': '#E1C16E'},     # 沙尘金
    '巳': {'wuxing': '火', 'color': '#B22222'},     # 熔岩红
    '午': {'wuxing': '火', 'color': '#DC143C'},     # 三昧真火
    '未': {'wuxing': '土', 'color': '#F5DEB3'},     # 麦浪黄
    '申': {'wuxing': '金', 'color': '#555555'},     # 寒铁灰
    '酉': {'wuxing': '金', 'color': '#E5E4E2'},     # 太白铂金
    '戌': {'wuxing': '土', 'color': '#8B4513'},     # 熔岩陶
    '亥': {'wuxing': '水', 'color': '#000000'}      # 墨玉玄
}

# 五行默认色（当干支均未明显支持时采用）
FIVE_ELEMENT_DEFAULT_COLOR = {
    '木': '#0B6623',
    '火': '#FF2400',
    '土': '#CC7722',
    '金': '#EDE6D3',
    '水': '#000000'
}

# ==================== 五行日常活动推荐 ====================
activities_by_wuxing = {
    "金": {
        "日常活动": [
            "理财与消费：管理财务、制定预算、储蓄、投资等。",
            "整理与清洁：打扫房间、整理物品、收纳等。",
            "工作与决策：制定计划、做决策、处理工作事务等。",
            "社交与礼仪：参加正式场合、商务活动、社交聚会等。",
            "健康与保养：皮肤护理、美容、健身等。"
        ]
    },
    "木": {
        "日常活动": [
            "学习与成长：阅读书籍、在线学习、参加培训课程等。",
            "户外活动：散步、跑步、爬山、露营等。",
            "社交与交流：与朋友聚会、参加社交活动、与人沟通交流等。",
            "创意与手工：绘画、写作、手工艺制作等。",
            "旅行与探索：计划旅行、探索新地方、体验新文化等。"
        ]
    },
    "水": {
        "日常活动": [
            "放松与疗愈：泡澡、冥想、瑜伽、听音乐等。",
            "情感交流：与家人、朋友深入交流、倾诉心事等。",
            "艺术欣赏：看电影、听音乐会、参观艺术展览等。",
            "研究与学习：深入研究某个主题、阅读专业书籍等。",
            "健康与养生：按摩、针灸、中医调理等。"
        ]
    },
    "火": {
        "日常活动": [
            "运动与健身：跑步、游泳、健身、瑜伽等。",
            "烹饪与饮食：做饭、享受美食、品尝新的菜肴等。",
            "社交与娱乐：参加派对、跳舞、唱歌等。",
            "工作与热情：积极投入工作、追求目标、完成任务等。",
            "情感表达：表达爱意、关心他人、积极沟通等。"
        ]
    },
    "土": {
        "日常活动": [
            "家务与照顾：照顾家人、做家务、照顾宠物等。",
            "种植与园艺：种植花草、蔬菜、打理花园等。",
            "稳定与规划：制定长期计划、稳定生活节奏、保持规律作息等。",
            "工作与责任：承担工作责任、完成任务、管理项目等。",
            "健康与养生：按摩、中医调理、保持健康的生活方式等。"
        ]
    }
}


# ==================== 天干&地支（八字）解析 ====================
def parse_bazi(bazi_list: list) -> dict:
    """解析八字结构，返回{'年柱': {'天干': 'X', '地支': 'Y'}, ...}"""
    columns = ['年柱', '月柱', '日柱', '时柱']
    
    if len(bazi_list) != 4:
        raise ValueError("八字必须包含四柱信息")
    
    bazi_dict = {}
    for col, ganzhi in zip(columns, bazi_list):
        if len(ganzhi) != 2:
            raise ValueError(f"干支格式错误：{ganzhi}")
        bazi_dict[col] = {'天干': ganzhi[0], '地支': ganzhi[1]}
    
    return bazi_dict

# ==================== 计算五行能量及强度 ====================
def calculate_wuxing_balance(bazi_dict: dict) -> dict:
    """统计天干及地支藏干的五行能量"""
    wuxing_count = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
    
    # 统计天干五行（权重1）
    for position in ['年柱', '月柱', '日柱', '时柱']:
        gan = bazi_dict[position]['天干']
        wuxing = TIANGAN_WUXING[gan]
        wuxing_count[wuxing] += 1
    
    # 统计地支藏干五行（权重0.5）
    for position in ['年柱', '月柱', '日柱', '时柱']:
        zhi = bazi_dict[position]['地支']
        for gan in DIZHI_CANGGAN[zhi]:
            wuxing = TIANGAN_WUXING[gan]
            wuxing_count[wuxing] += 0.5
            
    return wuxing_count

# ==================== 计算五行喜忌（喜用神、忌神） ====================
def determine_xi_ji_shen(wuxing_count: dict, rizhu_wx: str) -> tuple:
    weakest_wuxing = min(wuxing_count, key=wuxing_count.get)
    strongest_wuxing = max(wuxing_count, key=wuxing_count.get)
    
    xi_shen = WUXING_SHENGKE[weakest_wuxing]['生']
    ji_shen = WUXING_SHENGKE[strongest_wuxing]['克']
    
    wuxing_xi_ji = {
        '喜用神': f"{weakest_wuxing}({xi_shen})",
        '忌神': f"{strongest_wuxing}({ji_shen})"
    }
    
    if rizhu_wx == weakest_wuxing:
        wuxing_xi_ji['日主'] = f"日主（{rizhu_wx}）有喜用神（{xi_shen}）"
    elif rizhu_wx == strongest_wuxing:
        wuxing_xi_ji['日主'] = f"日主（{rizhu_wx}）有忌神（{ji_shen}）"
    else:
        wuxing_xi_ji['日主'] = f"日主（{rizhu_wx}）无明显喜忌神影响"
    
    xi_shen_tiangan = sorted(set([k for k, v in TIANGAN_WUXING.items() if v == xi_shen]))
    ji_shen_tiangan = sorted(set([k for k, v in TIANGAN_WUXING.items() if v == ji_shen]))
    
    return xi_shen_tiangan, ji_shen_tiangan, wuxing_xi_ji

# ==================== 综合八字分析 ====================
def advanced_analyze(bazi_list: list) -> dict:
    try:
        bazi = parse_bazi(bazi_list)
        rizhu_gan = bazi['日柱']['天干']
        rizhu_wx = TIANGAN_WUXING[rizhu_gan]
        
        wuxing_balance = calculate_wuxing_balance(bazi)
        xi_shen, ji_shen, wuxing_xi_ji = determine_xi_ji_shen(wuxing_balance, rizhu_wx)
        
        return {
            '八字': " ".join(bazi_list),
            '日主': f"{rizhu_gan}({rizhu_wx})",
            '五行强弱': wuxing_balance,
            '五行喜忌': wuxing_xi_ji,
            '喜用神_天干': xi_shen,
            '忌神_天干': ji_shen
        }
    except Exception as e:
        return {'error': str(e)}

# ==================== 根据喜用神选择水晶 ====================
def choose_crystals_based_on_xi_shen(analysis_result):
    try:
        wuxing_xi_ji_str = analysis_result["五行喜忌"]["喜用神"]
        beneficial_element = wuxing_xi_ji_str.split('(')[0]
        
        crystals = crystals_by_wuxing.get(beneficial_element, [])
        
        if not crystals:
            return {"error": f"未找到与 {beneficial_element} 五行相关的水晶推荐"}
        
        return {
            '推荐水晶': crystals
        }
    
    except KeyError as e:
        return {"error": "分析结果不完整，无法选择水晶"}

        # ==================== 根据五行缺失情况选择水晶 ====================
       # ==================== 根据五行缺失情况选择水晶 ====================
def choose_crystals_based_on_wuxing_deficiency(analysis_result):
    """
    根据八字五行的缺失情况来选择合适的水晶
    """
    try:
        print("分析结果:", analysis_result)  # 调试信息
        wuxing_balance = analysis_result.get("五行强弱", {})
        print("五行强弱:", wuxing_balance)  # 调试信息
        
        if not wuxing_balance:
            print("没有五行强弱数据")  # 调试信息
            return {"缺失五行": [], "推荐补充水晶": {}}
        
        # 计算平均值
        values = [float(v) for v in wuxing_balance.values()]
        avg = sum(values) / len(values) if values else 0
        print(f"五行平均值: {avg}")  # 调试信息
        
        # 找出显著低于平均值的五行（低于平均值20%视为偏弱）
        threshold = avg * 0.8
        print(f"阈值: {threshold}")  # 调试信息
        
        weak_elements = []
        for wuxing, percentage in wuxing_balance.items():
            try:
                value = float(percentage)
                if value < threshold:
                    weak_elements.append({
                        "五行": wuxing,
                        "比例": f"{value}%",
                        "分析": f"{wuxing}的能量为{value}%，低于平均水平，建议补充"
                    })
                    print(f"发现偏弱五行: {wuxing}, 比例: {value}%")  # 调试信息
            except (ValueError, TypeError) as e:
                print(f"处理{wuxing}时出错: {str(e)}")  # 调试信息
                continue
        
        print("偏弱五行:", weak_elements)  # 调试信息
        
        # 根据缺失的五行选择水晶
        crystals_for_missing_elements = {}
        for element in weak_elements:
            wuxing = element["五行"]
            crystals = crystals_by_wuxing.get(wuxing, [])
            if crystals:  # 只有当有推荐的水晶时才添加
                crystals_for_missing_elements[wuxing] = crystals
            print(f"为{wuxing}推荐水晶: {crystals}")  # 调试信息
        
        result = {
            "缺失五行": weak_elements,
            "推荐补充水晶": crystals_for_missing_elements
        }
        print("返回结果:", result)  # 调试信息
        return result
        
    except Exception as e:
        print("错误:", str(e))  # 调试信息
        return {"缺失五行": [], "推荐补充水晶": {}}
        # ==================== 幸运数字计算函数 ====================
def calculate_lucky_numbers(analysis_result: dict) -> list:
    """
    根据八字分析结果计算幸运数字。
    逻辑：
      - 从“喜用神”字段中提取最弱五行（格式："木(火)"，取括号前部分）
      - 从“日主”字段中提取日主五行（格式："丙(火)"，取括号内部分）
      - 利用五行数字映射表组合两部分对应的数字（去重后返回列表）
    """
    try:
        # 提取最弱五行（取“喜用神”中括号前的部分）
        xi_shen_str = analysis_result["五行喜忌"]["喜用神"]
        weakest_wuxing = xi_shen_str.split('(')[0]
        
        # 提取日主五行（取“日主”中括号内的部分）
        rizhu_str = analysis_result["日主"]
        day_master_wuxing = rizhu_str.split('(')[1].strip(')')
        
        lucky_nums = set(five_element_numbers.get(weakest_wuxing, []) + 
                         five_element_numbers.get(day_master_wuxing, []))
        return list(lucky_nums)
    except Exception as e:
        print("计算幸运数字时出错:", e)
        return []

# ==================== 获取八字数据（API请求） ====================
def get_bazi_from_api(name, sex, birth_type, year, month, day, hours, minute):
    """调用外部API获取用户八字数据"""
    url = 'https://api.yuanfenju.com/index.php/v1/Bazi/paipan'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    API_KEY = 'iq3cJAvmtKbYgLAMVF7Nl3XRk'
    
    data = {
        'api_key': API_KEY,
        'name': name,
        'sex': sex,
        'type': birth_type,
        'year': year,
        'month': month,
        'day': day,
        'hours': hours,
        'minute': minute
    }
    
    try:
        # 创建一个不使用代理的会话
        session = requests.Session()
        session.trust_env = False  # 这会忽略环境变量中的代理设置
        
        response = session.post(url, headers=headers, data=data, verify=True)
        response.raise_for_status()
        api_response = response.json()
        
        if 'data' in api_response and 'bazi_info' in api_response['data'] and 'bazi' in api_response['data']['bazi_info']:
            return api_response['data']['bazi_info']['bazi']
        else:
            raise ValueError("API 返回数据不包含 'bazi' 字段，请检查接口响应。")
    except requests.exceptions.RequestException as e:
        raise Exception(f"API请求失败: {str(e)}")
        

        # ==================== 自动获取今日天干地支 ====================
def get_today_ganzhi():
    """
    获取今日天干地支
    返回: (天干, 地支) 元组
    """
    try:
        today = datetime.datetime.today()
        
        # 使用简单算法计算天干地支
        tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        # 计算天干地支索引
        day_num = (today - datetime.datetime(1900, 1, 1)).days % 60
        gan_idx = day_num % 10
        zhi_idx = day_num % 12
        
        return tiangan[gan_idx], dizhi[zhi_idx]
        
    except Exception as e:
        print(f"获取今日天干地支失败: {str(e)}")
        return "甲", "子"  # 发生错误时返回默认值

# ==================== 每日幸运色生成 ====================
def generate_daily_lucky_color(bazi_list: list, today_tiangan: str, today_dizhi: str) -> dict:
    """
    根据用户八字分析（喜用神、五行强弱）以及今日干支，
    生成五行调衡策略，匹配色系组合，输出幸运色及策略说明。
    """
    # 1. 解析八字并分析五行
    analysis = advanced_analyze(bazi_list)
    if 'error' in analysis:
        return {'error': analysis['error']}
    
    # 从分析结果中提取日主及五行喜忌信息
    # 注意：analysis['五行喜忌']['喜用神'] 格式如 "木(火)"
    wuxing_xi_ji_str = analysis["五行喜忌"]["喜用神"]
    beneficial_element = wuxing_xi_ji_str.split('(')[1].strip(')')
    
    detrimental_str = analysis['五行喜忌']['忌神']
    detrimental_element = detrimental_str.split('(')[1].strip(')')
    
    # 日主元素（如 "丙(火)" -> "火"）
    rizhu_str = analysis['日主']
    rizhu_element = rizhu_str.split('(')[1].strip(')')
    
    # 2. 解析今日干支：获取天干与地支对应的五行
    today_tiangan_element = TIANGAN_WUXING[today_tiangan]  # 如甲->木
    # 简单定义地支五行（与藏干大致对应）
    DIZHI_WUXING_SIMPLE = {
        '子': '水', '丑': '土', '寅': '木', '卯': '木',
        '辰': '土', '巳': '火', '午': '火', '未': '土',
        '申': '金', '酉': '金', '戌': '土', '亥': '水'
    }
    today_dizhi_element = DIZHI_WUXING_SIMPLE[today_dizhi]
    
    # 3. 生成五行调衡策略及匹配色系
    if today_tiangan_element == beneficial_element:
        # 今日天干与喜用神相合或生
        lucky_color = TIANGAN_COLOR[today_tiangan]['color']
        strategy = (f"今日天干【{today_tiangan}】（{today_tiangan_element}）"
                    f"与您的喜用神【{beneficial_element}】相生，推荐使用天干主色。")
    elif today_dizhi_element == beneficial_element:
        lucky_color = DIZHI_COLOR[today_dizhi]['color']
        strategy = (f"今日地支【{today_dizhi}】（{today_dizhi_element}）"
                    f"与您的喜用神【{beneficial_element}】相合，推荐使用地支主色。")
    elif today_tiangan_element == detrimental_element or today_dizhi_element == detrimental_element:
        lucky_color = FIVE_ELEMENT_DEFAULT_COLOR[beneficial_element]
        strategy = (f"今日干支中出现忌神【{detrimental_element}】，"
                    f"因此采用补益喜用神【{beneficial_element}】的默认色。")
    else:
        lucky_color = FIVE_ELEMENT_DEFAULT_COLOR[beneficial_element]
        strategy = (f"今日干支未明显强化或削弱您的喜用神，"
                    f"推荐采用喜用神【{beneficial_element}】的默认色。")
    
    return {
        'lucky_color': lucky_color,
        'strategy': strategy, 
    }

# ==================== 根据喜用神与日主强弱选择日常活动 ====================
def choose_daily_activities(analysis_result):
    """
    根据八字分析结果中的喜用神、日柱的五行强弱来选择日常活动。
    """
    
    try:
        # 获取日主（如 "丙(火)"）
        rizhu_str = analysis_result["日主"]
        rizhu_element = rizhu_str.split('(')[1].strip(')')
        
        # 获取喜用神（如 "木(火)"），并提取五行
        wuxing_xi_ji_str = analysis_result['五行喜忌']['喜用神']
        beneficial_element = wuxing_xi_ji_str.split('(')[0]  # 提取喜用神的五行
        
        # 获取五行强弱信息
        wuxing_count = analysis_result["五行强弱"]
        
        # 根据喜用神推荐活动
        activities = activities_by_wuxing.get(beneficial_element, {}).get("日常活动", [])
        
        # 根据五行强弱进一步筛选推荐活动（如果某个五行特别弱，可以推荐增强该五行的活动）
        activities_for_weak_elements = []
        for element, count in wuxing_count.items():
            if count == 0:  # 如果该五行缺失，推荐与该五行相关的活动
                activities_for_weak_elements.extend(activities_by_wuxing.get(element, {}).get("日常活动", []))
        
        # 返回推荐的活动列表
        return {
            "喜用神": beneficial_element,
            "推荐活动": activities,
            "五行缺失活动": activities_for_weak_elements
        }
    
    except Exception as e:
        return {"error": str(e)}

# ==================== 颜色可视化函数 ====================
def visualize_color(hex_color):
    """
    将十六进制颜色代码转换为更易读的格式，包括RGB值和颜色描述
    """
    # 移除#号并转换为RGB
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # 创建颜色信息字典
    color_info = {
        'hex': f'#{hex_color}',
        'rgb': f'rgb({r}, {g}, {b})',
        'preview': f'#{hex_color}',  # 用于前端显示的颜色值
        'description': f'这是一个RGB值为({r}, {g}, {b})的颜色'
    }
    
    return color_info

# ==================== Flask 后端接口 ====================
#即对接文档
@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return send_file('index.html')
    try:
        data = request.get_json()
        print("收到的数据:", data)  # 添加日志
        
        if not data:
            return jsonify({'error': '未接收到数据'}), 400
            
        # 获取输入数据
        name = data.get('name')
        sex = data.get('sex')
        birth_type = data.get('type')
        year = data.get('year')
        month = data.get('month')
        day = data.get('day')
        hours = data.get('hours')
        minute = data.get('minute')
        
        # 检查必要参数
        required_fields = {
            'name': name,
            'sex': sex,
            'type': birth_type,
            'year': year,
            'month': month,
            'day': day,
            'hours': hours,
            'minute': minute
        }
        
        missing_fields = [field for field, value in required_fields.items() if value is None]
        if missing_fields:
            return jsonify({'error': f'缺少必要的参数: {", ".join(missing_fields)}'}), 400
            
        # 类型检查
        try:
            sex = int(sex)
            birth_type = int(birth_type)
            year = int(year)
            month = int(month)
            day = int(day)
            hours = int(hours)
            minute = int(minute)
        except (ValueError, TypeError) as e:
            return jsonify({'error': f'参数类型错误: {str(e)}'}), 400
            
        # 调用原有的分析函数
        return analyze_bazi()
        
    except Exception as e:
        print("错误:", str(e))  # 添加日志
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze_bazi():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '未接收到数据'}), 400
        
        # 获取输入数据
        name = data.get('name')
        sex = data.get('sex')
        birth_type = data.get('type')
        year = data.get('year')
        month = data.get('month')
        day = data.get('day')
        hours = data.get('hours')
        minute = data.get('minute')
        
        # 检查必要参数
        if not all([name, isinstance(sex, int), isinstance(birth_type, int), 
                   year, month, day, hours, minute]):
            return jsonify({'error': '请提供所有必要的参数'}), 400
        
        try:
            # 调用API获取八字数据
            bazi_list = get_bazi_from_api(
                name, sex, birth_type, year, month, day, hours, minute
            )
            
            if not bazi_list or len(bazi_list) != 4:
                return jsonify({'error': '无法获取有效的八字数据'}), 400
            
            # 进行八字分析
            analysis_result = advanced_analyze(bazi_list)
            if "error" in analysis_result:
                return jsonify({'error': analysis_result["error"]}), 400
            
            # 获取水晶推荐
            crystal_recommendations = choose_crystals_based_on_xi_shen(analysis_result)
            if "error" in crystal_recommendations:
                return jsonify({'error': crystal_recommendations["error"]}), 400
            
            # 获取五行缺失分析
            wuxing_crystal_recommendations = choose_crystals_based_on_wuxing_deficiency(analysis_result)
            if "error" in wuxing_crystal_recommendations:
                return jsonify({'error': wuxing_crystal_recommendations["error"]}), 400
            
            # 计算幸运数字
            lucky_numbers = calculate_lucky_numbers(analysis_result)

            # 获取今日干支
            today_tiangan, today_dizhi = get_today_ganzhi()
            if today_tiangan is None or today_dizhi is None:
                # 如果获取失败，使用年柱作为备选
                today_tiangan = bazi_list[0][0]
                today_dizhi = bazi_list[0][1]

            # 计算幸运颜色
            lucky_color_result = generate_daily_lucky_color(bazi_list, today_tiangan, today_dizhi)
            if "error" in lucky_color_result:
                return jsonify({'error': lucky_color_result["error"]}), 400

            #添加颜色可视化信息
            color_visualization = visualize_color(lucky_color_result['lucky_color'])
            lucky_color_result['visualization'] = color_visualization

            #推荐活动
            activities_recommendation=choose_daily_activities(analysis_result) 

            #今日干支
            today_tiangan=get_today_ganzhi()

            
            # 合并分析结果
            result = {
                '八字': " ".join(bazi_list),
                '日主': analysis_result.get('日主', ''),
                '五行强弱': analysis_result.get('五行强弱', {}),
                '五行喜忌': analysis_result.get('五行喜忌', {}),
                '喜用神_天干': crystal_recommendations.get('推荐水晶', []),
                '忌神_天干': analysis_result.get('忌神_天干', []),
                '五行_水晶': {
                    '缺失五行': wuxing_crystal_recommendations.get('缺失五行', []),
                    '推荐补充水晶': wuxing_crystal_recommendations.get('推荐补充水晶', {})
                },
                '幸运数字': lucky_numbers,
                '幸运颜色': {
                    'color': lucky_color_result['lucky_color'],
                    'strategy': lucky_color_result['strategy'],
                },
                '推荐活动': activities_recommendation,
                '今日天干': [today_tiangan, today_dizhi]  # 返回天干地支数组
            }
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({'error': f'处理数据时出错: {str(e)}'}), 400
            
    except Exception as e:
        return jsonify({'error': f'请求处理失败: {str(e)}'}), 400

@app.route('/api/analyze', methods=['OPTIONS'])
def handle_options():
    response = make_response()
    return response

#把主程序入口换成这个
if __name__ == "__main__":
    app.run(debug=True)