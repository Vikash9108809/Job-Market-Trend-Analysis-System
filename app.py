import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Job Market Trend Analysis System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS (dark premium theme) ──────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #0a0e1a; color: #e2e8f0; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1629 0%, #1a1f3a 100%);
    border-right: 1px solid #1e2d4a;
}
section[data-testid="stSidebar"] * { color: #c8d6e5 !important; }

.metric-card {
    background: linear-gradient(135deg, #1a2540 0%, #0f1629 100%);
    border: 1px solid #2a3a5c;
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
}
.metric-card:hover { transform: translateY(-3px); border-color: #00d4ff; }
.metric-value { font-size: 2rem; font-weight: 700; color: #00d4ff; }
.metric-label { font-size: 0.85rem; color: #94a3b8; margin-top: 4px; }

.page-header {
    background: linear-gradient(135deg, #1e3a5f 0%, #0f1629 100%);
    border-left: 4px solid #00d4ff;
    border-radius: 0 12px 12px 0;
    padding: 16px 24px;
    margin-bottom: 24px;
}
.page-header h1 { font-size: 1.6rem; font-weight: 700; color: #fff; margin: 0; }
.page-header p  { font-size: 0.9rem; color: #94a3b8; margin: 4px 0 0 0; }

.job-card {
    background: linear-gradient(135deg, #1a2540 0%, #111827 100%);
    border: 1px solid #2a3a5c;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    transition: border-color 0.2s;
}
.job-card:hover { border-color: #7c3aed; }
.job-card h4 { color: #00d4ff; margin: 0 0 6px 0; font-size: 1rem; }
.job-card .meta { color: #94a3b8; font-size: 0.82rem; }
.job-card .score-bar { background:#1e2d4a; border-radius:6px; height:8px; margin-top:8px; }
.job-card .score-fill { background: linear-gradient(90deg,#7c3aed,#00d4ff); border-radius:6px; height:8px; }

.sidebar-brand {
    background: linear-gradient(135deg, #00d4ff22, #7c3aed22);
    border: 1px solid #00d4ff44;
    border-radius: 12px;
    padding: 14px 16px;
    text-align: center;
    margin-bottom: 20px;
}
.sidebar-brand h2 { font-size: 1rem; font-weight: 700; color: #00d4ff !important; margin: 0; }
.sidebar-brand p  { font-size: 0.7rem; color: #94a3b8 !important; margin: 4px 0 0 0; }

div[data-testid="stMetric"] label { color: #94a3b8 !important; }
div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #00d4ff !important; font-size: 1.8rem !important; }

/* Custom Sidebar Navigation Button Styles */
div[data-testid="stSidebar"] button {
    display: flex;
    justify-content: flex-start !important;
    align-items: center;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    transition: all 0.2s ease-in-out !important;
    margin-bottom: 6px !important;
    border: 1px solid transparent !important;
}

/* Inactive button tab style */
div[data-testid="stSidebar"] button[kind="secondary"] {
    background-color: transparent !important;
    color: #94a3b8 !important;
    border: 1px solid #1e2d4a !important;
}
div[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background-color: #1e2d4a !important;
    color: #00d4ff !important;
    border-color: #00d4ff55 !important;
    transform: translateX(4px);
}

/* Active button tab style */
div[data-testid="stSidebar"] button[kind="primary"] {
    background: linear-gradient(90deg, #7c3aed 0%, #00d4ff 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 14px 0 rgba(0, 212, 255, 0.3) !important;
    border: none !important;
}
div[data-testid="stSidebar"] button[kind="primary"]:hover {
    transform: scale(1.02);
}

/* Style widget labels to be crisp white in dark theme */
label, 
div[data-testid="stWidgetLabel"] p, 
div[data-testid="stWidgetLabel"] label,
label[data-testid="stWidgetLabel"],
div[data-testid="stExpander"] p,
span[data-testid="stHeader"] {
    color: #ffffff !important;
}

/* Specific class overrides for streamlit selectbox, text input, slider and multi-select labels */
div[data-testid="stSelectbox"] label,
div[data-testid="stMultiSelect"] label,
div[data-testid="stSlider"] label,
div[data-testid="stTextInput"] label {
    color: #ffffff !important;
}

.stDataFrame { background: #111827 !important; border-radius: 8px !important; }

/* Custom Insights Style */
.insight-box {
    background: linear-gradient(135deg, #111827 0%, #1e293b 100%);
    border: 1px solid #2a3a5c;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 24px;
}
.insight-box h3 { margin-top: 0; color: #00d4ff; font-size: 1.25rem; font-weight: 600; }
.insight-box ul { margin: 0; padding-left: 20px; color: #e2e8f0; line-height: 1.6; }
.insight-box li { margin-bottom: 8px; }
.insight-box li b { color: #00d4ff; }
</style>
""", unsafe_allow_html=True)

# ── Colour palette for charts ─────────────────────────────────────────────────
COLORS = ["#00d4ff","#7c3aed","#06b6d4","#8b5cf6","#0ea5e9","#6366f1","#22d3ee","#a78bfa"]
CHART_LAYOUT = dict(
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font=dict(family="Inter", color="#e2e8f0"),
    title_font=dict(size=16, color="#fff"),
    legend=dict(bgcolor="#1a2540", bordercolor="#2a3a5c"),
    margin=dict(l=40, r=20, t=50, b=40),
    coloraxis_colorbar=dict(tickfont=dict(color="#e2e8f0")),
    xaxis=dict(gridcolor="#1e2d4a", linecolor="#2a3a5c", tickfont=dict(color="#94a3b8")),
    yaxis=dict(gridcolor="#1e2d4a", linecolor="#2a3a5c", tickfont=dict(color="#94a3b8")),
)

def style_fig(fig, height=450):
    fig.update_layout(**CHART_LAYOUT, height=height)
    return fig

# ── Data loading (optimized with cache_data) ──────────────────────────────────
DATA_PATH       = "data/processed/jobs_cleaned.parquet"
TOP_SKILLS_PATH = "data/processed/top_skills.csv"

@st.cache_data
def load_jobs():
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()
    df = pd.read_parquet(DATA_PATH)
    # Downsample if exceptionally large to avoid Streamlit MemoryError
    if len(df) > 400000:
        df = df.sample(n=400000, random_state=42).reset_index(drop=True)
    
    # Optimize data types to category to save 85% memory
    cat_cols = ["job_level", "job_type", "search_country", "search_city", "job_location"]
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype("category")
    return df

@st.cache_data
def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

# Dynamic metric helper functions
@st.cache_data
def get_all_unique_skills_count(data_path):
    if not os.path.exists(data_path):
        return 0
    df_temp = pd.read_parquet(data_path, columns=["job_skills"])
    unique_skills = set()
    for row in df_temp["job_skills"].dropna():
        if row:
            for s in row.split(","):
                s = s.strip().lower()
                if s and s != "nan":
                    unique_skills.add(s)
    return len(unique_skills)

@st.cache_data
def get_base_top_skills(data_path, n=20):
    if not os.path.exists(data_path):
        return pd.DataFrame()
    df_temp = pd.read_parquet(data_path, columns=["job_skills"])
    counter = Counter()
    for row in df_temp["job_skills"].dropna():
        if row:
            for s in row.split(","):
                s = s.strip().lower()
                if s and s != "nan":
                    counter[s] += 1
    skills_df = pd.DataFrame(counter.most_common(n), columns=["skill", "count"])
    skills_df["skill_name"] = skills_df["skill"].str.title()
    return skills_df

df         = load_jobs()
top_skills = load_csv(TOP_SKILLS_PATH)

# Safe checks for missing dataset
if df.empty:
    st.error("⚠️ Cleaned dataset not found at `data/processed/jobs_cleaned.parquet`. Please run preprocessing first.")
    st.stop()

# Helper to compute top skills from filtered df
def get_top_skills_filtered(df_subset, n=20):
    if len(df_subset) == len(df):
        return get_base_top_skills(DATA_PATH, n)
    
    counter = Counter()
    for row in df_subset["job_skills"].dropna():
        if row:
            for s in row.split(","):
                s = s.strip().lower()
                if s and s != "nan":
                    counter[s] += 1
    skills_df = pd.DataFrame(counter.most_common(n), columns=["skill", "count"])
    skills_df["skill_name"] = skills_df["skill"].str.title()
    return skills_df

# Helper to calculate skills count
def get_filtered_skills_count(df_subset):
    if len(df_subset) == len(df):
        return get_all_unique_skills_count(DATA_PATH)
    
    unique_skills = set()
    for row in df_subset["job_skills"].dropna():
        if row:
            for s in row.split(","):
                s = s.strip().lower()
                if s and s != "nan":
                    unique_skills.add(s)
    return len(unique_skills)

# Helper to construct Skill vs Job Role heatmap df
def get_skill_role_heatmap(df_subset):
    # Get top 10 job titles
    top_roles = df_subset["job_title"].value_counts().head(10).index.tolist()
    if not top_roles:
        return None
    
    df_roles = df_subset[df_subset["job_title"].isin(top_roles)]
    
    # Get top 15 skills in these roles
    counter = Counter()
    for skills in df_roles["job_skills"].dropna():
        if skills:
            for s in skills.split(","):
                s = s.strip().lower()
                if s and s != "nan":
                    counter[s] += 1
    top_skills_heatmap = [item[0] for item in counter.most_common(15)]
    if not top_skills_heatmap:
        return None
    
    matrix = []
    for role in top_roles:
        role_df = df_roles[df_roles["job_title"] == role]
        total_role_jobs = len(role_df)
        row_vals = []
        for skill in top_skills_heatmap:
            count = role_df["job_skills"].dropna().apply(lambda x: skill in [s.strip().lower() for s in x.split(",")]).sum()
            pct = (count / total_role_jobs * 100) if total_role_jobs > 0 else 0
            row_vals.append(round(pct, 1))
        matrix.append(row_vals)
        
    return pd.DataFrame(matrix, index=[r.title() for r in top_roles], columns=[s.title() for s in top_skills_heatmap])

# ── Session State for Navigation & AI Recommendations ─────────────────────────
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "🏠 Dashboard"
if "rec_results" not in st.session_state:
    st.session_state["rec_results"] = None
if "rec_query_skills" not in st.session_state:
    st.session_state["rec_query_skills"] = []

# ── Sidebar Navigation & Global Filters ────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
      <h2>📊 Job Market</h2>
      <p>Trend Analysis System</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("<p style='font-size:0.75rem;color:#94a3b8;margin-bottom:8px;font-weight:600;text-transform:uppercase;letter-spacing:1px;'>Navigation</p>", unsafe_allow_html=True)
    
    pages = [
        "🏠 Dashboard",
        "📈 Skill Trends",
        "🌍 Location Analysis",
        "🤖 Job Recommendation",
        "🔍 Job Search"
    ]
    
    for p in pages:
        is_active = st.session_state["active_page"] == p
        if st.button(
            p,
            key=f"nav_btn_{p}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state["active_page"] = p
            st.rerun()

    st.markdown("---")
    st.markdown("<p style='font-size:0.75rem;color:#94a3b8;margin-bottom:8px;font-weight:600;text-transform:uppercase;letter-spacing:1px;'>Global Filters</p>", unsafe_allow_html=True)

    # 1. Country Filter
    countries = sorted(df["search_country"].dropna().unique().tolist())
    selected_country = st.selectbox("Country", ["All"] + [c.title() for c in countries])
    
    # 2. City Filter (Dependent on Country selection)
    if selected_country != "All":
        cities_df = df[df["search_country"] == selected_country.lower()]
    else:
        cities_df = df
    cities = sorted(cities_df["search_city"].dropna().unique().tolist())
    selected_city = st.selectbox("City", ["All"] + [c.title() for c in cities])
    
    # 3. Job Type Filter
    types = sorted(df["job_type"].dropna().unique().tolist())
    selected_type = st.selectbox("Job Type", ["All"] + [t.title() for t in types])
    
    # 4. Job Level Filter
    levels = sorted(df["job_level"].dropna().unique().tolist())
    selected_level = st.selectbox("Job Level", ["All"] + [l.title() for l in levels])
    
    # 5. Skill Keyword Filter
    skill_kw = st.text_input("Skill keyword", "")
    
    # 6. Job Title Keyword Filter
    title_kw = st.text_input("Job Title keyword", "")

    st.markdown("---")
    st.markdown(f"<span style='color:#94a3b8;font-size:0.78rem;'>📁 {len(df):,} jobs loaded</span>", unsafe_allow_html=True)

# Apply global filters dynamically
df_filtered = df.copy()
if selected_country != "All":
    df_filtered = df_filtered[df_filtered["search_country"] == selected_country.lower()]
if selected_city != "All":
    df_filtered = df_filtered[df_filtered["search_city"] == selected_city.lower()]
if selected_type != "All":
    df_filtered = df_filtered[df_filtered["job_type"] == selected_type.lower()]
if selected_level != "All":
    df_filtered = df_filtered[df_filtered["job_level"] == selected_level.lower()]
if skill_kw:
    df_filtered = df_filtered[df_filtered["job_skills"].str.contains(skill_kw.lower(), case=False, na=False)]
if title_kw:
    df_filtered = df_filtered[df_filtered["job_title"].str.contains(title_kw.lower(), case=False, na=False)]

page = st.session_state["active_page"]

# ── Helper HTML Components ────────────────────────────────────────────────────
def header(title, subtitle=""):
    st.markdown(f"""
    <div class="page-header">
      <h1>{title}</h1>
      {'<p>'+subtitle+'</p>' if subtitle else ''}
    </div>""", unsafe_allow_html=True)

def kpi(col, label, value):
    col.markdown(f"""
    <div class="metric-card">
      <div class="metric-value">{value}</div>
      <div class="metric-label">{label}</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Dashboard":
    header("🏠 Dashboard Overview", "Real-time snapshot of the job market landscape")

    if df_filtered.empty:
        st.warning("⚠️ No data available matching the selected filters. Please adjust the sidebar filters.")
    else:
        # Calculate dynamic metrics for KPIs
        total_jobs = len(df_filtered)
        total_companies = df_filtered["company"].nunique()
        total_locations = df_filtered["job_location"].nunique()
        unique_titles = df_filtered["job_title"].nunique()
        
        # Calculate total unique skills for KPIs (optimized)
        total_skills_val = get_filtered_skills_count(df_filtered)
        
        # Calculate date range
        df_filtered["first_seen"] = pd.to_datetime(df_filtered["first_seen"], errors="coerce")
        valid_dates = df_filtered["first_seen"].dropna()
        if not valid_dates.empty:
            min_d = valid_dates.min().date()
            max_d = valid_dates.max().date()
            date_range_val = f"{min_d} to {max_d}"
        else:
            date_range_val = "N/A"

        # KPI Layout (5 Columns)
        c1, c2, c3, c4, c5 = st.columns(5)
        kpi(c1, "Total Jobs", f"{total_jobs:,}")
        kpi(c2, "Total Companies", f"{total_companies:,}")
        kpi(c3, "Total Locations", f"{total_locations:,}")
        kpi(c4, "Unique Job Titles", f"{unique_titles:,}")
        kpi(c5, "Total Unique Skills", f"{total_skills_val:,}")
        
        st.markdown("<br>", unsafe_allow_html=True)

        # Insights Summary Section
        st.subheader("💡 Key Market Insights")
        top_title = df_filtered["job_title"].value_counts().index[0].title()
        
        top_skills_calc = get_top_skills_filtered(df_filtered, n=1)
        top_skill = top_skills_calc.iloc[0]["skill_name"] if not top_skills_calc.empty else "N/A"
        
        top_country = df_filtered["search_country"].value_counts().index[0].title() if df_filtered["search_country"].nunique() > 0 else "N/A"
        top_city = df_filtered["search_city"].value_counts().index[0].title() if df_filtered["search_city"].nunique() > 0 else "N/A"
        top_location = f"{top_city}, {top_country}" if (top_city != "N/A" or top_country != "N/A") else "N/A"
        
        top_type = df_filtered["job_type"].value_counts().index[0].title() if df_filtered["job_type"].nunique() > 0 else "N/A"
        top_level = df_filtered["job_level"].value_counts().index[0].title() if df_filtered["job_level"].nunique() > 0 else "N/A"
        
        st.markdown(f"""
        <div class="insight-box">
            <ul>
                <li>🏆 <b>Most Demanded Job Title:</b> {top_title}</li>
                <li>🛠️ <b>Most Demanded Skill:</b> {top_skill}</li>
                <li>🌍 <b>Highest Job Demand Location:</b> {top_location}</li>
                <li>🕐 <b>Most Common Job Type:</b> {top_type}</li>
                <li>🎓 <b>Most Common Job Level:</b> {top_level}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # ── Job Posting Trend (Line / Area Chart) ────────────────────────────────
        st.subheader("📅 Job Posting Trend")
        if not valid_dates.empty:
            c_a, c_b = st.columns([1, 4])
            with c_a:
                granularity = st.radio("Granularity", ["Daily","Monthly"], horizontal=True, key="dashboard_trend_gran")
            with c_b:
                st.markdown("")
            
            valid_df = df_filtered.dropna(subset=["first_seen"]).copy()
            if granularity == "Daily":
                valid_df["period"] = valid_df["first_seen"].dt.date.astype(str)
            else:
                valid_df["period"] = valid_df["first_seen"].dt.to_period("M").astype(str)

            trend = valid_df.groupby("period").size().reset_index(name="count").sort_values("period")
            fig_trend = go.Figure(go.Scatter(
                x=trend["period"], y=trend["count"],
                mode="lines+markers",
                fill="tozeroy",
                fillcolor="rgba(0,212,255,0.08)",
                line=dict(color="#00d4ff", width=2),
                marker=dict(color="#00d4ff", size=5),
                hovertemplate="<b>%{x}</b><br>Jobs: %{y:,}<extra></extra>",
            ))
            style_fig(fig_trend, 380)
            fig_trend.update_layout(
                title=f"{granularity} Job Postings Volume over Time",
                xaxis=dict(title="Date / Period", tickangle=-45, gridcolor="#1e2d4a"),
                yaxis=dict(title="Number of Postings", gridcolor="#1e2d4a"),
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            st.markdown("<p style='font-size:0.78rem;color:#94a3b8;font-style:italic;margin-top:-10px;'>“The trend is based on available first_seen dates in the dataset.”</p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.info("No posting date information available to show trends.")

        # ── Row 1 Visualizations: Job Titles & Companies ──────────────────────────
        r1_l, r1_r = st.columns(2)
        with r1_l:
            st.subheader("🏆 Top 10 Job Titles")
            top_titles = df_filtered["job_title"].value_counts().head(10).reset_index()
            top_titles.columns = ["job_title","count"]
            top_titles["job_title"] = top_titles["job_title"].str.title()
            fig_titles = px.bar(
                top_titles.sort_values("count"),
                x="count", y="job_title", orientation="h",
                color="count", color_continuous_scale=["#1e3a5f","#00d4ff"],
                labels={"count":"# Jobs","job_title":""},
                title="Top Job Titles by Count"
            )
            fig_titles.update_traces(texttemplate="%{x:,}", textposition="outside")
            style_fig(fig_titles, 420)
            fig_titles.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_titles, use_container_width=True)

        with r1_r:
            st.subheader("🏢 Top Hiring Companies")
            comp = df_filtered["company"].value_counts().head(15).reset_index()
            comp.columns = ["company","count"]
            comp["company"] = comp["company"].str.title()
            
            view_comp = st.radio("Display as:", ["Treemap", "Bar Chart"], horizontal=True, key="dashboard_comp_view")
            if view_comp == "Treemap":
                fig_comp = px.treemap(
                    comp, path=["company"], values="count",
                    color="count", color_continuous_scale=["#1e3a5f","#00d4ff"],
                    title="Treemap representation of Hiring Companies"
                )
                fig_comp.update_traces(textfont=dict(size=12, color="#fff"))
            else:
                fig_comp = px.bar(
                    comp.sort_values("count"), x="count", y="company", orientation="h",
                    color="count", color_continuous_scale=["#1e3a5f","#7c3aed"],
                    labels={"count":"# Jobs","company":""},
                    title="Hiring Company Volumes"
                )
                fig_comp.update_traces(texttemplate="%{x:,}", textposition="outside")
                fig_comp.update_layout(coloraxis_showscale=False)
            style_fig(fig_comp, 420)
            st.plotly_chart(fig_comp, use_container_width=True)

        # ── Row 2 Visualizations: Job Type & Level ────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        r2_l, r2_r = st.columns(2)
        with r2_l:
            st.subheader("🍩 Job Type Distribution")
            jt = df_filtered["job_type"].value_counts().head(8).reset_index()
            jt.columns = ["type","count"]
            jt["type"] = jt["type"].str.title()
            fig_type = go.Figure(go.Pie(
                labels=jt["type"], values=jt["count"],
                hole=0.55,
                marker=dict(colors=COLORS, line=dict(color="#0a0e1a", width=2)),
                hovertemplate="<b>%{label}</b><br>Jobs: %{value:,}<br>Percentage: %{percent}<extra></extra>"
            ))
            fig_type.update_traces(textfont_color="#fff")
            style_fig(fig_type, 400)
            fig_type.update_layout(title="Job Types Breakdown")
            st.plotly_chart(fig_type, use_container_width=True)

        with r2_r:
            st.subheader("🎯 Job Level Distribution")
            jl = df_filtered["job_level"].value_counts().head(10).reset_index()
            jl.columns = ["level","count"]
            jl["level"] = jl["level"].str.title()
            fig_level = px.bar(
                jl, x="level", y="count",
                color="count", color_continuous_scale=["#1e3a5f","#7c3aed"],
                labels={"level":"","count":"# Jobs"},
                title="Job Count by Experience Level"
            )
            fig_level.update_traces(texttemplate="%{y:,}", textposition="outside")
            style_fig(fig_level, 400)
            fig_level.update_layout(coloraxis_showscale=False, xaxis_tickangle=-15)
            st.plotly_chart(fig_level, use_container_width=True)

        # ── Row 3 Visualizations: Role vs Type & Level vs Type ────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        r3_l, r3_r = st.columns(2)
        with r3_l:
            st.subheader("👔 Job Role vs Job Type")
            top_roles_l = df_filtered["job_title"].value_counts().head(10).index.tolist()
            if top_roles_l:
                df_roles_l = df_filtered[df_filtered["job_title"].isin(top_roles_l)]
                role_type_gp = df_roles_l.groupby(["job_title", "job_type"]).size().reset_index(name="count")
                role_type_gp["job_title"] = role_type_gp["job_title"].str.title()
                role_type_gp["job_type"] = role_type_gp["job_type"].str.title()
                
                fig_role_type = px.bar(
                    role_type_gp, y="job_title", x="count", color="job_type",
                    orientation="h", barmode="stack",
                    color_discrete_sequence=COLORS,
                    labels={"job_title": "", "count": "# Jobs", "job_type": "Job Type"},
                    title="Employment Type breakdown for Top 10 Roles"
                )
                style_fig(fig_role_type, 420)
                st.plotly_chart(fig_role_type, use_container_width=True)
            else:
                st.info("No role vs type details available.")

        with r3_r:
            st.subheader("🎓 Job Level vs Job Type")
            level_type_gp = df_filtered.groupby(["job_level", "job_type"]).size().reset_index(name="count")
            level_type_gp["job_level"] = level_type_gp["job_level"].str.title()
            level_type_gp["job_type"] = level_type_gp["job_type"].str.title()
            
            fig_level_type = px.bar(
                level_type_gp, x="job_level", y="count", color="job_type",
                barmode="group",
                color_discrete_sequence=COLORS,
                labels={"job_level": "", "count": "# Jobs", "job_type": "Job Type"},
                title="Job level mapped against employment types"
            )
            style_fig(fig_level_type, 420)
            st.plotly_chart(fig_level_type, use_container_width=True)

        # ── Row 4 Visualizations (Custom Additions from Antigravity) ────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        r4_l, r4_r = st.columns(2)
        with r4_l:
            st.subheader("👔 Job Role vs Experience Level")
            if top_roles_l:
                df_roles_l = df_filtered[df_filtered["job_title"].isin(top_roles_l)]
                role_level_gp = df_roles_l.groupby(["job_title", "job_level"]).size().reset_index(name="count")
                role_level_gp["job_title"] = role_level_gp["job_title"].str.title()
                role_level_gp["job_level"] = role_level_gp["job_level"].str.title()
                
                fig_role_level = px.bar(
                    role_level_gp, y="job_title", x="count", color="job_level",
                    orientation="h", barmode="stack",
                    color_discrete_sequence=COLORS,
                    labels={"job_title": "", "count": "# Jobs", "job_level": "Experience Level"},
                    title="Experience levels required for Top 10 Roles (Custom Insight)"
                )
                style_fig(fig_role_level, 420)
                st.plotly_chart(fig_role_level, use_container_width=True)
            else:
                st.info("No role vs level details available.")

        with r4_r:
            st.subheader("📊 Distribution of Skills Count per Job")
            skills_count = df_filtered["job_skills"].dropna().apply(
                lambda x: len([s for s in x.split(",") if s.strip() and s.strip() != "nan"]) if x else 0
            )
            if not skills_count.empty:
                fig_skills_dist = px.histogram(
                    skills_count, x=skills_count.values,
                    nbins=20,
                    color_discrete_sequence=[COLORS[0]],
                    labels={"x": "Number of Skills Required", "count": "Job Listings"},
                    title="How many skills are typically required per Job Posting? (Custom Insight)"
                )
                style_fig(fig_skills_dist, 420)
                fig_skills_dist.update_layout(
                    xaxis_title="Number of Skills Required",
                    yaxis_title="Number of Job Postings",
                    showlegend=False
                )
                st.plotly_chart(fig_skills_dist, use_container_width=True)
            else:
                st.info("No skill count data available.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SKILL TRENDS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈 Skill Trends":
    header("📈 Skill Trends", "Discover the most in-demand skills in today's job market")

    if df_filtered.empty:
        st.warning("⚠️ No data available matching the selected filters. Please adjust the sidebar filters.")
    else:
        # Get top skills for active subset
        skills_df = get_top_skills_filtered(df_filtered, n=100)

        if skills_df.empty:
            st.error("No skill data available matching these filters.")
        else:
            st.subheader("Top 20 In-Demand Skills")
            top20 = skills_df.head(20).sort_values("count")
            fig_top_skills = px.bar(
                top20, x="count", y="skill_name", orientation="h",
                color="count", color_continuous_scale=["#1e3a5f","#00d4ff"],
                labels={"count":"# Jobs","skill_name":""},
                title="Top 20 Skills required in filtered listings"
            )
            fig_top_skills.update_traces(texttemplate="%{x:,}", textposition="outside")
            style_fig(fig_top_skills, 500)
            fig_top_skills.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_top_skills, use_container_width=True)

            # Skill vs Job Role Heatmap
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("🔥 Skill vs Job Role Heatmap")
            heatmap_df = get_skill_role_heatmap(df_filtered)
            if heatmap_df is not None and not heatmap_df.empty:
                fig_heat = go.Figure(data=go.Heatmap(
                    z=heatmap_df.values,
                    x=heatmap_df.columns,
                    y=heatmap_df.index,
                    colorscale=[[0.0, "#0f1629"], [0.5, "#7c3aed"], [1.0, "#00d4ff"]],
                    hovertemplate="Role: %{y}<br>Skill: %{x}<br>Percentage of postings: %{z}%<extra></extra>"
                ))
                style_fig(fig_heat, 480)
                fig_heat.update_layout(
                    title="Skill Requirement Probability by Top Job Titles (%)",
                    xaxis=dict(title="Skills Required", tickangle=-45),
                    yaxis=dict(title="Job Title / Role"),
                )
                st.plotly_chart(fig_heat, use_container_width=True)
            else:
                st.info("Insufficient data to build a Skill vs Job Role heatmap.")

            # Top Skills by Selected Job Role
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("🎯 Top Skills by Selected Job Role")
            available_roles = df_filtered["job_title"].value_counts().head(30).index.tolist()
            if available_roles:
                selected_role = st.selectbox("Select a Job Role / Title", options=[r.title() for r in available_roles])
                role_subset = df_filtered[df_filtered["job_title"] == selected_role.lower()]
                role_skills = get_top_skills_filtered(role_subset, n=10)
                
                if not role_skills.empty:
                    fig_role_skills = px.bar(
                        role_skills.sort_values("count"), x="count", y="skill_name", orientation="h",
                        color="count", color_continuous_scale=["#1e3a5f","#00d4ff"],
                        labels={"count":"# Jobs","skill_name":""},
                        title=f"Top 10 skills required for {selected_role.title()}"
                    )
                    fig_role_skills.update_traces(texttemplate="%{x:,}", textposition="outside")
                    style_fig(fig_role_skills, 400)
                    fig_role_skills.update_layout(coloraxis_showscale=False)
                    st.plotly_chart(fig_role_skills, use_container_width=True)
                else:
                    st.info(f"No skill metrics available for the job role: '{selected_role}'")
            else:
                st.info("No job titles available to analyze.")

            # Search skills table
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("📋 Search all skills in selection")
            search_sk = st.text_input("🔍 Search a skill name", "")
            filtered_sk_table = skills_df[skills_df["skill"].str.contains(search_sk.lower(), case=False, na=False)] if search_sk else skills_df
            
            st.dataframe(
                filtered_sk_table[["skill_name", "count"]].reset_index(drop=True),
                use_container_width=True,
                height=300,
                column_config={"skill_name": "Skill Name", "count": "Job Postings Count"}
            )

            # Download CSV
            csv_sk = filtered_sk_table[["skill", "count"]].to_csv(index=False).encode()
            st.download_button("⬇ Download Skills CSV", csv_sk, "skills.csv", "text/csv")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: LOCATION ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🌍 Location Analysis":
    header("🌍 Location Analysis", "Geographic distribution of job opportunities")

    if df_filtered.empty:
        st.warning("⚠️ No data available matching the selected filters. Please adjust the sidebar filters.")
    else:
        # World Choropleth Map
        st.subheader("🗺️ Country-wise Job Demand Map")
        country_df = df_filtered["search_country"].value_counts().reset_index()
        country_df.columns = ["country","count"]
        country_df["country_name"] = country_df["country"].str.title()
        
        fig_map = px.choropleth(
            country_df, locations="country_name",
            locationmode="country names",
            color="count",
            color_continuous_scale=["#0f1629","#00d4ff"],
            labels={"count":"# Jobs", "country_name": "Country"},
            title="Global Job Postings volume by country"
        )
        style_fig(fig_map, 460)
        fig_map.update_geos(
            bgcolor="#0a0e1a",
            lakecolor="#0a0e1a",
            landcolor="#1a2540",
            showcoastlines=True, coastlinecolor="#2a3a5c",
            showframe=False,
        )
        st.plotly_chart(fig_map, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_l, col_r = st.columns(2)

        with col_l:
            st.subheader("🌐 Top Countries")
            cc = df_filtered["search_country"].value_counts().head(15).reset_index()
            cc.columns = ["country","count"]
            cc["country"] = cc["country"].str.title()
            
            fig_country = px.bar(
                cc, x="country", y="count",
                color="count", color_continuous_scale=["#1e3a5f","#00d4ff"],
                labels={"country":"","count":"# Jobs"},
                title="Job Postings by Search Country"
            )
            fig_country.update_traces(texttemplate="%{y:,}", textposition="outside")
            style_fig(fig_country, 400)
            fig_country.update_layout(coloraxis_showscale=False, xaxis_tickangle=-30)
            st.plotly_chart(fig_country, use_container_width=True)

        with col_r:
            st.subheader("🏙️ Top Cities by Job Demand")
            city_df = df_filtered["search_city"].value_counts().head(15).reset_index()
            city_df.columns = ["city","count"]
            city_df["city"] = city_df["city"].str.title()
            
            fig_city = px.bar(
                city_df.sort_values("count"), x="count", y="city", orientation="h",
                color="count", color_continuous_scale=["#1e3a5f","#7c3aed"],
                labels={"city":"","count":"# Jobs"},
                title="Top 15 Cities by demand volume"
            )
            fig_city.update_traces(texttemplate="%{x:,}", textposition="outside")
            style_fig(fig_city, 400)
            fig_city.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_city, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📍 Top Job Locations")
        loc_df = df_filtered["job_location"].value_counts().head(25).reset_index()
        loc_df.columns = ["location","count"]
        loc_df["location"] = loc_df["location"].str.title()
        
        fig_loc = px.bar(
            loc_df.sort_values("count"), x="count", y="location", orientation="h",
            color="count", color_continuous_scale=["#1e3a5f","#00d4ff"],
            labels={"location":"","count":"# Jobs"},
            title="Top 25 Job Locations details"
        )
        fig_loc.update_traces(texttemplate="%{x:,}", textposition="outside")
        style_fig(fig_loc, 600)
        fig_loc.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_loc, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: JOB RECOMMENDATION (IMPROVED WITH SESSION STATE & HIGHLIGHTS)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🤖 Job Recommendation":
    header("🤖 Job Recommendation", "Get AI-powered job matches based on your skills")

    # Load Nearest Neighbors model and resources
    try:
        import joblib
        vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
        model_knn  = joblib.load("models/job_recommender.pkl")
        rec_jobs   = pd.read_parquet("models/recommendation_data.parquet")
        model_ready = True
    except Exception:
        model_ready = False
        st.warning("⚠️ Recommendation model resources not found. Please run `python train_model.py` first to generate models.")

    # Determine known skills for multiselect
    if not top_skills.empty:
        known = top_skills["skill"].head(100).tolist()
    else:
        known = get_base_top_skills(DATA_PATH, n=100)["skill"].tolist()

    default_skills = [s for s in ["python", "sql", "aws", "excel"] if s in known]
    
    selected = st.multiselect("🎯 Select your skills", options=[s.title() for s in known], default=[s.title() for s in default_skills])
    extra    = st.text_input("➕ Add more skills manually (comma-separated)", "")
    n_recs   = st.slider("Number of recommendations to retrieve", 5, 100, 20)

    col_btn, _ = st.columns([1, 4])
    with col_btn:
        get_recs = st.button("🚀 Recommend Jobs", type="primary", use_container_width=True)

    if get_recs:
        if not model_ready:
            st.error("Recommendation model not loaded.")
        else:
            extra_list = [s.strip().lower() for s in extra.split(",") if s.strip()]
            user_skills = [s.lower() for s in selected] + extra_list
            if not user_skills:
                st.warning("Please select or enter at least one skill.")
            else:
                with st.spinner("Finding matches using TF-IDF + Nearest Neighbors..."):
                    query  = " ".join(user_skills)
                    qvec   = vectorizer.transform([query])
                    # Retrieve a larger set of neighbors (up to 200) to allow interactive local filtering
                    k = min(200, len(rec_jobs))
                    dist, idx = model_knn.kneighbors(qvec, n_neighbors=k)
                    results = rec_jobs.iloc[idx[0]].copy()
                    results["match_score"] = (1 - dist[0]).round(3)
                    
                    # Store results in session state
                    st.session_state["rec_results"] = results
                    st.session_state["rec_query_skills"] = user_skills
                    st.success("Recommendations computed successfully!")

    # Check and render session state recommendations if available
    if st.session_state["rec_results"] is not None:
        st.markdown("---")
        st.subheader("🔍 Refine and Filter Matches")

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            rec_loc_filter = st.text_input("📍 Filter recommendations by location (type to search)", "")
        with col_f2:
            levels_list = ["All"] + sorted([l.title() for l in st.session_state["rec_results"]["job_level"].dropna().unique().tolist() if l])
            rec_level_filter = st.selectbox("🎓 Filter recommendations by experience level", levels_list)

        # Apply filters on session state dataframe
        filtered_recs = st.session_state["rec_results"].copy()
        if rec_loc_filter:
            filtered_recs = filtered_recs[filtered_recs["job_location"].str.contains(rec_loc_filter.lower(), case=False, na=False)]
        if rec_level_filter != "All":
            filtered_recs = filtered_recs[filtered_recs["job_level"].str.lower() == rec_level_filter.lower()]

        display_recs = filtered_recs.head(n_recs)
        st.success(f"✅ Displaying **{len(display_recs)}** matching recommendations (from {len(filtered_recs)} total matches)")

        if display_recs.empty:
            st.info("No matching recommendations found for the selected location or level filters.")
        else:
            for _, row in display_recs.iterrows():
                score_pct = int(row["match_score"] * 100)
                job_link = row.get('job_link', '')
                link_html = f'<a href="{job_link}" target="_blank" style="text-decoration:none; color:#00d4ff; font-weight:600; font-size:0.82rem; margin-top:8px; display:inline-block;">🔗 View Job Posting &rarr;</a>' if job_link and str(job_link).startswith("http") else ''
                
                # Format skills: Highlight matching skills in bold cyan
                skills_list = [s.strip() for s in str(row.get('job_skills','')).split(",") if s.strip()]
                formatted_skills = []
                for s in skills_list:
                    if s.lower() in st.session_state["rec_query_skills"]:
                        formatted_skills.append(f"<b style='color:#00d4ff;'>{s.title()}</b>")
                    else:
                        formatted_skills.append(s.title())
                skills_str = ", ".join(formatted_skills)

                st.markdown(f"""
                <div class="job-card">
                  <h4>💼 {row.get('job_title','N/A').title()}</h4>
                  <div class="meta">
                    🏢 <b>{row.get('company','N/A').title()}</b> &nbsp;|&nbsp;
                    📍 {row.get('job_location','N/A').title()} &nbsp;|&nbsp;
                    🎓 {row.get('job_level','N/A').title()} &nbsp;|&nbsp;
                    🕐 {row.get('job_type','N/A').title()}
                  </div>
                  <div class="meta" style="margin-top:6px;">🛠️ Skills: {skills_str if skills_str else 'N/A'}</div>
                  {link_html}
                  <div style="margin-top:10px;font-size:0.8rem;color:#94a3b8;">Match Score: {score_pct}%</div>
                  <div class="score-bar">
                    <div class="score-fill" style="width:{score_pct}%;"></div>
                  </div>
                </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: JOB SEARCH (IMPROVED WITH SYNCHRONIZATION & CSV & SUMMARY METRICS)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Job Search":
    header("🔍 Job Search", "Find jobs by title, location, skill, type, and level")

    # Local Filters Expander, pre-populated with global sidebar inputs
    with st.expander("🎛️ Filter Results", expanded=True):
        f1, f2 = st.columns(2)
        title_q    = f1.text_input("Job Title Keyword", value=title_kw, key="search_page_title")
        location_q = f2.text_input("Location / City Keyword", value=selected_city if selected_city != "All" else "", key="search_page_loc")

        f3, f4, f5 = st.columns(3)
        skill_q    = f3.text_input("Skill keyword", value=skill_kw, key="search_page_skill")
        
        levels = ["All"] + sorted([l.title() for l in df["job_level"].dropna().unique().tolist() if l])
        types      = ["All"] + sorted([t.title() for t in df["job_type"].dropna().unique().tolist() if t])
        
        # Pre-select matching values from global filters
        def_level_idx = levels.index(selected_level) if selected_level in levels else 0
        def_type_idx = types.index(selected_type) if selected_type in types else 0
        
        level_sel  = f4.selectbox("Job Level", levels, index=def_level_idx, key="search_page_level")
        type_sel   = f5.selectbox("Job Type",  types, index=def_type_idx, key="search_page_type")

    # Apply search filters to the base dataset
    search_df = df.copy()
    if title_q:
        search_df = search_df[search_df["job_title"].str.contains(title_q.lower(), case=False, na=False)]
    if location_q:
        search_df = search_df[search_df["job_location"].str.contains(location_q.lower(), case=False, na=False)]
    if skill_q:
        search_df = search_df[search_df["job_skills"].str.contains(skill_q.lower(), case=False, na=False)]
    if level_sel != "All":
        search_df = search_df[search_df["job_level"] == level_sel.lower()]
    if type_sel != "All":
        search_df = search_df[search_df["job_type"] == type_sel.lower()]

    total = len(search_df)

    # Search Results KPIs
    s1, s2, s3 = st.columns(3)
    kpi(s1, "Matching Jobs Found", f"{total:,}")
    kpi(s2, "Companies", f"{search_df['company'].nunique() if total > 0 else 0:,}")
    kpi(s3, "Locations", f"{search_df['job_location'].nunique() if total > 0 else 0:,}")
    st.markdown("<br>", unsafe_allow_html=True)

    if total > 0:
        show_cols = ["job_title", "company", "job_location", "job_type", "job_level", "job_skills", "job_link"]
        avail     = [c for c in show_cols if c in search_df.columns]

        # Format dataframe fields for visualization
        disp_df = search_df[avail].head(200).copy()
        for col in ["job_title", "company", "job_location", "job_type", "job_level"]:
            if col in disp_df.columns:
                disp_df[col] = disp_df[col].astype(str).str.title()

        st.subheader(f"📋 Search Results (showing top 200 of {total:,})")
        st.dataframe(
            disp_df,
            use_container_width=True,
            height=400,
            column_config={
                "job_link": st.column_config.LinkColumn("Job Link", display_text="Open Link 🔗"),
                "job_title": "Job Title",
                "company": "Company",
                "job_location": "Location",
                "job_type": "Job Type",
                "job_level": "Job Level",
                "job_skills": "Skills"
            }
        )

        # CSV Download Button
        csv_out = search_df[avail].head(1000).to_csv(index=False).encode()
        st.download_button("⬇ Download Top 1000 Search Results CSV", csv_out, "job_search_results.csv", "text/csv")

        # Summary charts for search results
        st.markdown("---")
        st.subheader("📊 Search Results Insights")

        r1, r2 = st.columns(2)
        with r1:
            top_c = search_df["company"].value_counts().head(10).reset_index()
            top_c.columns = ["company","count"]
            top_c["company"] = top_c["company"].str.title()
            fc = px.bar(
                top_c.sort_values("count"), x="count", y="company", orientation="h",
                color="count", color_continuous_scale=["#1e3a5f","#00d4ff"],
                labels={"company":"","count":"# Jobs"},
                title="Top Hiring Companies in Results"
            )
            style_fig(fc, 350)
            fc.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fc, use_container_width=True)
            
        with r2:
            top_l = search_df["job_location"].value_counts().head(10).reset_index()
            top_l.columns = ["location","count"]
            top_l["location"] = top_l["location"].str.title()
            fl = px.bar(
                top_l.sort_values("count"), x="count", y="location", orientation="h",
                color="count", color_continuous_scale=["#1e3a5f","#7c3aed"],
                labels={"location":"","count":"# Jobs"},
                title="Top Job Locations in Results"
            )
            style_fig(fl, 350)
            fl.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fl, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🛠️ Top Skills in Search Results")
        results_skills = get_top_skills_filtered(search_df, n=15)
        if not results_skills.empty:
            fs = px.bar(
                results_skills.sort_values("count"), x="count", y="skill_name", orientation="h",
                color="count", color_continuous_scale=["#1e3a5f","#00d4ff"],
                labels={"skill_name":"","count":"# Jobs"},
                title="Top 15 Skills Required in filtered search results"
            )
            style_fig(fs, 400)
            fs.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fs, use_container_width=True)
        else:
            st.info("No skill counts available for the search results.")
    else:
        st.info("No job listings match your current filters. Try loosening your keywords or drop-down selects.")