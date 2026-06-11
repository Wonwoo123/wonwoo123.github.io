import os
import re
import requests

# --- YOUR CO-AUTHOR ROLODEX ---
# Add your co-authors and their website links here.
# Make sure to spell their names exactly as they appear in Zotero!
COAUTHOR_LINKS = {
    "Esther Banaian": "https://sites.google.com/view/esther-banaian/home",
    "Elizabeth Kelley": "https://sites.google.com/view/elizabeth-kelley/home",
    "Ezgi Kantarcı Oğuz":"https://sites.google.com/view/ezgikantarcioguz/main-page",
    "Emine Yıldırım":"https://emine-yildirim.github.io/",
    "Heehyun Park": "https://sites.google.com/view/heehyunpark/home",
    "Inkee Jung" : "https://inkeej.github.io/",
    # "Another Author": "https://their-website.com",
}
# ------------------------------

ZOTERO_USER_ID = os.environ.get("ZOTERO_USER_ID")
ZOTERO_API_KEY = os.environ.get("ZOTERO_API_KEY")
ZOTERO_COLLECTION_ID = os.environ.get("ZOTERO_COLLECTION_ID")

url = f"https://api.zotero.org/users/{ZOTERO_USER_ID}/collections/{ZOTERO_COLLECTION_ID}/items?format=json&direction=desc&sort=date"
headers = {"Zotero-API-Key": ZOTERO_API_KEY}
response = requests.get(url, headers=headers)
items = response.json()

published_html = ""
preprint_html = ""

for index, item in enumerate(items):
    data = item.get("data", {})
    item_type = data.get("itemType", "")
    
    if item_type == "attachment":
        continue

    title = data.get("title", "")
    abstract = data.get("abstractNote", "")
    paper_id = f"paper_zotero_{index}"
    
    creators = data.get("creators", [])
    author_names = []
    for c in creators:
        if c.get("creatorType") == "author":
            name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
            
            # Skip your own name
            if name.lower() != "wonwoo kang":
                # Check if the co-author is in your Rolodex
                if name in COAUTHOR_LINKS:
                    linked_name = f'<a href="{COAUTHOR_LINKS[name]}" target="_blank" rel="noopener noreferrer">{name}</a>'
                    author_names.append(linked_name)
                else:
                    # If not in Rolodex, just print their plain name
                    author_names.append(name)
    
    authors_str = ""
    if author_names:
        if len(author_names) == 1:
            authors_str = f"(with {author_names[0]})"
        else:
            authors_str = f"(with {', '.join(author_names[:-1])}, and {author_names[-1]})"

    extra_field = data.get("extra", "")
    arxiv_match = re.search(r"arXiv:\s*([\d\.]+)", extra_field, re.IGNORECASE)
    arxiv_num = arxiv_match.group(1) if arxiv_match else ""
    
    pub_title = data.get('publicationTitle', '').strip()
    pub_date = data.get('date', '2026')

    is_preprint = False
    if item_type == 'preprint' or 'preprint' in pub_title.lower() or 'arxiv' in pub_title.lower() or not pub_title:
        is_preprint = True

    display_title = pub_title if pub_title else 'Preprint'

    item_html = '\n                    <li>\n'
    item_html += f'                        {title}\n'
    item_html += '                        <span>\n'
    
    if author_names:
        item_html += f'                        {authors_str}\n'
        
    item_html += f'                        <a href="javascript:toggleAbstract(\'{paper_id}\')">\n'
    item_html += f'                            <img src="./Images/dot4.png" id="{paper_id}Viewarrow" alt="Down Arrow" style="display: inline;">\n'
    item_html += f'                            <img src="./Images/dot3.png" id="{paper_id}Hidearrow" alt="Up Arrow" style="display: none;">\n'
    item_html += '                        </a>\n'
    item_html += f'                        <br>\n'
    item_html += f'                        {display_title}, {pub_date}.\n'
    item_html += f'                        <br>'
    
    if arxiv_num:
        item_html += f'\n                        arXiv: <a href="https://arxiv.org/abs/{arxiv_num}" target="_blank" rel="noopener noreferrer">{arxiv_num}</a>'
        
    if abstract:
        item_html += f'\n                        <p id="{paper_id}" style="display: none; margin-top: 15px; padding-top: 15px; border-top: 1px dashed #ddd; font-weight: 400;">\n'
        item_html += f'                            <b>Abstract:</b> {abstract}\n'
        item_html += '                        </p>'
                        
    item_html += '\n                        </span>\n'
    item_html += '                    </li>\n'
    
    if is_preprint:
        preprint_html += item_html
    else:
        published_html += item_html

with open("research.html", "r", encoding="utf-8") as f:
    file_data = f.read()

published_anchor = '<div id="zotero-sync-published"></div>'
parts = file_data.split(published_anchor)
if len(parts) > 1:
    file_data = parts[0] + published_anchor + "\n" + published_html + "                " + parts[1]

preprint_anchor = '<div id="zotero-sync-preprints"></div>'
parts = file_data.split(preprint_anchor)
if len(parts) > 1:
    file_data = parts[0] + preprint_anchor + "\n" + preprint_html + "                " + parts[1]

with open("research.html", "w", encoding="utf-8") as f:
    f.write(file_data)
