"""Data processing utilities for AI Data Analyst."""
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np


def load_dataset(file_path: str) -> pd.DataFrame:
    """Load a CSV or Excel dataset."""
    try:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to load dataset: {e}")


def profile_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """Profile a loaded dataset and return key statistics."""
    if df is None or df.empty:
        return {"rows": 0, "columns": 0, "memory_mb": 0}
    
    rows = len(df)
    cols = len(df.columns)
    memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
    
    num_cols = 0
    cat_cols = 0
    date_cols = 0
    bool_cols = 0
    
    for col in df.columns:
        dtype = df[col].dtype
        if pd.api.types.is_numeric_dtype(dtype):
            num_cols += 1
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            date_cols += 1
        elif pd.api.types.is_bool_dtype(dtype):
            bool_cols += 1
        else:
            cat_cols += 1
    
    missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()
    unique_counts = {col: int(df[col].nunique()) for col in df.columns}
    
    return {
        "rows": rows,
        "columns": cols,
        "memory_mb": round(memory_mb, 2),
        "numeric_columns": num_cols,
        "categorical_columns": cat_cols,
        "date_columns": date_cols,
        "boolean_columns": bool_cols,
        "missing_values": int(missing),
        "duplicate_rows": int(duplicates),
        "unique_counts": unique_counts,
    }


def clean_dataset(df: pd.DataFrame) -> tuple:
    """Clean a dataset and return cleaned version plus summary."""
    original_shape = df.shape
    df_clean = df.drop_duplicates()
    duplicates_removed = original_shape[0] - df_clean.shape[0]
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df_clean[col].isnull().any():
            median_val = df_clean[col].median()
            df_clean[col].fillna(median_val, inplace=True)
    
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df_clean[col].isnull().any():
            mode_val = df_clean[col].mode()[0] if not df_clean[col].mode().empty else 'Unknown'
            df_clean[col].fillna(mode_val, inplace=True)
    
    summary = {
        "original_rows": original_shape[0],
        "cleaned_rows": df_clean.shape[0],
        "duplicates_removed": duplicates_removed,
        "missing_after_cleaning": df_clean.isnull().sum().sum(),
        "numeric_columns": len(numeric_cols),
        "categorical_columns": len(categorical_cols),
    }
    return df_clean, summary
