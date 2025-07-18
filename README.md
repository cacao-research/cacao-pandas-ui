# 🍫 cacao-pandas-ui

<img width="898" height="563" alt="image" src="https://github.com/user-attachments/assets/17f6aa69-5879-4ead-85c9-1f2dc745baf4" />

A pandas DataFrame table viewer with interactive desktop UI built on Cacao framework.

## Installation

```bash
pip install cacao-pandas-ui
```

## Features

- 🐼 **Pandas DataFrame Viewer**: Native pandas DataFrame table display
- 🖥️ **Desktop Application**: Cross-platform desktop window using Cacao
- 📊 **Multiple Table Modes**: Simple and advanced table views
- 🎯 **Interactive Features**: Sorting, filtering, pagination, and selection in advanced mode
- 📁 **Multiple File Formats**: CSV, Excel, JSON, Parquet, TSV, and Pickle support
- 🔧 **CLI Support**: Command-line interface with extensive options
- 🎨 **Customizable**: Configurable window size, titles, and table modes
- 🔄 **Type Preservation**: Maintains pandas data types and handles missing values
- 📋 **Export Options**: Export functionality in advanced mode
- 🎲 **Sample Data**: Built-in sample data generation for testing

## Usage

### Programmatic Usage 🍫

#### Basic Example

```python
import pandas as pd
from cacao_pandas_ui import preview_dataframe

# Create or load your DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'Age': [25, 30, 35, 28],
    'Department': ['Engineering', 'Marketing', 'Sales', 'HR'],
    'Salary': [75000, 65000, 70000, 60000]
})

# Preview in a desktop window
preview_dataframe(df, title="Employee Data")
```

#### Alternative Import Syntax

```python
import pandas as pd
from cacao_pandas_ui import preview  # Cleaner alias

# Load data from CSV
df = pd.read_csv('data.csv')

# Preview with custom settings
preview(df, title="CSV Data", width=1200, height=800, mode="advanced")
```

#### Advanced Table Mode

```python
from cacao_pandas_ui import preview_dataframe
import pandas as pd
import numpy as np

# Create DataFrame with various data types
df = pd.DataFrame({
    'ID': range(1, 101),
    'Name': [f'User_{i}' for i in range(1, 101)],
    'Score': np.random.uniform(0, 100, 100),
    'Active': np.random.choice([True, False], 100),
    'Join_Date': pd.date_range('2020-01-01', periods=100, freq='D')
})

# Advanced mode with interactive features
preview_dataframe(
    df, 
    title="Advanced Table Demo",
    mode="advanced",  # Enables sorting, filtering, pagination
    width=1200,
    height=800
)
```

#### Simple Table Mode

```python
from cacao_pandas_ui import preview_dataframe

# Small dataset for simple viewing
df = pd.DataFrame({
    'Product': ['Apple', 'Banana', 'Cherry'],
    'Price': [1.20, 0.80, 3.50],
    'Stock': [50, 100, 25]
})

# Simple mode for basic display
preview_dataframe(
    df,
    title="Product Inventory",
    mode="simple",
    width=800,
    height=500
)
```

### Function Parameters

```python
preview_dataframe(
    dataframe,                        # pandas DataFrame to display
    title="Pandas DataFrame Viewer",  # Window title
    width=1000,                       # Window width in pixels
    height=700,                       # Window height in pixels
    mode="advanced"                   # Table mode: "simple" or "advanced"
)
```

### Command Line Interface

#### Basic Usage

```bash
# View a CSV file
cacao-pandas-ui data.csv

# View an Excel file
cacao-pandas-ui data.xlsx

# View with custom window settings
cacao-pandas-ui data.csv --title "Sales Data" --width 1200 --height 800

# Use simple table mode
cacao-pandas-ui data.csv --mode simple
```

#### Sample Data Generation

```bash
# Generate and view sample data
cacao-pandas-ui --sample

# Sample data with custom settings
cacao-pandas-ui --sample --title "Sample Data" --mode advanced
```

#### File Format Support

