"""Core analytics engine for AI Data Analyst (Part 1)."""
from typing import Dict, List, Any, Tuple
import pandas as pd
import numpy as np
from .data import load_dataset, profile_dataset, clean_dataset, generate_summary_report


def run_exploratory_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """Run exploratory data analysis on the dataset."""
    if df is None or df.empty:
        return {"status": "no_data", "message": "Empty dataset"}
    
    # Numerical statistics
    numeric_stats = df.describe().to_dict()
    
    # Categorical frequencies
    categorical_stats = {}
    for col in df.select_dtypes(include=['object']).columns:
        freq = df[col].value_counts().to_dict()
        categorical_stats[col] = freq
    
    # Date-based aggregations
    if 'Date' in df.columns:
        # Convert date to datetime if not already
        df_copy = df.copy()
        df_copy['Date'] = pd.to_datetime(df_copy['Date'], dayfirst=True, errors='coerce')
        date_stats = df_copy['Date'].dt.to_period('M').value_counts().sort_index().to_dict()
    else:
        date_stats = {}
    
    return {
        "numerical_summary": numeric_stats,
        "categorical_summary": categorical_stats,
        "date_aggregations": str(date_stats),
    }


def run_correlation_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate correlation matrix for numerical columns."""
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.shape[1] >= 2:
        corr_matrix = numeric_df.corr()
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                val = abs(corr_matrix.iloc[i, j])
                if val > 0.5:
                    col1, col2 = corr_matrix.columns[i], corr_matrix.columns[j]
                    strong_correlations.append({
                        "pair": f"{col1} vs {col2}",
                        "correlation": round(val, 3),
                        "direction": "positive" if corr_matrix.iloc[i, j] > 0 else "negative"
                    })
        return {
            "strong_correlations": strong_correlations,
            "total_numerical_pairs": len(strong_correlations)
        }
    else:
        return {"message": "Not enough numerical columns for correlation analysis"}


def run_outlier_detection(df: pd.DataFrame) -> Dict[str, Any]:
    """Detect outliers using IQR method."""
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.shape[1] == 0:
        return {"message": "No numerical columns for outlier detection"}
    
    outliers = {}
    for col in numeric_df.columns:
        Q1 = numeric_df[col].quantile(0.25)
        Q3 = numeric_df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        below = ((numeric_df[col] < lower_bound).sum())
        above = ((numeric_df[col] > upper_bound).sum())
        outliers[col] = {
            "lower_bound": round(lower_bound, 2),
            "upper_bound": round(upper_bound, 2),
            "outliers_below": int(below),
            "outliers_above": int(above),
            "percentage": round((below + above) / len(numeric_df) * 100, 2)
        }
    return outliers
