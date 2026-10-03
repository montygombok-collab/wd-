import streamlit as st
import os

# 1. إعدادات الصفحة والهوية
st.set_page_config(
    page_title="ود الحاج AI - باحث الآثار",
    page_icon="🏺",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. تصميم الواجهة بلمسة أثرية (Custom CSS)
st.markdown("""
    <style>
    .main-title {
        color: #8B4513;
        text-align: center;
        font-family: 'Cairo', sans-serif;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #5A3A22;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }
    .stChatMessage {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. ترويسة الموقع
st.markdown('<h1 class="main-title">🏺 ود الحاج AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">الباحث الذكي المخصص للبحوث والمراجع الأثرية والتاريخية</p>', unsafe_allow_html=True)
st.divider()

# 4. الشريط الجانبي (Sidebar - التحكم بالداتا)
with st.sidebar:
    st.image("https://img.icons8.com/color/96/museum.png", width=70)
    st.header("⚙️ إدارة داتا ود الحاج")
    st.write("يقوم النظام بالقراءة من الملفات الجاهزة في مجلد النصوص `data/txt_files`.")
    
    # زر إعادة التحديث لتنشيط الفهرس
    reload_db = st.button("تحديث الفهرس والداتا 🔄", use_container_width=True)
    if reload_db:
        st.info("جاري تجهيز الربط مع محرك البحث...")

    st.divider()
    st.caption("إصدار V1.0 | كلية الآثار")

# 5. منطقة المحادثة والبحث (The "Ask" Section)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "مرحباً بك! أنا **ود الحاج AI**، مساعدك الذكي في كلية الآثار. اسألني عن أي معلومة أثرية أو مرجع تاريخي وسأجيبك فوراً من الواقع المتاح."}
    ]

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال سؤال جديد من الباحث (Ask)
user_query = st.chat_input("اسأل ود الحاج AI عن معلومة أثرية...")

if user_query:
    # 1. عرض سؤال الباحث
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # 2. منطقة الإجابة المؤقتة (حتى نربط مساعد اللغة)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⏳ *ود الحاج AI يفحص المراجع والمستندات...*")
        
        # مؤقتاً لحين ربط ai_helper.py
        dummy_response = f"تم استقبال سؤالك: **('{user_query}')**. الواجهة جاهزة تماماً وفي انتظار ربط 'مساعد اللغة' والقاعدة لتفعيل الإجابة الحقيقية!"
        
        message_placeholder.markdown(dummy_response)
        st.session_state.messages.append({"role": "assistant", "content": dummy_response})
