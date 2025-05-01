# Documentation Module Extractor

A Streamlit application that extracts and structures documentation content from websites into a hierarchical module-submodule format using AI. This tool helps in analyzing technical documentation and generating structured insights about its organization and content.

![image](https://github.com/user-attachments/assets/4906fb02-c7b1-4c75-8038-24dbaf80fc7a)
![image](https://github.com/user-attachments/assets/6c59cd79-0183-47b7-a835-a1fb68b5274e)


## Features

- Web scraping with BeautifulSoup
- AI-powered content analysis using Groq's LLM
- Hierarchical module-submodule structure generation
- Clean and intuitive Streamlit interface
- JSON output format for easy integration
- Content length management and optimization

## Technical Architecture

The application is built using the following components:

1. **Frontend**: Streamlit for the user interface
2. **Backend Processing**:
   - BeautifulSoup for web scraping
   - Groq's LLM (llama-3.3-70b-versatile) for content analysis
   - LangChain for prompt management and chain execution
3. **Data Processing**:
   - Content cleaning and normalization
   - JSON structure generation and validation
   - Error handling and edge case management

## Third-Party Libraries

- `streamlit`: Web application framework
- `requests`: HTTP client for web scraping
- `beautifulsoup4`: HTML parsing and content extraction
- `langchain-groq`: Interface for Groq's LLM
- `langchain`: Framework for LLM application development
- `python-dotenv`: Environment variable management

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Open the application in your web browser
2. Enter the URL of the documentation you want to analyze
3. Click "Extract Modules" to start the analysis
4. View the generated module structure
5. Download the results as JSON if needed

## Design Rationale

The application follows these design principles:

1. **Modularity**: Separate classes for different functionalities (DocumentationExtractor)
2. **Error Handling**: Comprehensive error handling for web requests and content processing
3. **Content Optimization**: Smart content truncation to handle large documents
4. **Clean Output**: Structured JSON format for easy integration
5. **User Experience**: Intuitive interface with clear feedback and progress indicators

## Assumptions

1. Documentation websites have a clear main content area (main/article/body tags)
2. Navigation and footer elements can be safely removed
3. Content is primarily text-based
4. Documentation follows a hierarchical structure
5. Groq API has sufficient context window for content analysis

## Limitations

1. **Content Length**: Limited to 100,000 characters per page
2. **Website Structure**: May not work well with highly dynamic or JavaScript-heavy websites
3. **API Dependencies**: Requires a valid Groq API key
4. **Processing Time**: Large documents may take longer to process
5. **Structure Recognition**: May not perfectly identify all modules in complex documentation
6. **Authentication**: Cannot access documentation behind login walls

## Edge Case Handling

1. **Invalid URLs**: Validates URLs before processing
2. **Request Failures**: Handles various HTTP errors gracefully
3. **Content Truncation**: Smart truncation with notification
4. **JSON Parsing**: Robust JSON structure validation and formatting
5. **Empty Content**: Handles cases where no main content is found

## Known Issues

1. May struggle with documentation that uses unconventional HTML structures
2. Performance may be affected by very large documentation sets
3. Some formatting may be lost during content extraction
4. Complex nested structures might not be perfectly captured

## Future Improvements

1. Support for multiple pages/documentation sets
2. Enhanced content cleaning and formatting
3. Customizable module structure templates
4. Support for different output formats
5. Caching mechanism for frequently accessed documentation
6. Authentication support for protected documentation

## Example Output

The application generates a JSON structure in the following format:

```json
[
  {
    "module": "Module Name",
    "Description": "Detailed description of the module",
    "Submodules": {
      "submodule_1": "Description of submodule 1",
      "submodule_2": "Description of submodule 2"
    }
  }
]
```

## Requirements

- Python 3.8+
- Streamlit
- BeautifulSoup4
- Requests
- LangChain
- LangChain-Groq
- Python-dotenv 
