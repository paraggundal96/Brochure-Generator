import gradio as gr
from brochureGenerator import create_brochure



with gr.Blocks() as app:
    gr.Markdown("# 📄 AI Brochure Generator")

    # INPUTS
    company_name = gr.Textbox(label="Company Name")
    url = gr.Textbox(label="Website URL")

    source = gr.Radio(
        choices=["OpenRouter", "Local"],
        label="Model Source",
        value="Local"
    )

    model = gr.Dropdown(
        choices=[
            "arcee-ai/trinity-mini:free",
            "openai/gpt-oss-20b:free",
            "llama3.2:latest",
            "phi3:mini"
        ],
        label="Model"
    )

    # OUTPUT
    output = gr.Markdown(label="Brochure")

    # BUTTON
    generate_btn = gr.Button("Generate Brochure")

    # FUNCTION BINDING
    generate_btn.click(
        fn=create_brochure,
        inputs=[company_name, url, source, model],
        outputs=output
    )

app.launch()