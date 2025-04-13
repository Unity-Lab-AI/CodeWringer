import requests
from bs4 import BeautifulSoup
import html2text
import logging

metadata = {
    "name": "search",
    "description": "Performs a web search using DuckDuckGo and extracts content as Markdown."
}

def execute(task: str) -> str:
    logger = logging.getLogger("SearchTool")
    query = task.strip()
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for result in soup.select(".result__body")[:3]:  # Top 3 results
            title = result.select_one(".result__title a") or "No title"
            title = title.text if hasattr(title, "text") else "No title"
            url = result.select_one(".result__url")
            url = url.text.strip() if url else ""
            if url:
                if not url.startswith(("http://", "https://")):
                    url = f"https://{url}"
                h = html2text.HTML2Text()
                h.ignore_links = False
                markdown = h.handle(requests.get(url, headers=headers, timeout=10).text)
                results.append(f"### {title}\n\n{markdown[:2000]}")
        logger.info(f"Search completed for query: {query}")
        return "\n\n".join(results) if results else "No relevant web content found."
    except Exception as e:
        logger.error(f"Search failed for query '{query}': {e}")
        return f"Error: {str(e)}"