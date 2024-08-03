from fasthtml.common import *  # type: ignore
from fasthtml.components import Svg
from fasthtml.svg import Path

# Add Tailwind CSS via CDN
tailwind_cdn = Link(
    rel="stylesheet",
    href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css",
)
# tailwind_cdn = Script(
#     src="https://cdn.tailwindcss.com",
# )


# Custom CSS
custom_css = Style(
    """
body {
    font-family: Times, serif;
    padding: 0 10px;
}

::selection {
    background-color: #47a3f3;
    color: #fefefe;
}

.prose {
    transition: all;
    color: black;
    text-underline-offset: 2px;
    text-decoration-thickness: 0.1em;
    font-weight: 500;
    line-height: 1.75;
}

.dark .prose {
    color: white;
}

.prose img {
    margin: 0;
}

.prose > :first-child {
    margin-top: 1.25em !important;
    margin-bottom: 1.25em !important;
}
"""
)

app, rt = fast_app(  # type: ignore
    live_reload=True,
    hdrs=(tailwind_cdn, custom_css),
    pico=False,
)


def ArrowIcon():
    return Svg(
        Path(
            d="M2.07102 11.3494L0.963068 10.2415L9.2017 1.98864H2.83807L2.85227 0.454545H11.8438V9.46023H10.2955L10.3097 3.09659L2.07102 11.3494Z",
            fill="currentColor",
        ),
        width="12",
        height="12",
        viewBox="0 0 12 12",
        fill="none",
        xmlns="http://www.w3.org/2000/svg",
    )


def create_a_element(url, text):
    return A(
        ArrowIcon(),
        P(text, cls="h-7 ml-2"),
        href=url,
        rel="noopener noreferrer",
        target="_blank",
        cls="flex items-center hover:text-neutral-800 dark:hover:text-neutral-100 transition-all",
    )


@rt("/")
def get():
    links = Ul(
        Li(
            create_a_element(
                "https://www.linkedin.com/in/omar-solano-539a091b5/", "LinkedIn"
            )
        ),
        Li(create_a_element("mailto:omarsolano27@gmail.com", "Email me")),
        Li(create_a_element("/omar_solano_resume.pdf", "CV")),
        cls="flex flex-col md:flex-row mt-8 space-x-0 md:space-x-4 space-y-2 md:space-y-0 font-sm text-black dark:text-neutral-300",
    )

    return Title("Omar Solano"), Body(
        Main(
            Section(
                H1(
                    "Omar Solano",
                    cls="font-bold text-2xl mb-8 tracking-tighter",
                ),
                P(
                    """Hello! I'm a Machine Learning Engineer with over three years of experience.
                    I completed my undergraduate studies at École de technologie supérieure (ÉTS) in Montréal, Canada,
                    and I'm currently pursuing a Master's degree with a focus on AI.
                    Passionate about using AI to enhance and upgrade products.
                    If you're interested in collaborating on innovative AI projects, feel free to reach out!""",
                    cls="prose prose-neutral dark:prose-invert max-w-none",
                ),
                links,
                cls="max-w-4xl",
            ),
            cls="flex-auto min-w-0 mt-6 flex flex-col px-2 md:px-0",
        ),
        cls="antialiased max-w-2xl mb-40 flex flex-col md:flex-row mx-4 mt-8 lg:mx-auto",
    )


serve()
