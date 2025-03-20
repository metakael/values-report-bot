#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility functions for the Values Report Bot
"""

import re
import logging

logger = logging.getLogger(__name__)

def parse_values(text):
    """
    Parse values from user input
    
    Args:
        text (str): User input containing values
        
    Returns:
        list: Extracted values
    """
    # Remove extra whitespace
    text = text.strip()
    
    # Try different separators (comma, period, semicolon, newline)
    for separator in [',', '.', ';', '\n']:
        if separator in text:
            values = [val.strip() for val in text.split(separator) if val.strip()]
            if values:
                return values
    
    # If no separators found, split by whitespace
    values = text.split()
    if values:
        return values
    
    # If still no values found, just return the entire text as a single value
    return [text] if text else []

def validate_age(age_text):
    """
    Validate age input
    
    Args:
        age_text (str): Age input from user
        
    Returns:
        tuple: (is_valid, age_or_error_message)
    """
    try:
        # Remove any non-numeric characters
        age_text = re.sub(r'[^0-9]', '', age_text)
        
        # Convert to integer
        age = int(age_text)
        
        # Validate age range (e.g., 18-120)
        if 18 <= age <= 120:
            return True, age
        else:
            return False, "Please enter a valid age between 18 and 120."
    
    except ValueError:
        return False, "Please enter a numeric age."

def validate_country(country_text):
    """
    Validate country input
    
    Args:
        country_text (str): Country input from user
        
    Returns:
        tuple: (is_valid, country_or_error_message)
    """
    # Simple validation - just check if it's not empty and contains letters
    country_text = country_text.strip()
    
    if not country_text:
        return False, "Please enter a valid country name."
    
    if not any(c.isalpha() for c in country_text):
        return False, "Please enter a valid country name with alphabetic characters."
    
    # Return the capitalized country name
    return True, country_text.title()

def validate_occupation(occupation_text):
    """
    Validate occupation input
    
    Args:
        occupation_text (str): Occupation input from user
        
    Returns:
        tuple: (is_valid, occupation_or_error_message)
    """
    # Simple validation - just check if it's not empty
    occupation_text = occupation_text.strip()
    
    if not occupation_text:
        return False, "Please enter your occupation."
    
    # Return the capitalized occupation
    return True, occupation_text.capitalize()

def format_values_for_display(values_list):
    """
    Format values list for display to user
    
    Args:
        values_list (list): List of values
        
    Returns:
        str: Formatted string of values
    """
    if not values_list:
        return "None"
    
    return ", ".join(values_list)