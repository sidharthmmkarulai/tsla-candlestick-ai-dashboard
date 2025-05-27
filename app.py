import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import ast

# Optional: Import Gemini AI (won't break chart if fails)
try:
    import google.generativeai as genai
    genai.configure(api_key="AIzaSyBEebw6qLJ8gLxO7OZ0ll6fmIp4OXylqmg")
    GEMINI_ENABLED = True
except Exception:
    GEMINI_ENABLED = False

# --- Streamlit Config ---
st.set_page_config(layout="wide")
st.title("TSLA Candlestick Dashboard with AI Chatbot")

# --- Load Data ---
df = pd.read_csv("tsla_data.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values('timestamp')

# Convert stringified lists to Python lists
df['Support'] = df['Support'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) and x != '' else [])
df['Resistance'] = df['Resistance'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) and x != '' else [])

# Calculate support/resistance bands
df['support_low'] = df['Support'].apply(lambda x: min(x) if x else None)
df['support_high'] = df['Support'].apply(lambda x: max(x) if x else None)
df['resist_low'] = df['Resistance'].apply(lambda x: min(x) if x else None)
df['resist_high'] = df['Resistance'].apply(lambda x: max(x) if x else None)

# Moving averages
df['ma_20'] = df['close'].rolling(window=20).mean()
df['ma_50'] = df['close'].rolling(window=50).mean()

# Sidebar filters
start_date = st.sidebar.date_input("Start Date", df['timestamp'].min().date())
end_date = st.sidebar.date_input("End Date", df['timestamp'].max().date())
df = df[(df['timestamp'] >= pd.to_datetime(start_date)) & (df['timestamp'] <= pd.to_datetime(end_date))]

# --- Tabs ---
tab1, tab2 = st.tabs(["Chart", "TSLA AI Chatbot"])

# --- Tab 1: Candlestick Chart ---
with tab1:
    fig = go.Figure()

    # Candlesticks
    fig.add_trace(go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        increasing_line_color='green',
        decreasing_line_color='red',
        name='Candlesticks'
    ))

    # Support band
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['support_low'],
        mode='lines',
        line=dict(width=0),
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['support_high'],
        mode='lines',
        fill='tonexty',
        fillcolor='rgba(0,255,0,0.15)',
        line=dict(width=0),
        name='Support Band'
    ))

    # Resistance band
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['resist_low'],
        mode='lines',
        line=dict(width=0),
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['resist_high'],
        mode='lines',
        fill='tonexty',
        fillcolor='rgba(255,0,0,0.15)',
        line=dict(width=0),
        name='Resistance Band'
    ))

    # Moving averages
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['ma_20'],
        mode='lines',
        line=dict(color='orange', width=2),
        name='20 MA'
    ))
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['ma_50'],
        mode='lines',
        line=dict(color='royalblue', width=2),
        name='50 MA'
    ))

    # Direction markers
    for i, row in df.iterrows():
        if row.get('direction') == 'LONG':
            fig.add_trace(go.Scatter(
                x=[row['timestamp']],
                y=[row['low'] - 2],
                mode='markers',
                marker=dict(symbol='triangle-up', color='green', size=12, line=dict(width=1.5, color='white')),
                showlegend=False
            ))
        elif row.get('direction') == 'SHORT':
            fig.add_trace(go.Scatter(
                x=[row['timestamp']],
                y=[row['high'] + 2],
                mode='markers',
                marker=dict(symbol='triangle-down', color='red', size=12, line=dict(width=1.5, color='white')),
                showlegend=False
            ))
        else:
            fig.add_trace(go.Scatter(
                x=[row['timestamp']],
                y=[(row['high'] + row['low']) / 2],
                mode='markers',
                marker=dict(symbol='circle', color='yellow', size=10, line=dict(width=1.5, color='white')),
                showlegend=False
            ))

    # Layout
    fig.update_layout(
        template='plotly_dark',
        height=800,
        xaxis_rangeslider_visible=False,
        title="TSLA Candlestick Chart with MA, Bands & Signals",
        plot_bgcolor='#111111',
        paper_bgcolor='#111111',
        font=dict(color='white'),
        xaxis_title="Date",
        yaxis_title="Price"
    )

    st.plotly_chart(fig, use_container_width=True)

# --- Tab 2: AI Chatbot ---
with tab2:
    st.header("Ask questions about TSLA Data")
    user_input = st.text_input("Enter your question here")

    if user_input:
        if GEMINI_ENABLED:
            try:
                model = genai.GenerativeModel("models/text-bison-001")
                response = model.generate_content(user_input)
                st.write("**You asked:**", user_input)
                st.write("**Gemini AI says:**", response.text)
            except Exception as e:
                st.error("Gemini AI failed to respond.")
        else:
            st.warning("Gemini AI is not enabled or failed to load.")
