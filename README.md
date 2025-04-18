## 📚 Elsevier Article Fetcher (Scopus API)

This Python script allows you to **search for academic journal articles** from Elsevier's Scopus database using their public API. It supports topic-based search, filtering by citation count, publication date, and returns key metadata like title, author(s), journal, and DOI link.

---

### ✨ Features

- Search articles by topic using Scopus (`TITLE-ABS-KEY`)
- Filter by:
  - Minimum number of citations
  - Date range (start and end)
- Retrieve metadata:
  - Title
  - Author (lead/first author)
  - Journal name and link
  - DOI and citation count
- Export results to a Pandas DataFrame

---

### 🧰 Requirements

- Python 3.7+
- Dependencies (install via pip):

```bash
pip install requests pandas python-dotenv
```

- A valid [Elsevier API Key](https://dev.elsevier.com/)

---

### 🔐 Setup

1. Get your Elsevier API key from [Elsevier Developer Portal](https://dev.elsevier.com/user/login).
2. Create a `.env` file in your project directory and add:

```
ELSEVIER_API_KEY=your_api_key_here
```

---

### 🚀 Usage

```python
from elsevier_fetcher import get_elsevier_articles

# Example query
topic = "impact of tariff policy on trade"
articles = get_elsevier_articles(topic, min_citations=10, limit=5)

# Convert to DataFrame
import pandas as pd
df = pd.DataFrame(articles)
print(df.head())
```

---

### 🧠 Function Signature

```python
get_elsevier_articles(
    topic: str,
    min_citations: int = 0,
    limit: int = 10,
    start_date: str = None,  # format: 'YYYY-MM-DD'
    end_date: str = None     # format: 'YYYY-MM-DD'
) -> List[Dict]
```

---

### 📝 Sample Output (as DataFrame)

| title | authors | publication_date | citations | journal | journal_link | doi_link |
|-------|---------|------------------|-----------|---------|---------------|----------|
| Article Title | John Smith | 2023-06-14 | 45 | Journal of Economic Policy | ... | https://doi.org/... |

---

### ⚠️ Notes

- Due to access limitations, this script uses the `"STANDARD"` view from the API, which usually only returns the lead author's name via `dc:creator`.
- Using the `"COMPLETE"` view or detailed author data requires institutional access.

---

### 📄 License

MIT License