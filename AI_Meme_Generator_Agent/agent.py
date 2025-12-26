from browser_use import Agent, SystemPrompt
import asyncio
import os
import re
from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogle
# import google.generativeai as genai


async def generate_meme(query:str, model_id:str, api_key:str) -> None:
    
    #Initialize the Appropriate LLM
    if model_id == "OPEN_AI":
        model = ChatOpenAI(model = "gpt-4o",
                           api_key = api_key,
                           temperature=0.0)
    
    task = (
        "You are a meme generator expert. You are given a query and you need to generate a meme for it.\n"
        "1. Go to https://imgflip.com/memetemplates \n"
        "2. Click on the Search bar in the middle and search for ONLY ONE MAIN ACTION VERB (like 'bully', 'laugh', 'cry') in this query: '{0}'\n"
        "3. Choose any meme template that metaphorically fits the meme topic: '{0}'\n"
        "   by clicking on the 'Add Caption' button below it\n"
        "4. Write a Top Text (setup/context) and Bottom Text (punchline/outcome) related to '{0}'.\n" 
        "5. Check the preview making sure it is funny and a meaningful meme. Adjust text directly if needed. \n"
        "6. Look at the meme and text on it, if it doesnt make sense, PLEASE retry by filling the text boxes with different text. \n"
        "7. Click on the Generate meme button to generate the meme\n"
        "8. Copy the image link and give it as the output\n"
    ).format(query)
    
    
    #Initialize the Agent
    agent = Agent(
        task = task,
        llm = model,
        max_actions_per_step = 5,
        max_failures = 25,
        use_vision = True
    )
    
    history = await agent.run()
    
    #Final Result
    final_result = history.final_result()
    
    url_match = re.search(r'https://imgflip\.com/i/(\w+)', final_result)
    if url_match:
        meme_id = url_match.group(1)
        return f"https://i.imgflip.com/{meme_id}.jpg"
    return None

if __name__ == "__main__":
    query = "Ilya's SSI quietly looking at the OpenAI vs Deepseek debate while diligently working on ASI"
    model_id = "OPEN_AI"
    api_key = os.getenv("OPENAI_KEY")
    
    result = asyncio.run(generate_meme(query, model_id, api_key))