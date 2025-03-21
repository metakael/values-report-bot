#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LLM Integration module for Google Gemini API
"""

import logging
import google.generativeai as genai
from config import Config

logger = logging.getLogger(__name__)

# Configure the Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)

def initialize_model():
    """Initialize and return the Gemini model"""
    try:
        # Update to use the correct model name and configuration
        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.0-pro')  # Updated model name
        return model
    except Exception as e:
        logger.error(f"Error initializing Gemini model: {e}")
        return None

def get_value_info(value_name):
    """
    Get information about a value from the hardcoded VALUES_LIST
    
    Args:
        value_name (str): Name of the value
        
    Returns:
        tuple: (description, schwartz_category, gouveia_category) or (None, None, None) if not found
    """
    # Normalize the value name for comparison
    value_name_lower = value_name.lower().strip()
    
    # Look for exact match first
    for value_info in Config.VALUES_LIST:
        if value_info["value"].lower() == value_name_lower:
            return (
                value_info["description"], 
                value_info["schwartz_category"], 
                value_info["gouveia_category"]
            )
    
    # If no exact match, look for partial match
    for value_info in Config.VALUES_LIST:
        if value_name_lower in value_info["value"].lower() or value_info["value"].lower() in value_name_lower:
            return (
                value_info["description"], 
                value_info["schwartz_category"], 
                value_info["gouveia_category"]
            )
    
    # No match found
    return None, None, None

def generate_prompt(user_data, section):
    """
    Generate a customized prompt based on user data and report section
    
    Args:
        user_data (dict): User's values and personal information
        section (dict): Report section data
        
    Returns:
        str: Customized prompt for LLM
    """
    # Extract all 10 values
    top_values = user_data.get('top_values', [])
    next_values = user_data.get('next_values', [])
    
    # Combine into a single list of all 10 values
    all_values = []
    all_values.extend(top_values[:5])  # First 5 ranked values
    all_values.extend(next_values[:5])  # Next 5 unranked values
    
    # Ensure we have 10 values (pad with "Unknown" if needed)
    while len(all_values) < 10:
        all_values.append("Unknown")
    
    # Get descriptions and categories for all 10 values
    descriptions = []
    schwartz_categories = []
    gouveia_categories = []
    
    for value in all_values:
        desc, schwartz_cat, gouveia_cat = get_value_info(value)
        descriptions.append(desc or "No description available")
        schwartz_categories.append(schwartz_cat or "Unknown")
        gouveia_categories.append(gouveia_cat or "Unknown")
    
    # Format the prompt using the section-specific template
    prompt = section["prompt_template"].format(
        # Top 5 ranked values
        value1=all_values[0],
        value2=all_values[1],
        value3=all_values[2],
        value4=all_values[3],
        value5=all_values[4],
        # Values 6-10 (unranked)
        value6=all_values[5],
        value7=all_values[6],
        value8=all_values[7],
        value9=all_values[8],
        value10=all_values[9],
        # Descriptions for all 10 values
        desc1=descriptions[0],
        desc2=descriptions[1],
        desc3=descriptions[2],
        desc4=descriptions[3],
        desc5=descriptions[4],
        desc6=descriptions[5],
        desc7=descriptions[6],
        desc8=descriptions[7],
        desc9=descriptions[8],
        desc10=descriptions[9],
        # Schwartz categories for all 10 values
        schwartz_cat1=schwartz_categories[0],
        schwartz_cat2=schwartz_categories[1],
        schwartz_cat3=schwartz_categories[2],
        schwartz_cat4=schwartz_categories[3],
        schwartz_cat5=schwartz_categories[4],
        schwartz_cat6=schwartz_categories[5],
        schwartz_cat7=schwartz_categories[6],
        schwartz_cat8=schwartz_categories[7],
        schwartz_cat9=schwartz_categories[8],
        schwartz_cat10=schwartz_categories[9],
        # Gouveia categories for all 10 values
        gouveia_cat1=gouveia_categories[0],
        gouveia_cat2=gouveia_categories[1],
        gouveia_cat3=gouveia_categories[2],
        gouveia_cat4=gouveia_categories[3],
        gouveia_cat5=gouveia_categories[4],
        gouveia_cat6=gouveia_categories[5],
        gouveia_cat7=gouveia_categories[6],
        gouveia_cat8=gouveia_categories[7],
        gouveia_cat9=gouveia_categories[8],
        gouveia_cat10=gouveia_categories[9],
        # Personal information
        age=user_data.get('age', 'Unknown'),
        country=user_data.get('country', 'Unknown'),
        occupation=user_data.get('occupation', 'Unknown')
    )
    
    return prompt

async def generate_content(user_data, section):
    """
    Generate content using Google Gemini for a specific report section
    
    Args:
        user_data (dict): User's values and personal information
        section (dict): Report section data
        
    Returns:
        tuple: (success, content, prompt)
            - success (bool): True if generation was successful
            - content (str): Generated content
            - prompt (str): Prompt used for generation
    """
    try:
        # Initialize model
        model = initialize_model()
        if not model:
            return False, "Failed to initialize LLM model", ""
        
        # Generate customized prompt
        prompt = generate_prompt(user_data, section)
        
        # Generate content
        response = model.generate_content(prompt)
        
        # Extract and return the generated text
        if response and hasattr(response, 'text'):
            return True, response.text, prompt
        else:
            return False, "No content generated", prompt
    
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        return False, f"Error generating content: {str(e)}", ""

async def generate_all_sections(user_data):
    """
    Generate content for all report sections
    
    Args:
        user_data (dict): User's values and personal information
        
    Returns:
        dict: Dictionary with section titles as keys and content as values
    """
    sections_content = {}
    prompts_used = {}
    
    for section in Config.REPORT_SECTIONS:
        success, content, prompt = await generate_content(user_data, section)
        
        if success:
            sections_content[section['title']] = content
            prompts_used[section['title']] = prompt
        else:
            sections_content[section['title']] = "Content generation failed for this section."
            prompts_used[section['title']] = prompt
    
    return sections_content, prompts_used