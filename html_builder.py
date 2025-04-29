# html_builder.py

from datetime import datetime

def build_index_html(articles, feeds):
    now_utc = datetime.utcnow().strftime("%d %b %Y, %H:%M UTC")

    # Prepare source filter checkboxes
    source_filters_html = ""
    for feed in feeds:
        source_filters_html += f"""<label><input type="checkbox" class="sourceFilter" value="{feed['uniqueid']}" checked> {feed['source']}</label>"""

    # Prepare initial table rows
    rows_html = ""
    for article in articles:
        date_display = article["date"] if article["date"] else ""
        row_class = "missing-date" if not article["date"] else ""
        rows_html += f"""<tr class="{row_class}" data-source="{article['source_id']}" data-date="{article['date']}" data-title="{article['title']}">
            <td>{date_display}</td>
            <td>{article['source']}</td>
            <td><a href="{article['link']}" target="_blank">{article['title']}</a></td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>My News Feed</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f9f9f9; }}
  h1 {{ margin: 0; }}
  .header-bar {{ display: flex; justify-content: space-between; align-items: center; }}
  .header-links a {{ margin-left: 15px; text-decoration: none; font-size: 0.9em; color: #007BFF; }}
  .header-links a:hover {{ text-decoration: underline; }}
  .source-scroll {{ max-height: 150px; overflow-y: auto; padding: 5px; border: 1px solid #ddd; background: #fafafa; border-radius: 4px; }}
  .generated-time {{ font-size: 0.8em; color: #555; margin-top: 4px; }}
  .filter-container {{ display: flex; gap: 40px; margin: 20px 0; background: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }}
  .filter-group {{ flex: 1; }}
  .filter-group label {{ display: block; margin-bottom: 6px; }}
  .filter-group select, .filter-group input[type="text"] {{ width: 80%; padding: 6px; margin-top: 6px; }}
  .button-group button {{ margin-right: 10px; background-color: #888888; color: white; border: none; border-radius: 4px; cursor: pointer; }}
  .button-group button:hover {{ background-color: #0056b3; }}
  table {{ border-collapse: collapse; width: 100%; background: #ffffff; border-radius: 8px; overflow: hidden; }}
  th, td {{ text-align: left; padding: 10px; border-bottom: 1px solid #ddd; }}
  th {{ background-color: #f2f2f2; cursor: pointer; }}
  .missing-date td:first-child {{ color: gray; }}
  #articleCount {{ margin: 10px 0; font-weight: bold; }}
  @keyframes fadeInModal {{ from {{ opacity: 0; transform: translate(-50%, -55%); }} to {{ opacity: 1; transform: translate(-50%, -50%); }}}}
  .table-wrapper {{ width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; /* smooth scrolling on iOS. Makes the article table auto-scroll horizontally on small screens rather than breaking layout */ }}

</style>
</head>
<body>

<div class="header-bar">
  <div>
    <h1>My News Feed</h1>
    <div class="generated-time">Page generated on {now_utc}</div>
  </div>
  <div class="header-links">
    <a href="config.html" target="_blank">Config</a>
    <a href="#" onclick="showAbout()">About</a>
  </div>
</div>

<div class="filter-container">
  <div class="filter-group">
    <strong>Filter by source:</strong><br>
    <div class="button-group">
      <button onclick="selectAllSources()">Select All</button>
      <button onclick="selectNoSources()">Select None</button>
    </div>
    <div class="source-scroll">
    {source_filters_html}
    </div>
  </div>

  <div class="filter-group">
    <strong>Filter by time:</strong><br>
    <select id="timeFilter">
      <option value="all">All time</option>
      <option value="24h">Past 24 hours</option>
      <option value="48h" selected>Past 48 hours</option>
      <option value="7d">Past week</option>
    </select>

    <br><br>
    <strong>Search titles:</strong><br>
    <input type="text" id="searchBox" placeholder="Type keywords..." />
  </div>
</div>

<div id="articleCount"></div>

<div class="table-wrapper">
<table id="newsTable">
<thead>
<tr>
  <th onclick="sortTable(0)">Date ▲▼</th>
  <th onclick="sortTable(1)">Source ▲▼</th>
  <th>Title</th>
</tr>
</thead>
<tbody>
{rows_html}
</tbody>
</table>
</div>

<!-- About Modal -->
<div id="aboutModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1000;">

  <div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); background:white; padding:30px; width:90%; max-width:500px; border-radius:10px; box-shadow:0 6px 20px rgba(0,0,0,0.3); animation: fadeInModal 0.3s ease;">
    <h2 style="margin-top:0;">About This Site</h2>
    <p style="margin:15px 0;">This website displays the latest articles from selected RSS feeds. You can filter by source, time, and keyword search. It is automatically updated daily. Made by <a href = "https://github.com/technoid99/my_news_feed" target="_blank">@technoid99</a> with ❤️.</p>
    <div style="text-align:right;">
      <button style="padding:8px 16px; background:#007BFF; color:white; border:none; border-radius:5px; cursor:pointer;" onclick="document.getElementById('aboutModal').style.display='none'">Close</button>
    </div>
  </div>

</div>

<script>
// -- URL Parameters
function getUrlParams() {{
    const params = new URLSearchParams(window.location.search);
    return {{
        sources: params.get('sources') ? params.get('sources').split(',') : [],
        time: params.get('time') || '48h',
        search: params.get('search') || ''
    }};
}}

function updateUrlParams() {{
    const sources = Array.from(document.querySelectorAll('.sourceFilter:checked')).map(cb => cb.value);
    const time = document.getElementById('timeFilter').value;
    const search = document.getElementById('searchBox').value.trim();

    const params = new URLSearchParams();
    if (sources.length) params.set('sources', sources.join(','));
    if (time) params.set('time', time);
    if (search) params.set('search', search);

    const newUrl = window.location.pathname + '?' + params.toString();
    window.history.replaceState(null, '', newUrl);
}}

function parseBooleanSearch(query) {{
    query = query.trim();
    if (!query) return () => true;

    let terms = [];
    let current = '';
    let inQuotes = false;

    for (let i = 0; i < query.length; i++) {{
        const char = query[i];
        if (char === '"') {{
            inQuotes = !inQuotes;
            if (!inQuotes && current.length) {{
                terms.push({{ type: 'TERM', value: current.toLowerCase() }});
                current = '';
            }}
        }} else if (!inQuotes && /\s/.test(char)) {{
            if (current.length) {{
                if (current.toUpperCase() === 'AND' || current.toUpperCase() === 'OR') {{
                    terms.push({{ type: 'OP', value: current.toUpperCase() }});
                }} else {{
                    terms.push({{ type: 'TERM', value: current.toLowerCase() }});
                }}
                current = '';
            }}
        }} else {{
            current += char;
        }}
    }}
    if (current.length) {{
        terms.push({{ type: 'TERM', value: current.toLowerCase() }});
    }}

    if (!terms.length) return () => true;

    return function(title) {{
        title = title.toLowerCase();
        let result = null;
        let op = 'AND';
        for (const term of terms) {{
            if (term.type === 'OP') {{
                op = term.value;
            }} else {{
                const match = title.includes(term.value);
                if (result === null) {{
                    result = match;
                }} else if (op === 'AND') {{
                    result = result && match;
                }} else if (op === 'OR') {{
                    result = result || match;
                }}
            }}
        }}
        return result;
    }};
}}

function applyFilters() {{
    const params = getUrlParams();

    // If no sources provided, read from checked checkboxes
    if (params.sources.length === 0) {{
        params.sources = Array.from(document.querySelectorAll('.sourceFilter:checked')).map(cb => cb.value);
    }}

    // If no time provided, read from time filter
    if (!params.time) {{
        params.time = document.getElementById('timeFilter').value;
    }}

    // If no search provided, assume empty
    if (!params.search) {{
        params.search = '';
    }}

    const sourceSet = new Set(params.sources);
    const filterTime = params.time;
    const searchFn = parseBooleanSearch(params.search);

    const now = new Date();

    // If no sources selected, hide all rows immediately
    if (params.sources.length === 0) {{
        document.querySelectorAll('#newsTable tbody tr').forEach(row => {{
            row.style.display = 'none';
        }});
        updateArticleCount();
        return;
    }}

    document.querySelectorAll('#newsTable tbody tr').forEach(row => {{
        const source = row.getAttribute('data-source');
        const dateStr = row.getAttribute('data-date');
        const title = row.getAttribute('data-title');

        let show = true;

        if (!sourceSet.has(source)) show = false;

        if (filterTime !== 'all' && dateStr) {{
            const articleDate = new Date(dateStr);
            let diffHours = (now - articleDate) / (1000 * 60 * 60);
            if ((filterTime === '24h' && diffHours > 24) ||
                (filterTime === '48h' && diffHours > 48) ||
                (filterTime === '7d' && diffHours > 168)) {{
                show = false;
            }}
        }}

        if (!searchFn(title)) show = false;

        row.style.display = show ? '' : 'none';
    }});

    updateArticleCount();
}}



function updateArticleCount() {{
    const visible = Array.from(document.querySelectorAll('#newsTable tbody tr'))
        .filter(row => row.style.display !== 'none').length;
    const total = document.querySelectorAll('#newsTable tbody tr').length;
    document.getElementById('articleCount').textContent = `Showing ${{visible}} of ${{total}} articles`;
}}

function selectAllSources() {{
    document.querySelectorAll('.sourceFilter').forEach(cb => cb.checked = true);
    updateUrlParams();
    applyFilters();
}}

function selectNoSources() {{
    document.querySelectorAll('.sourceFilter').forEach(cb => cb.checked = false);
    updateUrlParams();
    applyFilters();
}}

function showAbout() {{
    document.getElementById('aboutModal').style.display = 'block';
}}

function sortTable(colIndex) {{
    const tbody = document.querySelector('#newsTable tbody');
    const rows = Array.from(tbody.rows);
    let asc = true;
    rows.sort((a, b) => {{
        let valA = a.cells[colIndex].textContent.trim();
        let valB = b.cells[colIndex].textContent.trim();
        return asc ? valA.localeCompare(valB) : valB.localeCompare(valA);
    }});
    tbody.innerHTML = '';
    rows.forEach(r => tbody.appendChild(r));
}}

document.addEventListener('DOMContentLoaded', () => {{
    const params = getUrlParams();
    if (params.time) document.getElementById('timeFilter').value = params.time;
    if (params.search) document.getElementById('searchBox').value = params.search;
    if (params.sources.length) {{
        document.querySelectorAll('.sourceFilter').forEach(cb => {{
            cb.checked = params.sources.includes(cb.value);
        }});
    }}
    document.querySelectorAll('.sourceFilter').forEach(cb => cb.addEventListener('change', () => {{
        updateUrlParams();
        applyFilters();
    }}));
    document.getElementById('timeFilter').addEventListener('change', () => {{
        updateUrlParams();
        applyFilters();
    }});
    document.getElementById('searchBox').addEventListener('input', () => {{
        updateUrlParams();
        applyFilters();
    }});
    applyFilters();
}});
</script>

</body>
</html>"""
    return html
