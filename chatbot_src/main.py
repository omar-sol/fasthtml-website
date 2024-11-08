import logging
import pdb

import instructor
import logfire
import markdown
from claudette import Client
from components.daisy_components import navbar, sidebar
from fastcore.all import threaded
from fasthtml import FastHTML
from fasthtml.common import *  # type: ignore
from fasthtml.svg import Path
from js_scripts import js_scripts
from openai import AsyncOpenAI, OpenAI

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)
# logfire.configure()

sync_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),timeout=60, max_retries=0) 
# logfire.instrument_openai(sync_client)
# sync_client= instructor.from_openai(sync_client)

# async_client = AsyncOpenAI(timeout=60, max_retries=0)
# logfire.instrument_openai(async_client)
# async_client= instructor.from_openai(async_client)

# Set up the app, including daisyui and tailwind for the chat component
tlink = Script(src="https://cdn.tailwindcss.com")

dlink = Link(
    rel="stylesheet",
    href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css",
)

custom_tailwind = Style("""
    @tailwind base;
    @tailwind components;
    @tailwind utilities;

    @layer components {
        .prose pre {
            background-color: #FFFFFF;
            color: #000000;
            padding: 0.5rem;
            border-radius: 1rem;
            border: 0.1rem solid #000000 !important;
            }
        .prose code {
            padding: 0.2em 0.4em;
            background-color: #FFFFFF;
            border-radius: 0.25rem;
            border: 0.05rem solid #FFFF00 !important;
        }
                        
        /* Add styles for specific syntax highlighting classes */
        .codehilite .k { color: #007020; font-weight: bold; } /* Keyword */
        .codehilite .s { color: #4070a0; } /* String */
        .codehilite .c { color: #60a0b0; font-style: italic; } /* Comment */
        /* Add more classes as needed */
    }
""")

app = FastHTML(
    live_reload=True,
    hdrs=(
        tlink,
        dlink,
        custom_tailwind,
        js_scripts,
    ),
)

chat_history = []

arrow_right_svg = Svg(
    Path(d="M5 12h14"),
    Path(d="m12 5 7 7-7 7"),
    xmlns="http://www.w3.org/2000/svg",
    width="16",
    height="16",
    viewBox="0 0 24 24",
    fill="none",
    stroke="currentColor",
    stroke_width="2",
    stroke_linecap="round",
    stroke_linejoin="round",
    cls="lucide lucide-arrow-right",
)

assistant_icon = Svg(
    Path(
        d="M152,96H104a8,8,0,0,0-8,8v48a8,8,0,0,0,8,8h48a8,8,0,0,0,8-8V104A8,8,0,0,0,152,96Zm-8,48H112V112h32Zm88,0H216V112h16a8,8,0,0,0,0-16H216V56a16,16,0,0,0-16-16H160V24a8,8,0,0,0-16,0V40H112V24a8,8,0,0,0-16,0V40H56A16,16,0,0,0,40,56V96H24a8,8,0,0,0,0,16H40v32H24a8,8,0,0,0,0,16H40v40a16,16,0,0,0,16,16H96v16a8,8,0,0,0,16,0V216h32v16a8,8,0,0,0,16,0V216h40a16,16,0,0,0,16-16V160h16a8,8,0,0,0,0-16Zm-32,56H56V56H200v95.87s0,.09,0,.13,0,.09,0,.13V200Z"
    ),
    xmlns="http://www.w3.org/2000/svg",
    width="28",
    height="28",
    fill="currentColor",
    viewbox="0 0 256 256",
)


def ChatMessage(msg_idx):
    msg = chat_history[msg_idx]
    text = "..." if msg["content"] == "" else msg["content"]
    content = msg.get("html_content", "") if msg["content"] else "..."
    generating = "generating" in msg and msg["generating"]
    stream_args = (
        {
            "hx-trigger": "every 0.1s",
            "hx-swap": "outerHTML",
            "hx-get": f"/chat_message/{msg_idx}",
        }
        if generating
        else {}
    )

    if msg["role"] == "user":
        content = Div(
            Div(
                text,
                cls="prose dark:prose-invert dark:text-white prose-p:leading-relaxed break-words px-5 py-2.5 rounded-3xl bg-base-200 inline-block max-w-full",
            ),
            cls="flex justify-end",
        )
    else:
        content = Div(
            Div(
                Div(
                    assistant_icon,
                    cls="text-gray-800 dark:text-white flex size-[24px] shrink-0 select-none items-center justify-center rounded-md border shadow-sm dark:border-gray-700 dark:bg-gray-800",
                ),
                Div(
                    Div(
                        content,
                        cls="prose dark:prose-invert dark:text-white prose-p:leading-relaxed break-words",
                    ),
                    cls="space-y-1 overflow-hidden",
                ),
                # cls="flex items-start space-x-7 border border-yellow-500",
                cls="flex items-start space-x-7",
            ),
            cls="flex",
        )

    return Div(
        content,
        # cls=f"mb-8 {'mr-2' if msg["role"] == "user" else 'ml-2'} border border-purple-500",
        cls=f"mb-8 {'mr-2' if msg["role"] == "user" else 'ml-2'}",
        id=f"chat-message-{msg_idx}",
        **stream_args,
    )


