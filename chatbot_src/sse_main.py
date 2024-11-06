import asyncio
import json
import uuid

from claudette import Client
from components.daisy_components import navbar, sidebar
from fasthtml import FastHTML
from fasthtml.common import *
from fasthtml.svg import Path
from js_scripts import js_scripts

# from sse_starlette.sse import EventSourceResponse


# Set up the chat model client (https://claudette.answer.ai/)
client = Client(model="claude-3-haiku-20240307")
system_prompt = """You are a helpful assistant."""

app = FastHTML(
    live_reload=True,
    hdrs=(
        Script(src="https://cdn.tailwindcss.com"),
        Link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css",
        ),
        js_scripts,
    ),
)

chat_sessions = {}

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
# ... (Keep your existing SVG and icon definitions here) ...


def ChatMessage(session_id, msg_idx):
    msg = chat_sessions[session_id][msg_idx]
    text = "..." if msg["content"] == "" else msg["content"]
    generating = "generating" in msg and msg["generating"]

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
                        text,
                        cls="prose dark:prose-invert dark:text-white prose-p:leading-relaxed break-words",
                    ),
                    cls="space-y-1 overflow-hidden",
                ),
                cls="flex items-start space-x-7",
            ),
            cls="flex",
        )

    return Div(
        content,
        cls=f"mb-8 {'mr-2' if msg['role'] == 'user' else 'ml-2'}",
        id=f"chat-message-{session_id}-{msg_idx}",
        hx_trigger=f"sse:message-update-{session_id}-{msg_idx}",
        hx_swap="innerHTML",
    )


def ChatInput(session_id):
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


def main_layout(session_id):
    return Div(
        sidebar,
        Div(
            navbar,
            Div(
                Div(
                    Div(
                        Div(
                            *[
                                ChatMessage(session_id, i)
                                for i in range(len(chat_sessions[session_id]))
                            ],
                            id="chatlist",
                            cls="bg-base-100 p-8 overflow-y-auto flex-1",
                        ),
                        cls="flex flex-col flex-1 overflow-hidden",
                    ),
                    Form(
                        Div(
                            ChatInput(session_id),
                            Button(
                                arrow_right_svg,
                                type="submit",
                                id="send-button",
                                cls="btn btn-sm absolute right-2 top-1/2 transform -translate-y-1/2",
                            ),
                            cls="relative w-full",
                        ),
                        hx_post=f"/send_message/{session_id}",
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
        hx_sse=f"connect:/sse/{session_id}",
    )


@app.get("/")
def home():
    session_id = str(uuid.uuid4())
    chat_sessions[session_id] = []
    return Title("Chatbot"), Body(
        main_layout(session_id),
        cls="antialiased flex flex-col h-screen bg-gray-100",
    )


async def generate_response(session_id, msg_idx):
    messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in chat_sessions[session_id]
        if "generating" not in msg
    ]
    async for chunk in client(messages, sp=system_prompt, stream=True):
        chat_sessions[session_id][msg_idx]["content"] += chunk
        yield {
            "event": f"message-update-{session_id}-{msg_idx}",
            "data": json.dumps(
                {"content": chat_sessions[session_id][msg_idx]["content"]}
            ),
        }
        await asyncio.sleep(0.05)  # Small delay between chunks
    chat_sessions[session_id][msg_idx]["generating"] = False


@app.get("/sse/{session_id}")
async def sse(session_id: str):
    async def event_generator():
        while True:
            if session_id in chat_sessions:
                for msg_idx, msg in enumerate(chat_sessions[session_id]):
                    if msg.get("generating", False):
                        async for event in generate_response(session_id, msg_idx):
                            yield event
            await asyncio.sleep(0.1)

    return EventSourceResponse(event_generator())


@app.post("/send_message/{session_id}")
async def send_message(session_id: str, message: str):
    if not message.strip():
        return

    # Add user message to chat history
    user_idx = len(chat_sessions[session_id])
    chat_sessions[session_id].append({"role": "user", "content": message.rstrip()})

    # Add initial AI message
    ai_idx = len(chat_sessions[session_id])
    chat_sessions[session_id].append(
        {"role": "assistant", "generating": True, "content": ""}
    )

    # Return both messages and clear input
    return (
        ChatMessage(session_id, user_idx),
        ChatMessage(session_id, ai_idx),
        ChatInput(session_id),
        Script("scrollToBottom();"),
    )


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000)
if __name__ == "__main__":
    serve()
