import streamlit as st 
from pathlib import Path
import tempfile 
import logging
import os
from agents import initialize_agents
from agno.media import Image as AgnoImage

#Configure Logging for errors 
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


#=============Helper Function to Process the Uploaded images============
def process_image(files):
    processed_images = []
    
    for file in files:
        try:
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, f"temp_{file.name}")
            
            with open(temp_path, "wb") as f:
                f.write(file.getvalue())
                
            agno_image = AgnoImage(filepath = Path(temp_path))
            processed_images.append(agno_image)
        
        except Exception as e:
            logger.error(f"Error processing image {file.name}: {str(e)}")
            continue
        
        return processed_images

def main():
    
    #Set the page config and UI elements
    st.set_page_config(
        page_title="Emotional Support ❤️‍🩹",
        page_icon="❤️‍🩹",
        layout="wide"
    )
    
    
    #Side-Bar 
    with st.sidebar:
        st.header("🔑 API KEY Configuration")
        
        #Check if API_KEY present in session or not
        if "api_key_input" not in st.session_state:
            st.session_state.api_key_input = ""
            
        #$$$$$TODO:- Add Link to Google AI Studio
        api_key = st.text_input(
            "Enter your Gemini API Key",
            value = st.session_state.api_key_input,
            type = "password",
            help="Get your API Key from Google AI Studio",
            key = "api_key_widget"
        )
        
        if api_key != st.session_state.api_key_input:
            st.session_state.api_key_input = api_key
        
        if api_key:
            st.success("API KEY AUTHENTICATED ✅")
        else:
            st.warning("Please enter your API KEY to proceed")
            st.markdown(
                """ 
                To get your API key:
                1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
                2. Enable the Generative Language API in your [Google Cloud Console](https://console.developers.google.com/apis/api/generativelanguage.googleapis.com)
                """
            )
            
    #~~~~~~~~~~~~~~~~~~~~~~Main Section~~~~~~~~~~~~~~~~~~~~~~
    st.title("❤️‍🩹Emotional Support Chatbot")
    st.markdown("""
                ### Your Artificially-Intelligent Emotional Support
                Share your feelings and chat screenshots, and we'll provide emotional support to you in this harsh time.
                """)      
    
    #Input Section
    col1 , col2 = st.columns(2)
    
    #Get the User_Text
    with col1:
        st.subheader("Share your Heart Out!!!!")
        user_input_query = st.text_area(
            label="How are you feeling? Tell Me",
            height=150,
            placeholder="Tell me, What happened....."
        ) 
     
    #Get the User_ScreenShot   
    with col2:
        st.subheader("Upload your Screenshot")
        uploads = st.file_uploader(
            label="Upload your Chats [Optional]",
            type = ["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key = "screenshots"
        ) 
        
        if uploads:
            #Convert Uploaded Screenshots to Images
            for file in uploads:
                st.image(file, caption=file.name, use_container_width=True)
                
    #~~~~~~~~~~~~~~~~~~~~~~~~~Proceed Button & API KEY Validation~~~~~~~~~~~~~~~~           
    if st.button("Get Recovery Plan 💝", type="primary"):
        if not st.session_state.api_key_input:
            st.warning("Please Enter your API KEY in the sidebar first!!!")
        else:
            therapist_agent, closure_agent, recovery_planner_agent, stoic_agent = initialize_agents(st.session_state.api_key_input)
            
            if all([therapist_agent, closure_agent, recovery_planner_agent, stoic_agent]):
                if user_input_query or uploads:
                    try:
                        st.header("Your personalized recovery plan!!!")
                        
                        all_images = process_image(uploads) if uploads else []
                        
                        #Therapist Analysis
                        with st.spinner("Getting Empathetic Support......"):
                            therapist_prompt = f"""
                            Analyze the emotional state and provide empathetic support based on:
                            User's message: {user_input_query}
                            Please provide a compassionate response with:
                            1. Validation of feelings
                            2. Gentle words of comfort
                            3. Relatable experiences
                            4. Words of encouragement
                            """
                            response = therapist_agent.run(
                                message = therapist_prompt,
                                images = all_images
                            )
                            st.subheader(" Emotional Support...")
                            st.markdown(response.content)
                            
                            
                        #Closure Support
                        with st.spinner("Getting Closure messages..."):
                            closure_prompt = f"""
                            Help create emotional closure based on:
                            User's feelings: {user_input_query}
                            
                            Please provide the following:
                            1. Template for unsent messages.
                            2. Emotional release excercises.
                            """
                            # 3. Closure rituals
                            # 4. Moving forward strategies
                            response = closure_agent.run(
                                message = closure_prompt,
                                images = all_images
                            )
                            st.subheader("Finding Closure")
                            st.markdown(response.content)
                            
                            
                        #Recovery Schedule
                        with st.spinner("Creating a Recovery Schedule..."):
                            recovery_prompt = f"""
                            Design a 7-Day recovery plan based on:
                            Current state: {user_input_query}
                            Include the following:
                            1. Daily activities and challenges to motivate one.
                            2. Self-care routines.
                            """
                            # 3. Social Media guidelines.
                            # 4. Calm and Mood-Lifting music suggestions.
                            
                            response = recovery_planner_agent.run(
                                message = recovery_prompt,
                                images = all_images
                            )
                            
                            st.subheader("Your 7-Days Recovery Plan")
                            st.markdown(response.content)
                            
                        #Honest Feedback
                        with st.spinner("Getting Honest Opinion...."):
                            honest_prompt = f"""
                            Provide honest, constructive opinion about:
                            situation: {user_input_query}
                            """
                            #  Include:
                            # 1. Objective Analysis
                            # 2. Growth opprtunities
                            # 3. Future outlook
                            # 4. Acttionable steps
                            
                            response = stoic_agent.run(
                                message = honest_prompt,
                                image = all_images
                            )
                            
                            st.subheader("Honest Perspective")
                            st.markdown(response.content)
                    except Exception as e:
                        logger.error(f"Error during analysis: {str(e)}")
                        st.error("An error occured during analysis. Please check the logs for details.")
                
                #Else condition if query and image is not provided.
                else:
                    st.warning("Please share your feelings or upload screenshots to get help.")
            else:
                st.error("Failed to initialize agents. Please check your API key.")
                
    st.markdown("----")
    st.markdown(
        """ 
        <div style = 'text-align:center'>
                <p>Hope so you got what you were searching for 🤞 <p>
        </div>
        """, unsafe_allow_html=True
    )    

if __name__ == "__main__":
    main()