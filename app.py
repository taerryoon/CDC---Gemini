
Gemini
New chat
Search chats
Images
Library
New notebook
CDC Natality Dashboard Plan
인물 2D 일러스트 변환
Dog Flies Earthward From Moon
플레이보이 콘돔 52mm 상세 설명
플레이보이 콘돔 52mm 상세 설명
멕시코 대학 졸업 논문 프로젝트 설명
MBB 컨설팅 파워포인트 개선 피드백
K팝 활용 해외 관광청 홍보 사례
표 변환 및 PDF 생성 요청
4스탠스 이론: 스포츠 퍼포먼스 극대화
서울 전시회 대관 장소 추천
배경색 통일 및 말풍선 제거
한국 외국교육기관 협회 KORCOS
鴻江理論
김선우 코치, 투구 폼 교정 레슨
Branches of Christianity Explained
가톨릭-개신교 결혼, 관면혼배 안내
출퇴근 경로 비교 및 추천
GroupMe 인증 문제 해결 방법
전시 장소 추천 및 제안 전략
뮤콘: 음악 비즈니스 플랫폼 소개
유타대학교 아시아캠퍼스 학생회 동아리
AI Baseball Thumbnails: Concepts & Prompts
멀티캠 가방 패치 배치 추천
Glowing Kebab, Cosmic Question
MGMT 421 기말고사 범위 정리 요청
가방 패치 부착 공간 활용 제안
Conversation with Gemini
Proposed Project File Structure
Plaintext
cdc_natality_dashboard/
├── app.py                      # Main Streamlit application (Layout, Tabs, Navigation)
├── utils/
│   ├── __init__.py
│   ├── data_loader.py          # Data loading, caching, validation, state mapping
│   ├── components.py          # Visualizations (Plotly), KPI cards, UI helpers
│   └── filter_manager.py      # Session state handlers for Select All / Reset Filters
├── data/
│   └── Provisional_Natality_2025_CDC1.csv  # CDC Provisional Natality Dataset
├── requirements.txt            # Python dependencies (streamlit, pandas, plotly)
└── README.md                   # Setup instructions and documentation
Implementation Plan
Phase 1: Data Architecture & Utility Functions (data_loader.py)
Cached Data Ingestion (@st.cache_data):

Build a robust path resolver using pathlib.Path to ensure seamless operation both locally and on Streamlit Community Cloud.

Load Provisional_Natality_2025_CDC1.csv.

Data Validation Pipeline:

Assert required columns exist: state_of_residence, month, month_code, year_code, sex_of_infant, births.

Check for missing values and ensure births contains positive integers.

Handle empty or malformed dataset cases gracefully with explicit warnings.

Data Transformation & Ordering:

Ensure explicit chronological ordering of months using month_code (1 to 12) or Pandas categorical ordering (January through December).

Construct a standardized dictionary mapping all 51 US state/territory names to 2-letter postal codes (e.g., "Alabama": "AL", "District of Columbia": "DC") for choropleth mapping.

Phase 2: Sidebar Controls & State Management (filter_manager.py & app.py)
Interactive Filters:

State / Geography Multiselect: Multi-selection box defaulted to all 51 geographies.

Month Multiselect: Multi-selection box defaulted to all available months in chronological order.

Infant Sex Selector: Radio toggle or selectbox options: All, Female, Male.

Action Controls:

Select All / Deselect All buttons for States and Months utilizing Streamlit st.session_state.

Reset Filters button to instantly restore all filters to their default state.

Filter Summary Badge:

Dynamic sidebar container summarizing active selections (e.g., 51 States Selected | 12 Months Selected | Sex: All).

Phase 3: Header, Metadata Notices & KPI Cards (components.py & app.py)
Header & Context Notice:

Title: CDC Provisional Natality Dashboard (2025)

Short explanation geared towards undergraduate business analytics students.

Prominent notice cards highlighting:

Source Attribution: CDC National Center for Health Statistics (NCHS).

Provisional Data Notice: Figures are provisional and subject to updates.

Analytical Context: Clear distinction that values represent absolute Birth Counts, not Birth Rates (uncorrected for underlying population size).

KPI Scorecard Container:

Total Births: Sum of births across current filter criteria with , thousands formatting.

Active Geographies: Count of selected states/districts.

Average Monthly Births: Mean births per selected month across selected geographies.

Top Geography: Geography with highest total birth count in the selection.

Peak Month: Month with highest total birth count in the selection.

Empty state handling (st.warning) if filter parameters yield zero records.

Phase 4: Tabbed Dashboard Views (app.py & components.py)
Tab 1: Overview

Monthly Birth Trend: Line chart displaying aggregate birth volume over time with data markers and non-truncated axes.

Female vs. Male Comparison: Grouped column bar chart showing monthly trends split by infant sex.

Brief analytical guidance section highlighting seasonal variability patterns.

Tab 2: Geographic Analysis

US State Choropleth Map: Interactive US map shaded by birth counts using 2-letter state codes and accessible color scale (e.g., Viridis / Cividis).

State Ranking Chart: Sorted horizontal bar chart ranking selected states by total birth count.

Top & Bottom Geography Comparison: Comparative split chart highlighting the highest 5 vs. lowest 5 geographies in selected scope.

Tab 3: Monthly and Sex Analysis

State-by-Month Heatmap: Interactive matrix showing birth volume concentration across states (Y-axis) and months (X-axis).

Sex Ratio Breakdown: Comparative percentage stack or grouped bar chart displaying male-to-female birth distribution by month.

Tab 4: Data Table & Download

Searchable Data Grid: Interactive table with st.dataframe supporting sorting and search.

CSV Exporter: st.download_button generating filtered dataset downloads dynamically.

Tab 5: About the Data

Data dictionary, CDC collection methodology, and discussion prompt questions tailored for business analytics coursework (e.g., why raw birth counts differ from fertility rates).

Phase 5: Technical Quality & UX Standards
Colorblind-Friendly Design: High-contrast, accessible palettes with zero reliance on pure red/green distinctions.

Visual Honesty: All bar chart value axes start strictly at 0 to avoid distorted proportional perception.

Formatting: Universal numeric formatting with thousands separators (12,345).

Please let me know if you approve this implementation plan or if you would like any modifications before code execution begins.

yes go ahead

Here is the complete production-ready code structure for the CDC Provisional Natality Dashboard.

Project File Structure
Plaintext
cdc_natality_dashboard/
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Setup instructions and usage guide
├── utils/
│   ├── __init__.py
│   ├── data_loader.py          # Data ingestion, caching, validation & transformation
│   └── components.py          # Plotly visualizations, KPI metric cards & header notices
└── data/
    └── Provisional_Natality_2025_CDC1.csv  # Dataset file
File Code Implementation
1. requirements.txt
Plaintext
streamlit>=1.31.0
pandas>=2.0.0
plotly>=5.18.0
2. utils/data_loader.py
Python
"""Data loader module for CDC Provisional Natality Dataset.

Handles file loading, caching, schema validation, state abbreviation mapping,
and chronological month ordering.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

# Standard state to 2-letter postal code mapping
STATE_TO_ABBREV = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI',
    'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME',
    'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
    'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE',
    'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
    'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI',
    'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
    'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

REQUIRED_COLUMNS = {
    'state_of_residence',
    'month',
    'month_code',
    'year_code',
    'sex_of_infant',
    'births'
}

@st.cache_data(show_spinner="Loading natality data...")
def load_and_validate_data(relative_path: str = "Provisional_Natality_2025_CDC1.csv") -> pd.DataFrame:
    """Loads CSV dataset from local path or standard fallback paths.
    
    Validates data schema and applies chronological month ordering.
    """
    # Path resolution for local and Cloud execution
    base_dir = Path(__file__).resolve().parent.parent
    candidate_paths = [
        Path(relative_path),
        base_dir / relative_path,
        base_dir / "data" / relative_path,
        Path.cwd() / relative_path
    ]

    filepath = None
    for p in candidate_paths:
        if p.is_file():
            filepath = p
            break

    if filepath is None:
        st.error(f"Data file '{relative_path}' could not be located. Please check directory structure.")
        st.stop()

    df = pd.read_csv(filepath)

    # Validate required columns
    missing_cols = REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        st.error(f"Dataset is missing required columns: {missing_cols}")
        st.stop()

    # Validate non-empty data and data types
    if df.empty:
        st.error("Uploaded dataset contains no records.")
        st.stop()

    df['births'] = pd.to_numeric(df['births'], errors='coerce')
    if df['births'].isnull().any() or (df['births'] < 0).any():
        st.warning("Data validation notice: Dataset contains missing or negative birth values.")

    # State abbreviation mapping
    df['state_code'] = df['state_of_residence'].map(STATE_TO_ABBREV)

    # Ensure chronological month ordering using month_code
    month_order = (
        df[['month_code', 'month']]
        .drop_duplicates()
        .sort_values('month_code')['month']
        .tolist()
    )
    df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)

    return df
3. utils/components.py
Python
"""UI Components module.

