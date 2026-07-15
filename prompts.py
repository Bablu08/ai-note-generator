def build_summarize_prompt(raw_text, user_instructions):
    base = f"""
    Summarize the following text into clear, structured study notes.

    text:
    {raw_text}
    """
    
    return add_instruction(base, user_instructions)

def build_topic_prompt(topic, user_instructions):
    base = f"""
    Generate clear, structured study notes on the following topic, using your own knowledge.

    topic:
    {topic}
    """
    return add_instruction(base, user_instructions)

def add_instruction(base, user_instructions):
    if user_instructions:
        base += f"\n\nAdditional instructions from the user: {user_instructions}\nFollow these instructions carefully when structuring your response."
    else:
        base += "\n\nUse headings, bullet points, and bold key terms by default."
    
    return base