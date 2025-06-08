import google.generativeai as genai
from django.conf import settings
from datetime import datetime, timedelta

def setup_gemini():
    """Configure the Gemini API"""
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    return model

def generate_subtasks(task_title, task_description=None, task_due_date=None):
    """
    Generate subtasks for a given task using Google's Gemini AI
    """
    # Format due date for prompt
    due_date_str = ""
    if task_due_date:
        try:
            due_date = datetime.fromisoformat(task_due_date.replace('Z', '+00:00'))
            due_date_str = f"\nMain task due date: {due_date.strftime('%Y-%m-%d %H:%M')}"
        except:
            due_date_str = ""

    # Construct the prompt
    prompt = f"""
    Break down the following task into 3-5 specific, actionable subtasks:
    Task: {task_title}
    {f'Description: {task_description}' if task_description else ''}
    {due_date_str}

    For each subtask, provide:
    - Title: [subtask description]
    - Due: [YYYY-MM-DD HH:MM]

    Note: Keep responses in simple format, no markdown or formatting.
    """

    try:
        model = setup_gemini()
        response = model.generate_content(prompt)
        
        if not response.text:
            return []

        # Parse the response into structured data
        subtasks = []
        current_subtask = {}
        
        # Split into lines and clean up
        lines = [line.strip() for line in response.text.split('\n') if line.strip()]
        
        for line in lines:
            # Remove any markdown symbols and clean up
            line = line.replace('*', '').replace('**', '').strip()
            
            if line.lower().startswith('title:'):
                if current_subtask and 'title' in current_subtask and 'due_date' in current_subtask:
                    subtasks.append(current_subtask.copy())
                current_subtask = {'title': line[6:].strip()}
            elif line.lower().startswith('due:'):
                try:
                    due_str = line[4:].strip()
                    due_date = datetime.strptime(due_str, '%Y-%m-%d %H:%M')
                    current_subtask['due_date'] = due_date.isoformat()
                except:
                    if task_due_date:
                        default_due = datetime.fromisoformat(task_due_date.replace('Z', '+00:00')) - timedelta(hours=1)
                        current_subtask['due_date'] = default_due.isoformat()

        # Add the last subtask if complete
        if current_subtask and 'title' in current_subtask and 'due_date' in current_subtask:
            subtasks.append(current_subtask)

        print(f"Generated {len(subtasks)} subtasks")  # Debug log
        return subtasks

    except Exception as e:
        print(f"Error in generate_subtasks: {str(e)}")  # Debug log
        return []

def validate_subtasks(subtasks):
    """
    Validate the generated subtasks
    """
    if not isinstance(subtasks, list):
        return False
        
    if len(subtasks) < 1:
        return False
        
    for subtask in subtasks:
        if not isinstance(subtask, dict):
            return False
        if 'title' not in subtask or 'due_date' not in subtask:
            return False
        if not isinstance(subtask['title'], str) or not subtask['title']:
            return False
            
    return True
