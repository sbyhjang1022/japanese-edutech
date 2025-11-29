import streamlit as st

st.title("🗨️ 메타버스 일본어 회화 마을")

place = st.selectbox("장소를 선택하세요", ["편의점（コンビニ）", "역（駅）", "식당（レストラン）"])

if place == "편의점（コンビニ）":
    st.image("conv_store.jpg")
    st.write("店員：いらっしゃいませ！")
    st.radio("당신의 말 선택:", [
        "これください", "〜はどこですか？", "おすすめは何ですか？"
    ])

elif place == "역（駅）":
    st.image("station.jpg")
    st.write("駅員：どこまで行きますか？")
    st.radio("당신의 말 선택:", [
        "切符をください", "〜行きは何番線ですか？", "今、何時の電車がありますか？"
    ])

elif place == "식당（レストラン）":
    st.image("restaurant.jpg")
    st.write("店員：ご注文はお決まりですか？")
    st.radio("당신의 말:", [
        "おすすめは何ですか？", "これをください", "お水をください"
    ])

st.info("실제 말하기 녹음은 ‘말하기 녹음 제출’ 페이지에서 진행합니다!")
