from pydantic import BaseModel, Field
from typing import List
from scraper import fetch_website_contents, fetch_website_links

class Link(BaseModel):
    type: str = Field(description="about, careers, etc")
    url: str = Field(description="full https URL")

class LinkSchema(BaseModel):
    links: List[Link]


link_system_prompt = '''
Select 5-6 relevant links, exclude Terms of Service, Privacy, email links.
Return JSON:
{"links":[{"type":"about","url":"https://..."}]}
'''


def select_relevant_links(url, model):
    links = fetch_website_links(url)[:10]
    links_text = "\n".join(links)

    messages = [
        {"role": "system", "content": link_system_prompt},
        {"role": "user", "content": links_text}
    ]

    structured_model = model.with_structured_output(LinkSchema)
    response = structured_model.invoke(messages)

    return response.model_dump()


def fetch_content_from_relevant_links(url, model):
    content = fetch_website_contents(url)
    data = select_relevant_links(url, model)

    landing_page = f"## Landing Page\n{content}\n\n### Relevant Links:\n"

    for link in data["links"]:
        landing_page += f"\n\n#### {link['type']}\n"
        landing_page += fetch_website_contents(link["url"])

    return landing_page