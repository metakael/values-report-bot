#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PDF Generator module using WeasyPrint and Jinja2 templates
"""

import os
import logging
from datetime import datetime
import tempfile
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from config import Config

logger = logging.getLogger(__name__)

# Initialize Jinja2 environment
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
env = Environment(loader=FileSystemLoader(template_dir))

def generate_pdf(user_data, sections_content):
    """Generate a PDF report based on user data and section content"""
    try:
        # Calculate absolute paths
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        static_dir = os.path.join(base_dir, 'static')
        
        # Create file URLs for resources
        fonts_dir = f"file://{os.path.join(static_dir, 'fonts')}"
        logo_path = f"file://{os.path.join(static_dir, 'images', 'logo.png')}"
        css_file = os.path.join(static_dir, 'css', 'style.css')
        
        # Prepare template data
        template_data = {
            'user_name': user_data.get('telegram_username', 'User'),
            'generation_date': datetime.now().strftime('%B %d, %Y'),
            'top_values': user_data.get('top_values', [])[:5],
            'next_values': user_data.get('next_values', [])[:5],
            'age': user_data.get('age', 'Not specified'),
            'country': user_data.get('country', 'Not specified'),
            'occupation': user_data.get('occupation', 'Not specified'),
            'sections': [],
            'fonts_dir': fonts_dir,
            'logo_path': logo_path
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
        
        # Create temporary file for PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            pdf_path = tmp.name
        
        # Generate PDF (fix the constructor call)
        html = HTML(string=html_content, base_url=f"file://{base_dir}")
        css = CSS(filename=css_file)
        html.write_pdf(pdf_path, stylesheets=[css])
        
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