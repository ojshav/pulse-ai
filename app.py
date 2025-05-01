"""
Documentation Module Extractor

This Streamlit application extracts and structures documentation content from websites
into a hierarchical module-submodule format using AI. It uses BeautifulSoup for web scraping
and Groq's LLM for content analysis and structure generation.
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
import json
import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

# Constants
GROQ_MODEL_NAME = "llama-3.3-70b-versatile"
MAX_CONTENT_LENGTH = 100000  # Maximum content length to process
DEFAULT_TIMEOUT = 30  # Request timeout in seconds

class DocumentationExtractor:
    """Handles the extraction and processing of documentation content."""
    
    def __init__(self, groq_api_key: str):
        """Initialize the DocumentationExtractor with Groq API key.
        
        Args:
            groq_api_key (str): The Groq API key for LLM access
        """
        if not groq_api_key:
            raise ValueError("Groq API key is required")
        
        self.chat = ChatGroq(
            temperature=0,
            model_name=GROQ_MODEL_NAME,
            groq_api_key=groq_api_key
        )
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean the scraped text by removing extra whitespace and newlines.
        
        Args:
            text (str): The text to clean
            
        Returns:
            str: Cleaned text
        """
        return ' '.join(text.split())
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the provided URL is valid.
        
        Args:
            url (str): The URL to validate
            
        Returns:
            bool: True if URL is valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
    
    def scrape_website(self, url: str) -> str:
        """Scrape the website content, ignoring navigation and footer.
        
        Args:
            url (str): The URL to scrape
            
        Returns:
            str: The cleaned content of the website
            
        Raises:
            ValueError: If URL is invalid
            requests.RequestException: If request fails
        """
        if not self.is_valid_url(url):
            raise ValueError("Invalid URL provided")
        
        try:
            response = requests.get(url, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup.find_all(['nav', 'footer', 'header', 'script', 'style']):
                element.decompose()
            
            # Get main content
            main_content = soup.find('main') or soup.find('article') or soup.find('body')
            if not main_content:
                return "Could not find main content on the page"
            
            content = self.clean_text(main_content.get_text())
            
            # Truncate content if too long
            if len(content) > MAX_CONTENT_LENGTH:
                content = content[:MAX_CONTENT_LENGTH] + "... [Content truncated]"
            
            return content
            
        except requests.RequestException as e:
            raise requests.RequestException(f"Error accessing website: {str(e)}")
    
    def generate_module_structure(self, content: str) -> str:
        """Generate module and submodule structure using Groq.
        
        Args:
            content (str): The content to analyze
            
        Returns:
            str: The generated module structure in JSON format
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert technical documentation analyst. Your task is to analyze documentation content and create a detailed, hierarchical structure of modules and submodules.

For each module and submodule:
1. Provide a comprehensive description that:
   - Explains the purpose and functionality
   - Describes key features and capabilities
   - Highlights important use cases or scenarios
   - Explains how it fits into the overall system
2. Use clear, professional language
3. Avoid repeating the module name in the description
4. Make descriptions specific and detailed, not generic
5. Focus on the value and benefits of each component

The output should be in JSON format with the following structure:
{{
    "module": "Module Name",
    "Description": "Detailed, insightful description of the module's purpose, features, and value",
    "Submodules": {{
        "submodule_name": "Detailed description of the submodule's specific functionality and benefits"
    }}
}}

Remember to:
- Analyze the content thoroughly to identify true modules and submodules
- Provide meaningful, unique descriptions for each component
- Focus on the actual functionality and purpose described in the documentation
- Avoid generic or repetitive descriptions"""),
            ("user", "{content}")
        ])
        
        chain = (
            {"content": RunnablePassthrough()}
            | prompt
            | self.chat
            | StrOutputParser()
        )
        
        return chain.invoke(content)
    
    @staticmethod
    def format_output(text: str) -> str:
        """Format the LLM output into proper JSON structure.
        
        Args:
            text (str): The raw output from the LLM
            
        Returns:
            str: Formatted JSON string or error message
        """
        try:
            # First, try to find JSON-like content in the text
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                return "Error: No JSON structure found in the output"
            
            json_text = text[start_idx:end_idx]
            
            # Clean the text to ensure it's valid JSON
            cleaned_text = json_text.replace('}{', '},{')
            if not cleaned_text.startswith('['):
                cleaned_text = '[' + cleaned_text
            if not cleaned_text.endswith(']'):
                cleaned_text = cleaned_text + ']'
            
            # Parse and validate JSON
            data = json.loads(cleaned_text)
            return json.dumps(data, indent=2)
        except json.JSONDecodeError as e:
            return f"Error formatting JSON: {str(e)}\n\nRaw output:\n{text}"
        except Exception as e:
            return f"Unexpected error: {str(e)}\n\nRaw output:\n{text}"

def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(
        page_title="Documentation Module Extractor",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("Documentation Module Extractor")
    st.write("""
    This tool helps you extract and structure documentation content from websites.
    Enter a documentation URL below to analyze its content and generate a structured
    module hierarchy with detailed descriptions.
    """)
    
    # Get Groq API key
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        st.error("""
        Please set GROQ_API_KEY in your environment variables.
        Create a .env file in the project root with:
        GROQ_API_KEY=your_api_key_here
        """)
        st.stop()
    
    try:
        extractor = DocumentationExtractor(groq_api_key)
    except ValueError as e:
        st.error(str(e))
        st.stop()
    
    # URL input
    url = st.text_input(
        "Enter Documentation URL:",
        placeholder="https://docs.example.com",
        help="Enter the URL of the documentation website you want to analyze"
    )
    
    if st.button("Extract Modules", help="Click to analyze the documentation and generate module structure"):
        if not url:
            st.warning("Please enter a URL")
            return
        
        try:
            with st.spinner("Scraping website content..."):
                content = extractor.scrape_website(url)
            
            if content.startswith("Error"):
                st.error(content)
                return
            
            with st.spinner("Analyzing content and generating structure..."):
                result = extractor.generate_module_structure(content)
                formatted_output = extractor.format_output(result)
            
            st.subheader("Extracted Module Structure")
            
            if formatted_output.startswith("Error"):
                st.error(formatted_output)
                st.text_area("Raw LLM Output", result, height=200)
            else:
                st.json(formatted_output)
                # Add download button
                st.download_button(
                    label="Download JSON",
                    data=formatted_output,
                    file_name="module_structure.json",
                    mime="application/json",
                    help="Download the generated module structure as a JSON file"
                )
        
        except requests.RequestException as e:
            st.error(f"Error accessing the website: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
