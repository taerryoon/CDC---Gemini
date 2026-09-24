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
