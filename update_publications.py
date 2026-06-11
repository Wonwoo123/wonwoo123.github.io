import os
import re
import requests

# --- YOUR CO-AUTHOR ROLODEX ---
# Add your co-authors and their website links here.
# Make sure to spell their names exactly as they appear in Zotero!
COAUTHOR_LINKS = {
    "Kyeongjun Lee": "https://sites.google.com/view/kjlee",
    "Eunsung Lim": "https://sites.google.com/view/eunsung",
    "Esther Banaian": "https://sites.google.com/view/esther-banaian/home",
    "Elizabeth Kelley": "https://sites.google.com/view/elizabeth-kelley/home",
    "Ezgi Kantarcı Oğuz":"https://sites.google.com/view/ezgikantarcioguz/main-page",
    "Emine Yıldırım":"https://emine-yildirim.github.io/",
    "Heehyun Park": "https://sites.google.com/view/heehyunpark/home",
    "Inkee Jung" : "https://inkeej.github.io/",
    # "Another Author": "https://their-website.com",
}
# ------------------------------

# Helper function to cleanly strip any field from a BibTeX string using brace matching
def strip_bibtex_field(bibtex_str, field_name):
    match = re.search(r"^\s*" + field_name + r"\s*=\s*\{", bibtex_str, re.MULTILINE | re.IGNORECASE)
    if not match:
        return bibtex_str
    start = match.start()
    brace_start = bibtex_str.find('{', start)
    brace_count = 0
    end = -1
    for i in range(brace_start, len(bibtex_str)):
        if bibtex_str[i] == '{':
            brace_count += 1
        elif bibtex_str[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end = i
                break
    if end != -1:
        if end + 1 < len(bibtex_str) and bibtex_str[end+1] == ',':
            end += 1
        if end + 1 < len(bibtex_str) and bibtex_str[end+1] == '\n':
            end += 1
        return bibtex_str[:start] + bibtex_str[end+1:]
    return bibtex_str

ZOTERO_USER_ID = os.environ.get("ZOTERO_USER_ID")
ZOTERO_API_KEY = os.environ.get("ZOTERO_API_KEY")
ZOTERO_COLLECTION_ID = os.environ.get("ZOTERO_COLLECTION_ID")

# ADDED 'bibtex' to the include parameter so Zotero sends the formatted citation automatically
url = f"https://api.zotero.org/users/{ZOTERO_USER_ID}/collections/{ZOTERO_COLLECTION_ID}/items?format=json&direction=desc&sort=date&include=data,bibtex"
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
    
    # Grab the raw BibTeX and strip out the abstract and file fields
    raw_bibtex = item.get("bibtex", "")
    clean_bibtex = strip_bibtex_field(raw_bibtex, "abstract")
    clean_bibtex = strip_bibtex_field(clean_bibtex, "file") 
    
    creators = data.get("creators", [])
    author_names = []
    for c in creators:
        if c.get("creatorType") == "author":
            name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
            if name.lower() != "wonwoo kang":
                if name in COAUTHOR_LINKS:
                    linked_name = f'<a href="{COAUTHOR_LINKS[name]}" target="_blank" rel="noopener noreferrer">{name}</a>'
                    author_names.append(linked_name)
                else:
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
    
    # NEW: The clean text button that triggers the BibTeX toggle
    if clean_bibtex:
        item_html += f'                        <a href="javascript:toggleBibtex(\'bibtex_{paper_id}\')" style="margin-left: 10px; font-size: 0.9em; text-decoration: none; color: #555; border-bottom: 1px dotted #555;">[BibTeX]</a>\n'

    item_html += f'                        <br>\n'
    item_html += f'                        {display_title}, {pub_date}.\n'
    item_html += f'                        <br>'
    
    if arxiv_num:
        item_html += f'\n                        arXiv: <a href="https://arxiv.org/abs/{arxiv_num}" target="_blank" rel="noopener noreferrer">{arxiv_num}</a>'
        
    if abstract:
        item_html += f'\n                        <p id="{paper_id}" style="display: none; margin-top: 15px; padding-top: 15px; border-top: 1px dashed #ddd; font-weight: 400;">\n'
        item_html += f'                            <b>Abstract:</b> {abstract}\n'
        item_html += '                        </p>'
        
    # NEW: The cleanly formatted, hidden code block containing your stripped BibTeX
    if clean_bibtex:
        item_html += f'\n                        <div id="bibtex_{paper_id}" style="display: none; margin-top: 15px; padding: 15px; background-color: #f4f4f4; border-radius: 5px; overflow-x: auto;">\n'
        item_html += f'                            <pre style="margin: 0; font-size: 0.85em; color: #333; font-family: monospace;"><code>{clean_bibtex.strip()}</code></pre>\n'
        item_html += '                        </div>'
                        
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
