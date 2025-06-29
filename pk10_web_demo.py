import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from undetected_chromedriver.v2 import Chrome, ChromeOptions

st.set_page_config(layout="wide", page_title="PK10 即時分析 Web 版")
st.title("🏎️ PK10 即時預測分析系統 (正式版)")

@st.cache_data(ttl=15)
def fetch_real_data():
    options = ChromeOptions()
    options.add_argument("--headless")  # 瀏覽器無頭模式
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = Chrome(options=options)

    driver.get("https://1689567.com/view/jisusaiche/pk10kai_luzhufxzh.html")
    time.sleep(5)

    rows = driver.find_elements(By.CSS_SELECTOR, ".history-list tbody tr")
    data = []
    for tr in rows[:10]:
        tds = tr.find_elements(By.TAG_NAME, "td")
        numbers = [td.text for td in tds[1:11]]  # 取得名次資料
        data.append(numbers)

    driver.quit()
    df = pd.DataFrame(data, columns=[f"{i+1}名" for i in range(10)])
    return df

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

st.write("正在載入資料（請稍候）")
df = fetch_real_data()

if df.empty:
    st.error("⚠️ 沒有資料，可能是網頁結構改變或被封鎖。")
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
