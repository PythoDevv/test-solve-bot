from bs4 import BeautifulSoup

def is_html_valid(html):
    parsed_html = str(BeautifulSoup(html, "html.parser"))
    
    # If the parsed version differs from the original, it's invalid
    return html.strip() == parsed_html.strip()
