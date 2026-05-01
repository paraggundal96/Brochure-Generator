from relevantLinks import fetch_content_from_relevant_links
import gradio as gr
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI


brochure_system_prompt = '''
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
Include details of company culture, customers and careers/jobs if you have the information.
'''

def get_brochure_user_prompt(company_name, url):
    user_prompt = f"""
    You are looking at a company called: {company_name}
    Here are the contents of its landing page and other relevant pages;
    """
    user_prompt += fetch_content_from_relevant_links(url)
    user_prompt = user_prompt[:3000] # Truncate if more than 5,000 characters
    return user_prompt

def get_model(source, model_name):
    if source == "OpenRouter":
        return ChatOpenAI(
            model=model_name,
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0
        )
    else:
        return ChatOllama(
            model=model_name,
            temperature=0,
            num_ctx=2048
        )


def create_brochure(company_name, url, source, model_name):

    model = get_model(source, model_name)
    messages = [
        {"role":"system", "content": brochure_system_prompt},
        {"role":"user","content": get_brochure_user_prompt(company_name, url)}
    ]

    response = model.invoke(messages)

    return response.content


