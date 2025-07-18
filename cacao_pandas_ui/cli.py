"""
Command Line Interface for Cacao Pandas UI
"""
import sys
import argparse
import pandas as pd
from pathlib import Path
from cacao import App
from cacao_pandas_ui.viewer import PandasTablePage


def load_dataframe_from_file(filepath, **kwargs):
    """
    Load a DataFrame from various file formats.
    
    Args:
        filepath: Path to the data file
        **kwargs: Additional arguments for pandas read functions
        
    Returns:
        pandas.DataFrame: Loaded DataFrame
        
    Raises:
        ValueError: If file format is not supported
        Exception: If file cannot be read
    """
    filepath = Path(filepath)
    file_extension = filepath.suffix.lower()
    
    try:
        if file_extension == '.csv':
            return pd.read_csv(filepath, **kwargs)
        elif file_extension in ['.xlsx', '.xls']:
            return pd.read_excel(filepath, **kwargs)
        elif file_extension == '.json':
            return pd.read_json(filepath, **kwargs)
        elif file_extension == '.parquet':
            return pd.read_parquet(filepath, **kwargs)
        elif file_extension in ['.tsv', '.tab']:
            return pd.read_csv(filepath, sep='\t', **kwargs)
        elif file_extension == '.pkl' or file_extension == '.pickle':
            return pd.read_pickle(filepath, **kwargs)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    except Exception as e:
        raise Exception(f"Error loading file '{filepath}': {str(e)}")


def create_sample_dataframe():
    """
    Create a sample DataFrame for demonstration purposes.
    
    Returns:
        pandas.DataFrame: Sample DataFrame with various data types
    """
    import numpy as np
    from datetime import datetime, timedelta
    
    # Create sample data with various types
    np.random.seed(42)
    n_rows = 100
    
    return pd.DataFrame({
        'ID': range(1, n_rows + 1),
        'Name': [f'Person_{i}' for i in range(1, n_rows + 1)],
        'Age': np.random.randint(18, 80, n_rows),
        'Salary': np.random.normal(50000, 15000, n_rows).round(2),
        'Department': np.random.choice(['Engineering', 'Marketing', 'Sales', 'HR', 'Finance'], n_rows),
        'Join_Date': [datetime.now() - timedelta(days=np.random.randint(0, 3650)) for _ in range(n_rows)],
        'Performance_Score': np.random.uniform(1.0, 5.0, n_rows).round(2),
        'Is_Active': np.random.choice([True, False], n_rows, p=[0.8, 0.2])
    })


def main():
    """
    Main CLI function for Cacao Pandas UI.
    """
    parser = argparse.ArgumentParser(
        prog="cacao-pandas-ui",
        description="Open a desktop pandas DataFrame table viewer using Cacao"
    )
    
    parser.add_argument(
        "data_file", 
        nargs="?", 
        help="Path to data file (CSV, Excel, JSON, Parquet, TSV, or Pickle format)"
    )
    
    parser.add_argument(
        "--title", 
        default="Pandas DataFrame Viewer",
        help="Window title (default: 'Pandas DataFrame Viewer')"
    )
    
    parser.add_argument(
        "--width", 
        type=int, 
        default=1000,
        help="Window width in pixels (default: 1000)"
    )
    
    parser.add_argument(
        "--height", 
        type=int, 
        default=700,
        help="Window height in pixels (default: 700)"
    )
    
    parser.add_argument(
        "--mode", 
        choices=["simple", "advanced"], 
        default="advanced",
        help="Table display mode (default: advanced)"
    )
    
    parser.add_argument(
        "--sample", 
        action="store_true",
        help="Use sample data instead of loading from file"
    )
    
    # CSV-specific options
    parser.add_argument(
        "--delimiter", 
        default=",",
        help="Delimiter for CSV files (default: ',')"
    )
    
    parser.add_argument(
        "--encoding", 
        default="utf-8",
        help="File encoding (default: utf-8)"
    )
    
    parser.add_argument(
        "--header", 
        type=int, 
        default=0,
        help="Row number to use as column names (default: 0)"
    )
    
    parser.add_argument(
        "--sheet", 
        help="Sheet name for Excel files"
    )
    
    args = parser.parse_args()

    # Load DataFrame
    try:
        if args.sample:
            df = create_sample_dataframe()
            print("Using sample DataFrame with shape:", df.shape)
        elif args.data_file:
            # Prepare kwargs for file loading
            load_kwargs = {
                'encoding': args.encoding,
            }
            
            if args.data_file.endswith('.csv') or args.data_file.endswith('.tsv'):
                load_kwargs['delimiter'] = args.delimiter
                load_kwargs['header'] = args.header
            elif args.data_file.endswith(('.xlsx', '.xls')) and args.sheet:
                load_kwargs['sheet_name'] = args.sheet
            
            df = load_dataframe_from_file(args.data_file, **load_kwargs)
            print(f"Loaded DataFrame from '{args.data_file}' with shape: {df.shape}")
        else:
            print("Error: No data file specified and --sample not used.", file=sys.stderr)
            print("Use --help for usage information.", file=sys.stderr)
            sys.exit(1)
    
    except Exception as e:
        print(f"Error loading data: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate DataFrame
    if df.empty:
        print("Warning: DataFrame is empty", file=sys.stderr)
    
    # Create app and set up the page
    app = App()
    viewer = PandasTablePage(df, title=args.title, mode=args.mode)
    
    @app.mix("/")
    def home():
        return viewer.render()

    # Brew as desktop window
    app.brew(
        type="desktop",
        title=args.title,
        width=args.width,
        height=args.height,
        resizable=True,
        fullscreen=False,
    )


if __name__ == "__main__":
    main()