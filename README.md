# TSLA Candlestick Dashboard with AI Chatbot

This is a Streamlit web application that displays a candlestick chart for Tesla (TSLA) stock data with support and resistance bands, moving averages, and direction markers. It also includes an AI chatbot powered by Google's Gemini API for interactive queries about the TSLA data.

## Features

- Interactive candlestick chart with volume bars.
- Support and resistance bands visualization.
- Moving averages (20 and 50 periods).
- Direction markers indicating LONG, SHORT, or None signals.
- Animation mode to replay bars dynamically.
- AI chatbot tab integrated with Gemini API for natural language queries.

## Setup and Installation

### Prerequisites

- Python 3.10 or higher
- Streamlit
- Pandas
- Plotly
- Google Generative AI Python client (`google-generative-ai`)

### Installation

1. Clone the repository or download the source code.

2. Create and activate a Python virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Set your Gemini API key as an environment variable:

```bash
export GEMINI_API_KEY="your_api_key_here"  # On Windows: set GEMINI_API_KEY=your_api_key_here
```

5. Run the Streamlit app:

```bash
streamlit run app.py
```

## Files

- `app.py`: Main Streamlit application script.
- `tsla_data.csv`: Tesla stock data with support/resistance and signals.
- `requirements.txt`: Python package dependencies.

## Usage

- Use the sidebar to filter data by date range.
- Toggle animation mode to replay the candlestick bars.
- Use the AI Chatbot tab to ask questions about the TSLA data.

## Notes

- Ensure you have a valid Gemini API key for the chatbot functionality.
- The app uses Plotly for interactive charts.

## License

MIT License
