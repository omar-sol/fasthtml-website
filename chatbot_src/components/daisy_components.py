from fasthtml.common import *  # type: ignore
from fasthtml.svg import Path


def toggle_button(id):
    return Button(
        Svg(
            Path(
                d="M216,40H40A16,16,0,0,0,24,56V200a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V56A16,16,0,0,0,216,40ZM40,56H80V200H40ZM216,200H96V56H216V200Z"
            ),
            xmlns="http://www.w3.org/2000/svg",
            width="24",
            height="24",
            fill="currentColor",
            viewbox="0 0 256 256",
        ),
        id=id,
        onclick="toggleSidebar()",
        cls=f"btn btn-square btn-ghost {'hidden' if 'navbar' in id else ''} dark:text-gray-300",
    )


navbar = Div(
    Div(
        toggle_button("navbar-open-btn"),
        cls="flex-none",
    ),
    Div(A("Chatbot", cls="btn btn-ghost text-xl dark:text-gray-300"), cls="flex-1"),
    Div(
        Button(
            Svg(
                Path(
                    stroke_linecap="round",
                    stroke_linejoin="round",
                    stroke_width="2",
                    d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z",
                ),
                xmlns="http://www.w3.org/2000/svg",
                fill="none",
                viewbox="0 0 24 24",
                cls="inline-block h-5 w-5 stroke-current",
            ),
            cls="btn btn-square btn-ghost",
        ),
        cls="flex-none",
    ),
    # cls="navbar bg-base-100 flex-none border border-red-500",
    cls="navbar bg-base-100 flex-none",
)

sidebar = Div(
    Div(
        Div(
            Div(
                toggle_button("sidebar-close-btn"),
                cls="flex-none",
            ),
            cls="navbar flex-none",
        ),
        Ul(
            Li(
                A(
                    "Conversation Summary Request",
                    cls="hover:bg-base-300 whitespace-nowrap overflow-hidden text-ellipsis dark:text-gray-100",
                )
            ),
            Li(
                A(
                    "AI Question Handling Guide",
                    cls="hover:bg-base-300 whitespace-nowrap overflow-hidden text-ellipsis dark:text-gray-100",
                )
            ),
            Li(
                A(
                    "Data Science Job Listings",
                    cls="hover:bg-base-300 whitespace-nowrap overflow-hidden text-ellipsis dark:text-gray-100",
                )
            ),
            cls="menu pt-4 pl-1 flex-grow bg-base-200 text-base-content",
        ),
        cls="flex flex-col h-full",
    ),
    id="sidebar",
    cls="flex flex-col items-start w-64 bg-base-200 overflow-hidden transition-all duration-150 ease-in-out rounded-r-lg",
)
