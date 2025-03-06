import pandas as pd
import base64
import io
from datetime import datetime

def generate_csv_download_link(df):
    """Generate a link to download the dataframe as CSV"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'data:file/csv;base64,{b64}'
    return href

def generate_pdf_report(df, report_type="shipments"):
    """Generate a PDF report of the data"""
    buffer = io.BytesIO()
    
    # Convert DataFrame to HTML for PDF
    html = f"""
    <h2>{report_type.title()} Report</h2>
    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    {df.to_html()}
    """
    
    return html

def parse_uploaded_csv(uploaded_file):
    """Parse uploaded CSV file and validate data"""
    try:
        df = pd.read_csv(uploaded_file)
        required_columns = ['origin', 'destination', 'departure_time']
        
        # Validate columns
        if not all(col in df.columns for col in required_columns):
            return None, "Missing required columns: origin, destination, departure_time"
        
        return df, None
    except Exception as e:
        return None, f"Error parsing CSV: {str(e)}"
