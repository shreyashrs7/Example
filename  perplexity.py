import requests
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()

# Perplexity API setup
PERPLEXITY_API_KEY = os.getenv("")  # Add your Perplexity API key to .env file
PERPLEXITY_API_URL = "https://api.perplexity.ai/v1/chat/completions"  # Example endpoint, check Perplexity's docs

# Your text
text = """he Benefits of Mindfulness Meditation In today's fast-paced world, finding moments of peace and clarity can be challenging. Mindfulness meditation offers a powerful tool to help us navigate the chaos and cultivate a sense of inner calm. Let's explore some of the key benefits of incorporating mindfulness meditation into your daily routine. 1. Reduces Stress One of the most well-known benefits of mindfulness meditation is its ability to reduce stress. By focusing on the present moment and acknowledging your thoughts and feelings without judgment, you can create a mental space that allows stress to dissipate. Studies have shown that regular mindfulness practice can lower cortisol levels, the hormone associated with stress. 2. Improves Focus and Concentration Mindfulness meditation trains your brain to stay focused on the present moment. This practice can enhance your ability to concentrate on tasks and improve your overall productivity. By regularly meditating, you can develop a sharper mind and a greater capacity for sustained attention. 3. Enhances Emotional Well-being Mindfulness meditation encourages a deeper understanding of your emotions. By observing your thoughts and feelings without reacting to them, you can develop greater emotional resilience. This practice can lead to improved mood, reduced symptoms of anxiety and depression, and a more positive outlook on life. 4. Promotes Better Sleep Struggling with sleep issues? Mindfulness meditation can help. By calming the mind and reducing stress, meditation can improve the quality of your sleep. Practicing mindfulness before bedtime can create a relaxing routine that prepares your body and mind for restful sleep. 5. Boosts Physical Health The benefits of mindfulness meditation extend beyond mental well-being. Research suggests that regular meditation can lower blood pressure, improve immune function, and reduce chronic pain. By fostering a mind-body connection, mindfulness can contribute to overall physical health. How to Get Started Starting a mindfulness meditation practice is simple. Find a quiet space, sit comfortably, and focus on your breath. Begin with just a few minutes each day and gradually increase the duration as you become more comfortable. There are also many guided meditation apps and online resources available to help you on your journey. Incorporating mindfulness meditation into your daily routine can lead to profound improvements in both your mental and physical well-being. Give it a try and experience the transformative power of mindfulness for yourself!"""

# Function to call Perplexity API
def call_perplexity(prompt):
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "pplx-70b-online",  # Replace with the specific Perplexity model you want to use
        "messages": [
            {"role": "system", "content": "Answer based ONLY on the provided context."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500
    }
    response = requests.post(PERPLEXITY_API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Prompt template
prompt = PromptTemplate.from_template("""
Context: {context}

User: {user_question}
""")

parser = StrOutputParser()
history = []

# Main loop
while True:
    user_input = input("Enter your question: ")
    history.append(user_input)

    # Format the prompt with context and user question
    formatted_prompt = prompt.format(
        context=text,
        user_question=user_input
    )

    # Call Perplexity API
    result = call_perplexity(formatted_prompt)
    print(result)
    history.append(result)