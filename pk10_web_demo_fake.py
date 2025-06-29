import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="PK10 即時分析 Web 版")
st.title("🏎️ PK10 即時預測分析系統 (簡版 Web 示範)")

# 範例模擬資料（因 Streamlit Cloud 無法直接執行 Selenium）
@st.cache_data(ttl=15)
def fetch_fake_data():
    data = {
        "1名": [1, 5, 3, 8],
        "2名": [2, 7, 6, 4],
        "3名": [3, 8, 2, 1],
        "4名": [4, 6, 5, 3],
        "5名": [5, 1, 7, 9],
        "6名": [6, 3, 4, 2],
        "7名": [7, 9, 1, 5],
        "8名": [8, 2, 8, 7],
        "9名": [9, 4, 9, 6],
        "10名": [10, 10, 10, 10],
    }
    df = pd.DataFrame(data)
    return df

# 簡易分析邏輯
def simple_analysis(df):
    result = {}
    for col in df.columns:
        s = df[col].astype(int)
        if len(s) >= 4 and s.iloc[-1] == s.iloc[-3] and s.iloc[-2] == s.iloc[-4]:
            result[col] = "⭕ 對稱"
        elif len(s) >= 2 and s.iloc[-1] == s.iloc[-2]:
            result[col] = "📈 順風"
        else:
            result[col] = "—"
    return result

st.write("正在載入資料（這裡為示範假資料，正式版本會串 Selenium）")
df = fetch_fake_data()

if df.empty:
    st.error("⚠️ 沒有資料")
else:
    st.subheader("🎲 最新開獎號碼")
    st.dataframe(df)

    st.subheader("🔍 大路圖分析結果")
    analysis = simple_analysis(df)
    st.write(analysis)

    st.subheader("🔮 預測推薦")
    pred = {
        pos: f"推薦 {df[pos].iloc[-1]} 或 +/-1" if analysis[pos] != "—" else "無預測"
        for pos in df.columns
    }
    st.write(pred)

    st.success("✅ 資料分析完成！")
