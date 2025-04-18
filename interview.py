import asyncio
import os
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import re
from openai import OpenAI
import json

# Create server parameters for stdio connection to your server.py
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["server.py"],  # Your server script
    env=None,  # Optional environment variables
)

async def analyze_resume_with_gpt(resume_content):
    """
    Use GPT to analyze the resume content, extract top skills, and generate interview questions.
    """
    try:
        # Create a prompt for GPT
        prompt = f"""
        I have a resume text below. Please:
        1. Identify the top 3 technical or professional skills mentioned in the resume
        2. For each skill, generate 2 interview questions that would help assess the candidate's proficiency
        
        Resume:
        {resume_content}
        
        Format your response as JSON with the following structure:
        {{
            "skills": ["skill1", "skill2", "skill3"],
            "questions": {{
                "skill1": ["question1", "question2"],
                "skill2": ["question1", "question2"],
                "skill3": ["question1", "question2"]
            }}
        }}
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # Call the OpenAI API
        response = await client.chat.completions.create(
            model="gpt-4",  # or another appropriate model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes resumes and generates interview questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract and parse the response
        result = response.choices[0].message.content.strip()
        
        # Try to parse the JSON response
        try:
            json_result = json.loads(result)
            return json_result
        except json.JSONDecodeError:
            # If JSON parsing fails, extract information using regex
            skills_match = re.search(r'"skills":\s*\[(.*?)\]', result, re.DOTALL)
            skills = []
            if skills_match:
                skills_str = skills_match.group(1)
                skills = [s.strip(' "\'') for s in skills_str.split(',')]
            
            return {
                "skills": skills,
                "questions": {}
            }
            
    except Exception as e:
        print(f"Error analyzing resume with GPT: {e}")
        return {
            "skills": [],
            "questions": {}
        }

async def run_interview():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # Step 1: Navigate to Outlook Calendar
            print("Navigating to Outlook Calendar...")
            result = await session.call_tool("playwright_navigate", arguments={
                "url": "outlook.office.com/calendar/view/workweek"
            })
            print("Navigation result:", result)
            
            # Step 2: Wait for login page to load
            print("Waiting for login page to load...")
            await session.call_tool("playwright_wait_for_timeout", arguments={
                "timeout": 3000
            })
            
            # Step 3: Take a screenshot to see the login page
            await session.call_tool("playwright_screenshot", arguments={
                "name": "login_page"
            })
            print("Screenshot taken")
            
            # Step 4: Get text content to see what's on the page
            result = await session.call_tool("playwright_get_text_content", arguments={})
            print("Page content:", result)
            
            # Step 5: Prompt user to complete the login manually
            print("\n*** MANUAL ACTION REQUIRED ***")
            print("Please complete the login process in the browser window.")
            print("The script will continue after you press Enter...")
            input()
            
            # Step 6: Wait for calendar to load after login
            print("Waiting for calendar to load...")
            await session.call_tool("playwright_wait_for_timeout", arguments={
                "timeout": 5000
            })
            await session.call_tool("playwright_screenshot", arguments={
                "name": "calendar_page"
            })
            print("Screenshot taken")
            
            # Step 7: Find and click on the meeting with title "Demo Microsoft Meeting"
            print("Looking for 'Demo Microsoft Meeting'...")
            try:
                result = await session.call_tool("playwright_click_text", arguments={
                    "text": "Demo Microsoft Meeting"
                })
                print("Meeting found and clicked!")
            except Exception as e:
                print(f"Error clicking meeting: {e}")
                print("Taking screenshot to debug...")
                await session.call_tool("playwright_screenshot", arguments={
                    "name": "calendar_error"
                })
            
            # Step 8: Wait for meeting details to load
            await session.call_tool("playwright_wait_for_timeout", arguments={
                "timeout": 3000
            })
            await session.call_tool("playwright_screenshot", arguments={
                "name": "meeting_details"
            })
            print("Screenshot taken")
            
            # Step 9: Extract text to find the wiki URL
            result = await session.call_tool("playwright_get_text_content", arguments={})
            print("Meeting details:", result)
            
            # Step 10: Use JavaScript to find and extract the URL from the span element
            print("Extracting wiki URL from meeting details...")
            result = await session.call_tool("playwright_evaluate", arguments={
                "script": """
                    // Try to find the element using the specific selector
                    const element = document.querySelector("div:nth-of-type(8) div.VSXvP span");
                    if (element && element.textContent) {
                        // Extract URL from the span's text content
                        const text = element.textContent.trim();
                        // Check if it looks like a URL
                        if (text.startsWith('http') || text.includes('wiki')) {
                            return text;
                        }
                    }
                """
            })
            
            # Extract just the URL from the result
            result_str = str(result)
            wiki_url = None
            
            # Look for a URL pattern in the result string
            url_match = re.search(r'https?://[^\s\'"]+', result_str)
            if url_match:
                wiki_url = url_match.group(0)
            else:
                # If regex fails, try a simpler approach
                parts = result_str.split('result = ')
                if len(parts) > 1:
                    wiki_url = parts[1].split(',')[0].strip().rstrip("'").rstrip('"')
                else:
                    wiki_url = result_str
            
            if not wiki_url or wiki_url == "null":
                print("No wiki URL found in the meeting details")
                return
            
            print(f"Found wiki URL: {wiki_url}")
            
            # Step 11: Navigate to the wiki URL
            print(f"Navigating to wiki page: {wiki_url}")
            result = await session.call_tool("playwright_navigate", arguments={
                "url": wiki_url
            })
            
            # Step 12: Wait for wiki page to load and handle potential SSO login
            await session.call_tool("playwright_wait_for_timeout", arguments={
                "timeout": 3000
            })
            await session.call_tool("playwright_screenshot", arguments={
                "name": "wiki_page"
            })
            print("Screenshot taken")
            
            # Step 13: Check if we need to login again
            result = await session.call_tool("playwright_get_text_content", arguments={})
            result_text = str(result)
            if "login" in result_text.lower() or "sign in" in result_text.lower():
                print("\n*** MANUAL ACTION REQUIRED ***")
                print("Please complete the SSO login for the wiki page.")
                print("The script will continue after you press Enter...")
                input()
                await session.call_tool("playwright_wait_for_timeout", arguments={
                    "timeout": 5000
                })
            
            # Step 14: Look for resume.txt file and download it using the dedicated download tool
            print("Looking for resume.txt file...")
            await session.call_tool("playwright_screenshot", arguments={
                "name": "wiki_loaded"
            })
            print("Screenshot taken")
            
            # Use the dedicated download tool to handle the file download
            resume_path = "./resume.txt"
            print("Downloading resume.txt file...")
            try:
                result = await session.call_tool("playwright_download_file", arguments={
                    "selector": "span:nth-of-type(4) > a",
                    "save_path": resume_path
                })
                print(result)
            except Exception as e:
                print(f"Error downloading file: {e}")
                
                # Fallback: Try regular click
                print("Trying fallback method...")
                try:
                    result = await session.call_tool("playwright_click", arguments={
                        "selector": "span:nth-of-type(4) > a"
                    })
                    print("Clicked download link. Check downloads folder for the file.")
                    
                    # Wait for download to complete
                    await session.call_tool("playwright_wait_for_timeout", arguments={
                        "timeout": 10000
                    })
                except Exception as e2:
                    print(f"Error with fallback method: {e2}")
            
            # Step 15: Read and analyze the resume with GPT
            print("\n--- RESUME ANALYSIS WITH GPT ---")
            
            # Check if the resume file exists
            if os.path.exists(resume_path):
                print(f"Resume file found at {resume_path}")
                
                # Read the resume content
                with open(resume_path, 'r', encoding='utf-8') as file:
                    resume_content = file.read()
                
                print(f"Resume content (first 200 chars): {resume_content[:200]}...")
                
                # Analyze the resume with GPT
                print("\nAnalyzing resume with GPT...")
                analysis = await analyze_resume_with_gpt(resume_content)
                
                # Display the results
                if analysis and "skills" in analysis and analysis["skills"]:
                    print(f"\nTop skills identified by GPT: {', '.join(analysis['skills'])}")
                    
                    print("\n--- SUGGESTED INTERVIEW QUESTIONS ---")
                    
                    # Display questions for each skill
                    if "questions" in analysis:
                        for skill, questions in analysis["questions"].items():
                            print(f"\nQuestions for {skill}:")
                            for i, question in enumerate(questions, 1):
                                print(f"{i}. {question}")
                    else:
                        # Generate generic questions if GPT didn't provide specific ones
                        for skill in analysis["skills"]:
                            print(f"\nQuestions for {skill}:")
                            print(f"1. Can you describe your experience with {skill}?")
                            print(f"2. What challenges have you faced when working with {skill}?")
                else:
                    print("No specific skills were identified in the resume by GPT.")
            else:
                print(f"Resume file not found at {resume_path}. Check your downloads folder.")
            
            print("\nInterview process completed!")

if __name__ == "__main__":
    asyncio.run(run_interview())
