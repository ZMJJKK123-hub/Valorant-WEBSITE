import streamlit as st
import os
from PIL import Image
import pandas as pd

#streamlit run webcontent.py


# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem !important;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(45deg, #FF4655, #0F1923);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        padding: 1rem;
    }
    .section-header {
        font-size: 2rem !important;
        font-weight: bold;
        color: #FF4655;
        border-bottom: 2px solid #FF4655;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #0F1923;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #FF4655;
    }
    .sidebar .sidebar-content {
        background-color: #0F1923;
    }
    .stButton button {
        background-color: #FF4655;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #e63e4c;
        transform: translateY(-2px);
    }
    .weapon-card {
        background: linear-gradient(135deg, #1a2b3c, #0F1923);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #2a3b4c;
        transition: transform 0.3s ease;
    }
    .weapon-card:hover {
        transform: translateY(-5px);
        border-color: #FF4655;
    }
    .hero-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    .hero-card {
        background: #1a2b3c;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    .hero-card:hover {
        border-color: #FF4655;
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)


# 统一图片尺寸的函数
def resize_hero_image(image_path, target_size=(300, 400)):
    try:
        image = Image.open(image_path)
        # 保持宽高比进行缩放，然后裁剪到目标尺寸
        image.thumbnail((target_size[0], target_size[1] * 2), Image.Resampling.LANCZOS)

        # 创建新的空白图像
        new_image = Image.new('RGB', target_size, (0, 0, 0))

        # 计算粘贴位置（居中）
        x = (target_size[0] - image.width) // 2
        y = (target_size[1] - image.height) // 2

        # 粘贴图像
        new_image.paste(image, (x, y))

        return new_image
    except Exception as e:
        st.error(f"处理图片时出错: {e}")
        return None

def get_images(directory_path):
    image_files=[]
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            image_files.append(file_path)
    return image_files


# 清理 KAST 列数据
def clean_kast_data(df):
    # 方法1: 分割字符串并清理
    if df['KAST'].dtype == 'object':
        # 将整个字符串分割成单个百分比值
        kast_values = df['KAST'].iloc[0].split('%')  # 按 % 分割
        kast_values = [x for x in kast_values if x and x.strip()]  # 移除空值

        # 清理每个值，移除特殊字符
        cleaned_values = []
        for value in kast_values:
            # 移除所有非数字字符（除了小数点）
            cleaned = ''.join(filter(str.isdigit, value))
            if cleaned:  # 确保不是空字符串
                cleaned_values.append(int(cleaned))

        return cleaned_values
    return df['KAST']


# 使用清理后的数据



def resize_images(image_files_path,width,height):
    original_image = Image.open(image_files_path)
    new_image = original_image.resize((width,height))
    return new_image


def find_name_of_image(target_name,lst):
    for item in lst:
        if item==target_name:
            return item
    else:
        return None


def guns_info(name, text):
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button('🔙 返回上一页', key=f'back_{name}'):
            st.session_state.current = 'home'

    st.markdown(f'<div class="section-header">{name.upper()} 详细信息</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 3])
    with col1:
        st.image(f'guns\\{name}.png', width=400)
    with col2:
        st.markdown(f'<div class="card">{text}</div>', unsafe_allow_html=True)


def jump_to_guns(name):
    if st.button(f'🔍 查看{name}数据', key=name):
        st.session_state.current = name

def create_weapon_card(image_path, name, category):
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(image_path, width=150)
    with col2:
        st.subheader(name)
        st.caption(f"类别: {category}")
        if st.button(f'查看详情', key=f'btn_{name}'):
            st.session_state.current = name

def first_duel_heroes_info(name,text):
    if st.button('🔙返回上一页', key='home'):
        st.session_state.current = 'home'
    st.image(f'heroes\\duel\\first_duel\\{name}.png', width=400)
    st.markdown(f'''{text}''')


def second_duel_heroes_info(name,text):
    if st.button('🔙返回上一页', key='home'):
        st.session_state.current = 'home'
    st.image(f'heroes\\duel\\second_duel\\{name}.png', width=400)
    st.markdown(f'''{text}''')


def item_heroes_info(name,text):
    if st.button('🔙返回上一页', key='home'):
        st.session_state.current = 'home'
    st.image(f'heroes\\item\\{name}.png', width=400)
    st.markdown(f'''{text}''')


def controller_heroes_info(name,text):
    if st.button('🔙返回上一页', key='home'):
        st.session_state.current = 'home'
    st.image(f'heroes\\controller\\{name}.png', width=400)
    st.markdown(f'''{text}''')


def sentinel_heroes_info(name,text):
    if st.button('🔙返回上一页', key='home'):
        st.session_state.current = 'home'
    st.image(f'heroes\\sentinel\\{name}.png', width=400)
    st.markdown(f'''{text}''')

if __name__ == "__main__":

    st.set_page_config(
        page_title='Valorant Homepage',
        page_icon='🎮',
        layout='wide',
        initial_sidebar_state='expanded'
    )

    st.markdown('<div class="main-header">VALORANT 游戏指南</div>', unsafe_allow_html=True)

    if 'current' not in st.session_state:
        st.session_state.current = 'home'

    if 'radio_index' not in st.session_state:
        st.session_state.radio_index = 0

    if 'heroes' not in st.session_state:
        st.session_state.heroes = None



    if st.session_state.current == 'home':


        with st.sidebar:

            st.title='零基础开始的导航菜单'
            select_tab = st.radio(
                "选择学习章节",
                [
                    '👋 关于我们',
                    '📋 官方介绍',
                    '🎮 序章：游戏的基本认识',
                    '💰 第一章：经济系统介绍',
                    '🔫 第二章：枪械系统介绍',
                    '🦸 第三章：英雄角色介绍',
                    '🗺️ 第四章：地图基本介绍',
                    '⚡ 第五章：英雄进阶技巧',
                    '🏆 第六章：职业比赛学习',
                    '🚀 第七章：游戏进阶技巧',
                    '📊 附录：职业选手数据',
                ],
                index=st.session_state.radio_index
            )

        if select_tab == '👋 关于我们':
            st.session_state.radio_index = 0
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown('<div class="section-header">关于作者</div>', unsafe_allow_html=True)
                st.markdown("""
                        <div class="card">
                        <h3>👨‍💻 李义鑫</h3>
                        <p>清华大学水木书院54班</p>
                        <p>🎮 无畏契约爱好者</p>
                        </div>
                        """, unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="section-header">网站宗旨</div>', unsafe_allow_html=True)
                st.markdown("""
                        <div class="card">
                        <h3>🚀 解决萌新上手难题</h3>
                        <p>• 提供全面的游戏基础知识</p>
                        <p>• 降低游戏学习门槛</p>
                        <p>• 提升游戏体验和乐趣</p>
                        <p>• 再也不怕玩不懂游戏！</p>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 🎯 使用指南")
            st.info("💡 使用左侧导航菜单选择学习内容，从基础到进阶，循序渐进地掌握游戏技巧！")




        elif select_tab == '📋 官方介绍':

            st.session_state.radio_index = 1

            st.markdown('<div class="section-header">官方介绍</div>', unsafe_allow_html=True)

            st.warning("这些都是官方的原话，有点公式，完全可以不用看，后面会有更加详细的介绍")

            with st.expander('📖 点击查看官方附录', expanded=False):

                cols = st.columns(2)

                with cols[0]:
                    st.markdown("""

                            <div class="card">

                            <h3>🎮 游戏概览</h3>

                            <p>《无畏契约》是一款由拳头游戏开发的5V5战术射击游戏，结合了角色技能与经典射击玩法。</p>

                            </div>

                            """, unsafe_allow_html=True)

                    st.markdown("""

                            <div class="card">

                            <h3>🌍 游戏背景</h3>

                            <p>设定在近未来的地球，经历"原初之光"事件后，部分人类获得超能力，成为"辐射人"。</p>

                            </div>

                            """, unsafe_allow_html=True)

                with cols[1]:
                    st.markdown("""

                            <div class="card">

                            <h3>⚔️ 核心玩法</h3>

                            <p>• 战术射击爆破模式</p>

                            <p>• 角色技能组合</p>

                            <p>• 团队配合协作</p>

                            </div>

                            """, unsafe_allow_html=True)

                    st.markdown("""

                            <div class="card">

                            <h3>🎯 角色分类</h3>

                            <p>• 先锋 - 切入创造优势</p>

                            <p>• 控场者 - 控制战场</p>

                            <p>• 守卫 - 防守专家</p>

                            </div>

                            """, unsafe_allow_html=True)





        elif select_tab == '🎮 序章：游戏的基本认识':

            st.session_state.radio_index = 2

            st.markdown('<div class="section-header">游戏基本知识</div>', unsafe_allow_html=True)

            cols = st.columns(2)

            with cols[0]:

                st.markdown("""

                        <div class="card">

                        <h3>🎯 核心玩法</h3>

                        <p>这是一个以<strong>爆破模式</strong>为主的战术射击游戏</p>

                        </div>

                        """, unsafe_allow_html=True)

                st.markdown("""

                        <div class="card">

                        <h3>🏆 胜利条件</h3>

                        <p>先取得<strong>13局</strong>胜利的队伍获胜！</p>

                        <p>排位模式平局进入加时</p>

                        </div>

                        """, unsafe_allow_html=True)

                st.markdown("""

                        <div class="card">

                        <h3>🦸 角色系统</h3>

                        <p>多种<strong>特工角色</strong>可供选择</p>

                        <p>每个角色都有独特的<strong>技能</strong></p>

                        </div>

                        """, unsafe_allow_html=True)

            with cols[1]:

                st.markdown("""

                        <div class="card">

                        <h3>🔫 武器系统</h3>

                        <p>多种类型的<strong>枪械武器</strong></p>

                        <p>需要根据局势谨慎选择！</p>

                        </div>

                        """, unsafe_allow_html=True)

                st.markdown("""

                        <div class="card">

                        <h3>💰 经济系统</h3>

                        <p>游戏内<strong>货币系统</strong></p>

                        <p>购买枪械和道具</p>

                        <p>行为影响货币数量</p>

                        </div>

                        """, unsafe_allow_html=True)

                st.markdown("""

                        <div class="card">

                        <h3>🤝 团队合作</h3>

                        <p><strong>沟通</strong>至关重要！</p>

                        <p>多和队友交流，开麦沟通！</p>

                        </div>

                        """, unsafe_allow_html=True)

            with st.expander('📚 附录：爆破模式详解', expanded=False):

                st.markdown("""

                        - **10人5v5对决**，达到指定回合数获胜

                        - **进攻方**：安装C4炸弹或消灭所有防守方

                        - **防守方**：阻止安装或拆除C4，或消灭所有进攻方

                        """)



        elif select_tab == '💰 第一章：经济系统介绍':

            st.session_state.radio_index = 3

            st.markdown('<div class="section-header">经济系统详解</div>', unsafe_allow_html=True)

            st.markdown("""

                    <div class="card">

                    <h3>💡 经济系统核心概念</h3>

                    <p>每个回合开始前有时间购买枪械和道具，合理的经济管理是获胜的关键！</p>

                    </div>

                    """, unsafe_allow_html=True)

            tab1, tab2, tab3 = st.tabs(["🎯 购买界面", "💰 经济来源", "📊 经济管理"])

            with tab1:

                st.markdown("### 🛒 购买界面指南")

                if os.path.exists("economy_system/example.png"):

                    st.image("economy_system/example.png", use_container_width=True, caption="完整的购买界面")

                else:

                    st.error("图片文件不存在！")

                cols = st.columns(3)

                with cols[0]:

                    if os.path.exists("economy_system/detailed.png"):
                        st.image("economy_system/detailed.png", caption="个人信息界面")

                with cols[1]:

                    if os.path.exists("economy_system/guns.png"):
                        st.image("economy_system/guns.png", caption="枪械购买区域")

                with cols[2]:

                    if os.path.exists("economy_system/skill1.png"):
                        st.image("economy_system/skill1.png", caption="技能购买区域")

            with tab2:

                st.markdown("### 💰 经济来源")

                cols = st.columns(2)

                with cols[0]:
                    st.markdown("""

                            <div class="card">

                            <h3>🎯 击杀奖励</h3>

                            <p>每击杀一个敌人：<strong>+200</strong></p>

                            </div>

                            """, unsafe_allow_html=True)

                    st.markdown("""

                            <div class="card">

                            <h3>🏆 回合奖励</h3>

                            <p>获胜方：<strong>+3000</strong></p>

                            <p>失败方：<strong>+1900</strong></p>

                            </div>

                            """, unsafe_allow_html=True)

                with cols[1]:
                    st.markdown("""

                            <div class="card">

                            <h3>💣 下包奖励</h3>

                            <p>安装/拆除C4：<strong>+300</strong></p>

                            </div>

                            """, unsafe_allow_html=True)

                    st.markdown("""

                            <div class="card">

                            <h3>🔄 连败补偿</h3>

                            <p>第一次失败：<strong>+1900</strong></p>
                            
                            <p>第二次失败：<strong>+2400</strong></p>

                            <p>第三次失败：<strong>+2900</strong></p>
                            
                            <p>更多次失败（保持不变）：<strong>+2900</strong></p>

                            </div>

                            """, unsafe_allow_html=True)

            with tab3:

                st.markdown("### 📊 经济策略")

                strategies = {
                    "手枪局": {
                        "description": "每半场的第一局，双方都只有800初始经济",
                        "进攻方策略": [
                            "**经典鬼魅+轻甲**: 鬼魅(500) + 轻甲(400) = 900（超支100，需要队友给枪）",
                            "**技能优先**: 部分英雄如Sage、Killjoy优先购买技能，手枪使用默认经典",
                            "**团队配合**: 1-2人购买正义(800)负责近点突破，其他人鬼魅提供中距离火力",
                            "**道具协同**: 利用闪光弹、烟雾弹等技能创造对枪优势",
                            "**战术选择**: 快速Rush点位或默认架枪，避免长时间对枪"
                        ],
                        "防守方策略": [
                            "**架点优势**: 利用防守方架点优势，购买护甲提升生存能力",
                            "**幽灵战术**: 全队静步防守，利用声音信息获取优势",
                            "**交叉火力**: 设置交叉火力点，弥补手枪精度不足",
                            "**技能防守**: Cypher、Killjoy等利用陷阱技能拖延进攻",
                            "**经济规划**: 确保即使输掉手枪局，第二局也能强起"
                        ],
                        "关键要点": [
                            "爆头线控制至关重要，手枪爆头往往一击必杀",
                            "避免远距离对枪，尽量拉近交战距离",
                            "善用近战攻击，手枪局刀杀很常见",
                            "团队沟通集火目标，快速建立人数优势"
                        ]
                    },
                    "ECO局": {
                        "description": "经济不足时选择节省经济的回合，为下一局积累资金",
                        "购买策略": [
                            "**全ECO**: 只购买技能或什么都不买，确保下局全员长枪+全甲",
                            "**半起局**: 1-2人购买Spectre/Stinger等廉价冲锋枪，其他人手枪",
                            "**技能投资**: 购买关键技能如烟雾弹、闪光弹，增加翻盘机会",
                            "**护甲选择**: 优先购买轻甲(400)而非重甲(1000)，节省经济",
                            "**武器选择**: 正义(800)、鬼魅(500)、狂怒(450)等高性价比手枪"
                        ],
                        "战术目标": [
                            "**伤害输出**: 尽量对敌人造成伤害，消耗对方护甲和经济",
                            "**武器缴获**: 尝试击杀敌人获取更好的武器",
                            "**时间拖延**: 尽量拖延回合时间，消耗对方技能和耐心",
                            "**信息收集**: 侦察对方战术和站位，为下局做准备",
                            "**意外翻盘**: 利用对方大意创造翻盘机会"
                        ],
                        "关键要点": [
                            "经济临界点：团队总经济约15000-17000时考虑ECO",
                            "避免无谓的武器购买，确保下局经济健康",
                            "利用地图知识和技能弥补装备劣势",
                            "保持积极心态，ECO局是战术需要而非放弃"
                        ]
                    },
                    "半起局": {
                        "description": "经济状况不一时，部分队员购买较好装备的混合配置",
                        "阵容配置": [
                            "**2-3配置**: 2把长枪(Vandal/Phantom) + 3把冲锋枪(Spectre)/手枪",
                            "**1-4配置**: 1把狙击枪(Operator) + 4把廉价武器",
                            "**技能优先**: 关键英雄如控制器购买全技能，枪手购买基础装备",
                            "**护甲分配**: 长枪手购买重甲，其他队员轻甲或无甲",
                            "**经济平衡**: 确保下局无论胜负都能全员长枪"
                        ],
                        "战术执行": [
                            "**长枪掩护**: 长枪手负责远距离架枪，廉价武器负责近点突破",
                            "**道具协同**: 充分利用所有技能，弥补火力不足",
                            "**集火战术**: 团队集中火力，快速击杀持长枪的敌人",
                            "**位置选择**: 避免开阔地带交战，利用狭小空间优势",
                            "**转点策略**: 灵活转点，制造局部多打少"
                        ],
                        "武器选择": [
                            "**性价比之王**: Spectre(1600) - 消音、精度高、伤害可观",
                            "**近战霸主**: Judge(1850) - 近距离一击必杀",
                            "**经济狙击**: Marshal(950) - 远距离架点，爆头必杀",
                            "**全能选择**: Bulldog(2050) - 具备瞄准镜，中远距离优秀"
                        ]
                    },
                    "长枪局": {
                        "description": "全员购买最佳装备的回合，胜负对比赛走向影响重大",
                        "标准配置": [
                            "**步枪选择**: Vandal(2900) 或 Phantom(2900) + 重甲(1000)",
                            "**全技能**: 所有英雄购买全部可用技能",
                            "**道具齐全**: 烟雾弹、闪光弹、侦察道具等全部备齐",
                            "**阵容平衡**: 确保有远、中、近全距离作战能力",
                            "**经济预留**: 保留至少1000经济，为下局做准备"
                        ],
                        "进攻方战术": [
                            "**默认展开**: 控制地图关键区域，收集信息后再决定进攻方向",
                            "**道具压制**: 使用烟雾弹封锁视野，闪光弹创造突破机会",
                            "**同步进攻**: 多方向同步推进，分散防守方注意力",
                            "**爆弹战术**: 集中所有道具快速攻占一个点位",
                            "**转点欺骗**: 假打一个点位，实际转点另一个点位"
                        ],
                        "防守方战术": [
                            "**前压侦察**: 开局前压获取信息，了解进攻方向",
                            "**交叉火力**: 设置多个交叉火力点，覆盖所有入口",
                            "**技能联防**: 利用陷阱、摄像头等技能构建防御体系",
                            "**灵活回防**: 根据信息快速回防，形成局部人数优势",
                            "**经济控制**: 尽量避免死亡，保护昂贵装备"
                        ],
                        "关键要点": [
                            "**武器选择**: Vandal适合爆头玩家，Phantom适合扫射转移",
                            "**护甲必备**: 重甲对长枪局生存能力至关重要",
                            "**技能时机**: 不要一次性用完所有技能，留关键技能应对残局",
                            "**沟通协调**: 长枪局需要极高的团队配合和沟通"
                        ]
                    },
                    "加时局": {
                        "description": "比赛进入加时后的经济管理，每局经济固定为5000",
                        "经济特点": [
                            "**固定经济**: 每局开始固定5000经济，无需考虑经济积累",
                            "**全装购买**: 可以购买任何武器+全甲+全技能",
                            "**无后顾之忧**: 无需为下局经济考虑，全力争取当前回合",
                            "**心理因素**: 加时局心理压力大，需要保持冷静"
                        ],
                        "战术调整": [
                            "**阵容优化**: 根据加时比分调整英雄选择，侧重当前回合取胜",
                            "**激进战术**: 可以尝试高风险高回报的战术",
                            "**技能最大化**: 每回合都购买全技能，充分利用",
                            "**心态管理**: 保持稳定心态，避免因压力出现失误"
                        ],
                        "关键要点": [
                            "Operator在加时局价值巨大，可以考虑购买",
                            "不要保留经济，每回合都购买最佳装备",
                            "注意对方经济模式，预判对方购买选择",
                            "加时局往往取决于细节处理和心态稳定"
                        ]
                    },
                    "经济连锁反应": {
                        "description": "理解经济系统的连锁反应，做出最优决策",
                        "胜利经济": [
                            "**手枪局胜利**: 第二局建议4把长枪+1把冲锋枪，确保第三局也能全装",
                            "**连胜奖励**: 连续胜利时经济会越来越充裕",
                            "**装备保护**: 胜利时尽量保护自己的昂贵装备",
                            "**经济压制**: 通过连续胜利压制对方经济，建立装备优势"
                        ],
                        "失败经济": [
                            "**连败补偿**: 第二次失败2400，第三次及以后2900",
                            "**强起时机**: 有时选择强起打断对方经济连胜更有利",
                            "**ECO管理**: 合理选择ECO局，避免经济崩盘",
                            "**翻盘机会**: 利用对方大意实现经济翻盘"
                        ],
                        "团队协调": [
                            "**统一决策**: 全队必须统一经济决策，避免有人全装有人ECO",
                            "**经济沟通**: 每回合开始前沟通经济状况和购买计划",
                            "**武器共享**: 经济好的队员为经济差的队员购买武器",
                            "**策略调整**: 根据对方经济状况调整己方战术"
                        ]
                    }
                }

                # 在页面中显示扩充后的经济策略内容
                for strategy_name, strategy_info in strategies.items():
                    with st.expander(f"💰 {strategy_name} - {strategy_info['description']}",
                                     expanded=strategy_name == "手枪局"):

                        col1, col2 = st.columns(2)

                        with col1:
                            if '进攻方策略' in strategy_info:
                                st.markdown("#### 🎯 进攻策略")
                                for tactic in strategy_info['进攻方策略']:
                                    st.markdown(f"• {tactic}")

                            if '购买策略' in strategy_info:
                                st.markdown("#### 🛒 购买策略")
                                for purchase in strategy_info['购买策略']:
                                    st.markdown(f"• {purchase}")

                            if '标准配置' in strategy_info:
                                st.markdown("#### 🔫 标准配置")
                                for config in strategy_info['标准配置']:
                                    st.markdown(f"• {config}")

                            if '阵容配置' in strategy_info:
                                st.markdown("#### 🔫 阵容配置")
                                for config in strategy_info['阵容配置']:
                                    st.markdown(f"• {config}")

                            if '进攻方战术' in strategy_info:
                                st.markdown("#### 🔫 进攻方战术")
                                for config in strategy_info['进攻方战术']:
                                    st.markdown(f"• {config}")

                            if '经济特点' in strategy_info:
                                st.markdown("#### 🔫 经济特点")
                                for config in strategy_info['经济特点']:
                                    st.markdown(f"• {config}")

                        with col2:
                            if '防守方策略' in strategy_info:
                                st.markdown("#### 🛡️ 防守策略")
                                for tactic in strategy_info['防守方策略']:
                                    st.markdown(f"• {tactic}")

                            if '战术目标' in strategy_info:
                                st.markdown("#### 🎯 战术目标")
                                for goal in strategy_info['战术目标']:
                                    st.markdown(f"• {goal}")

                            if '战术执行' in strategy_info:
                                st.markdown("#### ⚡ 战术执行")
                                for execution in strategy_info['战术执行']:
                                    st.markdown(f"• {execution}")

                            if '武器选择' in strategy_info:
                                st.markdown("#### 🔫 武器选择")
                                for config in strategy_info['武器选择']:
                                    st.markdown(f"• {config}")

                            if '防守方战术' in strategy_info:
                                st.markdown("#### 🔫 防守方战术")
                                for config in strategy_info['防守方战术']:
                                    st.markdown(f"• {config}")

                            if '战术调整' in strategy_info:
                                st.markdown("#### 🔫 战术调整")
                                for config in strategy_info['战术调整']:
                                    st.markdown(f"• {config}")



                        # 显示关键要点
                        if '关键要点' in strategy_info:
                            st.markdown("#### 💡 关键要点")
                            cols = st.columns(2)
                            for i, point in enumerate(strategy_info['关键要点']):
                                with cols[i % 2]:
                                    st.info(f"• {point}")

                        # 特殊内容显示
                        if strategy_name == "经济连锁反应":
                            if strategy_name == "经济连锁反应":
                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    st.markdown("#### 🏆 胜利经济")
                                    for item in strategy_info['胜利经济']:
                                        st.markdown(f"• {item}")

                                with col2:
                                    st.markdown("#### 💔 失败经济")
                                    for item in strategy_info['失败经济']:
                                        st.markdown(f"• {item}")

                                with col3:
                                    st.markdown("#### 🤝 团队协调")
                                    for item in strategy_info['团队协调']:
                                        st.markdown(f"• {item}")
                            st.markdown("#### 🔄 经济连锁反应分析")
                            st.markdown("""
                            **经济雪球效应**: 一旦建立经济优势，可以通过连续压制让对方难以翻身  
                            **心理经济学**: 经济劣势时容易产生急躁情绪，导致决策失误  
                            **转折点识别**: 识别比赛的经济转折点，及时调整策略  
                            **风险回报**: 评估强起局的风险与潜在回报，做出最优选择
                            """)

                        st.markdown("---")



        elif select_tab == '🔫 第二章：枪械系统介绍':

            st.session_state.radio_index = 4

            st.markdown('<div class="section-header">枪械系统大全</div>', unsafe_allow_html=True)

            guns_image_path = get_images('guns')

            # 枪械分类

            weapon_categories = {

                "手枪": ["classic", "shorty", "frenzy", "ghost", "sheriff"],

                "冲锋枪": ["stinger", "spectre"],

                "霰弹枪": ["bucky", "judge"],

                "步枪": ["bulldog", "guardian", "phantom", "vandal"],

                "狙击枪": ["marshal", "outlaw", "operator"],

                "机枪": ["ares", "odin"]

            }

            tabs = st.tabs(list(weapon_categories.keys()))

            for tab, (category, weapons) in zip(tabs, weapon_categories.items()):

                with tab:

                    st.markdown(f"### 🔫 {category}")

                    cols = st.columns(2)

                    for idx, weapon in enumerate(weapons):

                        with cols[idx % 2]:

                            image_path = find_name_of_image(f'guns\\{weapon}.png', guns_image_path)

                            if image_path:
                                st.image(image_path, width=200)

                                jump_to_guns(weapon)

                            st.markdown("---")




        elif select_tab == '🦸 第三章：英雄角色介绍':

            st.session_state.radio_index = 5

            st.markdown('<div class="section-header">英雄角色图鉴</div>', unsafe_allow_html=True)

            # 英雄角色介绍

            roles = {

                "🎯 决斗者": {

                    "path": "heroes/duel",

                    "description": "负责突破和首杀，枪法和意识至关重要",

                    "color": "#FF4655"

                },

                "⚡ 先锋": {

                    "path": "heroes/item",

                    "description": "为团队创造进攻机会和信息优势",

                    "color": "#0FCE76"

                },

                "🌫️ 控场者": {

                    "path": "heroes/controller",

                    "description": "控制战场视野和区域封锁",

                    "color": "#1EB6D1"

                },

                "🛡️ 哨位": {

                    "path": "heroes/sentinel",

                    "description": "防守专家，保护点位和后方安全",

                    "color": "#FFD166"

                }

            }

            # 创建标签页

            tab_names = list(roles.keys())

            tabs = st.tabs(tab_names)

            for i, (role_name, role_info) in enumerate(roles.items()):

                with tabs[i]:

                    st.markdown(f'<h3 style="color:{role_info["color"]}">{role_info["description"]}</h3>',
                                unsafe_allow_html=True)

                    if role_name == "🎯 决斗者":

                        # 决斗者分为一突和二突

                        col1, col2 = st.columns(2)

                        with col1:

                            st.markdown("##### 🚀 第一决斗（一突）")

                            st.markdown("*主要负责首杀和突破*")

                            first_duel_images = get_images(f"{role_info['path']}/first_duel")

                            for img_path in first_duel_images:

                                hero_name = os.path.splitext(os.path.basename(img_path))[0]

                                with st.container():

                                    col_img, col_btn = st.columns([2, 3])

                                    with col_img:
                                        st.image(img_path, width=120)

                                    with col_btn:
                                        st.write(f"**{hero_name}**")

                                        if st.button(f"查看详情", key=f"first_duel_{hero_name}"):
                                            st.session_state.current = hero_name

                                        st.markdown("---")

                        with col2:

                            st.markdown("##### ⚡ 第二决斗（二突）")

                            st.markdown("*辅助突破和补枪*")

                            second_duel_images = get_images(f"{role_info['path']}/second_duel")

                            for img_path in second_duel_images:

                                hero_name = os.path.splitext(os.path.basename(img_path))[0]

                                with st.container():

                                    col_img, col_btn = st.columns([2, 3])

                                    with col_img:
                                        st.image(img_path, width=120)

                                    with col_btn:
                                        st.write(f"**{hero_name}**")

                                        if st.button(f"查看详情", key=f"second_duel_{hero_name}"):
                                            st.session_state.current = hero_name

                                        st.markdown("---")


                    else:

                        # 其他角色的展示

                        images = get_images(role_info['path'])

                        cols = st.columns(2)

                        for idx, img_path in enumerate(images):

                            hero_name = os.path.splitext(os.path.basename(img_path))[0]

                            with cols[idx % 2]:

                                with st.container():
                                    st.image(img_path, width=150)

                                    st.write(f"**{hero_name}**")

                                    if st.button(f"查看技能详情", key=f"{role_name}_{hero_name}"):
                                        st.session_state.current = hero_name

                                    st.markdown("---")


        elif select_tab == '🗺️ 第四章：地图基本介绍':

            st.session_state.radio_index = 6

            st.markdown('<div class="section-header">地图知识大全</div>', unsafe_allow_html=True)

            st.markdown("""

                    <div class="card">

                    <h3>🎯 地图学习要点</h3>

                    <p>• 熟悉炸弹点位置和布局</p>

                    <p>• 掌握关键对枪点位</p>

                    <p>• 了解进攻和防守路线</p>

                    <p>• 学习道具投掷点位</p>

                    </div>

                    """, unsafe_allow_html=True)

            # 获取地图图片

            map_images = get_images('map/map')

            # 创建网格布局

            cols = st.columns(3)

            for idx, map_path in enumerate(map_images):

                with cols[idx % 3]:

                    map_name = os.path.splitext(os.path.basename(map_path))[0]

                    # 创建地图卡片

                    with st.container():

                        st.image(map_path, use_container_width=True)

                        st.write(f"**{map_name}**")

                        # 添加查看详情按钮

                        col1, col2 = st.columns(2)

                        with col1:

                            if st.button(f"查看详情", key=f"map_{map_name}"):
                                st.session_state.current = map_name

                        with col2:

                            if st.button(f"平面图", key=f"plain_{map_name}"):
                                st.session_state.current = map_name

                        st.markdown("---")


        elif select_tab == '⚡ 第五章：英雄进阶技巧':

            st.session_state.radio_index = 7

            st.markdown('<div class="section-header">英雄进阶技巧</div>', unsafe_allow_html=True)

            st.warning("💡 推荐在掌握基础操作后再学习本章内容")

            col1, col2 = st.columns([1, 2])

            with col1:

                st.markdown("""

                        <div class="card">

                        <h3>🎮 基础设置</h3>

                        <p><strong>推荐键位：</strong></p>

                        <p>• Q, E, 鼠标侧键, X</p>

                        <p>• 选择最舒适的手感</p>

                        <p>• 保持一致性很重要</p>

                        </div>

                        """, unsafe_allow_html=True)

                st.markdown("""

                        <div class="card">

                        <h3>🎯 核心技巧</h3>

                        <p>• 预瞄头线位置</p>

                        <p>• 学习急停射击</p>

                        <p>• 掌握地图控制</p>

                        <p>• 团队配合沟通</p>

                        </div>

                        """, unsafe_allow_html=True)

            with col2:

                st.markdown("""

                        <div class="card">

                        <h3>🦸 英雄选择建议</h3>

                        <p>根据以下因素选择英雄：</p>

                        <p>• 个人游戏风格</p>

                        <p>• 团队阵容搭配</p>

                        <p>• 地图特性</p>

                        <p>• 对手阵容克制</p>

                        </div>

                        """, unsafe_allow_html=True)


            whole_heroes_image = get_images('whole heroes')

            # 完整的英雄进阶技巧数据库（包含所有英雄）
            # 完整的英雄进阶技巧数据库
            hero_advanced_techniques = {
                'jett': {
                    'name': '捷提',
                    'role': '决斗者',
                    'combos': [
                        "**基础连招**: Updraft(上飞) + 空中爆头 → Dash(冲刺)调整位置 → 继续输出",
                        "**进攻连招**: Cloudburst(烟雾)遮挡视野 → Dash突入点位 → 近距离击杀 → Dash撤离",
                        "**防守连招**: Operator架点 → 开枪后立即Dash换位 → 躲避还击并重新架枪",
                        "**大招连招**: Blade Storm启动 → Updraft升空 → 空中五连飞刀精准打击"
                    ],
                    'positioning': "• 利用高机动性占据非常规高点位\n• 作为Entry Fragger第一个进入点位创造空间\n• 使用烟雾瞬间阻挡关键枪线后快速突进",
                    'tips': [
                        "Dash可以在空中使用，配合Updraft创造意想不到的击杀角度",
                        "烟雾持续时间较短，主要用于瞬间遮挡而不是长期控制",
                        "大招飞刀可以右键三连发提高DPS，但会降低精度",
                        "练习Dash后的急停射击，保持高速移动中的准确度"
                    ]
                },
                'raze': {
                    'name': '雷兹',
                    'role': '决斗者',
                    'combos': [
                        "**侦察连招**: Boom Bot前探吸引火力 → 敌人暴露位置 → Blast Pack跳跃切入",
                        "**清点连招**: Paint Shells逼迫敌人离开掩体 → Blast Pack快速接近 → 近距离扫射",
                        "**大招连招**: Showstopper火箭筒准备 → Blast Pack跳跃获得高度优势 → 空中范围打击",
                        "**转点连招**: 双Blast Pack实现超远距离快速转点回防"
                    ],
                    'positioning': "• 利用爆炸包占据垂直优势的高点位\n• 机器人用于探测未知区域和吸引注意力\n• 榴弹专门用于逼迫敌人离开安全位置",
                    'tips': [
                        "爆炸包可以粘在墙上创造意想不到的移动路线和跳跃点",
                        "机器人不仅是伤害工具，更是重要的信息收集手段",
                        "火箭筒有较大爆炸半径，不必追求直接命中",
                        "熟练掌握各种爆炸包跳技巧，快速跨越地图关键区域"
                    ]
                },
                'reyna': {
                    'name': '芮娜',
                    'role': '决斗者',
                    'combos': [
                        "**基础连招**: Leer致盲掩护Peek → 快速击杀 → Devour吞噬回血维持状态",
                        "**残局连招**: 成功击杀 → Dismiss无视隐身调整站位 → 寻找下一个击杀机会",
                        "**大招连招**: Empress女皇形态启动 → 连续击杀刷新技能 → 持续收割战场",
                        "**防守连招**: Leer拖延敌人进攻节奏 → 击杀回复血量 → 维持防线稳定"
                    ],
                    'positioning': "• 极度依赖队友提供信息和支持的决斗者\n• 作为Secondary Entry跟随第一突破手进场收割\n• 利用技能特性在残局中创造1v多翻盘机会",
                    'tips': [
                        "Leer可以被敌人快速摧毁，放置时要注意角度和时机",
                        "Dismiss期间无法射击，主要用于调整位置和躲避伤害",
                        "大招期间每次击杀都会完全回复护甲，尽量保持满状态作战",
                        "没有击杀时Reyna作用有限，要保证首杀成功率"
                    ]
                },
                'phoenix': {
                    'name': '菲尼克斯',
                    'role': '决斗者',
                    'combos': [
                        "**自愈连招**: Hot Hands火球治疗自己 → Curveball闪光Peek → 精准击杀敌人",
                        "**突进连招**: Run it Back大招前压侦察 → 获取信息或击杀 → 在安全位置复活",
                        "**区域连招**: Blaze火墙分割战场 → Curveball闪光控制 → 团队协同突入",
                        "**续航连招**: 火墙治疗维持血量 → 闪光创造对枪优势 → 持续作战能力"
                    ],
                    'positioning': "• 游戏中唯一的自愈型决斗者，可以承受更多交战\n• 火墙既能治疗友军也能伤害敌人，使用要谨慎\n• 大招提供高风险高回报的侦察和突破机会",
                    'tips': [
                        "火墙可以弯曲放置，创造复杂的视线阻挡和行进路线",
                        "Curveball有左右两种闪光轨迹，根据掩体位置选择",
                        "大招期间死亡不会掉落枪械，可以大胆进行高风险行动",
                        "自奶技能也可以治疗队友，关键时刻记得帮助队友"
                    ]
                },
                'yoru': {
                    'name': '幽影',
                    'role': '决斗者',
                    'combos': [
                        "**欺骗连招**: Fakeout假脚步吸引注意力 → Gatecrash传送背后 → 出其不意偷袭",
                        "**闪光连招**: Blindside闪光弹投掷 → Gatecrash传送切入 → 背身轻松击杀",
                        "**侦察连招**: Dimensional Drift大招隐身侦察 → 精确定位所有敌人 → 取消大招收割",
                        "**复杂连招**: 假脚步+传送+闪光三重欺骗组合 → 让敌人完全失去判断"
                    ],
                    'positioning': "• 游戏中最复杂的欺骗大师，擅长心理博弈\n• 利用技能制造混乱和错误信息干扰敌人判断\n• 需要高超的游戏理解和时机把握能力",
                    'tips': [
                        "假脚步可以模仿队友或自己的脚步声，制造人数假象",
                        "传送信标可以被敌人摧毁，要选择隐蔽的放置位置",
                        "大招期间可以安全放置传送信标，创造极其意外的位置",
                        "练习多种欺骗组合，让敌人永远无法预测你的行动"
                    ]
                },
                'neon': {
                    'name': '霓虹',
                    'role': '决斗者',
                    'combos': [
                        "**速度连招**: High Gear疾跑快速Peek → Slide滑铲射击 → 立即撤离换位",
                        "**突进连招**: Relay Bolt电墙阻挡视线 → 滑铲快速进入 → 近距离优势战斗",
                        "**大招连招**: Overdrive大招启动 → 高速移动射击 → 电墙分割战场控制",
                        "**转点连招**: 疾跑能力快速转点 → 制造局部人数优势 → 出其不意进攻"
                    ],
                    'positioning': "• 全游戏移动速度最快的英雄，擅长快速转点和突袭\n• 利用速度优势创造出其不意的交战时机\n• 电墙可以阻挡视野并造成轻微伤害干扰",
                    'tips': [
                        "滑铲后立即射击有精度加成，适合快速Peek射击",
                        "电墙可以弯曲放置，适应各种复杂的地形环境",
                        "大招需要较近距离才能造成有效伤害，注意交战距离",
                        "练习高速移动中的射击准确度，保持机动性的同时保证输出"
                    ]
                },
                'iso': {
                    'name': '壹索',
                    'role': '决斗者',
                    'combos': [
                        "**单挑连招**: Double Tap启动增益 → 成功击杀刷新护盾 → 连续单挑取胜",
                        "**突进连招**: Contingency能量盾前压 → 吸收关键伤害 → 反击完成击杀",
                        "**大招连招**: Kill Contract决斗空间 → 1v1绝对优势 → 刷新护盾继续战斗",
                        "**残局连招**: 能量盾保护对枪 → 精确射击取胜 → 护盾维持生存能力"
                    ],
                    'positioning': "• 专精1v1对决的特化型决斗者\n• 利用护盾在对枪中占据血量优势\n• 大招创造绝对公平的单挑环境确保击杀",
                    'tips': [
                        "Double Tap需要击杀才能刷新护盾，保证首杀准确率至关重要",
                        "能量盾可以吸收单次任何伤害，包括狙击枪一击必杀",
                        "大招期间处于无敌状态，但结束后会回到原始位置",
                        "练习爆头线瞄准，最大化护盾带来的对枪优势"
                    ]
                },
                'sova': {
                    'name': '索瓦',
                    'role': '先锋',
                    'combos': [
                        "**信息连招**: Recon Bolt侦察箭获取敌人位置 → Shock Bolt雷箭补充伤害 → 队友跟进清理",
                        "**大招连招**: Owl Drone无人机精确定位 → Hunter's Fury大招穿墙收割 → 安全位置输出",
                        "**清点连招**: 双倍弹跳雷箭清理死角 → 侦察箭确认击杀结果 → 安全占领区域",
                        "**预设连招**: 提前设置侦察箭位置 → 敌人触发立即反应 → 雷箭反击压制"
                    ],
                    'positioning': "• 游戏中最重要的信息位英雄，团队的眼睛\n• 需要学习各种地图的复杂箭头弹跳点位\n• 与队友实时共享信息，指挥团队进攻方向",
                    'tips': [
                        "侦察箭即使被快速摧毁也能瞬间揭示敌人位置，价值巨大",
                        "雷箭可以双发连续使用，造成更大范围和更高伤害",
                        "无人机不仅可以侦察还能标记敌人，为队友提供精准信息",
                        "大招可以穿透多层墙壁，需要大量练习预判敌人移动轨迹"
                    ]
                },
                'skye': {
                    'name': '斯凯',
                    'role': '先锋',
                    'combos': [
                        "**侦察连招**: Trailblazer战狼前探侦察 → 获取敌人精确位置 → Guiding Light飞鹰闪光控制",
                        "**进攻连招**: 飞鹰闪光致盲敌人 → 战狼清空角落 → 队友安全跟进击杀",
                        "**治疗连招**: Regrowth治疗维持队友血量 → 闪光创造安全空间 → 团队持续作战",
                        "**大招连招**: Seekers追踪者释放 → 自动追踪最近敌人 → 团队集中火力消灭"
                    ],
                    'positioning': "• 全能型先锋，集信息、闪光、治疗于一身\n• 战狼可以眩晕敌人，创造完美击杀机会\n• 治疗需要引导时间，要注意自身安全位置",
                    'tips': [
                        "战狼可以被控制转向，实现更精确的区域侦察",
                        "飞鹰闪光可以曲线飞行，绕过各种障碍物致盲敌人",
                        "治疗可以同时治疗多个队友，团队作战价值极高",
                        "追踪者会优先追踪最近敌人，释放时注意位置和时机"
                    ]
                },
                'breach': {
                    'name': '布雷奇',
                    'role': '先锋',
                    'combos': [
                        "**控制连招**: Fault Line震波眩晕敌人 → Flashpoint闪光致盲 → Aftershock余震清点",
                        "**协同连招**: 全技能完美时机协同 → 为队友创造无敌进场时机 → 轻松清理点位",
                        "**大招连招**: Rolling Thunder大招全场控制 → 团队安全跟进清扫 → 完美回合胜利",
                        "**穿墙连招**: 所有技能都能穿透墙壁 → 安全位置控制战场 → 无风险创造优势"
                    ],
                    'positioning': "• 最强区域控制型先锋，擅长狭小空间作战\n• 所有技能都能穿透墙壁，安全创造优势\n• 需要与队友紧密配合技能使用时机",
                    'tips': [
                        "震波可以蓄力增加作用距离和宽度，适应不同情况",
                        "余震可以逼迫敌人离开完美掩体，创造击杀机会",
                        "闪光需要时间生效，要提前使用而不是同时使用",
                        "大招有很长的控制时间，配合队友可以轻松清空区域"
                    ]
                },
                'fade': {
                    'name': '菲德',
                    'role': '先锋',
                    'combos': [
                        "**追踪连招**: Prowler猎兽自动追踪 → Haunt鬼影全局揭示 → 团队集中火力消灭",
                        "**控制连招**: Seize束缚定身敌人 → Nightfall大招全面削弱 → 轻松完成击杀",
                        "**信息连招**: 鬼影大范围揭示 → 猎兽精确单个追踪 → 完整信息链获取",
                        "**残局连招**: 所有技能协同使用 → 1v1对枪绝对优势 → 残局大师表现"
                    ],
                    'positioning': "• 信息与控制完美结合的混合型先锋\n• 技能可以穿越墙壁和障碍物，难以防范\n• 特别擅长小范围战斗和残局处理",
                    'tips': [
                        "猎兽会自动追踪最近的血迹或鬼影标记目标",
                        "鬼影可以被敌人摧毁，但会立即暴露敌人位置",
                        "束缚不仅造成伤害还会使敌人耳聋，效果极佳",
                        "大招会削弱所有敌人视野和听力，团队作战价值巨大"
                    ]
                },
                'gekko': {
                    'name': '盖可',
                    'role': '先锋',
                    'combos': [
                        "**伙伴连招**: Wingman伙伴前探侦察/拆包 → Dizzy眩晕控制敌人 → 队友轻松击杀",
                        "**区域连招**: Mosh Pit区域封锁关键位置 → Thrash大招清空区域 → 安全占领点位",
                        "**回收连招**: 技能使用完成目标 → 安全时机回收技能 → 重复使用最大化价值",
                        "**欺骗连招**: 伙伴拆包吸引注意力 → 实际团队进攻另一侧 → 出其不意战术"
                    ],
                    'positioning': "• 独特技能回收机制的创新性先锋\n• 伙伴可以执行多种复杂任务，极其灵活\n• 需要精细管理技能使用和回收时机",
                    'tips': [
                        "所有技能都可以在安全时回收后再次使用，节省经济",
                        "伙伴既可以拆包也能植包，创造多种战术选择",
                        "眩晕会自动追踪敌人并限制视野，控制效果优秀",
                        "大招可以控制大片区域并获取关键击杀，改变战局"
                    ]
                },
                'killjoy': {
                    'name': '奇乐',
                    'role': '哨卫',
                    'combos': [
                        "**陷阱连招**: Alarmbot警报机器人 + Turret炮台交叉火力 → Nanoswarm蜂群补刀收割",
                        "**防守连招**: 预设完美陷阱阵型 → Lockdown大招区域控制 → 轻松防守点位",
                        "**信息连招**: 炮台自动侦察敌人 → 警报阻止快速突进 → 蜂群清理聚集敌人",
                        "**残局连招**: 所有装置协同作战 → 1v多防守创造奇迹 → 哨卫大师表现"
                    ],
                    'positioning': "• 最强区域防守专家，擅长固定点位防守\n• 装置有距离限制，需要精心规划防守区域\n• 大招可以完全重置战场局势，价值无限",
                    'tips': [
                        "装置在距离外会自动失效，要合理规划防守覆盖范围",
                        "蜂群可以隐藏起来，等待敌人进入后激活造成最大伤害",
                        "炮台不仅是伤害工具，更是重要的自动信息收集装置",
                        "大招可以被敌人摧毁，放置时要选择安全位置并保护"
                    ]
                },
                'cypher': {
                    'name': '零',
                    'role': '哨卫',
                    'combos': [
                        "**信息连招**: Spycam摄像头侦察敌人动向 → Trapwire绊线控制入口 → Neural Theft大招复活揭示",
                        "**防守连招**: 绊线阵完美封锁所有入口 → 摄像头实时监控 → 笼子烟雾干扰视野",
                        "**残局连招**: 摄像头定位最后敌人位置 → 笼子遮蔽视线 → 精准预瞄击杀",
                        "**反击连招**: 队友死亡立即使用大招 → 揭示所有敌人位置 → 完美反击机会"
                    ],
                    'positioning': "• 终极信息掌控者，团队防御大脑\n• 每个技能都专注于信息收集和控制\n• 需要精准预判敌人进攻路线和习惯",
                    'tips': [
                        "摄像头可以捡起重新放置，根据局势灵活调整监控点",
                        "绊线可以放在非常规位置，增加意外性和控制效果",
                        "笼子不仅遮蔽视野还能阻挡声音，干扰效果极佳",
                        "大招需要敌人尸体才能使用，要保证对战场的控制权"
                    ]
                },
                'sage': {
                    'name': '圣祈',
                    'role': '哨卫',
                    'combos': [
                        "**治疗连招**: Healing Orb治疗维持队友血量 → Barrier Orb冰墙分割战场创造优势",
                        "**防守连招**: 冰墙完美阻挡关键入口 → Slow Orb缓速拖延进攻节奏 → 治疗续航防守能力",
                        "**大招连招**: Resurrection复活关键队友 → 瞬间改变人数劣势 → 扭转战局机会",
                        "**区域连招**: 冰墙创造优势对枪位置 → 缓速限制敌人移动空间 → 团队轻松清理"
                    ],
                    'positioning': "• 游戏中唯一的治疗者，团队的生命保障\n• 冰墙可以创造性改变地形，影响战局\n• 复活能力可以完全扭转回合胜负",
                    'tips': [
                        "治疗可以对自己使用，但速度较慢，危急时使用",
                        "冰墙可以旋转放置，适应各种复杂的防守需求",
                        "缓速效果极其强大，可以有效拖延敌人进攻节奏",
                        "复活时机至关重要，要选择最关键的队友和时机"
                    ]
                },
                'chamber': {
                    'name': '钱博尔',
                    'role': '哨卫',
                    'combos': [
                        "**架点连招**: Trademark陷阱侦察侧翼 → Headhunter手枪精准架点 → 远距离击杀敌人",
                        "**转点连招**: Rendezvous传送锚点快速转位 → 出其不意角度架枪 → 连续收割敌人",
                        "**大招连招**: Tour De Force狙击枪架点 → 传送调整完美位置 → 统治关键区域",
                        "**经济连招**: 免费重型手枪节省经济 → 陷阱保护侧翼 → 团队经济优势"
                    ],
                    'positioning': "• 独特的狙击型哨卫，擅长远距离架点\n• 传送能力提供极强的位置灵活性\n• 免费手枪为团队经济做出巨大贡献",
                    'tips': [
                        "传送锚点有使用距离限制，要合理规划放置位置",
                        "重型手枪精度极高，可以替代步枪在经济局使用",
                        "陷阱不仅提供信息还能缓慢敌人，控制效果优秀",
                        "大招狙击枪可以穿透墙壁，练习预判穿射技巧"
                    ]
                },
                'deadlock': {
                    'name': '死锁',
                    'role': '哨卫',
                    'combos': [
                        "**控制连招**: Sonic Sensor声波传感器探测 → GravNet重力网困住敌人 → 轻松击杀目标",
                        "**封锁连招**: Barrier Mesh屏障网封锁区域 → 声波传感器监控 → 完美区域控制",
                        "**大招连招**: Annihilation大招锁定目标 → 强制拉回控制 → 团队集火消灭",
                        "**信息连招**: 声波传感器网络覆盖 → 实时掌握敌人动向 → 预判防守策略"
                    ],
                    'positioning': "• 声音控制专家，擅长区域封锁和信息收集\n• 利用声音传感器构建防御网络\n• 大招提供强力的单体控制能力",
                    'tips': [
                        "声波传感器对声音敏感，可以探测敌人脚步声",
                        "重力网可以困住多个敌人，创造完美击杀机会",
                        "屏障网可以封锁整个通道，拖延敌人进攻",
                        "大招需要精确瞄准，但命中后几乎确保击杀"
                    ]
                },
                'omen': {
                    'name': '欧门',
                    'role': '控场者',
                    'combos': [
                        "**烟雾连招**: Paranoia致盲穿过烟雾 → 敌人失去视野 → 团队安全进入点位",
                        "**传送连招**: Shrouded Step短传调整位置 → 出其不意角度 → 背身轻松击杀",
                        "**大招连招**: From the Shadows全球传送 → 敌人后方偷袭 → 制造混乱分散注意力",
                        "**区域连招**: 烟雾封锁关键视野 → 致盲控制通道 → 传送灵活支援"
                    ],
                    'positioning': "• 灵活的全球控场者，擅长心理博弈\n• 烟雾可以任意位置放置，极其灵活\n• 传送能力提供无限的战术可能性",
                    'tips': [
                        "烟雾有延迟生效时间，要提前放置而不是临时使用",
                        "短传有施法时间，确保安全时使用避免被打断",
                        "全球传送可以侦察敌人位置，即使取消也有价值",
                        "致盲可以穿透墙壁，练习各种角度的使用技巧"
                    ]
                },
                'brimstone': {
                    'name': '勃朗特',
                    'role': '控场者',
                    'combos': [
                        "**烟雾连招**: Sky Smoke烟雾弹完美封锁 → Stim Beacon激励信号增强 → 团队强势推进",
                        "**区域连招**: Incendiary燃烧弹封锁区域 → 烟雾弹控制视野 → 信号弹增强输出",
                        "**大招连招**: Orbital Strike轨道打击精准定位 → 逼迫敌人离开掩体 → 团队轻松清理",
                        "**推进连招**: 三烟封锁所有关键点位 → 信号弹增强枪法 → 完美战术推进"
                    ],
                    'positioning': "• 经典的控场大师，擅长结构化战术推进\n• 烟雾持续时间长，适合长期区域控制\n• 信号弹为团队提供重要战斗加成",
                    'tips': [
                        "烟雾弹可以同时放置三个，实现全面视野控制",
                        "燃烧弹弹道较慢，需要练习预判投掷位置",
                        "信号弹不仅提高射速还能减少换弹时间，价值巨大",
                        "轨道打击有较长的准备时间，要预判敌人位置使用"
                    ]
                },
                'viper': {
                    'name': '蝰蛇',
                    'role': '控场者',
                    'combos': [
                        "**毒墙连招**: Poison Cloud毒云 + Toxic Screen毒墙双重封锁 → 完美区域控制",
                        "**消耗连招**: 毒云持续消耗敌人血量 → Snakebite蛇咬补刀 → 轻松击杀残血",
                        "**大招连招**: Viper's Pit蝰蛇领域启动 → 领域内绝对优势 → 1v多防守能力",
                        "**燃料连招**: 精细管理燃料消耗 → 关键时刻开启技能 → 最大化控制效果"
                    ],
                    'positioning': "• 毒性控场专家，擅长持续区域压制\n• 技能需要燃料管理，使用时机至关重要\n• 大招在特定点位可以提供无敌防守能力",
                    'tips': [
                        "毒云可以捡起重新放置，根据战况灵活调整",
                        "蛇咬不仅造成伤害还能使敌人易伤，连招价值高",
                        "大招范围内视野极差，敌人很难与你有效对枪",
                        "燃料管理是玩好Viper的关键，不要随意浪费"
                    ]
                },
                'astra': {
                    'name': '星礈',
                    'role': '控场者',
                    'combos': [
                        "**星体连招**: 星体形式切换灵活应对 → 烟雾视野控制 → 重力井区域封锁",
                        "**控制连招**: Nova Pulse脉冲眩晕敌人 → Gravity Well重力井控制 → 团队轻松清理",
                        "**大招连招**: Cosmic Divide宇宙分割屏障 → 完全分割战场 → 制造局部多打少",
                        "**全局连招**: 全图范围星体放置 → 实时应对各种情况 → 终极控场大师"
                    ],
                    'positioning': "• 全球控场者，需要极强的大局观和预判\n• 星体可以全图放置，提供无限可能性\n• 技能需要提前规划，反应型玩法效果较差",
                    'tips': [
                        "星体放置后可以切换不同形式，适应战况变化",
                        "重力井可以把敌人拉向中心，创造完美击杀机会",
                        "宇宙分割可以完全阻挡子弹和声音，战术价值巨大",
                        "需要极强的大局观和预判能力，适合指挥型玩家"
                    ]
                },
                'harbor': {
                    'name': '海神',
                    'role': '控场者',
                    'combos': [
                        "**水域连招**: High Tide高潮水墙推进 → Cove庇护所创造安全空间 → 团队稳步推进",
                        "**控制连招**: Cascade瀑布封锁区域 → 水墙分割战场 → 庇护所保护队友",
                        "**大招连招**: Reckoning审判大招启动 → 敌人被眩晕标记 → 团队集中收割",
                        "**推进连招**: 水墙创造推进通道 → 瀑布控制侧翼 → 庇护所提供掩护"
                    ],
                    'positioning': "• 水域控场专家，擅长动态战场控制\n• 技能可以重新定向，适应复杂战况\n• 庇护所为团队提供宝贵的临时安全空间",
                    'tips': [
                        "水墙可以弯曲控制，创造复杂的推进路线",
                        "瀑布可以穿透墙壁继续前进，难以防范",
                        "庇护所可以阻挡所有攻击，包括大招，保护价值巨大",
                        "大招需要敌人在地面上才能眩晕，注意释放时机"
                    ]
                },
                'clove': {
                    'name': '克洛夫',
                    'role': '控场者',
                    'combos': [
                        "**视野连招**: Ruse烟幕弹视野控制 → Meddle干扰削弱敌人 → 团队对枪优势",
                        "**复活连招**: 死亡后使用Not Dead Yet复活 → 调整位置再次参战 → 扭转战局",
                        "**大招连招**: Bitter Rose终极领域 → 范围内持续削弱敌人 → 团队轻松取胜",
                        "**干扰连招**: 烟幕控制关键视野 → 干扰削弱敌人武器 → 创造绝对优势"
                    ],
                    'positioning': "• 独特的死后复活机制，容错率极高\n• 烟幕提供灵活视野控制，干扰削弱敌人\n• 大招创造持续削弱领域，团队作战价值大",
                    'tips': [
                        "死亡后有时间限制复活，要快速决定是否使用",
                        "烟幕可以快速放置，适合反应型控场需求",
                        "干扰效果可以使敌人武器精度大幅下降",
                        "大招领域内敌人持续受到削弱，团队配合效果极佳"
                    ]
                },
                'waylay': {
                    'name': '韦莱',
                    'role': '哨卫',
                    'combos': [
                        "**陷阱连招**: Tripwire绊索陷阱预设 → 敌人触发被困 → 精准预瞄轻松击杀",
                        "**信息连招**: 绊索网络覆盖侧翼 → 实时掌握敌人动向 → 预判防守策略调整",
                        "**区域连招**: 多重绊索封锁区域 → 敌人难以突破 → 完美区域控制防守",
                        "**残局连招**: 最后一个绊索触发 → 精确定位最后敌人 → 1v1对枪优势"
                    ],
                    'positioning': "• 陷阱专家，擅长预设防御和区域控制\n• 绊索提供宝贵的信息收集和敌人控制\n• 需要精准预判敌人进攻路线和习惯",
                    'tips': [
                        "绊索可以放在各种高度位置，增加意外性",
                        "陷阱触发后敌人会被短暂控制，创造击杀机会",
                        "构建绊索网络覆盖所有可能进攻路线",
                        "绊索可以被敌人摧毁，要选择隐蔽放置位置"
                    ]
                }
            }





            # 创建统一尺寸的英雄图片字典
            hero_images_resized = {}
            for hero_path in whole_heroes_image:
                hero_name = os.path.splitext(os.path.basename(hero_path))[0]
                resized_image = resize_hero_image(hero_path)
                if resized_image:
                    hero_images_resized[hero_name] = resized_image

            # 显示英雄网格
            st.markdown("### 🦸 英雄进阶技巧库")

            # 按角色分类显示英雄
            roles_order = ['决斗者', '先锋', '控场者', '哨卫']

            for role in roles_order:
                st.markdown(f"#### 🎯 {role}")

                # 获取该角色的所有英雄
                role_heroes = [hero for hero, info in hero_advanced_techniques.items() if info.get('role') == role]

                # 每行显示4个英雄
                heroes_per_row = 4
                hero_rows = [role_heroes[i:i + heroes_per_row] for i in range(0, len(role_heroes), heroes_per_row)]

                for row in hero_rows:
                    cols = st.columns(heroes_per_row)
                    for idx, hero_name in enumerate(row):
                        with cols[idx]:
                            # 显示统一尺寸的图片
                            if hero_name in hero_images_resized:
                                st.image(hero_images_resized[hero_name], use_container_width=True,
                                         caption=hero_advanced_techniques[hero_name]['name'])
                            else:
                                # 如果处理后的图片不存在，显示原始图片但限制尺寸
                                original_path = f"whole heroes/{hero_name}.png"
                                if os.path.exists(original_path):
                                    st.image(original_path, width=300,
                                             caption=hero_advanced_techniques[hero_name]['name'])

                            # 显示英雄信息和详情按钮
                            hero_info = hero_advanced_techniques[hero_name]

                            with st.expander(f"🎮 {hero_info['name']}技巧", expanded=False):
                                if hero_info['combos']:
                                    st.markdown("**核心连招:**")
                                    for combo in hero_info['combos'][:2]:  # 只显示前2个连招
                                        st.write(f"• {combo}")

                                if hero_info['tips']:
                                    st.markdown("**关键技巧:**")
                                    for tip in hero_info['tips'][:2]:  # 只显示前2个技巧
                                        st.write(f"• {tip}")
                                        st.markdown(hero_name)
                                        # st.markdown(hero_advanced_techniques.keys())

                            # 查看详细技巧按钮
                            if st.button(f"点击然后往下翻，详细学习吧！", key=f"detail_{hero_name}", use_container_width=True):
                                st.session_state.heroes =hero_name

            # 如果选择了具体英雄，显示详细页面
            if st.session_state.heroes in hero_advanced_techniques.keys():
                st.markdown('## 信息读取成功')
                hero_name = st.session_state.heroes
                hero_info = hero_advanced_techniques[hero_name]

                st.markdown(f'<div class="section-header">{hero_info["name"]} 大师级指南</div>', unsafe_allow_html=True)

                if st.button('🔙 返回英雄列表', key='back_hero_list'):
                    st.session_state.current = 'home'

                # 英雄详情布局
                col1, col2 = st.columns([1, 2])

                with col1:
                    # 显示统一尺寸的英雄图片
                    if hero_name in hero_images_resized:
                        st.image(hero_images_resized[hero_name], use_container_width=True)
                    else:
                        st.image(f"whole heroes/{hero_name}.png", use_container_width=True)

                    st.markdown(f"""
                    <div class="card">
                    <h3>🎯 英雄档案</h3>
                    <p><strong>角色:</strong> {hero_info['role']}</p>
                    <p><strong>难度:</strong> ⭐⭐⭐⭐</p>
                    <p><strong>定位:</strong> 主力输出/信息控制</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown("### 🎬 技能连招详解")

                    if hero_info['combos']:
                        for i, combo in enumerate(hero_info['combos']):
                            with st.expander(f"连招 {i + 1}: {combo.split(':** ')[0] if ':**' in combo else combo}",
                                             expanded=i == 0):
                                if '→' in combo:
                                    steps = combo.split('→')
                                    for j, step in enumerate(steps):
                                        st.markdown(f"{j + 1}. {step.strip()}")
                                else:
                                    st.write(combo)
                    else:
                        st.info("该英雄的连招信息正在更新中...")

                    st.markdown("### 🧠 高级战术思路")

                    tab1, tab2, tab3 = st.tabs(["进攻策略", "防守策略", "残局处理"])

                    with tab1:
                        st.markdown("""
                        **进攻核心思路:**
                        - 利用技能创造进入点位的安全通道
                        - 与队友同步技能使用时机
                        - 控制关键区域，分割敌人阵型
                        - 快速获取首杀建立人数优势
                        """)

                    with tab2:
                        st.markdown("""
                        **防守核心思路:**
                        - 利用技能拖延敌人进攻节奏
                        - 收集信息，预判敌人动向
                        - 创造交叉火力，配合队友
                        - 灵活转点，避免被包围
                        """)

                    with tab3:
                        st.markdown("""
                        **残局处理要点:**
                        - 保持冷静，分析局势
                        - 利用技能获取信息优势
                        - 制造1v1机会，避免多打少
                        - 控制时间，合理选择进攻或防守
                        """)

                # 英雄特定技巧
                if hero_info['tips']:
                    st.markdown("### 💡 英雄专属技巧")
                    tips_cols = st.columns(2)
                    for i, tip in enumerate(hero_info['tips']):
                        with tips_cols[i % 2]:
                            st.markdown(f"""
                            <div class="card">
                            <p>• {tip}</p>
                            </div>
                            """, unsafe_allow_html=True)

                # 练习建议
                st.markdown("### 🏆 职业级练习方案")
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("""
                    <div class="card">
                    <h3>🎯 每日练习</h3>
                    <p>• 15分钟训练场热身</p>
                    <p>• 10分钟死亡竞赛</p>
                    <p>• 特定连招重复练习</p>
                    <p>• 地图点位熟悉</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown("""
                    <div class="card">
                    <h3>📚 学习资源</h3>
                    <p>• 观看职业选手POV</p>
                    <p>• 学习道具投掷点位</p>
                    <p>• 分析自己比赛录像</p>
                    <p>• 加入社区讨论</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.markdown("""
                    <div class="card">
                    <h3>🚀 进阶目标</h3>
                    <p>• 掌握所有地图点位</p>
                    <p>• 熟练多种战术套路</p>
                    <p>• 提高游戏意识</p>
                    <p>• 加强团队配合</p>
                    </div>
                    """, unsafe_allow_html=True)



        elif select_tab == '🏆 第六章：职业比赛学习':

            st.session_state.radio_index = 8

            st.markdown('<div class="section-header">向职业选手学习</div>', unsafe_allow_html=True)

            st.markdown("""

                    <div class="card">

                    <h3>🎯 学习价值</h3>

                    <p>职业比赛是学习高级技巧和战术的最佳途径，能够快速提升游戏理解</p>

                    </div>

                    """, unsafe_allow_html=True)

            # 视频分析部分

            st.markdown("### 📹 比赛视频分析")

            if os.path.exists("extravideo/edglotus.mp4"):

                st.video("extravideo/edglotus.mp4")

                st.caption("EDG vs LOTUS 职业比赛精彩片段")

            else:

                st.warning("视频文件未找到，请检查文件路径")

            # 逐帧分析

            st.markdown("### 🔍 逐帧技术分析")

            analysis_points = [

                {

                    "time": "15秒",

                    "aspect": "准心摆放",

                    "analysis": "选手准心始终保持在头线位置，这是职业选手的基本功",

                    "lesson": "走路时不要瞄地面，保持头线预瞄"

                },

                {

                    "time": "18秒",

                    "aspect": "团队配合",

                    "analysis": "铁壁的E技能有效阻断敌人直架，创造1v1机会",

                    "lesson": "善用技能为队友创造对枪优势"

                },

                {

                    "time": "20秒",

                    "aspect": "枪线拆分",

                    "analysis": "烟雾弹放置在旋转门，成功将1v4拆分成多个1v1",

                    "lesson": "利用道具拆分敌人枪线，避免多打少"

                },

                {

                    "time": "25秒",

                    "aspect": "残局处理",

                    "analysis": "CHICHOO选手冷静处理残局，逐个击破",

                    "lesson": "保持冷静，寻找最佳击杀顺序"

                }

            ]

            for point in analysis_points:
                with st.expander(f"⏱️ {point['time']} - {point['aspect']}"):
                    st.success(f"**技术要点：** {point['analysis']}")

                    st.info(f"**学习心得：** {point['lesson']}")

            # 学习建议

            st.markdown("### 💡 学习建议")

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("""

                        <div class="card">

                        <h3>🎥 观看建议</h3>

                        <p>• 选择高水平比赛</p>

                        <p>• 关注选手第一视角</p>

                        <p>• 学习道具使用时机</p>

                        <p>• 观察团队配合方式</p>

                        </div>

                        """, unsafe_allow_html=True)

            with col2:

                st.markdown("""

                        <div class="card">

                        <h3>📚 学习方法</h3>

                        <p>• 观看POV分析视频</p>

                        <p>• 记录关键技巧</p>

                        <p>• 在游戏中实践</p>

                        <p>• 反复观看学习</p>

                        </div>

                        """, unsafe_allow_html=True)






        elif select_tab == '🚀 第七章：游戏进阶技巧':

            st.session_state.radio_index = 9

            st.markdown('<div class="section-header">游戏进阶技巧</div>', unsafe_allow_html=True)

            tabs = st.tabs(["🎯 枪法提升", "🧠 游戏意识", "🤝 团队配合", "⚡ 实战技巧"])

            with tabs[0]:

                st.markdown("### 🎯 枪法训练指南")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("""

                            <div class="card">

                            <h3>🔫 基础瞄准</h3>

                            <p>• 保持头线预瞄</p>

                            <p>• 练习急停射击</p>

                            <p>• 掌握不同枪械后坐力</p>

                            <p>• 训练反应速度</p>

                            </div>

                            """, unsafe_allow_html=True)

                    st.markdown("""

                            <div class="card">

                            <h3>🎯 瞄准训练</h3>

                            <p>• 死亡竞赛练习</p>

                            <p>• 训练场热身</p>

                            <p>• 自定义练枪</p>

                            <p>• 坚持每日练习</p>

                            </div>

                            """, unsafe_allow_html=True)

                with col2:
                    st.markdown("""

                            <div class="card">

                            <h3>📊 灵敏度设置</h3>

                            <p>• 找到适合自己的灵敏度</p>

                            <p>• 保持一致性</p>

                            <p>• 避免频繁调整</p>

                            <p>• 考虑鼠标DPI</p>

                            </div>

                            """, unsafe_allow_html=True)

                    st.markdown("""

                            <div class="card">

                            <h3>💪 肌肉记忆</h3>

                            <p>• 固定练习时间</p>

                            <p>• 重复基础动作</p>

                            <p>• 保持姿势一致</p>

                            <p>• 循序渐进提升</p>

                            </div>

                            """, unsafe_allow_html=True)

            with tabs[1]:

                st.markdown("### 🧠 游戏意识培养")

                awareness_points = {

                    "地图控制": "掌握关键点位控制权，预测敌人动向",

                    "声音判断": "通过声音判断敌人位置和行动",

                    "经济管理": "合理规划每回合经济，与队友协调",

                    "时机把握": "抓住最佳进攻和防守时机",

                    "信息收集": "通过小地图和队友报点收集信息"

                }

                for topic, description in awareness_points.items():
                    with st.expander(f"📖 {topic}"):
                        st.write(description)

                        st.progress(70)

            with tabs[2]:

                st.markdown("### 🤝 团队配合要点")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("""

                            <div class="card">

                            <h3>🎙️ 沟通技巧</h3>

                            <p>• 清晰简洁的报点</p>

                            <p>• 及时的信息分享</p>

                            <p>• 积极的团队氛围</p>

                            <p>• 战术决策讨论</p>

                            </div>

                            """, unsafe_allow_html=True)

                with col2:
                    st.markdown("""

                            <div class="card">

                            <h3>🔄 配合流程</h3>

                            <p>• 进攻同步性</p>

                            <p>• 道具协同使用</p>

                            <p>• 补枪及时性</p>

                            <p>• 防守交叉火力</p>

                            </div>

                            """, unsafe_allow_html=True)

            with tabs[3]:

                st.markdown("### ⚡ 实战技巧应用")

                techniques = [

                    "假拆骗局 - 假装拆包引诱敌人",

                    "静步绕后 - 利用静音脚步偷袭",

                    "道具压制 - 用技能控制区域",

                    "心理博弈 - 预测对手行动",

                    "残局处理 - 冷静应对少打多"

                ]

                for tech in techniques:
                    st.markdown(f"• **{tech}**")



        elif select_tab == '📊 附录：职业选手数据':

            st.session_state.radio_index = 10

            st.markdown('<div class="section-header">职业选手数据分析</div>', unsafe_allow_html=True)



            # 读取数据

            df = pd.read_excel('prodata/data.xlsx', sheet_name='Sheet1', index_col=False)

            # 数据概览

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric("选手数量", len(df))

            with col2:
                cleaned_kast = clean_kast_data(df)
                if cleaned_kast:
                    avg_kast = sum(cleaned_kast) / len(cleaned_kast)
                    st.metric("平均KAST", f"{avg_kast:.2f}%")
                #
                # st.metric("平均KAST", f"{df['KAST'].mean():.2f}")

            with col3:

                st.metric("平均ACS", f"{df['ACS'].mean():.2f}")

            with col4:

                st.metric("最高KD", f"{df['KD'].max():.2f}")

            # 数据表格

            st.markdown("### 📈 选手数据详情")

            st.dataframe(df, height=600, use_container_width=True)

            # 数据分析

            st.markdown("### 📊 数据洞察")

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("#### 🏆 顶级选手")

                top_players = df.nlargest(5, 'ACS')[['选手', 'ACS', '队伍']]

                st.dataframe(top_players, use_container_width=True,hide_index=True)

            with col2:

                st.markdown("#### 🎯 关键数据")

                st.write(f"**最高ACS:** {df['ACS'].max()} ({df.loc[df['ACS'].idxmax(), '选手']})")

                st.write(f"**最高KAST:** {df['KAST'].max()}% ({df.loc[df['KAST'].idxmax(), '选手']})")

                st.write(f"**最佳爆头率:** {df['Headshot'].max()}% ({df.loc[df['Headshot'].idxmax(), '选手']})")


            # except Exception as e:
            #
            #     st.error(f"数据加载失败: {e}")
            #
            #     st.info("请确保数据文件路径正确，且格式符合要求")




    elif st.session_state.current == 'classic':
        guns_info('classic','''标配手枪

                        售价：免费（初始枪械）
                        
                        特性：随身武器-半自动、低伤害
                        
                        
                        射速：6.75发/每秒	跑速：5.73公尺/每秒
                        装备速度：0.75秒	首发弹道偏移：0.4偏度（腰射/开镜）
                        填弹速度：1.75秒	弹匣：12发
                        伤害程度
                        
                        【无甲】0-30公尺：头部78、身体26、腿部22
                        
                        【无甲】30-50公尺：头部66、身体22、腿部18
                        
                        【小甲】0-30公尺：头部61、身体9、腿部7
                        
                        【小甲】30-50公尺：头部49、身体7、腿部5
                        
                        【大甲】0-30公尺：头部44、身体8、腿部7
                        
                        【大甲】30-50公尺：头部32、身体7、腿部5''')

    elif st.session_state.current == 'shorty':
        guns_info('shorty','''短炮

                        售价：150
                        
                        特性：随身武器-半自动、低伤害
                        
                        
                        射速：3.33发/每秒	跑速：5.4公尺/每秒
                        装备速度：0.75秒	首发弹道偏移：4偏度（腰射/开镜）
                        填弹速度：1.75秒	弹匣：2发
                        伤害程度
                        
                        【无甲】0-7公尺：头部24、身体12、腿部10
                        
                        【无甲】7-15公尺：头部16、身体8、腿部6
                        
                        【无甲】15-50公尺：头部6、身体3、腿部2''')

    elif st.session_state.current == 'frenzy':
        guns_info('frenzy','''狂怒

售价：450

特性：随身武器-全自动、低伤害


射速：10发/每秒	跑速：5.73公尺/每秒
装备速度：1秒	首发弹道偏移：0.45偏度（腰射/开镜）
填弹速度：1.5秒	弹匣：13发
伤害程度

【无甲】0-20公尺：头部78、身体26、腿部22

【无甲】20-50公尺：头部63、身体21、腿部17

【小甲】0-20公尺：头部61、身体9、腿部7

【小甲】20-50公尺：头部46、身体6、腿部5

【大甲】0-20公尺：头部44、身体8、腿部7

【大甲】20-50公尺：头部29、身体6、腿部5''')

    elif st.session_state.current == 'ghost':
        guns_info('ghost','''鬼魅

售价：500

特性：随身武器-全自动、中伤害


射速：6.75发/每秒	跑速：5.73公尺/每秒
装备速度：0.75秒	首发弹道偏移：0.3偏度（腰射/开镜）
填弹速度：1.5秒	弹匣：15发
伤害程度

【无甲】0-30公尺：头部105、身体30、腿部25

【无甲】30-50公尺：头部87、身体25、腿部21

【小甲】0-30公尺：头部88、身体13、腿部8

【小甲】30-50公尺：头部70、身体8、腿部6

【大甲】0-30公尺：头部71、身体9、腿部8

【大甲】30-50公尺：头部53、身体8、腿部6''')

    elif st.session_state.current == 'sheriff':
        guns_info('sheriff','''正义

售价：800

特性：随身武器-全自动、中伤害


射速：4发/每秒	跑速：5.4公尺/每秒
装备速度：1秒	首发弹道偏移：0.25偏度（腰射/开镜）
填弹速度：2.25秒	弹匣：6发
伤害程度

【无甲】0-30公尺：头部159、身体55、腿部46

【无甲】30-50公尺：头部145、身体50、腿部42

【小甲】0-30公尺：头部142、身体38、腿部29

【小甲】30-50公尺：头部128、身体33、腿部25

【大甲】0-30公尺：头部125、身体21、腿部15

【大甲】30-50公尺：头部111、身体16、腿部13''')

    elif st.session_state.current == 'stinger':
        guns_info('stinger','''蜂刺

售价：1100

特性：冲锋枪-全自动、低伤害


射速：16发/每秒	跑速：5.73公尺/每秒
装备速度：0.75秒	首发弹道偏移：0.65/0.35偏度（腰射/开镜）
填弹速度：2.25秒	弹匣：20发
伤害程度

【无甲】0-20公尺：头部67、身体27、腿部22

【无甲】20-50公尺：头部62、身体25、腿部21

【小甲】0-20公尺：头部50、身体10、腿部7

【小甲】20-50公尺：头部45、身体8、腿部6

【大甲】0-20公尺：头部33、身体8、腿部7

【大甲】20-50公尺：头部28、身体8、腿部6''')

    elif st.session_state.current == 'spectre':
        guns_info('spectre','''骇灵

售价：1600

特性：冲锋枪-全自动、中伤害


射速：13.33发/每秒	跑速：5.73公尺/每秒
装备速度：0.75秒	首发弹道偏移：0.4/0.25偏度（腰射/开镜）
填弹速度：2.25秒	弹匣：30    发
伤害程度

【无甲】0-15公尺：头部78、身体26、腿部22

【无甲】15-30公尺：头部66、身体22、腿部18

【无甲】30-50公尺：头部60、身体20、腿部17

【小甲】0-15公尺：头部61、身体9、腿部7

【小甲】15-30公尺：头部49、身体7、腿部5

【小甲】30-50公尺：头部43、身体6、腿部5

【大甲】0-15公尺：头部44、身体8、腿部7

【大甲】15-30公尺：头部32、身体7、腿部5

【大甲】30-50公尺：头部26、身体6、腿部5''')

    elif st.session_state.current == 'bucky':
        guns_info('bucky','''雄鹿

售价：850

特性：霰弹枪-半自动、低伤害


射速：1.1发/每秒	跑速：5.06公尺/每秒
装备速度：1秒	首发弹道偏移：2.6偏度（腰射/开镜）
填弹速度：2.5秒	弹匣：5发
伤害程度

0-8公尺：头部40、身体20、腿部18

8-12公尺：头部20、身体13、腿部9

15-50公尺：头部17、身体11、腿部7''')

    elif st.session_state.current == 'judge':
        guns_info('judge','''判官

售价：1850

特性：霰弹枪-全自动、低伤害


射速：3.5发/每秒	跑速：5.06公尺/每秒
装备速度：1秒	首发弹道偏移：2.25偏度（腰射/开镜）
填弹速度：2.2秒	弹匣：7发
伤害程度

0-10公尺：头部34、身体17、腿部14

10-15公尺：头部20、身体10、腿部8

15-50公尺：头部14、身体7、腿部5''')

    elif st.session_state.current == 'bulldog':
        guns_info('bulldog','''燎犬

售价：2050

特性：步枪-全自动、中伤害


射速：10发/每秒	跑速：5.4公尺/每秒
装备速度：1秒	首发弹道偏移：0.3偏度（腰射/开镜）
填弹速度：2.5秒	弹匣：24发
伤害程度

【无甲】0-50公尺：头部115、身体35、腿部29

【小甲】0-50公尺：头部98、身体18、腿部12

【大甲】0-50公尺：头部81、身体11、腿部9''')

    elif st.session_state.current == 'guardian':
        guns_info('guardian','''戍卫

售价：2250

特性：步枪-半自动、高伤害


射速：5.25发/每秒	跑速：5.4公尺/每秒
装备速度：1秒	首发弹道偏移：0.1/0偏度（腰射/开镜）
填弹速度：2.5秒	弹匣：12发
伤害程度

【无甲】0-50公尺：头部195、身体65、腿部48

【小甲】0-50公尺：头部178、身体48、腿部31

【大甲】0-50公尺：头部161、身体31、腿部15''')

    elif st.session_state.current == 'phantom':
        guns_info('phantom','''幻影

售价：2900

特性：步枪-全自动、中伤害


射速：11发/每秒	跑速：5.4公尺/每秒
装备速度：1秒	首发弹道偏移：0.2/0.11偏度（腰射/开镜）
填弹速度：2.5秒	弹匣：30发
伤害程度

【无甲】0-15公尺：头部156、身体39、腿部33

【无甲】15-30公尺：头部140、身体35、腿部29

【无甲】30-50公尺：头部124、身体31、腿部26

【小甲】0-15公尺：头部139、身体22、腿部16

【小甲】15-30公尺：头部123、身体18、腿部12

【小甲】30-50公尺：头部107、身体14、腿部9

【大甲】0-15公尺：头部122、身体12、腿部10

【大甲】15-30公尺：头部106、身体11、腿部9

【大甲】30-50公尺：头部90、身体10、腿部8''')

    elif st.session_state.current == 'vandal':
        guns_info('vandal','''狂徒

售价：2900

特性：步枪-全自动、中伤害


射速：9.75发/每秒	跑速：5.4公尺/每秒
装备速度：1秒	首发弹道偏移：0.25/0.157偏度（腰射/开镜）
填弹速度：2.5秒	弹匣：25发
伤害程度

【无甲】0-50公尺：头部160、身体40、腿部34

【小甲】0-50公尺：头部143、身体23、腿部27

【大甲】0-50公尺：头部126、身体13、腿部11''')

    elif st.session_state.current == 'marshal':
        guns_info('marshal','''飞将

售价：950

特性：狙击步枪-半自动、中伤害


射速：1.5发/每秒	跑速：5.4公尺/每秒
装备速度：1.25秒	首发弹道偏移：1/0偏度（腰射/开镜）
填弹速度：2.5秒	弹匣：5发
伤害程度

【无甲】0-50公尺：头部202、身体101、腿部85

【小甲】0-50公尺：头部185、身体84、腿部68

【大甲】0-50公尺：头部168、身体67、腿部51''')

    elif st.session_state.current == 'outlaw':
        guns_info('outlaw','''在《无畏契约》中，**莽侠（Outlaw）**的价格为 2400。以下是一些相关信息：
弹匣容量: 2/10
装填时间: 1.25秒
射速: 2.75
爆头伤害: 238
躯干伤害: 140
腿部伤害: 119
这把武器具有很高的穿透力，适合穿墙击杀。''')

    elif st.session_state.current == 'operator':
        guns_info('operator','''冥驹

售价：4700

特性：狙击步枪-半自动、高伤害


射速：0.6发/每秒	跑速：5.13公尺/每秒
装备速度：1.5秒	首发弹道偏移：5/0偏度（腰射/开镜）
填弹速度：3.7秒	弹匣：5发
伤害程度

【无甲】0-50公尺：头部255、身体150、腿部120

【小甲】0-50公尺：头部238、身体133、腿部103

【大甲】0-50公尺：头部221、身体116、腿部86''')

    elif st.session_state.current == 'ares':
        guns_info('ares','''战神

售价：1600

特性：机关枪-全自动、高伤害


射速：13发/每秒	跑速：5.13公尺/每秒
装备速度：1.25秒	首发弹道偏移：1/0.9偏度（腰射/开镜）
填弹速度：3.25秒	弹匣：50发
伤害程度

【无甲】0-30公尺：头部72、身体30、腿部25

【无甲】30-50公尺：头部67、身体28、腿部23

【小甲】0-30公尺：头部55、身体13、腿部8

【小甲】30-50公尺：头部50、身体11、腿部7

【大甲】0-30公尺：头部38、身体9、腿部8

【大甲】30-50公尺：头部33、身体9、腿部7''')

    elif st.session_state.current == 'odin':
        guns_info('odin','''奥丁

售价：3200

特性：机关枪-全自动、高伤害


射速：12发/每秒	跑速：5.13公尺/每秒
装备速度：1.25秒	首发弹道偏移：0.8/0.79偏度（腰射/开镜）
填弹速度：5秒	弹匣：100发
伤害程度

【无甲】0-30公尺：头部95、身体38、腿部32

【无甲】30-50公尺：头部77、身体31、腿部26

【小甲】0-30公尺：头部78、身体21、腿部15

【小甲】30-50公尺：头部60、身体14、腿部9

【大甲】0-30公尺：头部61、身体12、腿部10

【大甲】30-50公尺：头部43、身体10、腿部8''')

    elif st.session_state.current == 'jett':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\jett.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")


    elif st.session_state.current == 'neo':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\neon.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'raze':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\raze.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'waylay':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\waylay.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'astra':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\astra.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'breach':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\breach.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'brimstone':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\brimstone.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'chamber':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\chamber.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'clove':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\clove.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'cypher':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\cypher.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'deadlock':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\deadlock.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'fade':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\fade.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'gekko':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\gekko.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'harbor':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\harbor.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'iso':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\iso.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'killjoy':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\killjoy.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'KO':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\KO.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'omen':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\omen.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'phoenix':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\phoenix.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'reyna':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\reyna.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'sage':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\sage.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'skyer':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\skyer.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'sova':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\sova.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'tejo':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\tejo.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'viper':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\viper.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'vyse':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\vyse.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'waylay':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\waylay.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'yoru':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\yoru.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")


    elif st.session_state.current in ['abyss', 'ascent', 'bind', 'breeze', 'fracture',

                                      'haven', 'icebox', 'lotus', 'pearl', 'split', 'sunset']:

        if st.button('🔙 返回地图列表', key='back_map'):
            st.session_state.current = 'home'

        map_name = st.session_state.current

        st.markdown(f'<div class="section-header">{map_name.upper()} 地图详解</div>', unsafe_allow_html=True)

        # 显示平面图

        plain_map_path = f"map/plain_map/plain_{map_name}.png"

        if os.path.exists(plain_map_path):

            st.image(plain_map_path, use_container_width=True, caption=f"{map_name} 平面布局")

        else:

            st.warning("平面图暂未收录")

        # 地图特点介绍

        st.markdown("### 🎯 地图特点")

        col1, col2 = st.columns(2)

        with col1:
            # 根据不同地图提供具体的关键点位信息
            map_key_points = {
                'ascent': """
                <div class="card">
                <h3>📍 关键点位 - 天漠之峡</h3>
                <p>• <strong>A点进攻路线</strong> - A主道控制中路窗口，A小道快速突进</p>
                <p>• <strong>B点防守位置</strong> - B大厅双架位，B链接回防路线</p>
                <p>• <strong>中路控制权</strong> - 控制中路等于控制整个地图节奏</p>
                <p>• <strong>转点通道</strong> - 通过中路快速转点，利用传送门奇袭</p>
                <p>• <strong>特色机制</strong> - 可破坏的门，改变攻防路线</p>
                </div>
                """,
                'bind': """
                <div class="card">
                <h3>📍 关键点位 - 绑定点</h3>
                <p>• <strong>A点进攻路线</strong> - 浴室强攻，A短快速rush</p>
                <p>• <strong>B点防守位置</strong> - 窗口双架，B长走廊控制</p>
                <p>• <strong>中路控制权</strong> - 挂钩位置决定视野优势</p>
                <p>• <strong>转点通道</strong> - 双向传送门快速转移</p>
                <p>• <strong>战术要点</strong> - 传送门声音暴露位置，注意时机</p>
                </div>
                """,
                'haven': """
                <div class="card">
                <h3>📍 关键点位 - 天堂</h3>
                <p>• <strong>三点位布局</strong> - A、B、C三个炸弹点，防守压力大</p>
                <p>• <strong>A点进攻</strong> - A长道控制，A链接夹击</p>
                <p>• <strong>B点控制</strong> - 中路花园是关键，控制B等于控制全局</p>
                <p>• <strong>C点防守</strong> - 车库位置重要，C长道视野开阔</p>
                <p>• <strong>转点策略</strong> - 快速转点制造人数优势</p>
                </div>
                """,
                'split': """
                <div class="card">
                <h3>📍 关键点位 - 裂变峡谷</h3>
                <p>• <strong>A点进攻</strong> - A坡道控制，A大厅夹击</p>
                <p>• <strong>B点防守</strong> - B大厅双架，B窗口狙击</p>
                <p>• <strong>中路控制</strong> - 绳索位置决定主动权</p>
                <p>• <strong>垂直优势</strong> - 高低差明显，利用高度优势</p>
                <p>• <strong>防守要点</strong> - 利用绳索快速回防</p>
                </div>
                """,
                'icebox': """
                <div class="card">
                <h3>📍 关键点位 - 冰港</h3>
                <p>• <strong>A点进攻</strong> - 管道rush，A长道控制</p>
                <p>• <strong>B点防守</strong> - 黄色集装箱，B绿箱位置</p>
                <p>• <strong>中路控制</strong> - 中路通道连接两个点位</p>
                <p>• <strong>绳索系统</strong> - 快速垂直移动，改变战术</p>
                <p>• <strong>视野控制</strong> - 多个高点狙击位</p>
                </div>
                """,
                'breeze': """
                <div class="card">
                <h3>📍 关键点位 - 微风岛屿</h3>
                <p>• <strong>A点进攻</strong> - A大厅控制，A金字塔位置</p>
                <p>• <strong>B点防守</strong> - B大厅双架，B窗口狙击</p>
                <p>• <strong>中路控制</strong> - 中路通道极其重要</p>
                <p>• <strong>长距离对枪</strong> - 适合狙击手发挥</p>
                <p>• <strong>转点路线</strong> - 通过中路或侧翼快速转点</p>
                </div>
                """,
                'fracture': """
                <div class="card">
                <h3>📍 关键点位 - 霓虹町</h3>
                <p>• <strong>双生结构</strong> - 独特的H型布局，四个入口</p>
                <p>• <strong>A点进攻</strong> - 通过绳索快速进入A点</p>
                <p>• <strong>B点防守</strong> - 利用传送带控制B区</p>
                <p>• <strong>中路控制</strong> - 地下通道连接两侧</p>
                <p>• <strong>战术多样性</strong> - 多路线进攻，防守难度大</p>
                </div>
                """,
                'pearl': """
                <div class="card">
                <h3>📍 关键点位 - 珍珠港</h3>
                <p>• <strong>A点进攻</strong> - A主道控制，A链接夹击</p>
                <p>• <strong>B点防守</strong> - B长道控制，B大厅回防</p>
                <p>• <strong>中路控制</strong> - 中路水域视野开阔</p>
                <p>• <strong>水下通道</strong> - 独特的战术路线</p>
                <p>• <strong>转点策略</strong> - 通过中路快速转移</p>
                </div>
                """,
                'lotus': """
                <div class="card">
                <h3>📍 关键点位 - 莲花古城</h3>
                <p>• <strong>三入口设计</strong> - A、B、C三个入口，攻防复杂</p>
                <p>• <strong>旋转门机制</strong> - 可开关的门改变路线</p>
                <p>• <strong>A点控制</strong> - A主道和A小道的配合</p>
                <p>• <strong>B点战术</strong> - 利用声音门制造混乱</p>
                <p>• <strong>回防路线</strong> - 多个快速回防通道</p>
                </div>
                """,
                'sunset': """
                <div class="card">
                <h3>📍 关键点位 - 日落之城</h3>
                <p>• <strong>A点进攻</strong> - A市场控制，A链接夹击</p>
                <p>• <strong>B点防守</strong> - B长道狙击，B大厅控制</p>
                <p>• <strong>中路控制</strong> - 中路花园视野优势</p>
                <p>• <strong>垂直战斗</strong> - 多层结构，注意高低差</p>
                <p>• <strong>转点通道</strong> - 侧翼通道快速转移</p>
                </div>
                """,
                'abyss': """
                <div class="card">
                <h3>📍 关键点位 - 深渊</h3>
                <p>• <strong>无边界设计</strong> - 地图边缘无护栏，注意坠落</p>
                <p>• <strong>A点进攻</strong> - 绳索快速进入，A大厅控制</p>
                <p>• <strong>B点防守</strong> - B平台狙击，B链接回防</p>
                <p>• <strong>中路危险</strong> - 中路多个坠落点，小心走位</p>
                <p>• <strong>独特机制</strong> - 坠落即死，注意站位安全</p>
                </div>
                """
            }

            # 显示对应地图的关键点位信息
            current_map = st.session_state.current
            if current_map in map_key_points:
                st.markdown(map_key_points[current_map], unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="card">
                <h3>📍 关键点位</h3>
                <p>• <strong>A点进攻路线</strong> - 控制主要通道，寻找突破口</p>
                <p>• <strong>B点防守位置</strong> - 建立交叉火力，阻止进攻</p>
                <p>• <strong>中路控制权</strong> - 掌握地图节奏的关键</p>
                <p>• <strong>转点通道</strong> - 快速转移制造人数优势</p>
                <p>• <strong>信息控制</strong> - 利用技能获取敌人位置</p>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            # 根据不同地图提供具体的战术建议
            map_tactics = {
                'ascent': """
                <div class="card">
                <h3>🛡️ 战术建议 - 天漠之峡</h3>
                <p>• <strong>推荐英雄</strong> - 欧门(烟位)、婕提(突破)、奇乐(哨卫)</p>
                <p>• <strong>道具点位</strong> - 中路窗口烟，A小道闪，B链接火</p>
                <p>• <strong>团队配合</strong> - 中路控制后分推A/B点</p>
                <p>• <strong>常见套路</strong> - A大A小同步进攻，B点快速rush</p>
                <p>• <strong>防守策略</strong> - 前压中路获取信息，灵活回防</p>
                </div>
                """,
                'bind': """
                <div class="card">
                <h3>🛡️ 战术建议 - 绑定点</h3>
                <p>• <strong>推荐英雄</strong> - 幽影(烟位)、雷兹(突破)、零(信息)</p>
                <p>• <strong>道具点位</strong> - 浴室烟，挂钩闪，传送门陷阱</p>
                <p>• <strong>团队配合</strong> - 利用传送门快速转点</p>
                <p>• <strong>常见套路</strong> - A点佯攻转B点，传送门奇袭</p>
                <p>• <strong>防守策略</strong> - 前压获取信息，注意传送门声音</p>
                </div>
                """,
                'haven': """
                <div class="card">
                <h3>🛡️ 战术建议 - 天堂</h3>
                <p>• <strong>推荐英雄</strong> - 蝰蛇(烟位)、斯凯(先锋)、圣祈(哨卫)</p>
                <p>• <strong>道具点位</strong> - A长道烟，车库闪，C点火</p>
                <p>• <strong>团队配合</strong> - 三点位拉扯，制造局部多打少</p>
                <p>• <strong>常见套路</strong> - A点佯攻转C点，B点快速占领</p>
                <p>• <strong>防守策略</strong> - 2-1-2阵型，中路信息很重要</p>
                </div>
                """,
                'split': """
                <div class="card">
                <h3>🛡️ 战术建议 - 裂变峡谷</h3>
                <p>• <strong>推荐英雄</strong> -  Sage(哨卫)、Jett(突破)、Omen(烟位)</p>
                <p>• <strong>道具点位</strong> - A坡烟，B窗口闪，中路绳索控制</p>
                <p>• <strong>团队配合</strong> - 利用高低差制造优势</p>
                <p>• <strong>常见套路</strong> - A点快速rush，B点慢打控图</p>
                <p>• <strong>防守策略</strong> - 利用绳索快速回防，交叉火力</p>
                </div>
                """,
                'icebox': """
                <div class="card">
                <h3>🛡️ 战术建议 - 冰港</h3>
                <p>• <strong>推荐英雄</strong> -  Sage(冰墙)、Jett(高空)、Sova(信息)</p>
                <p>• <strong>道具点位</strong> - 管道烟，黄色箱闪，B点冰墙</p>
                <p>• <strong>团队配合</strong> - 利用绳索垂直进攻</p>
                <p>• <strong>常见套路</strong> - A点管道rush，B点慢打控制</p>
                <p>• <strong>防守策略</strong> - 前压获取信息，注意高空位置</p>
                </div>
                """,
                'breeze': """
                <div class="card">
                <h3>🛡️ 战术建议 - 微风岛屿</h3>
                <p>• <strong>推荐英雄</strong> -  Chamber(狙击)、Viper(烟位)、Sova(信息)</p>
                <p>• <strong>道具点位</strong> - A大厅烟，中路闪，B窗口狙</p>
                <p>• <strong>团队配合</strong> - 长距离对枪，狙击手很重要</p>
                <p>• <strong>常见套路</strong> - 中路控制后转点，侧翼包抄</p>
                <p>• <strong>防守策略</strong> - 利用视野优势，远距离对枪</p>
                </div>
                """,
                'fracture': """
                <div class="card">
                <h3>🛡️ 战术建议 - 霓虹町</h3>
                <p>• <strong>推荐英雄</strong> -  Raze(突破)、Killjoy(哨卫)、Astra(烟位)</p>
                <p>• <strong>道具点位</strong> - 绳索烟，传送带闪，地下通道控制</p>
                <p>• <strong>团队配合</strong> - 多路线同步进攻</p>
                <p>• <strong>常见套路</strong> - 四入口同时施压，制造混乱</p>
                <p>• <strong>防守策略</strong> - 信息收集很重要，灵活回防</p>
                </div>
                """,
                'pearl': """
                <div class="card">
                <h3>🛡️ 战术建议 - 珍珠港</h3>
                <p>• <strong>推荐英雄</strong> -  Viper(烟位)、Fade(信息)、Chamber(哨卫)</p>
                <p>• <strong>道具点位</strong> - 水下烟，中路闪，B长道控制</p>
                <p>• <strong>团队配合</strong> - 利用水下通道奇袭</p>
                <p>• <strong>常见套路</strong> - A点慢打控制，B点快速进攻</p>
                <p>• <strong>防守策略</strong> - 控制中路视野，注意水下</p>
                </div>
                """,
                'lotus': """
                <div class="card">
                <h3>🛡️ 战术建议 - 莲花古城</h3>
                <p>• <strong>推荐英雄</strong> -  Killjoy(哨卫)、Harbor(烟位)、Skye(先锋)</p>
                <p>• <strong>道具点位</strong> - 旋转门烟，A点闪，C点控制</p>
                <p>• <strong>团队配合</strong> - 利用声音门制造假象</p>
                <p>• <strong>常见套路</strong> - 多入口同步进攻，旋转门控制</p>
                <p>• <strong>防守策略</strong> - 灵活使用旋转门，快速回防</p>
                </div>
                """,
                'sunset': """
                <div class="card">
                <h3>🛡️ 战术建议 - 日落之城</h3>
                <p>• <strong>推荐英雄</strong> -  Omen(烟位)、Reyna(突破)、Cypher(哨卫)</p>
                <p>• <strong>道具点位</strong> - 市场烟，中路闪，B点控制</p>
                <p>• <strong>团队配合</strong> - 利用垂直优势，高低配合</p>
                <p>• <strong>常见套路</strong> - A点市场控制，B点快速进攻</p>
                <p>• <strong>防守策略</strong> - 控制中路花园，注意侧翼</p>
                </div>
                """,
                'abyss': """
                <div class="card">
                <h3>🛡️ 战术建议 - 深渊</h3>
                <p>• <strong>推荐英雄</strong> -  Jett(机动)、Neon(速度)、Sage(救援)</p>
                <p>• <strong>道具点位</strong> - 绳索烟，边缘闪，安全区控制</p>
                <p>• <strong>团队配合</strong> - 注意站位安全，避免坠落</p>
                <p>• <strong>常见套路</strong> - 利用绳索快速进攻，制造混乱</p>
                <p>• <strong>防守策略</strong> - 控制安全区域，逼迫敌人到边缘</p>
                </div>
                """
            }

            # 显示对应地图的战术建议
            if current_map in map_tactics:
                st.markdown(map_tactics[current_map], unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="card">
                <h3>🛡️ 战术建议</h3>
                <p>• <strong>推荐英雄选择</strong> - 根据地图特点选择合适英雄</p>
                <p>• <strong>道具使用点位</strong> - 学习职业选手的道具投掷</p>
                <p>• <strong>团队配合要点</strong> - 沟通协调，同步进攻</p>
                <p>• <strong>常见战术套路</strong> - 慢打控制 vs 快速rush</p>
                <p>• <strong>经济管理</strong> - 合理规划每回合购买</p>
                </div>
                """, unsafe_allow_html=True)

        # 添加地图特色提示
        st.markdown("### 💡 地图特色提示")

        map_tips = {
            'ascent': "**天漠之峡**: 中路窗口是兵家必争之地，控制中路等于控制整场比赛节奏",
            'bind': "**绑定点**: 善用传送门制造出其不意的进攻，注意传送门声音会暴露位置",
            'haven': "**天堂**: 三点位布局要求防守方灵活机动，进攻方要善于制造假象",
            'split': "**裂变峡谷**: 高低差明显，利用绳索创造垂直优势",
            'icebox': "**冰港**: 多个绳索点位，垂直战术很重要，注意高空敌人",
            'breeze': "**微风岛屿**: 长距离对枪地图，狙击手的天堂，注意视野控制",
            'fracture': "**霓虹町**: 独特的四入口设计，防守压力大，需要良好的信息收集",
            'pearl': "**珍珠港**: 水下通道提供独特战术路线，注意水下声音",
            'lotus': "**莲花古城**: 旋转门和声音门机制，善用可破坏元素",
            'sunset': "**日落之城**: 多层结构，注意高低配合，控制中路花园",
            'abyss': "**深渊**: 无边界设计，注意站位安全，坠落即死"
        }

        if current_map in map_tips:
            st.info(map_tips[current_map])
        else:
            st.info("熟悉地图布局和关键点位是提升胜率的关键，多练习地图控制和经济管理")

    elif st.session_state.current == 'jett.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\jett.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")


    elif st.session_state.current == 'neon.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\neon.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'raze.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\raze.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'waylay.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\waylay.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'astra.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\astra.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'breach.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\breach.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'brimstone.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\brimstone.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'chamber.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\chamber.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'clove.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\clove.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'cypher.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\cypher.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'deadlock.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\deadlock.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'fade.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\fade.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'gekko.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\gekko.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'harbor.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\harbor.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'iso.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\iso.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'killjoy.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\killjoy.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'KO.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\KO.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'omen.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\omen.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'phoenix.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\phoenix.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'reyna.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\reyna.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'sage.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\sage.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'skyer.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\skyer.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'sova.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\sova.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'tejo.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\tejo.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'viper.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\viper.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'vyse.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\vyse.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")

    elif st.session_state.current == 'yoru.png':
        if st.button('返回首页',key=1):
            st.session_state.current = 'home'
        video_path = "video\\yoru.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"视频文件不存在: {video_path}")










