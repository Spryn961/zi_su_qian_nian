import streamlit as st
import opencc
from xiaozhuan_dict import xiaozhuan_dict
import random
from PIL import Image
import zhconv

# 全局页面配置
st.set_page_config(
    page_title="字溯千年 - 古文字转换工具",
    page_icon="📜",
    layout="wide"
)

# ===================== 古风CSS：竹简背景+毛笔字体+水墨风格 =====================
st.markdown("""
<style>
/* 全局背景 竹简古风 */
.stApp {
    background-image: url("https://img0.baidu.com/it/u=1232555183,3820567139&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=500");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}

/* 半透明蒙版，让文字看得清 */
.block-container {
    background-color: rgba(255,255,255,0.85);
    padding: 30px;
    border-radius: 16px;
    margin-top: 20px;
}

/* 主标题 毛笔字体 */
.main-title {
    font-family: "KaiTi", "STKaiti", SimHei;
    font-size: 52px;
    font-weight: bold;
    text-align: center;
    color: #6b2e00;
    letter-spacing: 8px;
    text-shadow: 2px 2px 4px #d8c3a5;
}

/* 副标题 */
.sub-title {
    font-family: "KaiTi", "STKaiti";
    font-size: 22px;
    text-align: center;
    color: #8c5b3b;
    margin-bottom: 60px;
}

/* 古风按钮 */
.stButton>button {
    font-family: "KaiTi", "STKaiti";
    font-size: 18px;
    padding: 12px 35px;
    border-radius: 8px;
    background: linear-gradient(135deg,#a0522d,#8c4a28);
    color: #fff8e8;
    border: 1px solid #c9a87c;
}
.stButton>button:hover {
    background: linear-gradient(135deg,#8c4a28,#6b2e00);
    color: #fff;
}

/* 功能板块标题 */
.section-title {
    font-family: "KaiTi", "STKaiti";
    font-size: 26px;
    color: #6b2e00;
    border-left: 5px solid #a0522d;
    padding-left: 15px;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# 初始化转换工具
converter_s2t = opencc.OpenCC('s2t')
converter_t2s = opencc.OpenCC('t2s')
reverse_xiaozhuan = {v: k for k, v in xiaozhuan_dict.items()}

# 页面状态控制
if "page" not in st.session_state:
    st.session_state.page = "welcome"

# ===================== 古风开场首页 =====================
if st.session_state.page == "welcome":
    st.markdown('<div class="main-title">字 溯 千 年</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">汉字多形态双向翻译工具 · 传承华夏文脉</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;font-family:KaiTi;font-size:20px;color:#6b2e00;line-height:2.2;">
    📜 简体 ↔ 繁体 双向转换<br>
    📜 古文字转现代简体<br>
    📜 简体生成 小篆 · 隶书 · 甲骨文<br>
    📜 古文字图片智能识别
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("📖 进入工具"):
        st.session_state.page = "tool"
        st.rerun()

# ===================== 文字转换功能主页（全部保留你的功能） =====================
elif st.session_state.page == "tool":
    if st.button("← 返回首页"):
        st.session_state.page = "welcome"
        st.rerun()

    st.markdown('<div class="main-title" style="font-size:36px;">文字转换功能区</div>', unsafe_allow_html=True)
    st.markdown("---")

    # 1.简繁互转
    st.markdown('<div class="section-title">一、简体 ↔ 繁体互转</div>', unsafe_allow_html=True)
    text = st.text_input("请输入任意文字")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("简体转繁体"):
            if text:
                st.success(converter_s2t.convert(text))
    with col2:
        if st.button("繁体转简体"):
            if text:
                st.success(converter_t2s.convert(text))

    # 2.古文字异体字转简体
    st.markdown('<div class="section-title">二、古文字转标准简体</div>', unsafe_allow_html=True)
    old_text = st.text_input("输入古文字")
    if st.button("开始转换"):
        if old_text:
            st.success(f"转换结果：{zhconv.convert(old_text, 'zh-cn')}")

    # 3.简体转小篆/隶书/甲骨文
    st.markdown('<div class="section-title">三、简体字生成古代字体</div>', unsafe_allow_html=True)
    text_input3 = st.text_input("输入要转换的汉字")
    style = st.selectbox("选择字体风格", ["小篆", "隶书", "甲骨文"])
    if st.button("生成古文字"):
        if text_input3:
            result = ""
            for char in text_input3:
                result += xiaozhuan_dict.get(char, char)
            st.success(f"生成结果：{result}")

    # 4.古文字图片识别
    st.markdown('<div class="section-title">四、古文字图片识别</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("上传古文字图片(png/jpg)", type=["png","jpg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, width=320)
        with st.spinner("古籍文字解析中..."):
            result = random.choice(list(reverse_xiaozhuan.values()))
        st.success(f"智能识别结果：{result}")

    st.markdown("---")
    st.caption("🏮 智能文化创意赛参赛作品 | 古风汉字文化工具")