import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 🌟 배포 사이트 다크 테마 강제 적용 (배경 검은색)
st.set_page_config(
    page_title="자산 관리 대시보드",
    page_icon="🍩",
    layout="wide",
    initial_sidebar_state="expanded"


st.set_page_config(page_title="통합 자산 관리 대시보드", layout="wide")

# ====================================================
# 🎨 Custom CSS: 상단 메인 탭 글씨 및 높이 확대
# ====================================================
st.markdown("""
    <style>
        /* 상단 메인 탭 버튼 크기 및 글씨 키우기 */
        button[data-baseweb="tab"] {
            font-size: 18px !important;
            font-weight: bold !important;
            padding: 12px 20px !important;
        }
        /* 탭 내부 p 태그 폰트 크기 확대 */
        button[data-baseweb="tab"] p {
            font-size: 18px !important;
            font-weight: bold !important;
        }
    </style>
""", unsafe_allow_html=True)

# ====================================================
# 🔗 1. 구글 스프레드시트 탭별 고유 URL 설정
# ====================================================
URL_TOTAL_ASSETS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRI1ukc6E3nrKYLodL7FYXn8G4FEXO_57SYFhTIPargcHnAiKwSL6s8Hm4P82icbT9ElQL2tb486myu/pub?gid=1903489764&single=true&output=csv"
URL_DOMESTIC_1   = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRI1ukc6E3nrKYLodL7FYXn8G4FEXO_57SYFhTIPargcHnAiKwSL6s8Hm4P82icbT9ElQL2tb486myu/pub?gid=421267838&single=true&output=csv"
URL_DOMESTIC_2   = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRI1ukc6E3nrKYLodL7FYXn8G4FEXO_57SYFhTIPargcHnAiKwSL6s8Hm4P82icbT9ElQL2tb486myu/pub?gid=2071295463&single=true&output=csv"
URL_OVERSEAS     = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRI1ukc6E3nrKYLodL7FYXn8G4FEXO_57SYFhTIPargcHnAiKwSL6s8Hm4P82icbT9ElQL2tb486myu/pub?gid=366693116&single=true&output=csv"
URL_COIN         = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRI1ukc6E3nrKYLodL7FYXn8G4FEXO_57SYFhTIPargcHnAiKwSL6s8Hm4P82icbT9ElQL2tb486myu/pub?gid=562533829&single=true&output=csv"
URL_PENSION      = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRI1ukc6E3nrKYLodL7FYXn8G4FEXO_57SYFhTIPargcHnAiKwSL6s8Hm4P82icbT9ElQL2tb486myu/pub?gid=783376312&single=true&output=csv"

# ====================================================
# 🛠 2. 핵심 공통 처리 함수 정의
# ====================================================
@st.cache_data(ttl=0)
def load_pure_data(url):
    try:
        df = pd.read_csv(url, header=None)
        if df.empty: return None
        return df.iloc[4:].reset_index(drop=True)
    except Exception as e:
        return None

def clean_and_convert(value):
    if pd.isna(value): return 0
    if isinstance(value, str):
        value = value.replace(',', '').replace('%', '').replace('원', '').strip()
    try: return float(value)
    except: return 0

# 🌟 날짜를 YYYY/MM (예: 2026/07) 형태로 무조건 변환해주는 함수
def format_date_str(val):
    val_str = str(val).strip()
    if not val_str or val_str.lower() == 'nan':
        return ""
    
    dt = pd.to_datetime(val_str, errors='coerce')
    if pd.notna(dt):
        return dt.strftime('%Y/%m')
    
    val_clean = val_str.replace('-', '/')
    if len(val_clean) >= 7 and val_clean[:4].isdigit():
        return val_clean[:7]
        
    return val_str

def display_summary(df, is_total=False):
    if df.empty: return
    latest = df.iloc[0]
    val_invest = clean_and_convert(latest['투자원금'])
    val_balance = clean_and_convert(latest['현재잔고'])
    val_profit = clean_and_convert(latest['수익금액'])
    
    if is_total:
        val_ratio = (val_profit / val_invest * 100) if val_invest != 0 else 0
        val_ratio = round(val_ratio, 2)
    else:
        val_ratio = clean_and_convert(latest['수익률'])
    
    profit_color = "#FF5252" if val_profit > 0 else ("#448AFF" if val_profit < 0 else "#FFFFFF")
    profit_sign = "+" if val_profit > 0 else ""
    ratio_color = "#FF5252" if val_ratio > 0 else ("#448AFF" if val_ratio < 0 else "#FFFFFF")
    ratio_sign = "+" if val_ratio > 0 else ""

    # 🌟 [위쪽] 전체 요약: 가로로 넓은 프리미엄 통짜 대형 카드 1개형
    if is_total:
        st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #1E222A 0%, #121418 100%);
                border: 1px solid #3A3F4B;
                border-radius: 16px;
                padding: 24px 30px;
                margin-bottom: 25px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.5);
                display: flex;
                justify-content: space-between;
                align-items: center;
            '>
                <div style='flex: 1; border-right: 1px solid #2C313C; padding-right: 15px;'>
                    <div style='font-size: 13px; color: #9E9E9E; margin-bottom: 4px; font-weight: 500;'>💵 전체 투자원금</div>
                    <div style='font-size: 24px; font-weight: bold; color: #FFFFFF;'>{int(val_invest):,}원</div>
                </div>
                <div style='flex: 1; border-right: 1px solid #2C313C; padding-left: 20px; padding-right: 15px;'>
                    <div style='font-size: 13px; color: #9E9E9E; margin-bottom: 4px; font-weight: 500;'>🏦 전체 현재잔고</div>
                    <div style='font-size: 24px; font-weight: bold; color: #FFFFFF;'>{int(val_balance):,}원</div>
                </div>
                <div style='flex: 1; border-right: 1px solid #2C313C; padding-left: 20px; padding-right: 15px;'>
                    <div style='font-size: 13px; color: #9E9E9E; margin-bottom: 4px; font-weight: 500;'>📈 전체 수익금액</div>
                    <div style='font-size: 24px; font-weight: bold; color: {profit_color};'>{profit_sign}{int(val_profit):,}원</div>
                </div>
                <div style='flex: 1; padding-left: 20px;'>
                    <div style='font-size: 13px; color: #9E9E9E; margin-bottom: 4px; font-weight: 500;'>📊 전체 수익률</div>
                    <div style='font-size: 24px; font-weight: bold; color: {ratio_color};'>{ratio_sign}{val_ratio}%</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # 🌟 [아래쪽] 개별 계좌 요약: 기존 4개 분할 미니멀 카드형
    else:
        col1, col2, col3, col4 = st.columns(4)
        card_base = """
            background: #141619;
            border: 1px solid #262930;
            border-radius: 10px;
            padding: 14px 18px;
            text-align: left;
        """
        with col1: 
            st.markdown(f"""
                <div style='{card_base} border-left: 3px solid #FFA726;'>
                    <div style='font-size: 12px; color:#888888; margin-bottom:4px;'>💵 투자원금</div>
                    <div style='font-size: 18px; font-weight: bold; color:#FFFFFF;'>{int(val_invest):,}원</div>
                </div>
            """, unsafe_allow_html=True)
        with col2: 
            st.markdown(f"""
                <div style='{card_base} border-left: 3px solid #26A69A;'>
                    <div style='font-size: 12px; color:#888888; margin-bottom:4px;'>🏦 현재잔고</div>
                    <div style='font-size: 18px; font-weight: bold; color:#FFFFFF;'>{int(val_balance):,}원</div>
                </div>
            """, unsafe_allow_html=True)
        with col3: 
            st.markdown(f"""
                <div style='{card_base} border-left: 3px solid {profit_color};'>
                    <div style='font-size: 12px; color:#888888; margin-bottom:4px;'>📈 수익금액</div>
                    <div style='font-size: 18px; font-weight: bold; color:{profit_color};'>{profit_sign}{int(val_profit):,}원</div>
                </div>
            """, unsafe_allow_html=True)
        with col4: 
            st.markdown(f"""
                <div style='{card_base} border-left: 3px solid {ratio_color};'>
                    <div style='font-size: 12px; color:#888888; margin-bottom:4px;'>📊 수익률</div>
                    <div style='font-size: 18px; font-weight: bold; color:{ratio_color};'>{ratio_sign}{val_ratio}%</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)


def display_chart(df):
    if df.empty: return
    chart_df = df.copy()
    for col in ['투자원금', '현재잔고', '수익금액', '수익률']:
        chart_df[col] = chart_df[col].apply(clean_and_convert)
    
    chart_df['순수익'] = chart_df['현재잔고'] - chart_df['투자원금']
    
    # 차트 X축용으로 시간순(오래된 순 -> 최신순) 정렬
    chart_df['temp_dt'] = pd.to_datetime(chart_df['일자'], format='%Y/%m', errors='coerce')
    chart_df = chart_df.sort_values(by='temp_dt').reset_index(drop=True)
        
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Bar(
        x=chart_df['일자'], y=chart_df['투자원금'], name="투자원금",
        marker_color='#FFA726', opacity=0.85,
        hovertemplate='<b>투자원금</b>: %{y:,.0f}원'
    ), secondary_y=False)
    
    fig.add_trace(go.Bar(
        x=chart_df['일자'], y=chart_df['순수익'], name="평가손익",
        marker_color='#FF5252', opacity=0.85,
        hovertemplate='<b>평가손익</b>: %{y:+,.0f}원'
    ), secondary_y=False)
    
    fig.add_trace(go.Scatter(
        x=chart_df['일자'], y=chart_df['수익률'], name="수익률(%)", 
        line=dict(color='#BA55D3', width=3),
        hovertemplate='<b>수익률</b>: %{y:.2f}%'
    ), secondary_y=True)
    
    fig.update_layout(
        barmode='stack',
        height=340, margin=dict(l=0, r=0, t=20, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hovermode="x unified",
        yaxis=dict(tickformat=",.0f", ticksuffix="원"),
        yaxis2=dict(ticksuffix="%"),
        xaxis=dict(type='category')  # 👈 X축을 카테고리(YYYY/MM)로 고정
    )
    st.plotly_chart(fig, use_container_width=True)


def parse_account(df, start_idx):
    if df is None: return pd.DataFrame(columns=['일자', '투자원금', '현재잔고', '수익금액', '수익률', '월수익'])
    total_cols = df.shape[1]
    if total_cols >= start_idx + 5:
        sub_df = df[[0, start_idx, start_idx+1, start_idx+2, start_idx+3, start_idx+4]].copy()
        sub_df.columns = ['일자', '투자원금', '현재잔고', '수익금액', '수익률', '월수익']
    elif total_cols >= start_idx + 2:
        sub_df = df[[0, start_idx, start_idx+1]].copy()
        sub_df.columns = ['일자', '투자원금', '현재잔고']
        val_inv = sub_df['투자원금'].apply(clean_and_convert)
        val_bal = sub_df['현재잔고'].apply(clean_and_convert)
        sub_df['수익금액'] = val_bal - val_inv
        sub_df['수익률'] = ((sub_df['수익금액'] / val_inv) * 100).fillna(0).round(2)
        sub_df['월수익'] = 0
    else:
        return pd.DataFrame(columns=['일자', '투자원금', '현재잔고', '수익금액', '수익률', '월수익'])
        
    # 🌟 일자를 YYYY/MM 형태로 변환
    sub_df['일자'] = sub_df['일자'].apply(format_date_str)
    sub_df = sub_df[pd.notna(sub_df['일자']) & (sub_df['일자'] != '') & (sub_df['일자'].str.lower() != 'nan')].copy()
    
    sub_df['월수익'] = sub_df['월수익'].apply(clean_and_convert)
    if sub_df['월수익'].sum() == 0:
        profit_num = sub_df['수익금액'].apply(clean_and_convert)
        sub_df['월수익'] = profit_num.diff().fillna(profit_num)
        
    return sub_df

# 연금 전용 파싱 함수 (IRP의 '입금' 열 및 흥국생명의 2열 구조 대응)
def parse_pension_account(df, start_idx, is_irp=False, is_hunguk=False):
    if df is None: return pd.DataFrame(columns=['일자', '투자원금', '현재잔고', '수익금액', '수익률', '월수익'])
    
    if is_irp:
        sub_df = df[[0, start_idx, start_idx+2, start_idx+3, start_idx+4, start_idx+5]].copy()
    elif is_hunguk:
        sub_df = df[[0, start_idx, start_idx+1]].copy()
        sub_df['수익금액'] = sub_df[start_idx+1].apply(clean_and_convert) - sub_df[start_idx].apply(clean_and_convert)
        sub_df['수익률'] = 0
        sub_df['월수익'] = 0
    else:
        sub_df = df[[0, start_idx, start_idx+1, start_idx+2, start_idx+3, start_idx+4]].copy()

    sub_df.columns = ['일자', '투자원금', '현재잔고', '수익금액', '수익률', '월수익']

    # 🌟 일자를 YYYY/MM 형태로 변환
    sub_df['일자'] = sub_df['일자'].apply(format_date_str)
    sub_df = sub_df[pd.notna(sub_df['일자']) & (sub_df['일자'] != '') & (sub_df['일자'].str.lower() != 'nan')].copy()
    
    sub_df['월수익'] = sub_df['월수익'].apply(clean_and_convert)
    if sub_df['월수익'].sum() == 0:
        profit_num = sub_df['수익금액'].apply(clean_and_convert)
        sub_df['월수익'] = profit_num.diff().fillna(profit_num)
        
    return sub_df

def render_account_tab(sub_df, title):
    display_summary(sub_df, is_total=False)
    display_chart(sub_df)
    
    # 🎨 수익금액, 수익률 컬러 스타일링 함수 정의
    def color_profit_loss(val):
        num_val = clean_and_convert(val)
        if num_val > 0:
            return 'color: #FF5252; font-weight: bold;'  # 수익: 붉은색
        elif num_val < 0:
            return 'color: #448AFF; font-weight: bold;'  # 손실: 파란색
        return 'color: #8E9297;'                         # 0 또는 기타

    # 표로 보여줄 데이터 복사
    df_disp = sub_df.copy()
    
    for col in ['투자원금', '현재잔고', '수익금액', '수익률', '월수익']:
        if col in df_disp.columns:
            df_disp[col] = df_disp[col].apply(clean_and_convert)
            
    df_disp = df_disp.set_index('일자')
    
    # 숫자 포맷 및 스타일 적용
    styled_tab_df = df_disp.style\
        .map(color_profit_loss, subset=['수익금액', '수익률'])\
        .format({
            '투자원금': "{:,.0f}원", 
            '현재잔고': "{:,.0f}원", 
            '수익금액': "{:+,.0f}원", 
            '수익률': "{:+.2f}%", 
            '월수익': "{:+,.0f}원"
        }, na_rep="-")
        
    st.dataframe(styled_tab_df, use_container_width=True)

def calculate_total_df(accounts):
    total_df = pd.DataFrame()
    total_df['일자'] = accounts[0]['일자']
    
    for col in ['투자원금', '현재잔고', '수익금액']:
        total_df[col] = sum(acc[col].apply(clean_and_convert) for acc in accounts)
        
    total_df['수익률'] = (total_df['수익금액'] / total_df['투자원금'] * 100).fillna(0).round(2)
    total_df['월수익'] = total_df['수익금액'].diff().fillna(total_df['수익금액'])
    return total_df

# ====================================================
# 🚀 3. 메인 화면 레이아웃 & 탭 제어
# ====================================================
top_tabs = st.tabs(["🏠 대시보드", "📊 월별 손익", "🏦 국내", "🌐 해외", "🪙 코인", "💰 연금"])

data_total_asset = load_pure_data(URL_TOTAL_ASSETS)
data_dom1 = load_pure_data(URL_DOMESTIC_1)
data_dom2 = load_pure_data(URL_DOMESTIC_2)
data_overseas = load_pure_data(URL_OVERSEAS)
data_coin = load_pure_data(URL_COIN)
data_pension = load_pure_data(URL_PENSION)

account_dict = {}

if data_dom1 is not None and data_dom2 is not None:
    account_dict["단기스윙"] = parse_account(data_dom1, 3)
    account_dict["단타연습"] = parse_account(data_dom1, 8)
    account_dict["장기스윙"] = parse_account(data_dom1, 13)
    account_dict["한투계좌"] = parse_account(data_dom2, 3)
    account_dict["SPC계좌"] = parse_account(data_dom2, 8)
    dom_accs = [account_dict["단기스윙"], account_dict["단타연습"], account_dict["장기스윙"], account_dict["한투계좌"], account_dict["SPC계좌"]]
    df_dom_total = calculate_total_df(dom_accs)
else:
    df_dom_total = None

if data_overseas is not None:
    num_cols = len(data_overseas.columns)
    ovs_accs = [parse_account(data_overseas, 3)]
    account_dict["토스증권"] = ovs_accs[0]
    if num_cols > 8:
        ovs_accs.append(parse_account(data_overseas, 8))
        account_dict["SOXL Grid"] = ovs_accs[1]
    if num_cols > 13:
        ovs_accs.append(parse_account(data_overseas, 13))
        account_dict["떨사오팔"] = ovs_accs[2]
    df_ovs_total = calculate_total_df(ovs_accs)
else:
    df_ovs_total = None

if data_coin is not None:
    num_cols = len(data_coin.columns)
    coin_accs = [parse_account(data_coin, 3)]
    account_dict["테더자동"] = coin_accs[0]
    if num_cols > 8:
        coin_accs.append(parse_account(data_coin, 8))
        account_dict["비트겟"] = coin_accs[1]
    if num_cols > 13:
        coin_accs.append(parse_account(data_coin, 13))
        account_dict["코인계좌 3"] = coin_accs[2]
    df_coin_total = calculate_total_df(coin_accs)
else:
    df_coin_total = None

if data_pension is not None:
    num_cols = len(data_pension.columns)
    pen_accs = []
    
    if num_cols > 3:
        acc1 = parse_pension_account(data_pension, 3)
        pen_accs.append(acc1)
        account_dict["개인연금"] = acc1
        
    if num_cols > 8:
        acc2 = parse_pension_account(data_pension, 8, is_irp=True)
        pen_accs.append(acc2)
        account_dict["IRP"] = acc2
        
    if num_cols > 14:
        acc3 = parse_pension_account(data_pension, 14)
        pen_accs.append(acc3)
        account_dict["퇴직연금"] = acc3
        
    if num_cols > 19:
        acc4 = parse_pension_account(data_pension, 19, is_hunguk=True)
        pen_accs.append(acc4)
        account_dict["흥국생명"] = acc4
        
    df_pension_total = calculate_total_df(pen_accs)
else:
    df_pension_total = None

# ----------------------------------------------------
# 🌟 메인 탭 0 : 🏠 대시보드
# ----------------------------------------------------
with top_tabs[0]:
    if data_total_asset is not None and not data_total_asset.empty:
        valid_mask = pd.notna(data_total_asset.iloc[:, 0]) & (data_total_asset.iloc[:, 0].astype(str).str.strip() != '') & (data_total_asset.iloc[:, 0].astype(str).str.lower() != 'nan')
        data_clean = data_total_asset[valid_mask].reset_index(drop=True)
        
        # 🌟 최신 데이터(맨 위 행)
        df_asset_last = data_clean.iloc[0]
        has_prev_row = len(data_clean) >= 2
        df_asset_prev = data_clean.iloc[1] if has_prev_row else df_asset_last
        
        val_real_estate = clean_and_convert(df_asset_last.iloc[7])
        val_gold        = clean_and_convert(df_asset_last.iloc[8])
        val_cash        = clean_and_convert(df_asset_last.iloc[9]) + clean_and_convert(df_asset_last.iloc[10]) + clean_and_convert(df_asset_last.iloc[11])
        val_savings     = sum(clean_and_convert(df_asset_last.iloc[i]) for i in range(12, 16))
        
        df_assets = pd.DataFrame()
        df_assets['일자'] = data_clean.iloc[:, 0].apply(format_date_str)
        df_assets['총자산'] = data_clean.iloc[:, 3].apply(clean_and_convert)
        df_assets['증감액'] = data_clean.iloc[:, 4].apply(clean_and_convert)
        df_assets['증감율'] = data_clean.iloc[:, 5].apply(clean_and_convert)
        df_assets['Event'] = data_clean.iloc[:, 6].fillna('-').astype(str).str.strip()
        
        df_assets['부동산'] = data_clean.iloc[:, 7].apply(clean_and_convert)
        df_assets['Gold'] = data_clean.iloc[:, 8].apply(clean_and_convert)
        df_assets['통장(현금성)'] = data_clean.iloc[:, 9].apply(clean_and_convert) + data_clean.iloc[:, 10].apply(clean_and_convert) + data_clean.iloc[:, 11].apply(clean_and_convert)
        df_assets['적금/예금'] = data_clean.iloc[:, 12:16].map(clean_and_convert).sum(axis=1)
        
        stock_coin_pension = df_assets['총자산'] - (df_assets['부동산'] + df_assets['Gold'] + df_assets['통장(현금성)'] + df_assets['적금/예금'])
        df_assets['주식/코인/연금'] = stock_coin_pension.apply(lambda x: max(x, 0))

        df_assets['temp_dt'] = pd.to_datetime(df_assets['일자'], format='%Y/%m', errors='coerce')
        df_assets = df_assets.dropna(subset=['temp_dt']).sort_values(by='temp_dt').drop(columns=['temp_dt']).reset_index(drop=True)
    else:
        val_real_estate, val_gold, val_cash, val_savings = 0, 0, 0, 0
        df_assets = pd.DataFrame()

    def get_latest_acc_vals(df, indices):
        inv_tot, bal_tot = 0, 0
        for idx in indices:
            acc = parse_account(df, idx)
            if not acc.empty:
                inv_tot += clean_and_convert(acc.iloc[0]['투자원금'])
                bal_tot += clean_and_convert(acc.iloc[0]['현재잔고'])
        return inv_tot, bal_tot

    dom_inv1, dom_bal1 = get_latest_acc_vals(data_dom1, [3, 8, 13])
    dom_inv2, dom_bal2 = get_latest_acc_vals(data_dom2, [3, 8])
    dom_inv, dom_bal = dom_inv1 + dom_inv2, dom_bal1 + dom_bal2

    ovs_inv, ovs_bal = get_latest_acc_vals(data_overseas, [3, 8, 13])
    coin_inv, coin_bal = get_latest_acc_vals(data_coin, [3, 8])
    
    pen_inv, pen_bal = 0, 0
    if data_pension is not None:
        p1 = parse_pension_account(data_pension, 3)
        p2 = parse_pension_account(data_pension, 8, is_irp=True)
        p3 = parse_pension_account(data_pension, 14)
        p4 = parse_pension_account(data_pension, 19, is_hunguk=True)
        for acc in [p1, p2, p3, p4]:
            if not acc.empty:
                pen_inv += clean_and_convert(acc.iloc[0]['투자원금'])
                pen_bal += clean_and_convert(acc.iloc[0]['현재잔고'])

    dom_profit, ovs_profit, coin_profit, pen_profit = dom_bal - dom_inv, ovs_bal - ovs_inv, coin_bal - coin_inv, pen_bal - pen_inv
    total_tech_inv, total_tech_bal = dom_inv + ovs_inv + coin_inv + pen_inv, dom_bal + ovs_bal + coin_bal + pen_bal
    total_tech_profit = total_tech_bal - total_tech_inv

    val_stock_coin, val_pension_bal = dom_bal + ovs_bal + coin_bal, pen_bal
    val_total_assets = val_real_estate + val_stock_coin + val_pension_bal + val_savings + val_cash + val_gold

    prev_total_assets = clean_and_convert(df_asset_prev.iloc[3]) if has_prev_row else val_total_assets
    diff_amount = val_total_assets - prev_total_assets
    diff_rate = (diff_amount / prev_total_assets * 100) if prev_total_assets > 0 else 0.0
    
    diff_color = "#FF5252" if diff_amount > 0 else ("#448AFF" if diff_amount < 0 else "#8E9297")
    diff_sign = "+" if diff_amount > 0 else ""
    badge_html = f"""
        <span style='background-color: {diff_color}22; border: 1px solid {diff_color}; color: {diff_color}; 
                     font-size: 13px; font-weight: 600; padding: 3px 8px; border-radius: 6px; margin-left: 10px;'>
            {diff_sign}{int(diff_amount):,}원 ({diff_sign}{diff_rate:.2f}%)
        </span>
    """ if has_prev_row else ""

    def calc_rate(inv, bal): return round(((bal - inv) / inv * 100), 2) if inv > 0 else 0.0

    dom_rate, ovs_rate, coin_rate, pen_rate = calc_rate(dom_inv, dom_bal), calc_rate(ovs_inv, ovs_bal), calc_rate(coin_inv, coin_bal), calc_rate(pen_inv, pen_bal)
    total_tech_rate = calc_rate(total_tech_inv, total_tech_bal)

    card_style = "background-color: #16181A; border: 1px solid #2A2D32; border-radius: 12px; padding: 18px 16px; height: 100%; color: #FFFFFF;"
    row_style = "display: flex; justify-content: space-between; align-items: center; margin-top: 10px; font-size: 15px;"
    label_style = "color: #C2C5C9; font-weight: 500;"
    val_style = "font-weight: 600; font-size: 16px; color: #FFFFFF;"

    def format_profit_text(profit):
        if profit > 0: return f"<span style='color: #FF5252; font-weight: bold;'>+{int(profit):,}원</span>"
        elif profit < 0: return f"<span style='color: #448AFF; font-weight: bold;'>{int(profit):,}원</span>"
        return "<span style='color: #8E9297; font-weight: bold;'>0원</span>"

    def format_rate_color(rate):
        if rate > 0: return f"<span style='color: #FF5252; font-size: 12px; font-weight: bold;'>+{rate}%</span>"
        elif rate < 0: return f"<span style='color: #448AFF; font-size: 12px; font-weight: bold;'>{rate}%</span>"
        return f"<span style='color: #8E9297; font-size: 12px; font-weight: bold;'>0.0%</span>"

    # ====================================================
    # 🌟 [1번째 줄] 총자산 현황 + 자산 비중 + 총자산 누적 막대 추이 그래프
    # ====================================================
    r1_col1, r1_col2, r1_col3 = st.columns([0.7, 1.0, 1.8])

    with r1_col1:
        st.markdown(f"""
            <div style='{card_style}'>
                <div style='font-size: 19px; font-weight: bold; color: #FFFFFF; margin-bottom: 10px;'>
                    <span style='color: #00E676;'>●</span> 총자산 현황
                </div>
                <div style='color: #00E676; font-size: 12px; font-weight: bold;'>총자산</div>
                <div style='font-size: 22px; font-weight: 800; color: #FFFFFF; margin-bottom: 10px; letter-spacing: -0.5px;'>
                    {int(val_total_assets):,}원
                </div>
                <div style='border-top: 1px solid #2A2D32; padding-top: 6px;'>
                    <div style='{row_style}'><span style='{label_style}'>부동산</span><span style='{val_style}'>{int(val_real_estate):,}원</span></div>
                    <div style='{row_style}'><span style='{label_style}'>주식/코인</span><span style='{val_style}'>{int(val_stock_coin):,}원</span></div>
                    <div style='{row_style}'><span style='{label_style}'>연금</span><span style='{val_style}'>{int(val_pension_bal):,}원</span></div>
                    <div style='{row_style}'><span style='{label_style}'>예적금</span><span style='{val_style}'>{int(val_savings):,}원</span></div>
                    <div style='{row_style}'><span style='{label_style}'>현금성</span><span style='{val_style}'>{int(val_cash):,}원</span></div>
                    <div style='{row_style}'><span style='{label_style}'>Gold</span><span style='{val_style}'>{int(val_gold):,}원</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with r1_col2:
        if not df_assets.empty:
            latest_row = df_assets.iloc[-1]
            labels = ['부동산', 'Gold', '통장(현금성)', '적금/예금', '주식/코인/연금']
            values = [latest_row['부동산'], latest_row['Gold'], latest_row['통장(현금성)'], latest_row['적금/예금'], latest_row['주식/코인/연금']]
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=labels, values=values, hole=.45,
                marker=dict(colors=['#2E7D32', '#FBC02D', '#1E88E5', '#8E24AA', '#E65100']),
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b>: %{value:,.0f}원 (%{percent})'
            )])
            fig_pie.update_layout(
                title=dict(text="🍩 자산 포트폴리오 비중", font=dict(size=18, color="#FFFFFF")),
                height=350, margin=dict(l=10, r=10, t=35, b=35), showlegend=False
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    with r1_col3:
        if not df_assets.empty:
            fig_line = make_subplots(specs=[[{"secondary_y": True}]])

            asset_layers = [
                ('부동산', '#2E7D32'),
                ('Gold', '#FBC02D'),
                ('통장(현금성)', '#1E88E5'),
                ('적금/예금', '#8E24AA'),
                ('주식/코인/연금', '#E65100')
            ]
            
            for col_name, col_color in asset_layers:
                if col_name in df_assets.columns:
                    fig_line.add_trace(go.Bar(
                        x=df_assets['일자'], y=df_assets[col_name], name=col_name,
                        marker_color=col_color, opacity=0.85,
                        hovertemplate=f'<b>{col_name}</b>: %{{y:,.0f}}원'
                    ), secondary_y=False)

            fig_line.add_trace(go.Scatter(
                x=df_assets['일자'], y=df_assets['증감액'], mode='lines+markers', name='전월대비 증감액',
                line=dict(color='#FF5252', width=3),
                hovertemplate='<b>전월대비 증감액</b>: %{y:+,.0f}원'
            ), secondary_y=True)

            fig_line.update_layout(
                barmode='stack',
                title=dict(
                    text=f"📈 월별 자산 구성 & 증감액 추이 {badge_html}", 
                    font=dict(size=17, color="#FFFFFF"),
                    x=0, y=0.98  # 👈 제목 위치 고정
                ),
                height=370,  # 👈 높이를 370으로 늘려 아래 공간을 시원하게 채움!
                margin=dict(l=10, r=10, t=65, b=25),  # 👈 상단 여백(t=65)을 넉넉히 주어 겹침 방지!
                hovermode="x unified",
                legend=dict(
                    orientation="h", 
                    yanchor="bottom", 
                    y=1.03,  # 👈 범례 위치를 위로 살짝 올려 제목/뱃지와 분리
                    xanchor="right", 
                    x=1.0
                ),
                xaxis=dict(type='category')
            )
            
            # 왼쪽 Y축 (0부터 자연스럽게 누적 막대가 보이도록 범위를 지정하지 않음)
            fig_line.update_yaxes(
                tickformat=",.0f",
                ticksuffix="원",
                secondary_y=False
            )
            
            fig_line.update_yaxes(
                tickformat=",.0f",
                ticksuffix="원",
                showgrid=False,
                secondary_y=True
            )
            st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("<hr style='border: 0; height: 1px; background: #2A2D32; margin: 25px 0;'>", unsafe_allow_html=True)

    # ====================================================
    # 🌟 [2번째 줄] 재테크 투자원금 + 현재금액 + 수익 현황 3카드
    # ====================================================
    r2_col1, r2_col2, r2_col3 = st.columns(3)

    with r2_col1:
        st.markdown(f"""
            <div style='{card_style}'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;'>
                    <span style='font-size: 18px; font-weight: bold; color: #FFFFFF;'>
                        <span style='color: #FFD600;'>●</span> 재테크 투자원금
                    </span>
                    <span style='font-size: 18px; font-weight: bold; color: #FFD600;'>
                        {int(total_tech_inv):,}원
                    </span>
                </div>
                <div style='margin-bottom: 12px;'>
                    <div style='color: #7986CB; font-size: 12px; font-weight: bold;'>국내주식</div>
                    <div style='font-size: 20px; font-weight: bold;'>{int(dom_inv):,}원</div>
                </div>
                <div style='margin-bottom: 12px;'>
                    <div style='color: #FF8A80; font-size: 12px; font-weight: bold;'>해외주식 + 달러 RP</div>
                    <div style='font-size: 20px; font-weight: bold;'>{int(ovs_inv):,}원</div>
                </div>
                <div style='margin-bottom: 12px;'>
                    <div style='color: #FFB74D; font-size: 12px; font-weight: bold;'>코인</div>
                    <div style='font-size: 20px; font-weight: bold;'>{int(coin_inv):,}원</div>
                </div>
                <div>
                    <div style='color: #81C784; font-size: 12px; font-weight: bold;'>연금</div>
                    <div style='font-size: 20px; font-weight: bold;'>{int(pen_inv):,}원</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with r2_col2:
        st.markdown(f"""
            <div style='{card_style}'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;'>
                    <span style='font-size: 18px; font-weight: bold; color: #FFFFFF;'>
                        <span style='color: #00E676;'>●</span> 재테크 현재금액
                    </span>
                    <span style='font-size: 18px; font-weight: bold; color: #00E676;'>
                        {int(total_tech_bal):,}원
                    </span>
                </div>
                <div style='margin-bottom: 12px;'>
                    <div style='color: #7986CB; font-size: 12px; font-weight: bold;'>국내주식</div>
                    <div style='font-size: 20px; font-weight: bold;'>{int(dom_bal):,}원</div>
                </div>
                <div style='margin-bottom: 12px;'>
                    <div style='color: #FF8A80; font-size: 12px; font-weight: bold;'>해외 + RP</div>
                    <div style='font-size: 20px; font-weight: bold;'>{int(ovs_bal):,}원</div>
                </div>
                <div style='margin-bottom: 12px;'>
                    <div style='color: #FFB74D; font-size: 12px; font-weight: bold;'>코인</div>
                    <div style='font-size: 20px; font-weight: bold;'>{int(coin_bal):,}원</div>
                </div>
                <div>
                    <div style='color: #81C784; font-size: 12px; font-weight: bold;'>연금</div>
                    <div style='font-size: 20px; font-weight: bold;'>{int(pen_bal):,}원</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with r2_col3:
        st.markdown(f"""
            <div style='{card_style}'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;'>
                    <span style='font-size: 18px; font-weight: bold; color: #FFFFFF;'>
                        <span style='color: #FF5252;'>●</span> 재테크 수익 현황
                    </span>
                    <span style='font-size: 16px; text-align: right;'>
                        {format_profit_text(total_tech_profit)} <span style='margin-left: 2px;'>{format_rate_color(total_tech_rate)}</span>
                    </span>
                </div>
                <div style='margin-bottom: 12px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span style='color: #7986CB; font-size: 12px; font-weight: bold;'>국내주식</span>
                        {format_rate_color(dom_rate)}
                    </div>
                    <div style='font-size: 20px; font-weight: bold;'>{format_profit_text(dom_profit)}</div>
                </div>
                <div style='margin-bottom: 12px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span style='color: #FF8A80; font-size: 12px; font-weight: bold;'>해외주식</span>
                        {format_rate_color(ovs_rate)}
                    </div>
                    <div style='font-size: 20px; font-weight: bold;'>{format_profit_text(ovs_profit)}</div>
                </div>
                <div style='margin-bottom: 12px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span style='color: #FFB74D; font-size: 12px; font-weight: bold;'>코인</span>
                        {format_rate_color(coin_rate)}
                    </div>
                    <div style='font-size: 20px; font-weight: bold;'>{format_profit_text(coin_profit)}</div>
                </div>
                <div>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span style='color: #81C784; font-size: 12px; font-weight: bold;'>연금</span>
                        {format_rate_color(pen_rate)}
                    </div>
                    <div style='font-size: 20px; font-weight: bold;'>{format_profit_text(pen_profit)}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border: 0; height: 1px; background: #2A2D32; margin: 25px 0;'>", unsafe_allow_html=True)

# ====================================================
    # 🌟 [3번째 줄] 월별 자산 현황 & Event 기록 상세 표
    # ====================================================
    if not df_assets.empty:
        st.markdown("<div style='font-size: 19px; font-weight: bold; color: #FFFFFF; margin-bottom: 15px;'><span style='color: #00E676;'>●</span> 월별 자산 현황 & Event 기록</div>", unsafe_allow_html=True)
        
        # 🌟 표 표시용 데이터는 최신 월이 맨 위로 오도록 내림차순(ascending=False) 정렬!
        df_assets_table = df_assets.sort_values(by='일자', ascending=False).reset_index(drop=True)
        
        df_assets_disp = df_assets_table[['일자', '총자산', '증감액', '증감율', 'Event', '부동산', 'Gold', '통장(현금성)', '적금/예금', '주식/코인/연금']].copy().set_index('일자')
        
        def color_total_diff(val):
            if isinstance(val, (int, float)):
                if val > 0: return 'color: #FF5252; font-weight: bold;'
                elif val < 0: return 'color: #448AFF; font-weight: bold;'
            return 'color: #8E9297;'

        styled_assets = df_assets_disp.style\
            .map(color_total_diff, subset=['증감액', '증감율'])\
            .format({
                '총자산': "{:,.0f}원", '증감액': "{:,.0f}원", '증감율': "{:.2f}%",
                '부동산': "{:,.0f}원", 'Gold': "{:,.0f}원", '통장(현금성)': "{:,.0f}원",
                '적금/예금': "{:,.0f}원", '주식/코인/연금': "{:,.0f}원"
            })
            
        st.dataframe(styled_assets, use_container_width=True, height=400)

# ----------------------------------------------------
# 메인 탭 1 : 📊 월별 손익
# ----------------------------------------------------
with top_tabs[1]:
    if account_dict:
        all_dates = []
        for acc_df in account_dict.values():
            all_dates.extend(acc_df['일자'].dropna().tolist())
        
        unique_dates = [d for d in list(dict.fromkeys(all_dates)) if pd.notna(d) and str(d).strip() != '' and str(d).lower() != 'nan']
        df_monthly_all = pd.DataFrame({'일자': unique_dates})
        
        for name, acc_df in account_dict.items():
            temp_df = acc_df[['일자', '월수익']].copy()
            temp_df['월수익'] = temp_df['월수익'].apply(clean_and_convert)
            temp_df.rename(columns={'월수익': name}, inplace=True)
            df_monthly_all = pd.merge(df_monthly_all, temp_df, on='일자', how='left')
            
        acc_cols = list(account_dict.keys())
        df_monthly_all[acc_cols] = df_monthly_all[acc_cols].fillna(0)
        
        # 🌟 날짜형 변환 후 내림차순(ascending=False) 정렬 -> 최신 월이 맨 위로!
        df_monthly_all['temp_dt'] = pd.to_datetime(df_monthly_all['일자'], format='%Y/%m', errors='coerce')
        df_monthly_all = df_monthly_all.dropna(subset=['temp_dt']).sort_values(by='temp_dt', ascending=False).drop(columns=['temp_dt']).reset_index(drop=True)
        
        df_monthly_all['월 총손익'] = df_monthly_all[acc_cols].sum(axis=1)
        
        cols_order = ['일자', '월 총손익'] + acc_cols
        df_monthly_all = df_monthly_all[cols_order]
        
        # 📈 차트는 왼쪽에서 오른쪽으로 시간 흐름대로 보여주기 위해 오래된 순(ascending=True) 재정렬
        chart_m_df = df_monthly_all.iloc[::-1].reset_index(drop=True)
        
        fig_m = go.Figure()
        for name in acc_cols:
            fig_m.add_trace(go.Bar(
                x=chart_m_df['일자'], 
                y=chart_m_df[name], 
                name=name,
                hovertemplate=f'<b>{name}</b>: %{{y:,.0f}}원'
            ))
            
        fig_m.update_layout(
            barmode='relative',
            height=430,
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            hovermode="x unified",
            xaxis=dict(type='category'),
            yaxis=dict(tickformat=",.0f", ticksuffix="원", zeroline=True, zerolinewidth=2, zerolinecolor='#666666')
        )
        
        st.plotly_chart(fig_m, use_container_width=True)
        
        st.markdown("<h4 style='margin-top:20px; margin-bottom:10px;'>📄 계좌별 월간 손익 상세 표</h4>", unsafe_allow_html=True)
        
        def color_total_profit(val):
            if isinstance(val, (int, float)):
                if val > 0: return 'color: #FF5252; font-weight: bold;'
                elif val < 0: return 'color: #448AFF; font-weight: bold;'
            return 'color: #8E9297; font-weight: normal;'

        def color_account_profit(val):
            if isinstance(val, (int, float)):
                if val > 0: return 'color: #FFFFFF; font-weight: normal;'
                elif val < 0: return 'color: #448AFF; font-weight: normal;'
            return 'color: #8E9297; font-weight: normal;'

        df_disp = df_monthly_all.copy().set_index('일자')
        
        styled_df = df_disp.style\
            .map(color_total_profit, subset=['월 총손익'])\
            .map(color_account_profit, subset=acc_cols)\
            .format("{:,.0f}원")
            
        st.dataframe(styled_df, use_container_width=True, height=480)
    else:
        st.error("통합 월별 손익 데이터를 가져올 수 없습니다.")

# ----------------------------------------------------
# 메인 탭 2 : 국내자산 영역
# ----------------------------------------------------
with top_tabs[2]:
    if df_dom_total is not None:
        display_summary(df_dom_total, is_total=True)
        st.markdown("<hr style='border: 0; height: 1px; background: #333333; margin: 10px 0 20px 0;'>", unsafe_allow_html=True)
        sub_tabs = st.tabs(["단기스윙", "단타연습", "장기스윙", "한투계좌", "SPC계좌"])
        for i, tab in enumerate(sub_tabs):
            with tab: render_account_tab(dom_accs[i], "")

# ----------------------------------------------------
# 메인 탭 3 : 해외자산 영역
# ----------------------------------------------------
with top_tabs[3]:
    if df_ovs_total is not None:
        display_summary(df_ovs_total, is_total=True)
        st.markdown("<hr style='border: 0; height: 1px; background: #333333; margin: 10px 0 20px 0;'>", unsafe_allow_html=True)
        tab_names = ["토스증권"]
        if len(ovs_accs) > 1: tab_names.append("SOXL Grid")
        if len(ovs_accs) > 2: tab_names.append("떨사오팔")
        sub_tabs = st.tabs(tab_names)
        for i, tab in enumerate(sub_tabs):
            with tab: render_account_tab(ovs_accs[i], "")

# ----------------------------------------------------
# 메인 탭 4 : 코인자산 영역
# ----------------------------------------------------
with top_tabs[4]:
    if df_coin_total is not None:
        display_summary(df_coin_total, is_total=True)
        st.markdown("<hr style='border: 0; height: 1px; background: #333333; margin: 10px 0 20px 0;'>", unsafe_allow_html=True)
        tab_names = ["테더자동"]
        if len(coin_accs) > 1: tab_names.append("비트겟")
        if len(coin_accs) > 2: tab_names.append("코인계좌 3")
        sub_tabs = st.tabs(tab_names)
        for i, tab in enumerate(sub_tabs):
            with tab: render_account_tab(coin_accs[i], "")

# ----------------------------------------------------
# 메인 탭 5 : 연금자산 영역
# ----------------------------------------------------
with top_tabs[5]:
    if df_pension_total is not None:
        display_summary(df_pension_total, is_total=True)
        st.markdown("<hr style='border: 0; height: 1px; background: #333333; margin: 10px 0 20px 0;'>", unsafe_allow_html=True)
        tab_names = ["개인연금"]
        if len(pen_accs) > 1: tab_names.append("IRP")
        if len(pen_accs) > 2: tab_names.append("퇴직연금")
        if len(pen_accs) > 3: tab_names.append("흥국생명")
        sub_tabs = st.tabs(tab_names)
        for i, tab in enumerate(sub_tabs):
            with tab: render_account_tab(pen_accs[i], "")
