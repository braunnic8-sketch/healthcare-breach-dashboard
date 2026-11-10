from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='HHS Healthcare Breach Dashboard', layout='wide')
st.title('HHS Healthcare Breach Dashboard')
st.caption('Shared starter template | Cyber Risk Management | Public HHS OCR breach reports')
FILENAME = 'hhs_breaches.xlsx'  # Change this only if your workbook has a different name.

@st.cache_data
def load_excel(content):
    return pd.read_excel(content)

uploaded = st.sidebar.file_uploader('Optional: upload an Excel workbook', type='xlsx')
if uploaded:
    content = uploaded.getvalue()
elif Path(FILENAME).exists():
    content = Path(FILENAME).read_bytes()
else:
    st.info(f'Add {FILENAME} to the same GitHub repository as app.py, or upload it in the sidebar.')
    st.stop()
try:
    df = load_excel(content)
except Exception as e:
    st.error(f'Unable to read Excel: {e}')
    st.stop()
df.columns = [str(c).strip() for c in df.columns]
if df.empty or df.columns.duplicated().any():
    st.error('Workbook is empty or has duplicate column names. Check the Excel file.')
    st.stop()

def find_col(*names):
    normalized = {''.join(c.lower().split()).replace('_',''): c for c in df.columns}
    for name in names:
        key = ''.join(name.lower().split()).replace('_','')
        if key in normalized:
            return normalized[key]
    return None

date_col = find_col('Breach Submission Date', 'Submission Date')
state_col = find_col('State')
type_col = find_col('Type of Breach', 'Breach Type')
count_col = find_col('Individuals Affected', 'Number of Individuals Affected')
entity_col = find_col('Covered Entity Type', 'Entity Type')
associate_col = find_col('Business Associate Present', 'Business Associate Involved')
location_col = find_col('Location of Breached Information', 'Location of Breach')

work = df.copy()
if date_col:
    work['_date'] = pd.to_datetime(work[date_col], errors='coerce')
    work['_year'] = work['_date'].dt.year
if count_col:
    work['_affected'] = pd.to_numeric(work[count_col].astype(str).str.replace(',','',regex=False), errors='coerce')

st.sidebar.header('Interactive filters')
if date_col:
    years = sorted(work['_year'].dropna().astype(int).unique().tolist())
    chosen_years = st.sidebar.multiselect('Submission year', years, default=years)
    work = work[work['_year'].isin(chosen_years)]
else:
    st.sidebar.warning('No Breach Submission Date column found; year filter unavailable.')
for column, label in [(state_col,'State'), (type_col,'Breach type'), (entity_col,'Covered entity type'), (associate_col,'Business associate'), (location_col,'Information location')]:
    if column:
        options = sorted(work[column].dropna().astype(str).unique().tolist())
        if len(options) <= 150:
            selected = st.sidebar.multiselect(label, options)
            if selected:
                work = work[work[column].astype(str).isin(selected)]
if count_col:
    maximum = int(max(0, work['_affected'].max())) if work['_affected'].notna().any() else 0
    minimum = st.sidebar.number_input('Minimum individuals affected', min_value=0, max_value=maximum, value=0, step=500)
    work = work[work['_affected'].ge(minimum)]

st.subheader('Summary')
a,b,c = st.columns(3)
a.metric('Matching breach reports', f'{len(work):,}')
b.metric('Individuals affected (sum of reports)', f"{work['_affected'].sum():,.0f}" if count_col else 'Not available')
c.metric('Total records in workbook', f'{len(df):,}')
st.caption('Individuals affected is a sum across reports, not necessarily unique people. Report counts do not measure breach probability.')
if work.empty:
    st.warning('No records match the selected filters. Change the filters to continue.')
    st.stop()

st.subheader('Visualization 1: Compare categories')
category_options = [x for x in [type_col, state_col, entity_col, associate_col, location_col] if x]
if category_options:
    category = st.selectbox('Group breach reports by', category_options)
    counts = work[category].fillna('Not reported').astype(str).value_counts().head(20).rename_axis('Category').reset_index(name='Reports')
    st.plotly_chart(px.bar(counts, x='Category', y='Reports', title='Number of reported breaches'), use_container_width=True)
else:
    st.info('No recognized categorical columns available.')

st.subheader('Visualization 2: Trend by submission year')
if date_col:
    trend = work.groupby('_year').size().reset_index(name='Reports').sort_values('_year')
    st.plotly_chart(px.line(trend, x='_year', y='Reports', markers=True, title='Breach reports by submission year', labels={'_year':'Year'}), use_container_width=True)
else:
    st.info('A submission date column is needed for this chart.')

st.subheader('Visualization 3: Scale of reported breaches')
if count_col:
    valid = work[work['_affected'].notna()]
    st.plotly_chart(px.histogram(valid, x='_affected', nbins=30, title='Distribution of individuals affected', labels={'_affected':'Individuals affected'}), use_container_width=True)
else:
    st.info('An Individuals Affected column is needed for this chart.')

st.subheader('Explore records')
st.dataframe(work.drop(columns=[c for c in ['_date','_year','_affected'] if c in work], errors='ignore'), use_container_width=True)
st.download_button('Download filtered data (CSV)', data=work.drop(columns=[c for c in ['_date','_year','_affected'] if c in work], errors='ignore').to_csv(index=False).encode('utf-8'), file_name='filtered_hhs_breaches.csv', mime='text/csv')
st.info('For your final project: select the two most relevant interactive features and three visualizations, and explain how they answer your assigned risk management question. Do not infer causal relationships or breach probabilities from report counts.')
