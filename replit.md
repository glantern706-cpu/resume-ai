# Overview

This is an AI-powered resume analysis application built with Flask that allows users to upload resumes in PDF or DOCX format and receive comprehensive feedback. The system uses OpenAI's GPT-4o model to analyze resumes and provide detailed insights including overall scores, section-specific feedback, ATS optimization suggestions, and keyword analysis. The application features a modern web interface with drag-and-drop file upload functionality and presents results in an organized, visually appealing format.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask for server-side rendering
- **UI Framework**: Bootstrap with dark theme for responsive design
- **Interactive Features**: JavaScript for drag-and-drop file uploads and dynamic form handling
- **Styling**: Custom CSS with Bootstrap integration for modern, accessible interface

## Backend Architecture
- **Web Framework**: Flask with WSGI middleware for production deployment
- **File Processing**: Modular design with separate `FileProcessor` class for extracting text from PDF and DOCX files
- **AI Analysis**: Dedicated `ResumeAnalyzer` class that interfaces with OpenAI's API
- **Session Management**: Flask sessions with configurable secret keys
- **Error Handling**: Comprehensive logging and user-friendly error messages

## File Processing Pipeline
- **Upload Validation**: File type and size restrictions (PDF, DOCX, DOC up to 16MB)
- **Text Extraction**: PyPDF2 for PDF files and python-docx for Word documents
- **Security**: Werkzeug's secure filename handling and temporary file management
- **Storage**: Local file system with configurable upload directories

## AI Integration
- **Model**: OpenAI GPT-4o for resume analysis
- **Structured Output**: JSON-formatted responses with predefined schema for consistent analysis
- **Analysis Components**: Overall scoring, section-specific evaluation, ATS optimization, keyword analysis, and improvement suggestions

# External Dependencies

## AI Services
- **OpenAI API**: GPT-4o model for resume analysis and feedback generation
- **Authentication**: API key-based authentication stored in environment variables

## File Processing Libraries
- **PyPDF2**: PDF text extraction and manipulation
- **python-docx**: Microsoft Word document processing
- **Werkzeug**: File upload handling and security utilities

## Web Framework Dependencies
- **Flask**: Core web framework with templating and routing
- **Bootstrap**: Frontend UI framework via CDN
- **Font Awesome**: Icon library for enhanced user interface

## Development Tools
- **Logging**: Python's built-in logging module for debugging and monitoring
- **Tempfile**: Secure temporary file handling for uploaded documents