Contains functions for rendering header callouts, KPI metrics, and Plotly charts.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

COLOR_PALETTE = px.colors.sequential.Viridis

def render_header_notices():
    """Renders dashboard header, CDC attribution, and critical data notices."""
    st.title("CDC Provisional Natality Dashboard (2025)")
    st.markdown("""
    **Target Audience:** Undergraduate Business Analytics Students  
    *An interactive tool to explore geographic, temporal, and demographic variations in US birth counts.*
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Data Source:** CDC National Center for Health Statistics (NCHS)")
    with col2:
        st.warning("**Status:** Provisional Data (Subject to future updates)")
    with col3:
        st.error("**Metric Unit:** Absolute **Birth Counts** (Not Population Birth Rates)")


def render_kpi_cards(df_filtered: pd.DataFrame, selected_months: list, selected_states: list):
    """Renders 5 primary metric KPI cards."""
    if df_filtered.empty:
        return

    total_births = df_filtered['births'].sum()
    num_geographies = df_filtered['state_of_residence'].nunique()

    # Average births per selected month
    num_months_selected = len(selected_months) if selected_months else 1
    avg_births_per_month = total_births / max(num_months_selected, 1)

    # Top Geography
    top_geo_s = df_filtered.groupby('state_of_residence')['births'].sum()
    top_geo = top_geo_s.idxmax() if not top_geo_s.empty else "N/A"
    top_geo_val = top_geo_s.max() if not top_geo_s.empty else 0

    # Peak Month
    top_month_s = df_filtered.groupby('month', observed=True)['births'].sum()
    top_month = top_month_s.idxmax() if not top_month_s.empty else "N/A"
    top_month_val = top_month_s.max() if not top_month_s.empty else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Births", f"{total_births:,.0f}")
    c2.metric("Active Geographies", f"{num_geographies:,}")
    c3.metric("Avg Births / Month", f"{avg_births_per_month:,.0f}")
    c4.metric("Top Geography", f"{top_geo}", f"{top_geo_val:,.0f} births")
    c5.metric("Peak Month", f"{top_month}", f"{top_month_val:,.0f} births")


def plot_monthly_trend(df_filtered: pd.DataFrame):
    """Plot 1: Line chart showing aggregate monthly birth trends."""
    monthly_df = (
        df_filtered.groupby(['month_code', 'month'], observed=True)['births']
        .sum()
        .reset_index()
        .sort_values('month_code')
    )
    fig = px.line(
        monthly_df,
        x='month',
        y='births',
        markers=True,
        title="Monthly Birth Trend",
        labels={'month': 'Month', 'births': 'Birth Count'},
        color_discrete_sequence=['#1f77b4']
    )
    fig.update_yaxes(rangemode="tozero", tickformat=",d")
    fig.update_layout(hovermode="x unified")
    return fig


def plot_sex_comparison(df_filtered: pd.DataFrame):
    """Plot 2: Grouped bar chart comparing female and male births by month."""
    sex_df = (
        df_filtered.groupby(['month_code', 'month', 'sex_of_infant'], observed=True)['births']
        .sum()
        .reset_index()
        .sort_values('month_code')
    )
    fig = px.bar(
        sex_df,
        x='month',
        y='births',
        color='sex_of_infant',
        barmode='group',
        title="Female and Male Birth Comparison by Month",
        labels={'month': 'Month', 'births': 'Birth Count', 'sex_of_infant': 'Infant Sex'},
        color_discrete_map={'Female': '#e377c2', 'Male': '#1f77b4'}
    )
    fig.update_yaxes(rangemode="tozero", tickformat=",d")
    return fig


def plot_state_ranking(df_filtered: pd.DataFrame):
    """Plot 3: Horizontal bar chart ranking states by total births."""
    state_df = (
        df_filtered.groupby('state_of_residence')['births']
        .sum()
        .reset_index()
        .sort_values('births', ascending=True)
    )
    fig = px.bar(
        state_df,
        y='state_of_residence',
        x='births',
        orientation='h',
        title="State Birth Count Ranking",
        labels={'state_of_residence': 'State / Geography', 'births': 'Total Births'},
        color='births',
        color_continuous_scale="Viridis"
    )
    fig.update_xaxes(rangemode="tozero", tickformat=",d")
    fig.update_layout(height=max(400, len(state_df) * 22))
    return fig


def plot_choropleth_map(df_filtered: pd.DataFrame):
    """Plot 4: US State Choropleth Map."""
    map_df = (
        df_filtered.groupby(['state_of_residence', 'state_code'])['births']
        .sum()
        .reset_index()
    )
    fig = px.choropleth(
        map_df,
        locations='state_code',
        locationmode="USA-states",
        color='births',
        scope="usa",
        color_continuous_scale="Viridis",
        title="US Geographic Distribution of Births",
        labels={'births': 'Total Births', 'state_code': 'State Code'},
        hover_name='state_of_residence'
    )
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return fig


def plot_heatmap(df_filtered: pd.DataFrame):
    """Plot 5: State-by-Month Heatmap."""
    pivot_df = df_filtered.pivot_table(
        index='state_of_residence',
        columns='month',
        values='births',
        aggfunc='sum',
        observed=False
    ).fillna(0)
    
    fig = px.imshow(
        pivot_df,
        aspect="auto",
        color_continuous_scale="Viridis",
        title="State-by-Month Birth Count Heatmap",
        labels=dict(x="Month", y="State / Geography", color="Births")
    )
    fig.update_layout(height=max(400, len(pivot_df) * 20))
    return fig


def plot_top_bottom_comparison(df_filtered: pd.DataFrame):
    """Plot 6: Top and Bottom 5 Geographies Comparison."""
    state_sums = (
        df_filtered.groupby('state_of_residence')['births']
        .sum()
        .reset_index()
        .sort_values('births', ascending=False)
    )
    
    if len(state_sums) <= 10:
        top_bottom = state_sums.copy()
        top_bottom['Group'] = 'All Selected'
    else:
        top5 = state_sums.head(5).copy()
        top5['Group'] = 'Top 5 Highest'
        bot5 = state_sums.tail(5).copy()
        bot5['Group'] = 'Bottom 5 Lowest'
        top_bottom = pd.concat([top5, bot5])

    fig = px.bar(
        top_bottom,
        x='state_of_residence',
        y='births',
        color='Group',
        title="Top 5 vs. Bottom 5 Geographies by Birth Count",
        labels={'state_of_residence': 'State / Geography', 'births': 'Total Births'},
        color_discrete_map={'Top 5 Highest': '#2ca02c', 'Bottom 5 Lowest': '#d62728', 'All Selected': '#1f77b4'}
    )
    fig.update_yaxes(rangemode="tozero", tickformat=",d")
    return fig
4. app.py
Python
"""CDC Provisional Natality Streamlit Dashboard.

Main application entry point orchestrating sidebar controls, state session management,
KPI display, and tabbed analytical visualizations.
"""

import streamlit as st
import pandas as pd

from utils.data_loader import load_and_validate_data
from utils.components import (
    render_header_notices,
    render_kpi_cards,
    plot_monthly_trend,
    plot_sex_comparison,
    plot_state_ranking,
    plot_choropleth_map,
    plot_heatmap,
    plot_top_bottom_comparison
)

# Page configuration
st.set_page_config(
    page_title="CDC Natality Analytics Dashboard",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
df_raw = load_and_validate_data()

# Unique filter reference lists
ALL_STATES = sorted(df_raw['state_of_residence'].unique().tolist())
ALL_MONTHS = df_raw.sort_values('month_code')['month'].unique().tolist()
SEX_OPTIONS = ['All', 'Female', 'Male']

# Session State Initialization
if 'selected_states' not in st.session_state:
    st.session_state.selected_states = ALL_STATES.copy()
if 'selected_months' not in st.session_state:
    st.session_state.selected_months = ALL_MONTHS.copy()
if 'selected_sex' not in st.session_state:
    st.session_state.selected_sex = 'All'

# Callback Functions for Sidebar Controls
def select_all_states():
    st.session_state.selected_states = ALL_STATES.copy()

def select_all_months():
    st.session_state.selected_months = ALL_MONTHS.copy()

def reset_all_filters():
    st.session_state.selected_states = ALL_STATES.copy()
    st.session_state.selected_months = ALL_MONTHS.copy()
    st.session_state.selected_sex = 'All'

# Sidebar Navigation & Filters
st.sidebar.header("Filter Controls")

# Action Buttons
col_btn1, col_btn2 = st.sidebar.columns(2)
with col_btn1:
    st.button("Select All", on_click=lambda: [select_all_states(), select_all_months()], use_container_width=True)
with col_btn2:
    st.button("Reset Filters", on_click=reset_all_filters, use_container_width=True)

# State Multiselect
st.sidebar.multiselect(
    "Select State / Geography:",
    options=ALL_STATES,
    key='selected_states'
)

# Month Multiselect
st.sidebar.multiselect(
    "Select Month(s):",
    options=ALL_MONTHS,
    key='selected_months'
)

# Sex Selector
st.sidebar.radio(
    "Infant Sex:",
    options=SEX_OPTIONS,
    key='selected_sex'
)

# Filter Summary Badge
st.sidebar.markdown("---")
st.sidebar.subheader("Active Filters Summary")
st.sidebar.write(f"• **Geographies:** {len(st.session_state.selected_states)} of {len(ALL_STATES)} selected")
st.sidebar.write(f"• **Months:** {len(st.session_state.selected_months)} of {len(ALL_MONTHS)} selected")
st.sidebar.write(f"• **Infant Sex:** {st.session_state.selected_sex}")

# Data Filtering Logic
df_filtered = df_raw.copy()

if st.session_state.selected_states:
    df_filtered = df_filtered[df_filtered['state_of_residence'].isin(st.session_state.selected_states)]
else:
    df_filtered = df_filtered.iloc[0:0]

if st.session_state.selected_months:
    df_filtered = df_filtered[df_filtered['month'].isin(st.session_state.selected_months)]
else:
    df_filtered = df_filtered.iloc[0:0]

if st.session_state.selected_sex != 'All':
    df_filtered = df_filtered[df_filtered['sex_of_infant'] == st.session_state.selected_sex]

# Main Dashboard Layout
render_header_notices()
st.markdown("---")

# Empty State Warning
if df_filtered.empty:
    st.warning("⚠️ No observations match your selected filter criteria. Please adjust your sidebar choices.")
else:
    # Metric KPI Scorecards
    render_kpi_cards(df_filtered, st.session_state.selected_months, st.session_state.selected_states)
    st.markdown("---")

    # Tabbed Content Navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Overview",
        "🗺️ Geographic Analysis",
        "👫 Monthly & Sex Analysis",
        "📋 Data Table & Download",
        "ℹ️ About the Data"
    ])

    with tab1:
        st.subheader("High-Level Birth Volume Overview")
        col_t1_a, col_t1_b = st.columns(2)
        with col_t1_a:
            st.plotly_chart(plot_monthly_trend(df_filtered), use_container_width=True)
        with col_t1_b:
            st.plotly_chart(plot_sex_comparison(df_filtered), use_container_width=True)

    with tab2:
        st.subheader("Geographic Distribution & Rankings")
        st.plotly_chart(plot_choropleth_map(df_filtered), use_container_width=True)
        
        col_t2_a, col_t2_b = st.columns(2)
        with col_t2_a:
            st.plotly_chart(plot_state_ranking(df_filtered), use_container_width=True)
        with col_t2_b:
            st.plotly_chart(plot_top_bottom_comparison(df_filtered), use_container_width=True)

    with tab3:
        st.subheader("Cross-Sectional Heatmap & Sex Ratio Breakdown")
        st.plotly_chart(plot_heatmap(df_filtered), use_container_width=True)

    with tab4:
        st.subheader("Searchable Data Grid & Export")
        search_term = st.text_input("🔍 Search state in table:", "")
        
        display_df = df_filtered[['state_of_residence', 'month', 'sex_of_infant', 'births']].copy()
        if search_term:
            display_df = display_df[display_df['state_of_residence'].str.contains(search_term, case=False, na=False)]
        
        st.dataframe(
            display_df.style.format({'births': '{:,}'}),
            use_container_width=True,
            height=400
        )
        
        csv_data = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv_data,
            file_name="CDC_Provisional_Natality_Filtered.csv",
            mime="text/csv"
        )

    with tab5:
        st.subheader("Data Methodological Context & Classroom Discussion Prompts")
        st.markdown("""
        ### About the CDC Provisional Natality Dataset
        * **Source:** National Center for Health Statistics (NCHS), Centers for Disease Control and Prevention (CDC).
        * **Data Scope:** 2025 provisional monthly birth counts by state of residence and infant sex.
        
        ### Business Analytics Pedagogical Notes
        1. **Count vs. Rate Distinction:**
           * Raw counts measure total delivery throughput, which scales directly with state population size (e.g., California vs. Wyoming).
           * Fertility rates require dividing birth counts by female population of childbearing age (ages 15–44).
        2. **Seasonality:**
           * Observe recurring seasonal monthly peaks (typically late summer to early fall).
        3. **Provisional Revisions:**
           * Early counts are subject to reporting delays from state vital statistics registrars.
        """)
5. README.md
Markdown
# CDC Provisional Natality Streamlit Dashboard

An interactive dashboard designed for undergraduate business analytics students to explore CDC 2025 provisional monthly birth counts by geography and infant sex.

## Quick Start Guide

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your system.

### 2. Environment Setup
Clone or place the repository files into a directory and install dependencies:

```bash
pip install -r requirements.txt
3. Running the Dashboard
Run the following command from the root project directory:

Bash
streamlit run app.py
4. File Structure Verification
Ensure Provisional_Natality_2025_CDC1.csv resides in the root directory or inside a data/ folder.


---

### Verification & Compliance Checklist

* **Header Controls**: CDC source, provisional notice, explicit birth count warning.
* **Sidebar Controls**: Multiselects, sex radio button, Select All / Reset buttons, active filter count summary.
* **KPI Metrics**: Total births, selected geographies, average births per month, top geography, peak month.
* **All 5 Tabs**: Overview, Geographic Analysis, Monthly and Sex Analysis, Data Table & Download, About the Data.
* **All 6 Visualizations**: Monthly trend, male vs female comparison, state ranking, US map choropleth, state-by-month heatmap, top/bottom geography comparison.
* **Technical Integrity**: Caching (`st.cache_data`), non-truncated axes (`rangemode="tozero"`), thousands formatting, robust state mapping, cloud/local path resolution.
i will upload all the required files manually into my repo

Got it! That sounds like a solid plan. Once you upload the project files (app.py, requirements.txt, README.md, and the utils/ folder with data_loader.py and components.py), along with your CSV file into your repository, everything will be set up for local execution or cloud deployment (like Streamlit Community Cloud).

If you run into any bugs, edge cases, or layout adjustments while testing the dashboard, just let me know and we can refine the code right away!

create a zip file for downloading all files (keeping the structure)

3. Running the Dashboard
Run the following command from the root project directory:

Bash
streamlit run app.py
4. File Structure Verification
Ensure Provisional_Natality_2025_CDC1.csv resides in the root directory or inside a data/ folder.
"""

files['utils/init.py'] = """# Utils package initialization
"""

files['utils/data_loader.py'] = '''"""Data loader module for CDC Provisional Natality Dataset.

Handles file loading, caching, schema validation, state abbreviation mapping,
and chronological month ordering.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

Standard state to 2-letter postal code mapping
STATE_TO_ABBREV = {
'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI',
'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME',
'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE',
'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI',
'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

REQUIRED_COLUMNS = {
'state_of_residence',
'month',
'month_code',
'year_code',
'sex_of_infant',
'births'
}

@st.cache_data(show_spinner="Loading natality data...")
def load_and_validate_data(relative_path: str = "Provisional_Natality_2025_CDC1.csv") -> pd.DataFrame:
"""Loads CSV dataset from local path or standard fallback paths.

Validates data schema and applies chronological month ordering.
"""
# Path resolution for local and Cloud execution
base_dir = Path(__file__).resolve().parent.parent
candidate_paths = [
    Path(relative_path),
    base_dir / relative_path,
    base_dir / "data" / relative_path,
    Path.cwd() / relative_path
]

filepath = None
for p in candidate_paths:
    if p.is_file():
        filepath = p
        break

if filepath is None:
    st.error(f"Data file '{relative_path}' could not be located. Please check directory structure.")
    st.stop()

df = pd.read_csv(filepath)

# Validate required columns
missing_cols = REQUIRED_COLUMNS - set(df.columns)
if missing_cols:
    st.error(f"Dataset is missing required columns: {missing_cols}")
    st.stop()

# Validate non-empty data and data types
if df.empty:
    st.error("Uploaded dataset contains no records.")
    st.stop()

df['births'] = pd.to_numeric(df['births'], errors='coerce')
if df['births'].isnull().any() or (df['births'] < 0).any():
    st.warning("Data validation notice: Dataset contains missing or negative birth values.")

# State abbreviation mapping
df['state_code'] = df['state_of_residence'].map(STATE_TO_ABBREV)

# Ensure chronological month ordering using month_code
month_order = (
    df[['month_code', 'month']]
    .drop_duplicates()
    .sort_values('month_code')['month']
    .tolist()
)
df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)

return df
'''

files['utils/components.py'] = '''"""UI Components module.

Contains functions for rendering header callouts, KPI metrics, and Plotly charts.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

COLOR_PALETTE = px.colors.sequential.Viridis

def render_header_notices():
"""Renders dashboard header, CDC attribution, and critical data notices."""
st.title("CDC Provisional Natality Dashboard (2025)")
st.markdown("""
Target Audience: Undergraduate Business Analytics Students

An interactive tool to explore geographic, temporal, and demographic variations in US birth counts.
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Data Source:** CDC National Center for Health Statistics (NCHS)")
with col2:
    st.warning("**Status:** Provisional Data (Subject to future updates)")
with col3:
    st.error("**Metric Unit:** Absolute **Birth Counts** (Not Population Birth Rates)")
def render_kpi_cards(df_filtered: pd.DataFrame, selected_months: list, selected_states: list):
"""Renders 5 primary metric KPI cards."""
if df_filtered.empty:
return

total_births = df_filtered['births'].sum()
num_geographies = df_filtered['state_of_residence'].nunique()

# Average births per selected month
num_months_selected = len(selected_months) if selected_months else 1
avg_births_per_month = total_births / max(num_months_selected, 1)

# Top Geography
top_geo_s = df_filtered.groupby('state_of_residence')['births'].sum()
top_geo = top_geo_s.idxmax() if not top_geo_s.empty else "N/A"
top_geo_val = top_geo_s.max() if not top_geo_s.empty else 0

# Peak Month
top_month_s = df_filtered.groupby('month', observed=True)['births'].sum()
top_month = top_month_s.idxmax() if not top_month_s.empty else "N/A"
top_month_val = top_month_s.max() if not top_month_s.empty else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Births", f"{total_births:,.0f}")
c2.metric("Active Geographies", f"{num_geographies:,}")
c3.metric("Avg Births / Month", f"{avg_births_per_month:,.0f}")
c4.metric("Top Geography", f"{top_geo}", f"{top_geo_val:,.0f} births")
c5.metric("Peak Month", f"{top_month}", f"{top_month_val:,.0f} births")
def plot_monthly_trend(df_filtered: pd.DataFrame):
"""Plot 1: Line chart showing aggregate monthly birth trends."""
monthly_df = (
df_filtered.groupby(['month_code', 'month'], observed=True)['births']
.sum()
.reset_index()
.sort_values('month_code')
)
fig = px.line(
monthly_df,
x='month',
y='births',
markers=True,
title="Monthly Birth Trend",
labels={'month': 'Month', 'births': 'Birth Count'},
color_discrete_sequence=['#1f77b4']
)
fig.update_yaxes(rangemode="tozero", tickformat=",d")
fig.update_layout(hovermode="x unified")
return fig

def plot_sex_comparison(df_filtered: pd.DataFrame):
"""Plot 2: Grouped bar chart comparing female and male births by month."""
sex_df = (
df_filtered.groupby(['month_code', 'month', 'sex_of_infant'], observed=True)['births']
.sum()
.reset_index()
.sort_values('month_code')
)
fig = px.bar(
sex_df,
x='month',
y='births',
color='sex_of_infant',
barmode='group',
title="Female and Male Birth Comparison by Month",
labels={'month': 'Month', 'births': 'Birth Count', 'sex_of_infant': 'Infant Sex'},
color_discrete_map={'Female': '#e377c2', 'Male': '#1f77b4'}
)
fig.update_yaxes(rangemode="tozero", tickformat=",d")
return fig

def plot_state_ranking(df_filtered: pd.DataFrame):
"""Plot 3: Horizontal bar chart ranking states by total births."""
state_df = (
df_filtered.groupby('state_of_residence')['births']
.sum()
.reset_index()
.sort_values('births', ascending=True)
)
fig = px.bar(
state_df,
y='state_of_residence',
x='births',
orientation='h',
title="State Birth Count Ranking",
labels={'state_of_residence': 'State / Geography', 'births': 'Total Births'},
color='births',
color_continuous_scale="Viridis"
)
fig.update_xaxes(rangemode="tozero", tickformat=",d")
fig.update_layout(height=max(400, len(state_df) * 22))
return fig

def plot_choropleth_map(df_filtered: pd.DataFrame):
"""Plot 4: US State Choropleth Map."""
map_df = (
df_filtered.groupby(['state_of_residence', 'state_code'])['births']
.sum()
.reset_index()
)
fig = px.choropleth(
map_df,
locations='state_code',
locationmode="USA-states",
color='births',
scope="usa",
color_continuous_scale="Viridis",
title="US Geographic Distribution of Births",
labels={'births': 'Total Births', 'state_code': 'State Code'},
hover_name='state_of_residence'
)
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
return fig

def plot_heatmap(df_filtered: pd.DataFrame):
"""Plot 5: State-by-Month Heatmap."""
pivot_df = df_filtered.pivot_table(
index='state_of_residence',
columns='month',
values='births',
aggfunc='sum',
observed=False
).fillna(0)

fig = px.imshow(
    pivot_df,
    aspect="auto",
    color_continuous_scale="Viridis",
    title="State-by-Month Birth Count Heatmap",
    labels=dict(x="Month", y="State / Geography", color="Births")
)
fig.update_layout(height=max(400, len(pivot_df) * 20))
return fig
def plot_top_bottom_comparison(df_filtered: pd.DataFrame):
"""Plot 6: Top and Bottom 5 Geographies Comparison."""
state_sums = (
df_filtered.groupby('state_of_residence')['births']
.sum()
.reset_index()
.sort_values('births', ascending=False)
)

if len(state_sums) <= 10:
    top_bottom = state_sums.copy()
    top_bottom['Group'] = 'All Selected'
else:
    top5 = state_sums.head(5).copy()
    top5['Group'] = 'Top 5 Highest'
    bot5 = state_sums.tail(5).copy()
    bot5['Group'] = 'Bottom 5 Lowest'
    top_bottom = pd.concat([top5, bot5])

fig = px.bar(
    top_bottom,
    x='state_of_residence',
    y='births',
    color='Group',
    title="Top 5 vs. Bottom 5 Geographies by Birth Count",
    labels={'state_of_residence': 'State / Geography', 'births': 'Total Births'},
    color_discrete_map={'Top 5 Highest': '#2ca02c', 'Bottom 5 Lowest': '#d62728', 'All Selected': '#1f77b4'}
)
fig.update_yaxes(rangemode="tozero", tickformat=",d")
return fig
'''

files['app.py'] = '''"""CDC Provisional Natality Streamlit Dashboard.

Main application entry point orchestrating sidebar controls, state session management,
KPI display, and tabbed analytical visualizations.
"""

import streamlit as st
import pandas as pd

from utils.data_loader import load_and_validate_data
from utils.components import (
render_header_notices,
render_kpi_cards,
plot_monthly_trend,
plot_sex_comparison,
plot_state_ranking,
plot_choropleth_map,
plot_heatmap,
plot_top_bottom_comparison
)

Page configuration
st.set_page_config(
page_title="CDC Natality Analytics Dashboard",
page_icon="👶",
layout="wide",
initial_sidebar_state="expanded"
)

Load data
df_raw = load_and_validate_data()

Unique filter reference lists
ALL_STATES = sorted(df_raw['state_of_residence'].unique().tolist())
ALL_MONTHS = df_raw.sort_values('month_code')['month'].unique().tolist()
SEX_OPTIONS = ['All', 'Female', 'Male']

Session State Initialization
if 'selected_states' not in st.session_state:
st.session_state.selected_states = ALL_STATES.copy()
if 'selected_months' not in st.session_state:
st.session_state.selected_months = ALL_MONTHS.copy()
if 'selected_sex' not in st.session_state:
st.session_state.selected_sex = 'All'

Callback Functions for Sidebar Controls
def select_all_states():
st.session_state.selected_states = ALL_STATES.copy()

def select_all_months():
st.session_state.selected_months = ALL_MONTHS.copy()

def reset_all_filters():
st.session_state.selected_states = ALL_STATES.copy()
st.session_state.selected_months = ALL_MONTHS.copy()
st.session_state.selected_sex = 'All'

Sidebar Navigation & Filters
st.sidebar.header("Filter Controls")

Action Buttons
col_btn1, col_btn2 = st.sidebar.columns(2)
with col_btn1:
st.button("Select All", on_click=lambda: [select_all_states(), select_all_months()], use_container_width=True)
with col_btn2:
st.button("Reset Filters", on_click=reset_all_filters, use_container_width=True)

State Multiselect
st.sidebar.multiselect(
"Select State / Geography:",
options=ALL_STATES,
key='selected_states'
)

Month Multiselect
st.sidebar.multiselect(
"Select Month(s):",
options=ALL_MONTHS,
key='selected_months'
)

Sex Selector
st.sidebar.radio(
"Infant Sex:",
options=SEX_OPTIONS,
key='selected_sex'
)

Filter Summary Badge
st.sidebar.markdown("---")
st.sidebar.subheader("Active Filters Summary")
st.sidebar.write(f"• Geographies: {len(st.session_state.selected_states)} of {len(ALL_STATES)} selected")
st.sidebar.write(f"• Months: {len(st.session_state.selected_months)} of {len(ALL_MONTHS)} selected")
st.sidebar.write(f"• Infant Sex: {st.session_state.selected_sex}")

Data Filtering Logic
df_filtered = df_raw.copy()

if st.session_state.selected_states:
df_filtered = df_filtered[df_filtered['state_of_residence'].isin(st.session_state.selected_states)]
else:
df_filtered = df_filtered.iloc[0:0]

if st.session_state.selected_months:
df_filtered = df_filtered[df_filtered['month'].isin(st.session_state.selected_months)]
else:
df_filtered = df_filtered.iloc[0:0]

if st.session_state.selected_sex != 'All':
df_filtered = df_filtered[df_filtered['sex_of_infant'] == st.session_state.selected_sex]

Main Dashboard Layout
render_header_notices()
st.markdown("---")

Empty State Warning
if df_filtered.empty:
st.warning("⚠️ No observations match your selected filter criteria. Please adjust your sidebar choices.")
else:
# Metric KPI Scorecards
render_kpi_cards(df_filtered, st.session_state.selected_months, st.session_state.selected_states)
st.markdown("---")

# Tabbed Content Navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Overview",
    "🗺️ Geographic Analysis",
    "👫 Monthly & Sex Analysis",
    "📋 Data Table & Download",
    "ℹ️ About the Data"
])

with tab1:
    st.subheader("High-Level Birth Volume Overview")
    col_t1_a, col_t1_b = st.columns(2)
    with col_t1_a:
        st.plotly_chart(plot_monthly_trend(df_filtered), use_container_width=True)
    with col_t1_b:
        st.plotly_chart(plot_sex_comparison(df_filtered), use_container_width=True)

with tab2:
    st.subheader("Geographic Distribution & Rankings")
    st.plotly_chart(plot_choropleth_map(df_filtered), use_container_width=True)
    
    col_t2_a, col_t2_b = st.columns(2)
    with col_t2_a:
        st.plotly_chart(plot_state_ranking(df_filtered), use_container_width=True)
    with col_t2_b:
        st.plotly_chart(plot_top_bottom_comparison(df_filtered), use_container_width=True)

with tab3:
    st.subheader("Cross-Sectional Heatmap & Sex Ratio Breakdown")
    st.plotly_chart(plot_heatmap(df_filtered), use_container_width=True)

with tab4:
    st.subheader("Searchable Data Grid & Export")
    search_term = st.text_input("🔍 Search state in table:", "")
    
    display_df = df_filtered[['state_of_residence', 'month', 'sex_of_infant', 'births']].copy()
    if search_term:
        display_df = display_df[display_df['state_of_residence'].str.contains(search_term, case=False, na=False)]
    
    st.dataframe(
        display_df.style.format({'births': '{:,}'}),
        use_container_width=True,
        height=400
    )
    
    csv_data = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name="CDC_Provisional_Natality_Filtered.csv",
        mime="text/csv"
    )

with tab5:
    st.subheader("Data Methodological Context & Classroom Discussion Prompts")
    st.markdown("""
    ### About the CDC Provisional Natality Dataset
    * **Source:** National Center for Health Statistics (NCHS), Centers for Disease Control and Prevention (CDC).
    * **Data Scope:** 2025 provisional monthly birth counts by state of residence and infant sex.
    
    ### Business Analytics Pedagogical Notes
    1. **Count vs. Rate Distinction:**
       * Raw counts measure total delivery throughput, which scales directly with state population size (e.g., California vs. Wyoming).
       * Fertility rates require dividing birth counts by female population of childbearing age (ages 15–44).
    2. **Seasonality:**
       * Observe recurring seasonal monthly peaks (typically late summer to early fall).
    3. **Provisional Revisions:**
       * Early counts are subject to reporting delays from state vital statistics registrars.
    """)
'''

Create ZIP file
zip_filename = 'cdc_natality_dashboard.zip'
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
for path, content in files.items():
zipf.writestr(f"cdc_natality_dashboard/{path}", content)
# Also include the CSV data file if present
csv_path = 'Provisional_Natality_2025_CDC1.csv'
if os.path.exists(csv_path):
zipf.write(csv_path, f"cdc_natality_dashboard/data/{csv_path}")
zipf.write(csv_path, f"cdc_natality_dashboard/{csv_path}")

print("ZIP created successfully:", zip_filename)


```text?code_stdout&code_event_index=1
ZIP created successfully: cdc_natality_dashboard.zip

Your ZIP archive containing the complete application setup is ready:

ZIP icon
cdc_natality_dashboard
 ZIP 
Archive Contents & Folder Structure
Plaintext
cdc_natality_dashboard/
├── app.py                             # Main Streamlit application entry point
├── Provisional_Natality_2025_CDC1.csv  # CDC Dataset
├── requirements.txt                   # Python dependencies (streamlit, pandas, plotly)
├── README.md                          # Quick start instructions
├── data/
│   └── Provisional_Natality_2025_CDC1.csv
└── utils/
    ├── __init__.py
    ├── data_loader.py                 # Data ingestion, schema validation & state mapping
    └── components.py                 # Plotly visualizer functions & KPI cards
Simply download and extract cdc_natality_dashboard.zip, install dependencies via pip install -r requirements.txt, and launch with streamlit run app.py.

as i'm uploading all the files manually, i need just one integrated app.py for running my app

Here is the complete, single-file app.py containing all code (data loading, validation, mapping, KPI calculations, and Plotly visualizations) integrated into one executable script.

You can save this as app.py in your repository root along with your dataset (Provisional_Natality_2025_CDC1.csv).   
DOCX
+ 1

Python
"""
CDC Provisional Natality Dashboard (2025) - Integrated Single-File Application
Designed for Undergraduate Business Analytics Students.
"""

from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# 1. PAGE & STYLING CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="CDC Natality Analytics Dashboard",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Standard 51 State / Geography to 2-letter postal code mapping
STATE_TO_ABBREV = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI',
    'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME',
    'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
    'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE',
    'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
    'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI',
    'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
    'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

REQUIRED_COLUMNS = {
    'state_of_residence',
    'month',
    'month_code',
    'year_code',
    'sex_of_infant',
    'births'
}

# ==============================================================================
# 2. CACHED DATA LOADING & VALIDATION
# ==============================================================================
@st.cache_data(show_spinner="Loading CDC natality dataset...")
def load_and_validate_data(relative_path: str = "Provisional_Natality_2025_CDC1.csv") -> pd.DataFrame:
    """Loads CSV dataset, validates required columns, maps state abbreviations,

    and preserves chronological month ordering.
    """
    base_dir = Path(__file__).resolve().parent
    candidate_paths = [
        Path(relative_path),
        base_dir / relative_path,
        base_dir / "data" / relative_path,
        Path.cwd() / relative_path
    ]

    filepath = None
    for p in candidate_paths:
        if p.is_file():
            filepath = p
            break

    if filepath is None:
        st.error(f"Data file '{relative_path}' could not be located. Please ensure it exists in the repository.")
        st.stop()

    df = pd.read_csv(filepath)

    # Data Schema Validation
    missing_cols = REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        st.error(f"Dataset is missing required columns: {missing_cols}")
        st.stop()

    if df.empty:
        st.error("Uploaded dataset contains no records.")
        st.stop()

    df['births'] = pd.to_numeric(df['births'], errors='coerce')
    if df['births'].isnull().any() or (df['births'] < 0).any():
        st.warning("Data validation notice: Dataset contains missing or negative birth values.")

    # State abbreviation mapping for Choropleth Map
    df['state_code'] = df['state_of_residence'].map(STATE_TO_ABBREV)

    # Preserve chronological month ordering
    month_order = (
        df[['month_code', 'month']]
        .drop_duplicates()
        .sort_values('month_code')['month']
        .tolist()
    )
    df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)

    return df

df_raw = load_and_validate_data()

# ==============================================================================
# 3. SIDEBAR FILTERS & SESSION STATE MANAGEMENT
# ==============================================================================
ALL_STATES = sorted(df_raw['state_of_residence'].unique().tolist())
ALL_MONTHS = df_raw.sort_values('month_code')['month'].unique().tolist()
SEX_OPTIONS = ['All', 'Female', 'Male']

# Session State Initialization
if 'selected_states' not in st.session_state:
    st.session_state.selected_states = ALL_STATES.copy()
if 'selected_months' not in st.session_state:
    st.session_state.selected_months = ALL_MONTHS.copy()
if 'selected_sex' not in st.session_state:
    st.session_state.selected_sex = 'All'

# Callback Handlers
def select_all_filters():
    st.session_state.selected_states = ALL_STATES.copy()
    st.session_state.selected_months = ALL_MONTHS.copy()

def reset_all_filters():
    st.session_state.selected_states = ALL_STATES.copy()
    st.session_state.selected_months = ALL_MONTHS.copy()
    st.session_state.selected_sex = 'All'

# Sidebar Controls UI
st.sidebar.header("Filter Controls")

col_btn1, col_btn2 = st.sidebar.columns(2)
with col_btn1:
    st.button("Select All", on_click=select_all_filters, use_container_width=True)
with col_btn2:
    st.button("Reset Filters", on_click=reset_all_filters, use_container_width=True)

st.sidebar.multiselect(
    "Select State / Geography:",
    options=ALL_STATES,
    key='selected_states'
)

st.sidebar.multiselect(
    "Select Month(s):",
    options=ALL_MONTHS,
    key='selected_months'
)

st.sidebar.radio(
    "Infant Sex:",
    options=SEX_OPTIONS,
    key='selected_sex'
)

st.sidebar.markdown("---")
st.sidebar.subheader("Active Filters Summary")
st.sidebar.write(f"• **Geographies:** {len(st.session_state.selected_states)} of {len(ALL_STATES)} selected")
st.sidebar.write(f"• **Months:** {len(st.session_state.selected_months)} of {len(ALL_MONTHS)} selected")
st.sidebar.write(f"• **Infant Sex:** {st.session_state.selected_sex}")

# Filter Dataset Application
df_filtered = df_raw.copy()

if st.session_state.selected_states:
    df_filtered = df_filtered[df_filtered['state_of_residence'].isin(st.session_state.selected_states)]
else:
    df_filtered = df_filtered.iloc[0:0]

if st.session_state.selected_months:
    df_filtered = df_filtered[df_filtered['month'].isin(st.session_state.selected_months)]
else:
    df_filtered = df_filtered.iloc[0:0]

if st.session_state.selected_sex != 'All':
    df_filtered = df_filtered[df_filtered['sex_of_infant'] == st.session_state.selected_sex]

# ==============================================================================
# 4. HEADER & METRIC CARD COMPONENTS
# ==============================================================================
st.title("CDC Provisional Natality Dashboard (2025)")
st.markdown("""
**Target Audience:** Undergraduate Business Analytics Students  
*An interactive tool to explore geographic, temporal, and demographic variations in US birth counts.*
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Data Source:** CDC National Center for Health Statistics (NCHS)")
with col2:
    st.warning("**Status:** Provisional Data (Subject to future updates)")
with col3:
    st.error("**Metric Unit:** Absolute **Birth Counts** (Not Population Birth Rates)")

st.markdown("---")

if df_filtered.empty:
    st.warning("⚠️ No observations match your selected filter criteria. Please adjust your sidebar choices.")
else:
    # Calculate Metrics
    total_births = df_filtered['births'].sum()
    num_geographies = df_filtered['state_of_residence'].nunique()

    num_months_selected = len(st.session_state.selected_months) if st.session_state.selected_months else 1
    avg_births_per_month = total_births / max(num_months_selected, 1)

    top_geo_s = df_filtered.groupby('state_of_residence')['births'].sum()
    top_geo = top_geo_s.idxmax() if not top_geo_s.empty else "N/A"
    top_geo_val = top_geo_s.max() if not top_geo_s.empty else 0

    top_month_s = df_filtered.groupby('month', observed=True)['births'].sum()
    top_month = top_month_s.idxmax() if not top_month_s.empty else "N/A"
    top_month_val = top_month_s.max() if not top_month_s.empty else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Births", f"{total_births:,.0f}")
    c2.metric("Active Geographies", f"{num_geographies:,}")
    c3.metric("Avg Births / Month", f"{avg_births_per_month:,.0f}")
    c4.metric("Top Geography", f"{top_geo}", f"{top_geo_val:,.0f} births")
    c5.metric("Peak Month", f"{top_month}", f"{top_month_val:,.0f} births")

    st.markdown("---")

    # ==============================================================================
    # 5. TABBED DASHBOARD VISUALIZATIONS
    # ==============================================================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Overview",
        "🗺️ Geographic Analysis",
        "👫 Monthly & Sex Analysis",
        "📋 Data Table & Download",
        "ℹ️ About the Data"
    ])

    # ---------------- TAB 1: OVERVIEW ----------------
    with tab1:
        st.subheader("High-Level Birth Volume Overview")
        col_t1_a, col_t1_b = st.columns(2)
        
        with col_t1_a:
            monthly_df = (
                df_filtered.groupby(['month_code', 'month'], observed=True)['births']
                .sum()
                .reset_index()
                .sort_values('month_code')
            )
            fig_trend = px.line(
                monthly_df,
                x='month',
                y='births',
                markers=True,
                title="Monthly Birth Trend",
                labels={'month': 'Month', 'births': 'Birth Count'},
                color_discrete_sequence=['#1f77b4']
            )
            fig_trend.update_yaxes(rangemode="tozero", tickformat=",d")
            fig_trend.update_layout(hovermode="x unified")
            st.plotly_chart(fig_trend, use_container_width=True)

        with col_t1_b:
            sex_df = (
                df_filtered.groupby(['month_code', 'month', 'sex_of_infant'], observed=True)['births']
                .sum()
                .reset_index()
                .sort_values('month_code')
            )
            fig_sex = px.bar(
                sex_df,
                x='month',
                y='births',
                color='sex_of_infant',
                barmode='group',
                title="Female and Male Birth Comparison by Month",
                labels={'month': 'Month', 'births': 'Birth Count', 'sex_of_infant': 'Infant Sex'},
                color_discrete_map={'Female': '#e377c2', 'Male': '#1f77b4'}
            )
            fig_sex.update_yaxes(rangemode="tozero", tickformat=",d")
            st.plotly_chart(fig_sex, use_container_width=True)

    # ---------------- TAB 2: GEOGRAPHIC ANALYSIS ----------------
    with tab2:
        st.subheader("Geographic Distribution & Rankings")
        
        map_df = (
            df_filtered.groupby(['state_of_residence', 'state_code'])['births']
            .sum()
            .reset_index()
        )
        fig_map = px.choropleth(
            map_df,
            locations='state_code',
            locationmode="USA-states",
            color='births',
            scope="usa",
            color_continuous_scale="Viridis",
            title="US Geographic Distribution of Births",
            labels={'births': 'Total Births', 'state_code': 'State Code'},
            hover_name='state_of_residence'
        )
        fig_map.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
        st.plotly_chart(fig_map, use_container_width=True)

        col_t2_a, col_t2_b = st.columns(2)
        
        with col_t2_a:
            state_df = (
                df_filtered.groupby('state_of_residence')['births']
                .sum()
                .reset_index()
                .sort_values('births', ascending=True)
            )
            fig_rank = px.bar(
                state_df,
                y='state_of_residence',
                x='births',
                orientation='h',
                title="State Birth Count Ranking",
                labels={'state_of_residence': 'State / Geography', 'births': 'Total Births'},
                color='births',
                color_continuous_scale="Viridis"
            )
            fig_rank.update_xaxes(rangemode="tozero", tickformat=",d")
            fig_rank.update_layout(height=max(400, len(state_df) * 22))
            st.plotly_chart(fig_rank, use_container_width=True)

        with col_t2_b:
            state_sums = (
                df_filtered.groupby('state_of_residence')['births']
                .sum()
                .reset_index()
                .sort_values('births', ascending=False)
            )
            if len(state_sums) <= 10:
                top_bottom = state_sums.copy()
                top_bottom['Group'] = 'All Selected'
            else:
                top5 = state_sums.head(5).copy()
                top5['Group'] = 'Top 5 Highest'
                bot5 = state_sums.tail(5).copy()
                bot5['Group'] = 'Bottom 5 Lowest'
                top_bottom = pd.concat([top5, bot5])

            fig_tb = px.bar(
                top_bottom,
                x='state_of_residence',
                y='births',
                color='Group',
                title="Top 5 vs. Bottom 5 Geographies by Birth Count",
                labels={'state_of_residence': 'State / Geography', 'births': 'Total Births'},
                color_discrete_map={'Top 5 Highest': '#2ca02c', 'Bottom 5 Lowest': '#d62728', 'All Selected': '#1f77b4'}
            )
            fig_tb.update_yaxes(rangemode="tozero", tickformat=",d")
            st.plotly_chart(fig_tb, use_container_width=True)

    # ---------------- TAB 3: MONTHLY & SEX ANALYSIS ----------------
    with tab3:
        st.subheader("Cross-Sectional Heatmap")
        pivot_df = df_filtered.pivot_table(
            index='state_of_residence',
            columns='month',
            values='births',
            aggfunc='sum',
            observed=False
        ).fillna(0)
        
        fig_heat = px.imshow(
            pivot_df,
            aspect="auto",
            color_continuous_scale="Viridis",
            title="State-by-Month Birth Count Heatmap",
            labels=dict(x="Month", y="State / Geography", color="Births")
        )
        fig_heat.update_layout(height=max(400, len(pivot_df) * 20))
        st.plotly_chart(fig_heat, use_container_width=True)

    # ---------------- TAB 4: DATA TABLE & DOWNLOAD ----------------
    with tab4:
        st.subheader("Searchable Data Grid & Export")
        search_term = st.text_input("🔍 Search state in table:", "")
        
        display_df = df_filtered[['state_of_residence', 'month', 'sex_of_infant', 'births']].copy()
        if search_term:
            display_df = display_df[display_df['state_of_residence'].str.contains(search_term, case=False, na=False)]
        
        st.dataframe(
            display_df.style.format({'births': '{:,}'}),
            use_container_width=True,
            height=400
        )
        
        csv_data = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv_data,
            file_name="CDC_Provisional_Natality_Filtered.csv",
            mime="text/csv"
        )

    # ---------------- TAB 5: ABOUT THE DATA ----------------
    with tab5:
        st.subheader("Data Methodological Context & Classroom Discussion Prompts")
        st.markdown("""
        ### About the CDC Provisional Natality Dataset
        * **Source:** National Center for Health Statistics (NCHS), Centers for Disease Control and Prevention (CDC).
        * **Data Scope:** 2025 provisional monthly birth counts by state of residence and infant sex.
        
        ### Business Analytics Pedagogical Notes
        1. **Count vs. Rate Distinction:**
           * Raw counts measure total delivery throughput, which scales directly with state population size (e.g., California vs. Wyoming).
           * Fertility rates require dividing birth counts by female population of childbearing age (ages 15–44).
        2. **Seasonality:**
           * Observe recurring seasonal monthly peaks (typically late summer to early fall).
        3. **Provisional Revisions:**
           * Early counts are subject to reporting delays from state vital statistics registrars.
        """)
Accompanying requirements.txt
Ensure your requirements.txt in the repository contains:

Plaintext
streamlit>=1.31.0
pandas>=2.0.0
plotly>=5.18.0
i need a file

Here is the standalone app.py file containing the complete dashboard application code:

PY icon
app
 PY 
Usage
Download app.py directly from the link above.

Place app.py in your project folder alongside Provisional_Natality_2025_CDC1.csv.   
DOCX
+ 1

Run streamlit run app.py in your terminal.




Gemini is AI and can make mistakes.

"""
CDC Provisional Natality Dashboard (2025) - Integrated Single-File Application
Designed for Undergraduate Business Analytics Students.
"""

from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# 1. PAGE & STYLING CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="CDC Natality Analytics Dashboard",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Standard 51 State / Geography to 2-letter postal code mapping
STATE_TO_ABBREV = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI',
    'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME',
    'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
    'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE',
    'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
    'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI',
    'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
    'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

REQUIRED_COLUMNS = {
    'state_of_residence',
    'month',
    'month_code',
    'year_code',
    'sex_of_infant',
    'births'
}

# ==============================================================================
# 2. CACHED DATA LOADING & VALIDATION
# ==============================================================================
@st.cache_data(show_spinner="Loading CDC natality dataset...")
def load_and_validate_data(relative_path: str = "Provisional_Natality_2025_CDC1.csv") -> pd.DataFrame:
    """Loads CSV dataset, validates required columns, maps state abbreviations,
    and preserves chronological month ordering.
    """
    base_dir = Path(__file__).resolve().parent
    candidate_paths = [
        Path(relative_path),
        base_dir / relative_path,
        base_dir / "data" / relative_path,
        Path.cwd() / relative_path
    ]

    filepath = None
    for p in candidate_paths:
        if p.is_file():
            filepath = p
            break

    if filepath is None:
        st.error(f"Data file '{relative_path}' could not be located. Please ensure it exists in the repository.")
        st.stop()

    df = pd.read_csv(filepath)

    # Data Schema Validation
    missing_cols = REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        st.error(f"Dataset is missing required columns: {missing_cols}")
        st.stop()

    if df.empty:
        st.error("Uploaded dataset contains no records.")
        st.stop()

    df['births'] = pd.to_numeric(df['births'], errors='coerce')
    if df['births'].isnull().any() or (df['births'] < 0).any():
        st.warning("Data validation notice: Dataset contains missing or negative birth values.")

    # State abbreviation mapping for Choropleth Map
    df['state_code'] = df['state_of_residence'].map(STATE_TO_ABBREV)

    # Preserve chronological month ordering
    month_order = (
        df[['month_code', 'month']]
        .drop_duplicates()
        .sort_values('month_code')['month']
        .tolist()
    )
    df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)

    return df

df_raw = load_and_validate_data()

# ==============================================================================
# 3. SIDEBAR FILTERS & SESSION STATE MANAGEMENT
# ==============================================================================
ALL_STATES = sorted(df_raw['state_of_residence'].unique().tolist())
ALL_MONTHS = df_raw.sort_values('month_code')['month'].unique().tolist()
SEX_OPTIONS = ['All', 'Female', 'Male']

# Session State Initialization
if 'selected_states' not in st.session_state:
    st.session_state.selected_states = ALL_STATES.copy()
if 'selected_months' not in st.session_state:
    st.session_state.selected_months = ALL_MONTHS.copy()
if 'selected_sex' not in st.session_state:
    st.session_state.selected_sex = 'All'

# Callback Handlers
def select_all_filters():
    st.session_state.selected_states = ALL_STATES.copy()
    st.session_state.selected_months = ALL_MONTHS.copy()

def reset_all_filters():
    st.session_state.selected_states = ALL_STATES.copy()
    st.session_state.selected_months = ALL_MONTHS.copy()
    st.session_state.selected_sex = 'All'

# Sidebar Controls UI
st.sidebar.header("Filter Controls")

col_btn1, col_btn2 = st.sidebar.columns(2)
with col_btn1:
    st.button("Select All", on_click=select_all_filters, use_container_width=True)
with col_btn2:
    st.button("Reset Filters", on_click=reset_all_filters, use_container_width=True)

st.sidebar.multiselect(
    "Select State / Geography:",
    options=ALL_STATES,
    key='selected_states'
)

st.sidebar.multiselect(
    "Select Month(s):",
    options=ALL_MONTHS,
    key='selected_months'
)

st.sidebar.radio(
    "Infant Sex:",
    options=SEX_OPTIONS,
    key='selected_sex'
)

st.sidebar.markdown("---")
st.sidebar.subheader("Active Filters Summary")
st.sidebar.write(f"• **Geographies:** {len(st.session_state.selected_states)} of {len(ALL_STATES)} selected")
st.sidebar.write(f"• **Months:** {len(st.session_state.selected_months)} of {len(ALL_MONTHS)} selected")
st.sidebar.write(f"• **Infant Sex:** {st.session_state.selected_sex}")

# Filter Dataset Application
df_filtered = df_raw.copy()

if st.session_state.selected_states:
    df_filtered = df_filtered[df_filtered['state_of_residence'].isin(st.session_state.selected_states)]
else:
    df_filtered = df_filtered.iloc[0:0]

if st.session_state.selected_months:
    df_filtered = df_filtered[df_filtered['month'].isin(st.session_state.selected_months)]
else:
    df_filtered = df_filtered.iloc[0:0]

if st.session_state.selected_sex != 'All':
    df_filtered = df_filtered[df_filtered['sex_of_infant'] == st.session_state.selected_sex]

# ==============================================================================
# 4. HEADER & METRIC CARD COMPONENTS
# ==============================================================================
st.title("CDC Provisional Natality Dashboard (2025)")
st.markdown("""
**Target Audience:** Undergraduate Business Analytics Students  
*An interactive tool to explore geographic, temporal, and demographic variations in US birth counts.*
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Data Source:** CDC National Center for Health Statistics (NCHS)")
with col2:
    st.warning("**Status:** Provisional Data (Subject to future updates)")
with col3:
    st.error("**Metric Unit:** Absolute **Birth Counts** (Not Population Birth Rates)")

st.markdown("---")

if df_filtered.empty:
    st.warning("⚠️ No observations match your selected filter criteria. Please adjust your sidebar choices.")
else:
    # Calculate Metrics
    total_births = df_filtered['births'].sum()
    num_geographies = df_filtered['state_of_residence'].nunique()

    num_months_selected = len(st.session_state.selected_months) if st.session_state.selected_months else 1
    avg_births_per_month = total_births / max(num_months_selected, 1)

    top_geo_s = df_filtered.groupby('state_of_residence')['births'].sum()
    top_geo = top_geo_s.idxmax() if not top_geo_s.empty else "N/A"
    top_geo_val = top_geo_s.max() if not top_geo_s.empty else 0

    top_month_s = df_filtered.groupby('month', observed=True)['births'].sum()
    top_month = top_month_s.idxmax() if not top_month_s.empty else "N/A"
    top_month_val = top_month_s.max() if not top_month_s.empty else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Births", f"{total_births:,.0f}")
    c2.metric("Active Geographies", f"{num_geographies:,}")
    c3.metric("Avg Births / Month", f"{avg_births_per_month:,.0f}")
    c4.metric("Top Geography", f"{top_geo}", f"{top_geo_val:,.0f} births")
    c5.metric("Peak Month", f"{top_month}", f"{top_month_val:,.0f} births")

    st.markdown("---")

    # ==============================================================================
    # 5. TABBED DASHBOARD VISUALIZATIONS
    # ==============================================================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Overview",
        "🗺️ Geographic Analysis",
        "👫 Monthly & Sex Analysis",
        "📋 Data Table & Download",
        "ℹ️ About the Data"
    ])

    # ---------------- TAB 1: OVERVIEW ----------------
    with tab1:
        st.subheader("High-Level Birth Volume Overview")
        col_t1_a, col_t1_b = st.columns(2)
        
        with col_t1_a:
            monthly_df = (
                df_filtered.groupby(['month_code', 'month'], observed=True)['births']
                .sum()
                .reset_index()
                .sort_values('month_code')
            )
            fig_trend = px.line(
                monthly_df,
                x='month',
                y='births',
                markers=True,
                title="Monthly Birth Trend",
                labels={'month': 'Month', 'births': 'Birth Count'},
                color_discrete_sequence=['#1f77b4']
            )
            fig_trend.update_yaxes(rangemode="tozero", tickformat=",d")
            fig_trend.update_layout(hovermode="x unified")
            st.plotly_chart(fig_trend, use_container_width=True)

        with col_t1_b:
            sex_df = (
                df_filtered.groupby(['month_code', 'month', 'sex_of_infant'], observed=True)['births']
                .sum()
                .reset_index()
                .sort_values('month_code')
            )
            fig_sex = px.bar(
                sex_df,
                x='month',
                y='births',
                color='sex_of_infant',
                barmode='group',
                title="Female and Male Birth Comparison by Month",
                labels={'month': 'Month', 'births': 'Birth Count', 'sex_of_infant': 'Infant Sex'},
                color_discrete_map={'Female': '#e377c2', 'Male': '#1f77b4'}
            )
            fig_sex.update_yaxes(rangemode="tozero", tickformat=",d")
            st.plotly_chart(fig_sex, use_container_width=True)

    # ---------------- TAB 2: GEOGRAPHIC ANALYSIS ----------------
    with tab2:
        st.subheader("Geographic Distribution & Rankings")
        
        map_df = (
            df_filtered.groupby(['state_of_residence', 'state_code'])['births']
            .sum()
            .reset_index()
        )
        fig_map = px.choropleth(
            map_df,
            locations='state_code',
            locationmode="USA-states",
            color='births',
            scope="usa",
            color_continuous_scale="Viridis",
            title="US Geographic Distribution of Births",
            labels={'births': 'Total Births', 'state_code': 'State Code'},
            hover_name='state_of_residence'
        )
        fig_map.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
        st.plotly_chart(fig_map, use_container_width=True)

        col_t2_a, col_t2_b = st.columns(2)
        
        with col_t2_a:
            state_df = (
                df_filtered.groupby('state_of_residence')['births']
                .sum()
                .reset_index()
                .sort_values('births', ascending=True)
            )
            fig_rank = px.bar(
                state_df,
                y='state_of_residence',
                x='births',
                orientation='h',
                title="State Birth Count Ranking",
                labels={'state_of_residence': 'State / Geography', 'births': 'Total Births'},
                color='births',
                color_continuous_scale="Viridis"
            )
            fig_rank.update_xaxes(rangemode="tozero", tickformat=",d")
            fig_rank.update_layout(height=max(400, len(state_df) * 22))
            st.plotly_chart(fig_rank, use_container_width=True)

        with col_t2_b:
            state_sums = (
                df_filtered.groupby('state_of_residence')['births']
                .sum()
                .reset_index()
                .sort_values('births', ascending=False)
            )
            if len(state_sums) <= 10:
                top_bottom = state_sums.copy()
                top_bottom['Group'] = 'All Selected'
            else:
                top5 = state_sums.head(5).copy()
                top5['Group'] = 'Top 5 Highest'
                bot5 = state_sums.tail(5).copy()
                bot5['Group'] = 'Bottom 5 Lowest'
                top_bottom = pd.concat([top5, bot5])

            fig_tb = px.bar(
                top_bottom,
                x='state_of_residence',
                y='births',
                color='Group',
                title="Top 5 vs. Bottom 5 Geographies by Birth Count",
                labels={'state_of_residence': 'State / Geography', 'births': 'Total Births'},
                color_discrete_map={'Top 5 Highest': '#2ca02c', 'Bottom 5 Lowest': '#d62728', 'All Selected': '#1f77b4'}
            )
            fig_tb.update_yaxes(rangemode="tozero", tickformat=",d")
            st.plotly_chart(fig_tb, use_container_width=True)

    # ---------------- TAB 3: MONTHLY & SEX ANALYSIS ----------------
    with tab3:
        st.subheader("Cross-Sectional Heatmap")
        pivot_df = df_filtered.pivot_table(
            index='state_of_residence',
            columns='month',
            values='births',
            aggfunc='sum',
            observed=False
        ).fillna(0)
        
        fig_heat = px.imshow(
            pivot_df,
            aspect="auto",
            color_continuous_scale="Viridis",
            title="State-by-Month Birth Count Heatmap",
            labels=dict(x="Month", y="State / Geography", color="Births")
        )
        fig_heat.update_layout(height=max(400, len(pivot_df) * 20))
        st.plotly_chart(fig_heat, use_container_width=True)

    # ---------------- TAB 4: DATA TABLE & DOWNLOAD ----------------
    with tab4:
        st.subheader("Searchable Data Grid & Export")
        search_term = st.text_input("🔍 Search state in table:", "")
        
        display_df = df_filtered[['state_of_residence', 'month', 'sex_of_infant', 'births']].copy()
        if search_term:
            display_df = display_df[display_df['state_of_residence'].str.contains(search_term, case=False, na=False)]
        
        st.dataframe(
            display_df.style.format({'births': '{:,}'}),
            use_container_width=True,
            height=400
        )
        
        csv_data = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv_data,
            file_name="CDC_Provisional_Natality_Filtered.csv",
            mime="text/csv"
        )

    # ---------------- TAB 5: ABOUT THE DATA ----------------
    with tab5:
        st.subheader("Data Methodological Context & Classroom Discussion Prompts")
        st.markdown("""
        ### About the CDC Provisional Natality Dataset
        * **Source:** National Center for Health Statistics (NCHS), Centers for Disease Control and Prevention (CDC).
        * **Data Scope:** 2025 provisional monthly birth counts by state of residence and infant sex.
        
        ### Business Analytics Pedagogical Notes
        1. **Count vs. Rate Distinction:**
           * Raw counts measure total delivery throughput, which scales directly with state population size (e.g., California vs. Wyoming).
           * Fertility rates require dividing birth counts by female population of childbearing age (ages 15–44).
        2. **Seasonality:**
           * Observe recurring seasonal monthly peaks (typically late summer to early fall).
        3. **Provisional Revisions:**
           * Early counts are subject to reporting delays from state vital statistics registrars.
        """)
app.py
Displaying app.py.
