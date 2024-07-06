# ^(\\[^\\]) \ at the beginning
# ([^\\]\\)$ \ at the end
from string import Template

SKILLS_FLAG = "SKILLS"
EXPERIENCE_FLAG = "EXPERIENCE"
EDUCATION_FLAG = "EDUCATION"
CERTIFICATION_FLAG = "CERTIFICATION"
END_FLAG = "END"
SUBSECTION_FLAG = "_"
EXPERIENCE_SKILL_FLAG = "Habilidades: "

HEADER = Template(
    """
\\documentclass[11pt,a4paper,sans]{moderncv}
\\usepackage[utf8]{inputenc}
\\usepackage{ragged2e}
\\usepackage[scale=0.85]{geometry}
\\usepackage{import}
\\usepackage{multicol}
\\usepackage{import}
\\usepackage{enumitem}
\\usepackage[utf8]{inputenc}
\\usepackage{amssymb}


\\moderncvstyle{banking}
\\moderncvcolor{black}
\\nopagenumbers{}

\\newcommand*{\customcventry}[7][.13em]{
  \\begin{tabular}{@{}l}
  {\\bfseries #4} \\
  {\itshape #3}
  \end{tabular}
  \hfill
  \\begin{tabular}{l@{}}
  {\\bfseries #5} \\
  {\itshape #2}
  \end{tabular}
  \ifx&#7&%
  \else{\\
  \\begin{minipage}{\maincolumnwidth}%
  \small#7%
  \end{minipage}}\\fi%
  \par\\addvspace{#1}
}

\\newcommand*{\customclientcventry}[7][.33em]{
  \\begin{tabular}{@{}l}
  {\\bfseries #3}
  \end{tabular}
  \hfill
  \\begin{tabular}{l@{}}
  {\\bfseries #5} \\
  {\itshape #2}
  \end{tabular}
  \ifx&#7&%
  \else{\\
  \\begin{minipage}{\maincolumnwidth}%
  \small#7%
  \end{minipage}}\\fi%
  \par\\addvspace{#1}
}
"""
)

NAME = Template(
    """
\\name{$first_name}{$last_name}
"""
)

TITLE = Template(
    """
\\begin{document}
\\makecvtitle
\\vspace*{-16mm}
\\begin{center}\\textbf{$role}\end{center}
\\begin{center}
  \\begin{tabular}{ c c c }
    \enspace\\faAt\enspace {$email} &
    \enspace\\faHome\enspace {$location} &
    \enspace\\faLinkedin\enspace \color{blue} \href{$linkedin_link}{$linkedin_label}    
  \end{tabular}
\\end{center}
"""
)

PROFILE = Template(
    """
\\section{Profile}
{
    $data
}
"""
)

TAIL = Template(
    """
\\end{document}
"""
)
