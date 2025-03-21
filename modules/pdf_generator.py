#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PDF Generator module using pdfkit and Jinja2 templates
"""

import os
import logging
import platform
from datetime import datetime
import tempfile
import pdfkit
from jinja2 import Environment, FileSystemLoader
from config import Config

logger = logging.getLogger(__name__)

# Initialize Jinja2 environment
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
env = Environment(loader=FileSystemLoader(template_dir))

# Determine the path to wkhtmltopdf based on the environment
if platform.system() == 'Darwin':  # macOS
    WKHTMLTOPDF_PATH = '/usr/local/bin/wkhtmltopdf'
elif platform.system() == 'Windows':  # Windows
    WKHTMLTOPDF_PATH = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
else:  # Linux (Render)
    WKHTMLTOPDF_PATH = '/usr/bin/wkhtmltopdf'

def generate_pdf(user_data, sections_content):
    """
    Generate a PDF report based on user data and section content
    
    Args:
        user_data (dict): User's values and personal information
        sections_content (dict): Content for each section of the report
        
    Returns:
        tuple: (success, pdf_path or error_message)
    """
    try:
        # Prepare template data
        template_data = {
            'user_name': user_data.get('telegram_username', 'User'),
            'generation_date': datetime.now().strftime('%B %d, %Y'),
            'top_values': user_data.get('top_values', [])[:5],
            'next_values': user_data.get('next_values', [])[:5],
            'age': user_data.get('age', 'Not specified'),
            'country': user_data.get('country', 'Not specified'),
            'occupation': user_data.get('occupation', 'Not specified'),
            'sections': []
        }
        
        # Format sections
        for section in Config.REPORT_SECTIONS:
            section_title = section['title']
            section_content = sections_content.get(section_title, 'Content not available')
            
            template_data['sections'].append({
                'title': section_title,
                'content': section_content
            })
        
        # Load template
        template = env.get_template('report_template.html')
        
        # Render template
        html_content = template.render(**template_data)
        
        # Create temporary file for HTML
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as html_tmp:
            html_path = html_tmp.name
            html_tmp.write(html_content.encode('utf-8'))
        
        # Create PDF filename
        pdf_path = html_path.replace('.html', '.pdf')
        
        # Configure PDF options
        pdf_options = {
            'page-size': 'A4',
            'margin-top': '20mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            'encoding': 'UTF-8',
            'no-outline': None
        }
        
        # Configure pdfkit with proper wkhtmltopdf path
        config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
        
        # Generate PDF
        pdfkit.from_file(html_path, pdf_path, options=pdf_options, configuration=config)
        
        # Clean up the temporary HTML file
        if os.path.exists(html_path):
            os.unlink(html_path)
        
        logger.info(f"PDF generated successfully at {pdf_path}")
        
        return True, pdf_path
    
    except Exception as e:
        logger.error(f"Error generating PDF: {e}", exc_info=True)
        return False, f"Error generating PDF: {str(e)}"

def cleanup_pdf(pdf_path):
    """
    Remove the temporary PDF file after it has been sent
    
    Args:
        pdf_path (str): Path to the PDF file
    """
    try:
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)
            logger.info(f"Temporary PDF file removed: {pdf_path}")
    except Exception as e:
        logger.error(f"Error removing temporary PDF file: {e}")