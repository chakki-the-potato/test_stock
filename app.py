import streamlit as st
from data_fetcher import STOCKS, get_all_data
from chart import create_candlestick_chart

# 페이지 설정
st.set_page_config(
    page_title="주식 차트 대시보드",
    page_icon="📈",
    layout="wide",
)

# 타이틀
st.title("📈 주식 차트 대시보드")
st.caption("2025년 10월 ~ 12월 데이터")

# 사이드바: 종목 선택
st.sidebar.header("종목 선택")
selected_stock = st.sidebar.selectbox(
    "종목을 선택하세요",
    options=list(STOCKS.keys()),
)

# 데이터 로딩
with st.spinner("데이터를 불러오는 중..."):
    try:
        daily, weekly, monthly, info = get_all_data(selected_stock)

        # 현재가 정보 카드
        st.subheader(f"{selected_stock} 현재가 정보")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="현재가",
                value=f"{info['current_price']:,.0f}원",
                delta=f"{info['change']:+,.0f}원 ({info['change_percent']:+.2f}%)",
            )

        with col2:
            st.metric(
                label="52주 최고",
                value=f"{info['high_52week']:,.0f}원",
            )

        with col3:
            st.metric(
                label="52주 최저",
                value=f"{info['low_52week']:,.0f}원",
            )

        with col4:
            st.metric(
                label="거래량",
                value=f"{info['volume']:,.0f}",
            )

        st.divider()

        # 탭: 일봉 / 주봉 / 월봉
        tab1, tab2, tab3 = st.tabs(["📊 일봉", "📅 주봉", "📆 월봉"])

        with tab1:
            if len(daily) > 0:
                fig = create_candlestick_chart(daily, f"{selected_stock} 일봉 차트")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("일봉 데이터가 없습니다.")

        with tab2:
            if len(weekly) > 0:
                fig = create_candlestick_chart(weekly, f"{selected_stock} 주봉 차트")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("주봉 데이터가 없습니다.")

        with tab3:
            if len(monthly) > 0:
                fig = create_candlestick_chart(monthly, f"{selected_stock} 월봉 차트")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("월봉 데이터가 없습니다.")

    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")

# 푸터
st.sidebar.divider()
st.sidebar.caption("데이터 출처: Yahoo Finance (yfinance)")