# Route that gets polled while streaming
@app.get("/chat_message/{msg_idx}")
def get_chat_message(msg_idx: int):
    if msg_idx >= len(chat_history):
        print("Message index out of range")
        return ""
    return ChatMessage(msg_idx)


# The input field for the user message
def ChatInput():
    return Input(
        type="text",
        name="message",
        id="message-input",
        placeholder="Ask me anything ...",
        cls="w-full pl-3 pr-16 py-2 text-gray-700 border rounded-lg focus:outline-none dark:text-white dark:border-gray-700",
        hx_swap_oob="true",
        oninput="toggleButton()",
        autofocus=True,
    )


main_layout = Div(
    sidebar,
    Div(
        navbar,
        Div(
            Div(
                Div(
                    Div(
                        *[ChatMessage(i) for i in range(len(chat_history))],
                        id="chatlist",
                        cls="bg-base-100 p-8 overflow-y-auto flex-1",
                    ),
                    cls="flex flex-col flex-1 overflow-hidden",
                ),
                Form(
                    Div(
                        ChatInput(),
                        Button(
                            arrow_right_svg,
                            type="submit",
                            id="send-button",
                            cls="btn btn-sm absolute right-2 top-1/2 transform -translate-y-1/2",
                        ),
                        cls="relative w-full",
                    ),
                    hx_post="/send_message",
                    hx_target="#chatlist",
                    hx_swap="beforeend",
                    cls="bg-base-100 p-4 rounded-t-lg shadow-md w-full max-w-3xl mx-auto border border-gray-200",
                ),
                id="main-content",
                cls="flex flex-col h-full w-full max-w-4xl mx-auto",
            ),
            cls="flex flex-col flex-grow overflow-auto",
        ),
        cls="flex flex-col flex-grow overflow-hidden",
    ),
    cls="flex flex-1 h-screen bg-base-100 overflow-hidden",
)


@app.get("/")
def home():
    return Title("Chatbot"), Body(
        main_layout,
        cls="antialiased flex flex-col h-screen bg-gray-100",
    )


# Generate AI response
@threaded
def generate_response(idx):
    system_prompt = """You are a helpful assistant."""
    messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in chat_history
        if "generating" not in msg
    ]
    messages.insert(0, {"role": "system", "content": system_prompt})
    response = sync_client.chat.completions.create(model="gpt-4o", messages=messages, stream=True)
    for chunk in response:
        token = chunk.choices[0].delta.content
        token = "" if token is None else token
        chat_history[idx]["content"] += token

        # Convert the entire content to HTML after each token
        html_content = markdown.markdown(chat_history[idx]["content"], extensions=['fenced_code', 'codehilite'])
        chat_history[idx]["html_content"] = NotStr(html_content)

    chat_history[idx]["generating"] = False



# Handle sending a message
@app.post("/send_message")
def send_message(message: str):

    if not message.strip():
        return

    # Add user message to chat history
    user_idx = len(chat_history)
    print("user_idx", user_idx)  # user_idx 0
    chat_history.append({"role": "user", "content": message.rstrip()})

    # Add initial AI message
    ai_idx = len(chat_history)
    print("ai_idx", ai_idx)  # ai_idx 1
    chat_history.append({"role": "assistant", "generating": True, "content": ""})

    # Start generating response in background
    generate_response(ai_idx)

    # Return both messages and clear input
    return (
        ChatMessage(user_idx),
        ChatMessage(ai_idx),
        ChatInput(),
        Script("scrollToBottom();"),
    )


# # Serve static files (for background image)
# @app.get("/ui/{file}")
# async def static_file(file: str):
#     return FileResponse(f"ui/{file}")


if __name__ == "__main__":
    serve()


# innerHTML: Replace the target element’s content with the result.
# outerHTML: Replace the target element with the result.
# beforebegin: Insert the result before the target element.
# beforeend: Insert the result inside the target element, after its last child.
# afterbegin: Insert the result inside the target element, before its first child.
# afterend: Insert the result after the target element.