```bash
# CSV files
cacao-pandas-ui data.csv
cacao-pandas-ui data.csv --delimiter ";" --encoding "utf-8"

# Excel files
cacao-pandas-ui data.xlsx
cacao-pandas-ui data.xlsx --sheet "Sheet2"

# JSON files
cacao-pandas-ui data.json

# Parquet files
cacao-pandas-ui data.parquet

# TSV files
cacao-pandas-ui data.tsv
cacao-pandas-ui data.tab

# Pickle files
cacao-pandas-ui data.pkl
cacao-pandas-ui data.pickle
```

#### CLI Options

```bash
# General options
--title TITLE           Window title
--width WIDTH           Window width in pixels (default: 1000)
--height HEIGHT         Window height in pixels (default: 700)
--mode {simple,advanced} Table display mode (default: advanced)
--sample                Use sample data instead of file

# File-specific options
--delimiter DELIMITER   Delimiter for CSV files (default: ',')
--encoding ENCODING     File encoding (default: 'utf-8')
--header HEADER         Row number for column names (default: 0)
--sheet SHEET          Sheet name for Excel files
```

### Advanced Usage Examples

#### Working with Different Data Types

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from cacao_pandas_ui import preview_dataframe

# Create DataFrame with complex data types
df = pd.DataFrame({
    'Timestamp': pd.date_range('2023-01-01', periods=50, freq='D'),
    'Category': pd.Categorical(['A', 'B', 'C'] * 16 + ['A', 'B']),
    'Value': np.random.randn(50).cumsum(),
    'Count': np.random.randint(1, 100, 50),
    'Flag': np.random.choice([True, False], 50),
    'Grade': pd.Categorical(['Good', 'Better', 'Best'] * 16 + ['Good', 'Better'])
})

# Handle missing values
df.loc[5:10, 'Value'] = np.nan

preview_dataframe(df, title="Complex Data Types")
```

#### Using Table Components

```python
from cacao_pandas_ui import create_advanced_table, create_simple_table

# Create table components for custom applications
df = pd.read_csv('data.csv')

# Create advanced table component
advanced_table = create_advanced_table(df, title="Advanced View")

# Create simple table component
simple_table = create_simple_table(df, title="Simple View")
```

## Table Modes

### Simple Mode
- Basic table display
- Minimal styling
- Fast rendering
- Best for small datasets

### Advanced Mode (Default)
- Interactive features:
  - **Sorting**: Click column headers to sort
  - **Filtering**: Column-based filtering
  - **Pagination**: Navigate through large datasets (50 rows per page)
  - **Selection**: Multiple row selection
  - **Export**: Export to CSV and Excel formats
- Enhanced styling with hover effects
- Better for large datasets and interactive exploration

## Supported File Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| CSV | `.csv` | Comma-separated values |
| Excel | `.xlsx`, `.xls` | Microsoft Excel files |
| JSON | `.json` | JavaScript Object Notation |
| Parquet | `.parquet` | Apache Parquet format |
| TSV | `.tsv`, `.tab` | Tab-separated values |
| Pickle | `.pkl`, `.pickle` | Python pickle format |

## Requirements

- Python 3.8+
- pandas >= 1.0.0
- cacao framework
- numpy (for sample data generation)

## API Reference

### Core Functions

#### `preview_dataframe(dataframe, title, width, height, mode)`
Main function to preview pandas DataFrame in desktop window.

**Parameters:**
- `dataframe` (pd.DataFrame): The pandas DataFrame to display
- `title` (str): Window title (default: "Pandas DataFrame Viewer")
- `width` (int): Window width in pixels (default: 1000)
- `height` (int): Window height in pixels (default: 700)
- `mode` (str): Table mode - "simple" or "advanced" (default: "advanced")

#### `preview(dataframe, **kwargs)`
Alias for `preview_dataframe()` with same parameters.

### Classes

#### `PandasTablePage(dataframe, title, mode)`
Core class for rendering pandas DataFrame as table component.

**Methods:**
- `render()`: Returns Cacao component structure
- `_prepare_table_data()`: Prepares DataFrame for table display
- `_create_table_component()`: Creates appropriate table component

### Helper Functions

#### `create_simple_table(dataframe, **kwargs)`
Creates a simple table component from pandas DataFrame.

#### `create_advanced_table(dataframe, **kwargs)`
Creates an advanced table component from pandas DataFrame.

## Examples

Complete examples are available in the `examples/` directory:

- `sample.py`: Comprehensive usage examples
- `sample_data.csv`: Sample CSV data for testing

## License

MIT