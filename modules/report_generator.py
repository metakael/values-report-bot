#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Report Generator module using Jinja2 templates with markdown support
"""

import os
import logging
import base64
from datetime import datetime
import tempfile
from jinja2 import Environment, FileSystemLoader
import markdown
from config import Config

logger = logging.getLogger(__name__)

# Initialize Jinja2 environment
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
env = Environment(loader=FileSystemLoader(template_dir))

def get_base64_logo():
    """
    Convert logo to base64 for embedding in HTML
    
    Returns:
        str: base64 encoded image string with data URI prefix
    """
    # Path to your logo file in your project
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'logo.png')
    
    try:
        with open(logo_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:image/png;base64,{encoded_string}"
    except Exception as e:
        logger.error(f"Error encoding logo: {e}")
        # Return empty string or a placeholder if logo can't be found
        return ""

def generate_report(user_data, sections_content):
    """
    Generate an HTML report based on user data and section content
    
    Args:
        user_data (dict): User's values and personal information
        sections_content (dict): Content for each section of the report
        
    Returns:
        tuple: (success, html_path or error_message)
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
            'sections': [],
            'logo_base64': get_base64_logo()  # Add the base64 encoded logo
        }
        
        # Format sections with markdown conversion
        for section in Config.REPORT_SECTIONS:
            section_title = section['title']
            raw_content = sections_content.get(section_title, 'Content not available')
            
            # Convert markdown to HTML
            html_content = markdown.markdown(
                raw_content,
                extensions=['extra', 'nl2br', 'sane_lists']
            )
            
            template_data['sections'].append({
                'title': section_title,
                'content': html_content
            })
        
        # Load template
        template = env.get_template('report_template.html')
        
        # Render template
        html_content = template.render(**template_data)
        
        # Create temporary file for HTML
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as html_tmp:
            html_path = html_tmp.name
            html_tmp.write(html_content.encode('utf-8'))
        
        logger.info(f"HTML report generated successfully at {html_path}")
        
        return True, html_path
    
    except Exception as e:
        logger.error(f"Error generating HTML report: {e}", exc_info=True)
        return False, f"Error generating report: {str(e)}"

def cleanup_report(report_path):
    """
    Remove the temporary report file after it has been sent
    """
    try:
        if os.path.exists(report_path):
            os.unlink(report_path)
            logger.info(f"Temporary report file removed: {report_path}")
    except Exception as e:
        logger.error(f"Error removing temporary report file: {e}")