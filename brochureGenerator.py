from relevantLinks import fetch_content_from_relevant_links
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

brochure_system_prompt = '''
You are an assistant that creates a short brochure about a company.
Include company culture, customers, and careers if available.
Return clean markdown.
'''


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

    user_prompt = f"""
    Company: {company_name}
    Website data:
    """
    user_prompt += fetch_content_from_relevant_links(url, model)
    user_prompt = user_prompt[:3000]

    messages = [
        {"role": "system", "content": brochure_system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = model.invoke(messages)

    return response.content