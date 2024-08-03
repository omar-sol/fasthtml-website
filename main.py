import pdb
import re

from fasthtml.common import *  # type: ignore
from fasthtml.components import Image, Sections, Svg
from fasthtml.svg import Path
from markdown import markdown

Link(rel="stylesheet", href="/globals.css")
app, rt = fast_app(  # type: ignore
    live_reload=True, hdrs=(Link(rel="stylesheet", href="/globals.css"),), pico=False
)

arrow_icon = Svg(
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


def create_a_element(url, text, **kwargs):
    return A(
        arrow_icon,
        Span(text, cls="link-text"),
        href=url,
        rel="noopener noreferrer",
        cls="link-item",
    )


@rt("/", methods=["GET"])
def home_page():
    links = Ul(
        Li(
            A(
                arrow_icon,
                Span("Blog", cls="link-text"),
                hx_get="/blog",
                hx_target="#maincontent",
                hx_swap="outerHTML",
                hx_push_url="true",
                cls="link-item",
            )
        ),
        Li(create_a_element("https://www.linkedin.com/in/omar-solano1/", "LinkedIn")),
        Li(create_a_element("https://github.com/omar-sol", "GitHub")),
        Li(create_a_element("mailto:omarsolano27@gmail.com", "Email me")),
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
            If you're interested in collaborating on innovative AI projects, feel free to reach out!""",
            id="mainparagraph",
        ),
        links,
        id="maincontent",
    )


@rt("/blog", methods=["GET"])
def blogs_list():

    blog_posts = os.listdir("content")
    blog_list_items = []

    for blog_post in blog_posts:
        with open(f"content/{blog_post}", "r") as f:
            content = f.read()

        # Extract the frontmatter and title
        frontmatter_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            title_match = re.search(r"title:\s*'(.+)'", frontmatter)
            title = (
                title_match.group(1) if title_match else blog_post.replace(".mdx", "")
            )
        else:
            title = blog_post.replace(".mdx", "")

        blog_list_items.append(
            Li(
                A(
                    title,
                    hx_get=f"/blog/{blog_post.replace('.mdx', '')}",
                    hx_target="#maincontent",
                    hx_swap="outerHTML",
                    hx_push_url="true",
                    cls="link-item",
                ),
                style="margin-bottom: 0.5rem;",
            )
        )

    blog_list = Ul(
        *blog_list_items,
        style="list-style-type: none; padding: 0;",
        cls="blog-list",
    )
    return Div(
        H2(
            "Blog",
            style="font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem;",
        ),
        blog_list,
        A(
            "← Back to home",
            hx_get="/",
            hx_target="#maincontent",
            hx_swap="outerHTML",
            hx_push_url="true",
            style="text-decoration: underline; color: #000000;",
        ),
        id="maincontent",
    )


@rt("/blog/{post_name}", methods=["GET"])
def blog_post(post_name: str):

    md_exts = "codehilite", "smarty", "extra", "sane_lists"

    def Markdown(s, exts=md_exts, **kw):
        html = markdown(s, extensions=exts)

        return Div(NotStr(html), **kw)

    # Read the content of the .mdx file
    with open(f"content/{post_name}.mdx", "r") as f:
        post = f.read()

    # Extract the frontmatter and content using regex
    frontmatter_match = re.match(r"^---\n(.*?)\n---\n(.*)", post, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        content = frontmatter_match.group(2)
        # Extract the title from frontmatter
        title_match = re.search(r"title:\s*'(.+)'", frontmatter)
        title = title_match.group(1) if title_match else post_name
    else:
        title = post_name
        content = post

    return Div(
        H1(title),
        Markdown(content),
        A(
            "← Back to blog list",
            hx_get="/blog",
            hx_target="#maincontent",
            hx_swap="outerHTML",
            hx_push_url="true",
        ),
        id="maincontent",
    )


serve()


# innerHTML: Replace the target element’s content with the result.
# outerHTML: Replace the target element with the result.
# beforebegin: Insert the result before the target element.
# beforeend: Insert the result inside the target element, after its last child.
# afterbegin: Insert the result inside the target element, before its first child.
# afterend: Insert the result after the target element.
