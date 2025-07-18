"""
Pandas DataFrame Table Viewer for Cacao
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

try:
    from cacao.ui.components.data import Table, create_simple_table, create_advanced_table
    from cacao.extensions.plugins.pandas_table import PandasTablePlugin
    CACAO_COMPONENTS_AVAILABLE = True
except ImportError:
    CACAO_COMPONENTS_AVAILABLE = False


class PandasTablePage:
    """
    A page class that renders pandas DataFrames as interactive tables.
    """
    
    def __init__(self, dataframe, title=None, mode="advanced"):
        """
        Initialize the PandasTablePage.
        
        Args:
            dataframe: pandas DataFrame to display
            title: Title for the table display (optional, but will be ignored for display)
            mode: "simple" or "advanced" table mode
        """
        if not isinstance(dataframe, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
        
        self.dataframe = dataframe
        self.title = title
        self.mode = mode
        
        # Initialize PandasTablePlugin
        if CACAO_COMPONENTS_AVAILABLE:
            self.plugin = PandasTablePlugin(
                enhanced_mode=(mode == "advanced"),
                row_threshold=100,
                memory_threshold_mb=1
            )

    def _prepare_table_data(self):
        """
        Prepare DataFrame data for table display.
        
        Returns:
            dict: Table data structure compatible with cacao table components
        """
        # Convert DataFrame to table-compatible format
        df = self.dataframe.copy()
        
        # Handle missing values
        df = df.fillna("N/A")
        
        # Convert to records format for table
        columns = [{"key": col, "title": col, "dataType": str(df[col].dtype)} 
                  for col in df.columns]
        
        # Convert DataFrame to list of dictionaries
        data = []
        for idx, row in df.iterrows():
            row_data = {"_index": str(idx)}
            for col in df.columns:
                value = row[col]
                # Handle different data types
                if pd.isna(value):
                    row_data[col] = "N/A"
                elif isinstance(value, (int, float)):
                    row_data[col] = value
                elif isinstance(value, (datetime, pd.Timestamp)):
                    row_data[col] = value.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    row_data[col] = str(value)
            data.append(row_data)
        
        return {
            "columns": columns,
            "data": data,
            "totalRows": len(df),
            "shape": df.shape
        }

    def _create_toolbar(self):
        """
        Create Excel-like toolbar with action buttons.
        
        Returns:
            dict: Toolbar component structure
        """
        return {
            "type": "div",
            "props": {
                "style": {
                    "display": "flex",
                    "alignItems": "center",
                    "padding": "8px 12px",
                    "backgroundColor": "#F8F9FA",
                    "borderBottom": "1px solid #E2E8F0",
                    "gap": "8px",
                    "fontFamily": "Arial, sans-serif",
                    "fontSize": "13px"
                },
                "children": [
                    {
                        "type": "button",
                        "props": {
                            "label": "Download CSV",
                            "style": {
                                "padding": "6px 12px",
                                "backgroundColor": "#4CAF50",
                                "color": "white",
                                "border": "none",
                                "borderRadius": "4px",
                                "cursor": "pointer",
                                "fontSize": "13px",
                                "fontWeight": "500"
                            }
                        }
                    },
                    {
                        "type": "button",
                        "props": {
                            "label": "Download Excel",
                            "style": {
                                "padding": "6px 12px",
                                "backgroundColor": "#2196F3",
                                "color": "white",
                                "border": "none",
                                "borderRadius": "4px",
                                "cursor": "pointer",
                                "fontSize": "13px",
                                "fontWeight": "500"
                            }
                        }
                    },
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "marginLeft": "auto",
                                "color": "#666",
                                "fontSize": "12px"
                            },
                            "content": f"Rows: {self.dataframe.shape[0]} | Columns: {self.dataframe.shape[1]}"
                        }
                    }
                ]
            }
        }

    def render(self):
        """
        Render the pandas DataFrame as a table component with Excel-like interface.
        
        Returns:
            dict: Cacao component structure for rendering
        """
        # Use PandasTablePlugin if available, otherwise fallback to basic implementation
        if CACAO_COMPONENTS_AVAILABLE:
            table_component = self.plugin.process(self.dataframe)
            
            # Create Excel-like layout with toolbar and no title
            return {
                "type": "div",
                "props": {
                    "style": {
                        "height": "100%",
                        "display": "flex",
                        "flexDirection": "column",
                        "backgroundColor": "#FFFFFF",
                        "fontFamily": "Arial, sans-serif"
                    },
                    "children": [
                        self._create_toolbar(),
                        {
                            "type": "div",
                            "props": {
                                "style": {
                                    "flex": "1",
                                    "overflow": "auto",
                                    "border": "1px solid #E2E8F0"
                                },
                                "children": [table_component.render()]
                            }
                        }
                    ]
                }
            }
        else:
            # Fallback to basic implementation
            table_data = self._prepare_table_data()
            
            # Create Excel-like layout with toolbar and no title
            return {
                "type": "div",
                "props": {
                    "style": {
                        "height": "100%",
                        "display": "flex",
                        "flexDirection": "column",
                        "backgroundColor": "#FFFFFF",
                        "fontFamily": "Arial, sans-serif"
                    },
                    "children": [
                        self._create_toolbar(),
                        {
                            "type": "div",
                            "props": {
                                "style": {
                                    "flex": "1",
                                    "overflow": "auto",
                                    "border": "1px solid #E2E8F0"
                                },
                                "children": [self._create_table_component(table_data)]
                            }
                        }
                    ]
                }
            }

    def _create_table_component(self, table_data):
        """
        Create the appropriate table component based on mode.
        
        Args:
            table_data: Prepared table data
            
        Returns:
            dict: Table component structure
        """
        if self.mode == "simple":
            return self._create_simple_table(table_data)
        else:
            return self._create_advanced_table(table_data)

    def _create_simple_table(self, table_data):
        """
        Create a simple table component with Excel-like styling.
        
        Args:
            table_data: Prepared table data
            
        Returns:
            dict: Simple table component
        """
        return {
            "type": "table",
            "props": {
                "id": "pandasTable",
                "columns": table_data["columns"],
                "data": table_data["data"],
                "style": {
                    "width": "100%",
                    "border": "1px solid #D4D4D4",
                    "borderCollapse": "collapse",
                    "fontSize": "13px",
                    "fontFamily": "Arial, sans-serif",
                    "backgroundColor": "#FFFFFF"
                },
                "headerStyle": {
                    "backgroundColor": "#F2F2F2",
                    "fontWeight": "bold",
                    "padding": "6px 8px",
                    "textAlign": "left",
                    "border": "1px solid #D4D4D4",
                    "color": "#333333"
                },
                "cellStyle": {
                    "padding": "6px 8px",
                    "border": "1px solid #D4D4D4",
                    "textAlign": "left",
                    "verticalAlign": "top"
                },
                "rowStyle": {
                    "hover": {
                        "backgroundColor": "#E8F4FD"
                    }
                }
            }
        }

    def _create_advanced_table(self, table_data):
        """
        Create an advanced table component with enhanced Excel-like features.
        
        Args:
            table_data: Prepared table data
            
        Returns:
            dict: Advanced table component using proper cacao Table
        """
        # Use cacao Table component with advanced features
        if CACAO_COMPONENTS_AVAILABLE:
            # Create table headers from DataFrame columns
            headers = [col["title"] for col in table_data["columns"]]
            
            # Create table rows from DataFrame data
            rows = []
            for row_data in table_data["data"]:
                row = [row_data.get(col["key"], "") for col in table_data["columns"]]
                rows.append(row)
            
            # Create Table component with advanced features
            table = Table(headers=headers, rows=rows, advanced=True)
            return table.render()
        else:
            # Fallback to Excel-like HTML table structure
            return {
                "type": "table",
                "props": {
                    "id": "pandasAdvancedTable",
                    "columns": table_data["columns"],
                    "data": table_data["data"],
                    "style": {
                        "width": "100%",
                        "border": "1px solid #D4D4D4",
                        "borderCollapse": "collapse",
                        "fontSize": "13px",
                        "fontFamily": "Arial, sans-serif",
                        "backgroundColor": "#FFFFFF"
                    },
                    "headerStyle": {
                        "backgroundColor": "#F2F2F2",
                        "color": "#333333",
                        "fontWeight": "bold",
                        "padding": "6px 8px",
                        "textAlign": "left",
                        "border": "1px solid #D4D4D4",
                        "position": "sticky",
                        "top": "0",
                        "zIndex": "1"
                    },
                    "cellStyle": {
                        "padding": "6px 8px",
                        "border": "1px solid #D4D4D4",
                        "textAlign": "left",
                        "verticalAlign": "top"
                    },
                    "rowStyle": {
                        "hover": {
                            "backgroundColor": "#E8F4FD"
                        },
                        "alternating": {
                            "backgroundColor": "#FAFAFA"
                        }
                    }
                }
            }


def preview_dataframe(dataframe, title=None, width=1000, height=700, mode="advanced"):
    """
    Preview pandas DataFrame in a desktop window.

    Args:
        dataframe: pandas DataFrame to display
        title: Window and table title (optional, default: None)
        width: Window width (default: 1000)
        height: Window height (default: 700)
        mode: Table mode - "simple" or "advanced" (default: "advanced")
    
    Example:
        import pandas as pd
        from cacao_pandas_ui import preview_dataframe
        
        # Create sample DataFrame
        df = pd.DataFrame({
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'City': ['New York', 'London', 'Tokyo']
        })
        
        # Preview in desktop window with title
        preview_dataframe(df, title="Sample Data", mode="advanced")
        
        # Preview without title
        preview_dataframe(df, mode="simple")
    """
    import sys
    
    # Prevent infinite loops in framework reload scenarios
    if hasattr(sys, '_cacao_pandas_viewer_running'):
        print("Warning: Cacao Pandas UI is already running. Ignoring duplicate call.")
        return
    
    sys._cacao_pandas_viewer_running = True
    
    try:
        from cacao import App

        app = App()
        viewer = PandasTablePage(dataframe, title=title, mode=mode)

        @app.mix("/")
        def home():
            return viewer.render()

        # Set window title - use provided title or default
        window_title = title if title else "Pandas DataFrame Viewer"
        
        app.brew(
            type="desktop",
            title=window_title,
            width=width,
            height=height,
            resizable=True,
            fullscreen=False,
        )
    finally:
        if hasattr(sys, '_cacao_pandas_viewer_running'):
            delattr(sys, '_cacao_pandas_viewer_running')


def create_simple_table(dataframe, **kwargs):
    """
    Create a simple table component from a pandas DataFrame.
    
    Args:
        dataframe: pandas DataFrame
        **kwargs: Additional table properties
        
    Returns:
        PandasTablePage: Table page instance in simple mode
    """
    return PandasTablePage(dataframe, mode="simple", **kwargs)


def create_advanced_table(dataframe, **kwargs):
    """
    Create an advanced table component from a pandas DataFrame.
    
    Args:
        dataframe: pandas DataFrame
        **kwargs: Additional table properties
        
    Returns:
        PandasTablePage: Table page instance in advanced mode
    """
    return PandasTablePage(dataframe, mode="advanced", **kwargs)


# Alias for backward compatibility and convenience
preview = preview_dataframe
