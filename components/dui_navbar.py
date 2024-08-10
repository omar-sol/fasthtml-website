from fasthtml import FastHTML
from fasthtml.common import *  # type: ignore
from fasthtml.svg import Path

navbar = Div(
    Div(
        Button(
            Svg(
                Path(
                    stroke_linecap="round",
                    stroke_linejoin="round",
                    stroke_width="2",
                    d="M4 6h16M4 12h16M4 18h16",
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
    Div(A("Chatbot", cls="btn btn-ghost text-xl"), cls="flex-1"),
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
    cls="navbar bg-base-100",
)

# navbar = Div(
#     Div(A("Chatbot", cls="btn btn-ghost text-xl"), cls="flex-1"),
#     Div(
#         Button(
#             Svg(
#                 Path(
#                     stroke_linecap="round",
#                     stroke_linejoin="round",
#                     stroke_width="2",
#                     d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z",
#                 ),
#                 xmlns="http://www.w3.org/2000/svg",
#                 fill="none",
#                 viewbox="0 0 24 24",
#                 cls="inline-block h-5 w-5 stroke-current",
#             ),
#             cls="btn btn-square btn-ghost",
#         ),
#         cls="flex-none",
#     ),
#     cls="navbar bg-base-100 fixed top-0 left-0 right-0 z-10",
# )

# sidebar = Div(
#     Ul(
#         Li(A("Sidebar Item 1", cls="hover:bg-base-300")),
#         Li(A("Sidebar Item 2", cls="hover:bg-base-300")),
#         cls="menu p-4 w-80 h-full bg-base-200 text-base-content",
#     ),
#     cls="fixed top-16 left-0 w-80 h-[calc(100vh-4rem)] bg-base-200 overflow-y-auto border border-green-500",
# )
