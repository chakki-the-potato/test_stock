import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def create_candlestick_chart(df: pd.DataFrame, title: str = "주가 차트") -> go.Figure:
    """캔들스틱 + 이동평균선 + 거래량 차트 생성"""

    # 서브플롯 생성 (캔들스틱 + 거래량)
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3],
    )

    # 캔들스틱 차트 (상승: 빨강, 하락: 파랑)
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            increasing_line_color="red",
            decreasing_line_color="blue",
            increasing_fillcolor="red",
            decreasing_fillcolor="blue",
            name="가격",
        ),
        row=1,
        col=1,
    )

    # 이동평균선 추가
    if "MA5" in df.columns and df["MA5"].notna().any():
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["MA5"],
                mode="lines",
                name="MA5",
                line=dict(color="gold", width=1),
            ),
            row=1,
            col=1,
        )

    if "MA20" in df.columns and df["MA20"].notna().any():
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["MA20"],
                mode="lines",
                name="MA20",
                line=dict(color="green", width=1),
            ),
            row=1,
            col=1,
        )

    if "MA60" in df.columns and df["MA60"].notna().any():
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["MA60"],
                mode="lines",
                name="MA60",
                line=dict(color="purple", width=1),
            ),
            row=1,
            col=1,
        )

    # 거래량 바 차트 (상승/하락 색상 연동)
    colors = [
        "red" if df["Close"].iloc[i] >= df["Open"].iloc[i] else "blue"
        for i in range(len(df))
    ]

    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["Volume"],
            marker_color=colors,
            name="거래량",
            opacity=0.7,
        ),
        row=2,
        col=1,
    )

    # 레이아웃 설정
    fig.update_layout(
        title=title,
        xaxis_rangeslider_visible=False,
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    # Y축 레이블
    fig.update_yaxes(title_text="가격 (원)", row=1, col=1)
    fig.update_yaxes(title_text="거래량", row=2, col=1)

    # X축 레이블 (거래량 차트에만)
    fig.update_xaxes(title_text="날짜", row=2, col=1)

    return fig
