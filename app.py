import gradio as gr
import requests
import os
import re
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY", "")
API_URL = os.getenv("API_URL", "https://openrouter.ai/api/v1/chat/completions")
MODEL = os.getenv("MODEL", "moonshotai/Kimi-K2-Thinking")

# Load the prompt template
def load_prompt():
    with open("prompt.txt", "r") as f:
        return f.read()

PROMPT_TEMPLATE = load_prompt()

def generate_human_text(content: str, progress=gr.Progress()):
    """Generate human-like text using Kimi-K2-Thinking model."""

    if not content.strip():
        yield "⚠️ Please enter some content!"
        return

    if not API_KEY:
        yield "⚠️ API key not configured. Please contact the administrator."
        return

    progress(0.1, desc="Preparing request...")

    # Build the prompt
    prompt = PROMPT_TEMPLATE.replace("{content}", content)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 16000,
        "stream": True
    }

    progress(0.3, desc="Connecting to AI...")

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=180,
            stream=True
        )

        response.raise_for_status()

        progress(0.5, desc="Receiving response...")

        full_content = ""
        is_streaming_answer = False

        # Process streaming response
        for line in response.iter_lines():
            if not line:
                continue

            line = line.decode('utf-8')

            if line.startswith('data: '):
                data_str = line[6:]

                if data_str == '[DONE]':
                    break

                try:
                    data = json.loads(data_str)
                    if 'choices' in data and len(data['choices']) > 0:
                        delta = data['choices'][0].get('delta', {})
                        chunk = delta.get('content', '')

                        if chunk:
                            full_content += chunk

                            # Wait until thinking is done
                            if '</think>' in full_content and not is_streaming_answer:
                                is_streaming_answer = True
                                progress(0.7, desc="Generating human-like text...")

                            # Only stream if we're past the thinking phase
                            if is_streaming_answer:
                                # Remove all thinking content
                                clean_content = re.sub(r'<think>.*?</think>', '', full_content, flags=re.DOTALL)
                                clean_content = clean_content.strip()

                                if clean_content:
                                    yield clean_content
                except:
                    continue

        progress(1.0, desc="Done!")

        # Final cleanup - remove all thinking tokens
        final_content = re.sub(r'<think>.*?</think>', '', full_content, flags=re.DOTALL)
        # Also remove any remaining unclosed think tags
        final_content = re.sub(r'<think>.*$', '', final_content, flags=re.DOTALL)
        final_content = final_content.strip()

        yield final_content if final_content else "⚠️ No content generated. Please try again with different text."

    except requests.exceptions.Timeout:
        yield "⏱️ Request timed out. The AI is taking too long to respond. Try with shorter text or try again later."
    except requests.exceptions.RequestException as e:
        yield f"❌ API Error: {str(e)}"
    except Exception as e:
        yield f"❌ Unexpected error: {str(e)}"

# Create the Gradio interface
with gr.Blocks(title="Human-Like Text Generator - Kimi K2") as app:
    gr.Markdown("""
    # ✍️ Human-Like Text Generator
    Transform AI-generated or formal text into natural, human-sounding content using Open Source Model.

    ⚡ **Streaming enabled!** You'll see the text appear in real-time as the AI writes.
    """)

    with gr.Row():
        with gr.Column():
            content = gr.Textbox(
                label="Your Content",
                placeholder="Paste the content you want rewritten in a human style...",
                lines=12,
                max_lines=20
            )
            generate_btn = gr.Button("🚀 Generate Human Version", variant="primary", size="lg")

        with gr.Column():
            output = gr.Textbox(
                label="Human-Like Output",
                lines=12,
                max_lines=20
            )

    gr.Markdown("💡 **Tip:** For best results, paste clear, complete paragraphs. The output will match the length and topic of your input.")

    generate_btn.click(
        fn=generate_human_text,
        inputs=[content],
        outputs=output
    )

    content.submit(
        fn=generate_human_text,
        inputs=[content],
        outputs=output
    )

if __name__ == "__main__":
    app.launch()
