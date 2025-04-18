# import packages
import os
from datetime import datetime
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

def get_elsevier_articles(topic, min_citations=0, limit=10, start_date=None, end_date=None):
    """
    Fetch journal articles from the Elsevier Scopus API using API key from .env file.

    Parameters:
        topic (str): Search topic/query.
        min_citations (int): Minimum number of citations an article must have.
        limit (int): Maximum number of articles to retrieve.

    Returns:
        List of dictionaries containing title, journal link, and DOI link.
    """
    api_key = os.getenv("ELSEVIER_API_KEY")
    if not api_key:
        raise EnvironmentError("Missing ELSEVIER_API_KEY in .env file.")

    base_url = "https://api.elsevier.com/content/search/scopus"
    headers = {
        "Accept": "application/json",
        "X-ELS-APIKey": api_key
    }
    params = {
        "query": f"TITLE-ABS-KEY({topic})",
        "count": min(25, limit),
        "sort": "citedby-count",
        "view": "STANDARD",
        # "view": "COMPLETE"
    }

    articles = []
    start = 0

    while len(articles) < limit:
        params['start'] = start
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        results = response.json().get('search-results', {}).get('entry', [])
        if not results:
            break

        for entry in results:
            citations = int(entry.get('citedby-count', 0))
            if citations >= min_citations:
                title = entry.get('dc:title')
                doi = entry.get('prism:doi')
                journal = entry.get('prism:publicationName')
                journal_link = entry.get('prism:url', 'N/A')
                doi_link = f"https://doi.org/{doi}" if doi else "N/A"
                pub_date = entry.get('prism:coverDate', 'N/A')
                authors = entry.get('dc:creator', 'N/A')
                
                ## If you have `"view": "COMPLETE"` on API call
                # authors_list = entry.get('author', [])
                # if isinstance(authors_list, list):
                #     author_names = [f"{a.get('given-name', '')} {a.get('surname', '')}".strip() for a in authors_list]
                #     authors = ', '.join(author_names) if author_names else entry.get('dc:creator', 'N/A')
                # else:
                #     authors = entry.get('dc:creator', 'N/A')

                
                
                # Filter by date range if applicable
                if pub_date != 'N/A' and (start_date or end_date):
                    try:
                        pub_dt = datetime.strptime(pub_date, '%Y-%m-%d')
                        if start_date and pub_dt < datetime.strptime(start_date, '%Y-%m-%d'):
                            continue
                        if end_date and pub_dt > datetime.strptime(end_date, '%Y-%m-%d'):
                            continue
                    except ValueError:
                        continue  # Skip entries with invalid date format
                
                

                articles.append({
                    "title": title,
                    "authors": authors,
                    "publication_date": pub_date,
                    "citations": citations,
                    "journal": journal,
                    "journal_link": journal_link,
                    "doi_link": doi_link,
                })

                if len(articles) >= limit:
                    break

        start += params['count']

    return articles