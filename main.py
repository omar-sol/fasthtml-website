from fasthtml.common import *  # type: ignore
from fasthtml.components import Svg
from fasthtml.svg import Path

# app, rt = fast_app(live_reload=True, hdrs=(), pico=False)  # type: ignore
Link(rel="stylesheet", href="/globals.css")
app, rt = fast_app(  # type: ignore
    live_reload=True, hdrs=(Link(rel="stylesheet", href="/globals.css"),), pico=False
)


def create_a_element(url, text):
    return A(
        Svg(
            Path(
                d="M2.07102 11.3494L0.963068 10.2415L9.2017 1.98864H2.83807L2.85227 0.454545H11.8438V9.46023H10.2955L10.3097 3.09659L2.07102 11.3494Z",
                fill="currentColor",
            ),
            width="12",
            height="12",
            viewBox="0 0 12 12",
            fill="none",
            xmlns="http://www.w3.org/2000/svg",
        ),
        Span(text, cls="link-text"),
        href=url,
        rel="noopener noreferrer",
        target="_blank",
        cls="link-item",
    )


@rt("/")
def get():
    links = Ul(
        Li(create_a_element("https://www.linkedin.com/in/omar-solano1/", "LinkedIn")),
        Li(create_a_element("mailto:omarsolano27@gmail.com", "Email me")),
        Li(create_a_element("/omar_solano_resume.pdf", "CV")),
        cls="link-list",
    )

    return Title("Omar Solano"), Div(
        H2(
            "Omar Solano",
            style="font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem;",
        ),
        P(
            """Hello! I'm a Machine Learning Engineer with over three years of experience.
            I completed my undergraduate studies at École de technologie supérieure (ÉTS) in Montréal, Canada,
            and I'm currently pursuing a Master's degree with a focus on AI.
            Passionate about using AI to enhance and upgrade products.
            If you're interested in collaborating on innovative AI projects, feel free to reach out!"""
        ),
        links,
        id="maincontent",
    )


serve()
