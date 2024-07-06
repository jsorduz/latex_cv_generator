from string import Template

from utils import remove_left_spaces


def get_latex_skills(skills):
    if not skills:
        return ""
    ans = """
    \section{Habilidades}
    \\begin{multicols}{3}
    """
    for group, skills in skills:
        if not group.has_enabled_skills:
            continue
        ans += Template("\\textbf{$group}\n").substitute(group=group)
        ans += "\\begin{itemize}[label=\\textbullet]\n"
        for skill in skills:
            if not skill.selected:
                continue
            ans += f"\\item {skill}\n"
        ans += "\end{itemize}\n"
    ans += """
    \end{multicols}
    """

    return remove_left_spaces(ans)


def get_latex_experience(experiences):
    if not experiences:
        return ""
    ans = """
    \section{Experiencia}
    """
    for dates, role, company, location, description, skills, selected in experiences:
        if not selected:
            continue
        # Use the following to use bullet points instead of one paragraph description.
        cv_description = "\\begin{itemize}[leftmargin=0.6cm, label={\\textbullet}]\n"
        for item in description.split("\n"):
            cv_description += f"\item {item}\n"
        cv_description += "\end{itemize}"
        ans += Template(
            """
        \customcventry{$dates}{{{$company}}}{$role,}{$location}{}{
        {
            $description
            \\textbf{Habilidades:} $skills
        }}"""
        ).substitute(
            dates=dates,
            role=role,
            company=company,
            location=location,
            description=cv_description,
            skills=skills,
        )

    return remove_left_spaces(ans)


def get_latex_education(educations):
    if not educations:
        return ""
    ans = """
    \section{Educacion}
    """
    for dates, title, organization, location, description, selected in educations:
        if not selected:
            continue
        ans += Template(
            "\customcventry{$dates}{{{$organization}}}{$title,}{$location}{}{{$description}}\n"
        ).substitute(
            dates=dates,
            title=title,
            organization=organization,
            location=location,
            description=description,
        )

    return remove_left_spaces(ans)


def get_latex_certification(certifications):
    if not certifications:
        return ""
    ans = """
    \section{Certificados}
    {\\begin{itemize}[label=\\textbullet]
    """
    for date, title, organization, selected in certifications:
        if not selected:
            continue
        tmpl_str = "\\item $title ($date)"
        if organization:
            tmpl_str += " - $organization"
        ans += Template(tmpl_str + "\n").substitute(
            date=date, title=title, organization=organization
        )
    ans += """
    \end{itemize}}
    """
    return remove_left_spaces(ans)
