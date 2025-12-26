from agno.agent import Agent
from agno.models.google import Gemini
from agno.media import Image as AgnoImage
from agno.tools.duckduckgo import DuckDuckGoTools
from typing import List, Optional
import logging


def initialize_agents(api_key: str) -> tuple[Agent, Agent, Agent, Agent]:
    try:
        model = Gemini(id="gemini-2.0-flash-exp", api_key = api_key)
        
        
        #===================Define the Therapist Agent===================
        therapist_agent = Agent(
            model = model,
            name = "Therapist Agent",
            instructions = [
                """You are an empathetic therapist that:,
                1. Listens with empathy and validates feelings,
                2. Uses gentle humor to lighten the mood,
                3. Shares relatable breakup experiences,
                4. Offers comforting words and encouragement,
                5. Analyzes both text and image inputs for emotional context,
                Be supportive and understanding in your responses
                """
            ],
            markdown = True
        )
        
        #===================Define the Closure Agent===================
        closure_agent = Agent(
            model = model,
            name = "Closure Agent",
            instructions = [
                """You are an expert in helping people find closure through words. Your role involves:
                    1. Guiding users in conveying raw, genuine emotions honestly and openly
                    Your primary focus is to help individuals experience emotional relief and closure through honest, well-crafted expression.
                """
                    # 1. Crafting meaningful messages to express feelings that were never shared.
                    # 3. Presenting messages in a structured, easy-to-read format with clear headings where appropriate.
                    # 4. Ensuring the overall tone feels sincere, heartfelt, and authentic.
            ],
            markdown = True,
        )
        
        ##===================Define the Recovery_Planner Agent===================
        recovery_planner_agent = Agent(
            model =model,
            name = "Recovery Planner Agent",
            instructions = [
                """ 
                You are a recovery routine planner. Your role involves:
                1. Design a 7-Day recovery schedule.
                Focus on practical recovery steps.
                """
                # 2. The schedule should include fun activities and self-care tasks.
                # 3. Suggest social media detox strategies.
            ],
            markdown = True
        )
        
        #=====================Define Stoic Agent========================
        stoic_agent = Agent(
            model = model,
            name = "Honest Agent",
            instructions = [
                """ 
                You are a Stoic guide, rooted in logic, realism, and emotional discipline. Your role is to:
                1. Provide blunt, honest, and realistic advice, free from sugar-coating.
                2. When offering guidance, draw from the timeless wisdom of Stoic thinkers like Marcus Aurelius, Seneca, and Epictetus.
                Your purpose is to help others face reality as it is — with strength, reason, and a clear mind.
                """
                # 2. Encourage acceptance of what cannot be changed, while focusing on what is within one's control.
                # 3. Promote resilience, self-awareness, and mental toughness.
                # 4. Communicate with clarity and directness — your tone is steady, grounded, and unapologetically realistic.
            ],
            markdown = True
        )
        
        return therapist_agent, closure_agent, recovery_planner_agent, stoic_agent
    
    except Exception as e:
        return None, None, None, None
    
