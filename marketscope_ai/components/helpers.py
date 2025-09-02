import plotly.graph_objects as go
import pandas as pd

# ---------- Plot Helpers ----------
def _apply_dark_layout(fig: go.Figure, title: str = None) -> go.Figure:
    """Apply consistent dark theme to a plotly figure and optionally set title."""
    if title:
        fig.update_layout(title=dict(text=title, x=0.5))  # center title
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig


# ---------- Format Helpers ----------
def _fmt_num(val):
    """Format large numbers with commas or return 'N/A' for missing values."""
    if isinstance(val, (int, float)):
        try:
            return f"{val:,.0f}" if float(val).is_integer() else f"{val:,.2f}"
        except Exception:
            return str(val)
    return "N/A"


def _fmt_percent(val):
    """Format a number as percentage string with 2 decimals."""
    if isinstance(val, (int, float)):
        return f"{val:.2%}"
    return "N/A"


# ---------- Data Validation Helpers ----------
def _safe_df(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure dataframe is valid, else return empty DataFrame."""
    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        return pd.DataFrame()
    return df


def _safe_series(series: pd.Series) -> pd.Series:
    """Ensure series is valid, else return empty Series."""
    if series is None or not isinstance(series, pd.Series) or series.empty:
        return pd.Series(dtype="float64")
    return series
