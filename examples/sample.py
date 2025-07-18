"""
Sample usage of cacao_pandas_ui with pandas DataFrames.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from cacao_pandas_ui import preview_dataframe, PandasTablePage, create_advanced_table


def create_sample_dataframe():
    """
    Create a sample DataFrame with various data types for testing.
    """
    np.random.seed(42)
    n_rows = 50
    
    # Create sample data with various types
    data = {
        'ID': range(1, n_rows + 1),
        'Name': [f'Employee_{i}' for i in range(1, n_rows + 1)],
        'Age': np.random.randint(22, 65, n_rows),
        'Salary': np.random.normal(75000, 25000, n_rows).round(2),
        'Department': np.random.choice(['Engineering', 'Marketing', 'Sales', 'HR', 'Finance'], n_rows),
        'Join_Date': [datetime.now() - timedelta(days=np.random.randint(30, 2000)) for _ in range(n_rows)],
        'Performance_Score': np.random.uniform(2.5, 5.0, n_rows).round(2),
        'Is_Active': np.random.choice([True, False], n_rows, p=[0.85, 0.15]),
        'Bonus_Percentage': np.random.uniform(0, 25, n_rows).round(1),
        'Projects_Count': np.random.randint(0, 15, n_rows)
    }
    
    df = pd.DataFrame(data)
    
    # Add some missing values for testing
    df.loc[5:8, 'Bonus_Percentage'] = np.nan
    df.loc[2, 'Performance_Score'] = np.nan
    
    return df


def demo_basic_usage():
    """
    Demonstrate basic usage of preview_dataframe.
    """
    print("Creating sample DataFrame...")
    df = create_sample_dataframe()
    
    print(f"DataFrame shape: {df.shape}")
    print(f"DataFrame columns: {list(df.columns)}")
    print(f"DataFrame dtypes:\n{df.dtypes}")
    print("\nFirst 5 rows:")
    print(df.head())
    
    print("\n--- Opening DataFrame in advanced table mode ---")
    preview_dataframe(
        df, 
        title="Employee Data - Advanced Table",
        mode="advanced",
        width=1200,
        height=800
    )


def demo_simple_mode():
    """
    Demonstrate simple table mode.
    """
    print("\n--- Creating a smaller dataset for simple mode ---")
    small_df = pd.DataFrame({
        'Product': ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'],
        'Price': [1.20, 0.80, 3.50, 2.00, 4.75],
        'Stock': [50, 100, 25, 30, 10],
        'Category': ['Fruit', 'Fruit', 'Fruit', 'Fruit', 'Berry']
    })
    
    print("Simple DataFrame:")
    print(small_df)
    
    print("\n--- Opening DataFrame in simple table mode ---")
    preview_dataframe(
        small_df,
        title="Product Inventory - Simple Table",
        mode="simple",
        width=800,
        height=500
    )


def demo_advanced_features():
    """
    Demonstrate advanced DataFrame features.
    """
    print("\n--- Creating DataFrame with complex data types ---")
    
    # Create DataFrame with various data types
    df = pd.DataFrame({
        'Timestamp': pd.date_range('2023-01-01', periods=20, freq='D'),
        'Category': pd.Categorical(['A', 'B', 'C'] * 6 + ['A', 'B']),
        'Value': np.random.randn(20).cumsum(),
        'Count': np.random.randint(1, 100, 20),
        'Flag': np.random.choice([True, False], 20),
        'Grade': pd.Categorical(['Good', 'Better', 'Best'] * 6 + ['Good', 'Better'], 
                               categories=['Good', 'Better', 'Best'], ordered=True)
    })
    
    print("Complex DataFrame:")
    print(df.head(10))
    print(f"\nData types:\n{df.dtypes}")
    
    print("\n--- Opening complex DataFrame ---")
    preview_dataframe(
        df,
        title="Complex Data Types Demo",
        mode="advanced",
        width=1000,
        height=700
    )


def main():
    """
    Main function to run the demonstrations.
    """
    print("=" * 50)
    print("Cacao Pandas UI - Sample Demonstrations")
    print("=" * 50)
    
    # Run basic demo
    demo_basic_usage()
    
    # Uncomment the lines below to run additional demos
    # demo_simple_mode()
    # demo_advanced_features()


if __name__ == "__main__":
    main()