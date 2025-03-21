#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Report Generator module using Jinja2 templates
"""

import os
import logging
from datetime import datetime
import tempfile
from jinja2 import Environment, FileSystemLoader
from config import Config

logger = logging.getLogger(__name__)

# Initialize Jinja2 environment
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
env = Environment(loader=FileSystemLoader(template_dir))

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
            'sections': []
        }
        
        # Format sections
        for section in Config.REPORT_SECTIONS:
            section_title = section['title']
            section_content = sections_content.get(section_title, 'Content not available')

            # Process content to convert formatting to HTML
            processed_content = process_content_for_html(section_content)
            
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
        
        logger.info(f"HTML report generated successfully at {html_path}")
        
        return True, html_path
    
    except Exception as e:
        logger.error(f"Error generating HTML report: {e}", exc_info=True)
        return False, f"Error generating report: {str(e)}"

def cleanup_report(report_path):
    """
    Remove the temporary report file after it has been sent
    
    Args:
        report_path (str): Path to the report file
    """
    try:
        if os.path.exists(report_path):
            os.unlink(report_path)
            logger.info(f"Temporary report file removed: {report_path}")
    except Exception as e:
        logger.error(f"Error removing temporary report file: {e}")

def process_content_for_html(content):
    """
    Process LLM-generated content to proper HTML formatting
    
    Args:
        content (str): Raw content from LLM
        
    Returns:
        str: HTML-formatted content
    """
    import re
    
    # Replace asterisks with proper bold tags
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
    
    # Convert bullet point lists
    bullet_pattern = r'(\n\s*[-*]\s+.*?(?:\n|$))'
    bullets = re.findall(bullet_pattern, content, re.DOTALL)
    
    for bullet_block in bullets:
        html_list = '<ul>\n'
        for line in bullet_block.strip().split('\n'):
            if line.strip().startswith('-') or line.strip().startswith('*'):
                item_text = line.strip()[1:].strip()
                html_list += f'  <li>{item_text}</li>\n'
        html_list += '</ul>'
        content = content.replace(bullet_block, html_list)
    
    # Convert numbered lists
    numbered_pattern = r'(\n\s*\d+\.\s+.*?(?:\n|$))'
    numbered = re.findall(numbered_pattern, content, re.DOTALL)
    
    for numbered_block in numbered:
        html_list = '<ol>\n'
        for line in numbered_block.strip().split('\n'):
            if re.match(r'^\s*\d+\.', line):
                item_text = re.sub(r'^\s*\d+\.\s*', '', line)
                html_list += f'  <li>{item_text}</li>\n'
        html_list += '</ol>'
        content = content.replace(numbered_block, html_list)
    
    # Add paragraph breaks
    paragraphs = content.split('\n\n')
    processed_content = ''
    for p in paragraphs:
        if p.strip() and not p.strip().startswith('<'):
            processed_content += f'<p>{p.strip()}</p>\n\n'
        else:
            processed_content += p + '\n\n'
    
    return processed_content