import os
from langchain.agents import initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from send_story_agent import send_story_via_email

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY
)

def generate_story_tool_func(theme):
    prompt = f""" {theme} temalı çocuklara yönelik kısa bir hikaye oluştur. 300-400 kelime uzunluğunda, 5-12 yaş grubu için uygun olsun. """
    # Burada istersen llm.generate veya başka şekilde çağırabilirsin
    # Basit örnek olarak llm kullanıyoruz:
    return llm.predict(prompt)

generate_story_tool = Tool(
    name="GenerateStory",
    func=generate_story_tool_func,
    description="Generate a story based on the given theme."
)

def send_email_tool_func(email_and_story):
    try:
        email, story = email_and_story.split("|", 1)
        send_story_via_email(email.strip(), story.strip())
        return f"Story sent to {email} successfully."
    except Exception as e:
        return f"Failed to send email: {str(e)}"

send_email_tool = Tool(
    name="SendEmail",
    func=send_email_tool_func,
    description="Send the story to the specified email. Format: email|story"
)

agent = initialize_agent(
    tools=[generate_story_tool, send_email_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

def run_email_agent(theme, email):
    # Agent’a e-posta ve temayı tek komutla gönderiyoruz
    command = f"Generate a story with theme '{theme}' and send it to '{email}'."
    return agent.run(command)
