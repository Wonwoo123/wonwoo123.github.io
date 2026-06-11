clean_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Wonwoo Kang - Research</title>
    <link rel="icon" type="image/png" href="./Images/favicon.png">    
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link href="./main.css" rel="stylesheet" type="text/css">
    <script type="text/javascript">
    function toggleAbstract(abstractID) {
        var CurrentAbstract = document.getElementById(abstractID);
        var ViewArrow = document.getElementById(abstractID + "Viewarrow");
        var HideArrow = document.getElementById(abstractID + "Hidearrow");

        if (CurrentAbstract.style.display == 'none' || CurrentAbstract.style.display == '') {
            CurrentAbstract.style.display = 'block';
            ViewArrow.style.display = 'none';
            HideArrow.style.display = 'inline';
        } else {
            CurrentAbstract.style.display = 'none';
            ViewArrow.style.display = 'inline';
            HideArrow.style.display = 'none';
        }
    }

    function toggleBibtex(bibtexID) {
        var CurrentBibtex = document.getElementById(bibtexID);
        if (CurrentBibtex.style.display == 'none' || CurrentBibtex.style.display == '') {
            CurrentBibtex.style.display = 'block';
        } else {
            CurrentBibtex.style.display = 'none';
        }
    }
    </script>
    <script>
    window.MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']]
      }
    };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>

<body>
    <h1> Wonwoo Kang </h1>
    
    <div id="wrapper">
        <div id="nav">
            <ul>
                <li><a href="index.html">Home</a></li>
                <li class="current"><a href="research.html">Research</a></li>
                <li><a href="teaching.html">Teaching</a></li> 
                <li><a href="CV.pdf">CV</a></li>
            </ul>
        </div>

        <div id="main" class="papers">
            <div id="maintext">
                Click buttons <img src="./Images/dot4.png" class="toggle-btn" alt="button"> to reveal abstracts.
                <br><br>

                <h3>Published Papers</h3> 
                <ol reversed="">
                    <div id="zotero-sync-published"></div>
                </ol>

                <h3 style="margin-top: 40px;">Preprints</h3> 
                <ol reversed="">
                    <div id="zotero-sync-preprints"></div>
                </ol>
            </div>
        </div>
    </div>
</body>
</html>"""

with open("research.html", "w", encoding="utf-8") as f:
    f.write(clean_html)
print("Bloat successfully cleared with BibTeX scripts added!")
