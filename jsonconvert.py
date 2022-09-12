import json
import re

# --- Constants ---

VIDEO_SOURCES = {
    "youtube": """<iframe width="560" height="315" src="https://www.youtube.com/embed/{}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>""",
}

# --- Utilities ---

def normalize_url(url: str) -> str:
    return f"https:{url}" if url[:2] == "//" else url

def unescape(s: str) -> str:
    return re.sub(r"\\(.)", r"\1", s)

def replace_markdown_links(s: str):
    return re.sub(r"\[(.+)\]\((.+\))", r"""<a href="\2">\1</a>""", s)

def replace_curly_quotes(s: str):
    return re.sub(r"([“”])", r'"', s)

# --- Parsers ---

def parse_unrecognized(s: dict):
    print("Parser found unrecognized value, please enter replacement html:")
    print(s)
    return input("Replacement HTML: ")

def parse_text(s: dict) -> str:
    return f"<p>{replace_markdown_links(s['text'])}</p>"

def parse_heading(s: dict) -> str:
    return f"<h1>{s['text']}</h1>"

def parse_image(s: dict) -> str:
    img_url = normalize_url(s["file"]["full"])
    img_alt = s["text"]

    return f"""<img src="{img_url}" alt="{img_alt}">"""

def parse_video(s: dict) -> str:
    source_html = VIDEO_SOURCES.get(s["source"])
    if source_html == None:
        return parse_unrecognized(s)
    
    return source_html.format(s["remote_id"])

def parse_list(s: dict) -> str:
    lines = s["text"].split("\n")
    trimmed_lines = []

    for line in lines:
        if line == "":
            continue
        # print(line[:3])
        # assert line[:3] == " - "
        trimmed_lines.append(unescape(line[3:]))
    
    html_string = "<ul>"

    for line in trimmed_lines:
        html_string += f"<li>{line}</li>"
    
    html_string += "</ul>"
    return html_string

PARSERS = {
    "text": parse_text,
    "heading": parse_heading,
    "image": parse_image,
    "video": parse_video,
    "list": parse_list,
}

# --- Main Converter ---

def handle_item(s: dict) -> str:
    parser = PARSERS[s["type"]]
    if parser == None:
        return parse_unrecognized(s["data"])
    return parser(s["data"])

def convert_to_html(filestr: str) -> str:
    json_structure = json.loads(replace_curly_quotes(filestr))
    data = json_structure["data"]
    html_out = ""

    for item in data:
        html_out += handle_item(item)
    
    return html_out

# --- Main ---

if __name__ == "__main__":
    fname_in = input("Input File > ")
    fname_out = input("Output File > ")

    if fname_out == "":
        fname_out = re.sub(r"(.+)\..+", r"\1_out.html", fname_in)

    with open(fname_in, "r") as f:
        html = convert_to_html(f.read())
        with open(fname_out, "w") as output:
            output.write(html)

    print("Conversion Done!")