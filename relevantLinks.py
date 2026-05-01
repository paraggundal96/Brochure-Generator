from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
import gradio as gr
from scraper import fetch_website_contents, fetch_website_links
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List



load_dotenv()
import os
key = os.getenv("OPENAI_API_KEY")

class Link(BaseModel):
    type : str = Field(description = "about, careers, etc")
    url : str = Field(description = "full https URL")

class LinkSchema(BaseModel):
    links : List[Link]

link_system_prompt = '''
Select 5-6 relevant links, exclude Terms of Service, Privacy, email links.
{"links":[{"type":"about","url":"https://..."}]}
'''

def list_of_links(url):
    links = fetch_website_links(url)[:10]
    return "\n".join(links)

model = ChatOpenAI(
    model = "openai/gpt-oss-20b:free",
    base_url = "https://openrouter.ai/api/v1",
    api_key = key,
    temperature = 0
)

local_model = ChatOllama(
    model = "llama3.2:latest",
    model_provider = "ollama",
    temperature = 0,
    num_ctx = 2048
)

def select_relevant_links(url,m=local_model):

    messages = [
        {"role":"system","content":link_system_prompt},
        {"role":"system","content":list_of_links(url)}
    ]
    # Here we are constraining LLM to generate a defined format output, thus indirectly reducing token costs
    # Metaphorically: Pydantic is Form, LLM is person filling the form, required fields only, no extra content
    structured_output = m.with_structured_output(LinkSchema) #Internally works as JSON, but produces schema defined structure
    response =  structured_output.invoke(messages) # We recieve Python Object, whereas LLM actually generated JSON
    return response # returns plain python dictionary


def fetch_content_from_relevant_links(url,m):
    content = fetch_website_contents(url)
    data = select_relevant_links(url,m)
    landing_page = f'##Landing Page {content}\n ###Relevant Links:\n'
    for link in data.links:
        landing_page += f"\n\n ####Link:{link.type}"
        landing_page += fetch_website_contents(link.url)
    return landing_page


print(fetch_content_from_relevant_links("https://huggingface.co/",local_model))

