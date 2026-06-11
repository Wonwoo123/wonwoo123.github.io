import os
import re
import requests

# 1. Credentials from environment secrets
ZOTERO_USER_ID = os.environ.get("ZOTERO_USER_ID")
ZOTERO_API_KEY = os.environ.get("ZOTERO_API_KEY")
ZOTERO_COLLECTION_ID = os.environ.get("ZOTERO_COLLECTION_ID")

# 2. Fetch data from Zotero API
url = f"https://api.zotero.org/users/{ZOTERO_USER_ID}/collections/{ZOTERO_COLLECTION_ID}/items?format=json&direction=desc&sort=date"
headers = {"Zotero-API-Key": ZOTERO_API_KEY}
response = requests.get(url, headers=headers)
items = response.json()

html_content = ""

# 3. Parse and build your exact HTML structure loop
for index, item in enumerate(items):
    data = item.get("data", {})
    if data.get("itemType") == "attachment":
        continue  # Skip raw PDF files if they exist in the collection

    title = data.get("title", "")
    abstract = data.get("abstractNote", "")
    paper_id = f"paper_zotero_{index}"
    
    # Handle Creators / Co-authors
    creators = data.get("creators", [])
    author_names = []
    for c in creators:
        if c.get("creatorType") == "author":
            name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
            author_names.append(name)
    
    authors_str = ""
    if author_names:
        if len(author_names) == 1:
            authors_str = f"(with {author_names[0]})"
        else:
            authors_str = f"(with {', '.join(author_names[:-1])}, and {author_names[-1]})"

    # Grab extra metadata if available (e.g., arXiv stored in Extra or Archive fields)
    extra_field = data.get("extra", "")
    arxiv_match = re.search(r"arXiv:\s*([\d\.]+)", extra_field, re.IGNORECASE)
    arxiv_num = arxiv_match.group(1) if arxiv_match else ""
    
    # Generate item block matching your exact styling
    html_content += f"""
                    <li>
                        {title}
                        <span>
                        {authors_str if author_names else ""}
                        <a href="javascript:toggleAbstract('{paper_id}')">
                            <img src="./Images/dot4.png" id="{paper_id}Viewarrow" alt="Down Arrow" style="display: inline;">
                            <img src="./Images/dot3.png" id="{paper_id}Hidearrow" alt="Up Arrow" style="display: none;">
                        </a>
                        <br>
                        {data.get('publicationTitle', 'Preprint')}, {data.get('date', '2026')}.
                        <br>
                        """
    if arxiv_num:
        html_content += f'arXiv: <a href="https://arxiv.org/abs/{arxiv_num}" target="_blank" rel="noopener noreferrer">{arxiv_num}</a>'
        
    if abstract:
        html_content += f"""
                        <p id="{paper_id}" style="display: none; margin-top: 15px; padding-top: 15px; border-top: 1px dashed #ddd; font-weight: 400;">
                            <b>Abstract:</b> {abstract}
                        </p>
                        """
    html_content += """
                        </span>
                    </li>\n"""

# 4. Inject back into research.html file
with open("research.html", "r", encoding="utf-8") as f:
    file_data = f.read()

pattern = re.compile(
    r"().*?()", 
    re.DOTALL
)
updated_data = pattern.sub(f"\\1\n{html_content}                \\2", file_data)

with open("research.html", "w", encoding="utf-8") as f:
    f.write(updated_data)
