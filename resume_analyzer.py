import os
import json
import logging
from openai import OpenAI

class ResumeAnalyzer:
    def __init__(self):
        """Initialize OpenAI client"""
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
    def analyze_resume(self, resume_text):
        """
        Analyze resume and return comprehensive feedback
        """
        try:
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert resume analyst and career coach. 
                        Analyze the provided resume and return a comprehensive analysis in JSON format.
                        
                        Your response must be valid JSON with this exact structure:
                        {
                            "overall_score": number (1-100),
                            "section_scores": {
                                "contact_info": number (1-100),
                                "professional_summary": number (1-100),
                                "work_experience": number (1-100),
                                "education": number (1-100),
                                "skills": number (1-100),
                                "formatting": number (1-100)
                            },
                            "strengths": [array of 3-5 specific strengths],
                            "weaknesses": [array of 3-5 specific areas for improvement],
                            "suggestions": [array of 5-8 actionable improvement suggestions],
                            "missing_elements": [array of important missing elements],
                            "keyword_analysis": {
                                "relevant_keywords_found": [array of keywords found],
                                "missing_keywords": [array of important missing keywords],
                                "keyword_density_score": number (1-100)
                            },
                            "optimized_summary": "An improved professional summary based on the content",
                            "ats_score": number (1-100),
                            "readability_score": number (1-100)
                        }"""
                    },
                    {
                        "role": "user", 
                        "content": f"Please analyze this resume:\n\n{resume_text}"
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=2000
            )
            
            result = json.loads(response.choices[0].message.content or '{}')
            return result
            
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {str(e)}")
            return self._get_fallback_analysis()
        except Exception as e:
            logging.error(f"OpenAI API error: {str(e)}")
            return self._get_fallback_analysis()
    
    def _get_fallback_analysis(self):
        """Return a fallback analysis when AI analysis fails"""
        return {
            "overall_score": 0,
            "section_scores": {
                "contact_info": 0,
                "professional_summary": 0,
                "work_experience": 0,
                "education": 0,
                "skills": 0,
                "formatting": 0
            },
            "strengths": ["Unable to analyze - please try again"],
            "weaknesses": ["Analysis failed - please check your resume format"],
            "suggestions": ["Please ensure your resume contains readable text and try uploading again"],
            "missing_elements": ["Analysis could not be completed"],
            "keyword_analysis": {
                "relevant_keywords_found": [],
                "missing_keywords": ["Analysis failed"],
                "keyword_density_score": 0
            },
            "optimized_summary": "Analysis failed. Please try uploading your resume again.",
            "ats_score": 0,
            "readability_score": 0
        }
    
    def generate_optimized_content(self, original_text, analysis):
        """
        Generate optimized resume content based on analysis
        """
        try:
            prompt = f"""Based on this resume analysis, create an optimized version of the resume content.

            Original Resume:
            {original_text}

            Analysis Feedback:
            - Overall Score: {analysis.get('overall_score', 0)}/100
            - Key Weaknesses: {', '.join(analysis.get('weaknesses', []))}
            - Suggestions: {', '.join(analysis.get('suggestions', []))}
            - Missing Keywords: {', '.join(analysis.get('keyword_analysis', {}).get('missing_keywords', []))}

            Please provide an improved version that addresses the identified issues while maintaining the original information accuracy."""

            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional resume writer. Optimize the provided resume while keeping all factual information accurate."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f"Error generating optimized content: {str(e)}")
            return "Error generating optimized content. Please try again."
