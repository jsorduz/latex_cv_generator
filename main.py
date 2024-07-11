from io import StringIO

import streamlit as st

from const import (
    CERTIFICATION_FLAG,
    EDUCATION_FLAG,
    END_FLAG,
    EXPERIENCE_FLAG,
    EXPERIENCE_SKILL_FLAG,
    HEADER,
    NAME,
    PROFILE,
    SKILLS_FLAG,
    SUBSECTION_FLAG,
    TAIL,
    TITLE,
)
from latex import (
    get_latex_certification,
    get_latex_education,
    get_latex_experience,
    get_latex_skills,
)
from logger import logger
from models import Certification, Education, Experience, Skill, SkillType


def get_line(generator: StringIO):
    return generator.readline().strip()


def load_file(uploaded_file):
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    st.session_state._first_name = get_line(stringio)
    st.session_state._last_name = get_line(stringio)
    st.session_state._role = get_line(stringio)
    st.session_state._email = get_line(stringio)
    st.session_state._location = get_line(stringio)
    st.session_state._linkedin_label = get_line(stringio)
    st.session_state._linkedin_link = get_line(stringio)
    st.session_state._professional_profile = get_line(stringio)

    while get_line(stringio) != SKILLS_FLAG:
        continue

    logger.info("Loading Skills")
    line = get_line(stringio)
    skills = []
    skill_type = None
    curr_skills = []
    while line != EXPERIENCE_FLAG:
        if line:
            if line.startswith(SUBSECTION_FLAG):
                skill_type = SkillType(line[1:])
                curr_skills = []
                skills.append([skill_type, curr_skills])
            else:
                skill = Skill(line)
                curr_skills.append(skill)
                if skill_type:
                    skill_type.skills.append(skill)
        line = get_line(stringio)
    st.session_state._skills = skills

    logger.info("Loading Experience")
    line = get_line(stringio)
    experiences = []
    experience = []
    while line != EDUCATION_FLAG:
        if line:
            experience.append(line)
        else:
            date, role, company, location, *description, skills = experience
            experiences.append(
                Experience(date, role, company, location, description, skills)
            )
            experience = []
        line = get_line(stringio)
    st.session_state._experience = experiences

    logger.info("Loading Education")
    line = get_line(stringio)
    educations = []
    education = []
    while line != CERTIFICATION_FLAG:
        if line:
            education.append(line)
        else:
            educations.append(Education(*education))
            education = []
        line = get_line(stringio)
    st.session_state._education = educations

    logger.info("Loading Certification")
    line = get_line(stringio)
    certifications = []
    certification = []
    while line != END_FLAG:
        if line:
            certification.append(line)
        else:
            certifications.append(Certification(*certification))
            certification = []
        line = get_line(stringio)
    st.session_state._certification = certifications

    logger.info("Finished Load data")


def set_non_existing_variable(key: str):
    if key not in st.session_state:
        st.session_state[key] = None


def set_session_variable(key: str, label: str):
    if key:
        st.session_state[label] = key


def configure_page() -> None:
    st.set_page_config(page_title="Latext CV Generator", layout="wide")
    set_non_existing_variable("_first_name")
    set_non_existing_variable("_last_name")
    set_non_existing_variable("_role")
    set_non_existing_variable("_email")
    set_non_existing_variable("_location")
    set_non_existing_variable("_linkedin_label")
    set_non_existing_variable("_linkedin_link")
    set_non_existing_variable("_professional_profile")
    set_non_existing_variable("_skills")
    set_non_existing_variable("_experience")
    set_non_existing_variable("_education")
    set_non_existing_variable("_certification")


def configure_sidebar():
    uploaded_file = st.sidebar.file_uploader("Upload File")
    if uploaded_file is not None:
        load_file(uploaded_file)


def configure_overview() -> None:
    st.title("Latext CV generator")


def configure_basic_data() -> None:
    st.header("Basic Data")
    col1, col2 = st.columns(2)
    col1.subheader("Personal Data")
    set_session_variable(
        col1.text_input(label="First Name", value=st.session_state.get("_first_name")),
        "_first_name",
    )
    set_session_variable(
        col1.text_input(label="Last Name", value=st.session_state.get("_last_name")),
        "_last_name",
    )
    set_session_variable(
        col1.text_input(label="Email", value=st.session_state.get("_email")), "_email"
    )
    set_session_variable(
        col1.text_input(label="Location", value=st.session_state.get("_location")),
        "_location",
    )

    col2.subheader("Social Network")
    set_session_variable(
        col2.text_input(
            label="LinkedIn Label", value=st.session_state.get("_linkedin_label")
        ),
        "_linkedin_label",
    )
    set_session_variable(
        col2.text_input(
            label="LinkedIn Link", value=st.session_state.get("_linkedin_link")
        ),
        "_linkedin_link",
    )


def configure_professional_profile() -> None:
    st.header("Professional Profile")
    professional_profile = st.text_area(
        label="Professional Profile",
        value=st.session_state.get("_professional_profile"),
    )
    if professional_profile:
        st.session_state._professional_profile = professional_profile


def configure_skills():
    st.header("Skills")
    if not st.session_state._skills:
        return
    col1, col2, col3 = st.columns(3)
    for idx, (subsection, skills) in enumerate(st.session_state._skills):
        skill_mod = idx % 3
        if skill_mod == 1:
            col = col1
        elif skill_mod == 2:
            col = col2
        else:
            col = col3

        subsection.selected = col.toggle(subsection.value, value=subsection.selected)
        for skill in skills:
            skill.selected = col.checkbox(skill.value, value=skill.selected)


def configure_experience():
    st.header("Experience")
    if not st.session_state._experience:
        return
    for experience in st.session_state._experience:
        experience.selected = st.toggle(str(experience), value=experience.selected)
        st.text(f"{experience.description}\nSkills:{experience.skills}")


def configure_education():
    st.header("Education")
    if not st.session_state._education:
        return
    for education in st.session_state._education:
        education.selected = st.toggle(str(education), value=education.selected)
        if education.description:
            st.text(education.description)


def configure_certification():
    st.header("Certification")
    if not st.session_state._certification:
        return
    for certification in st.session_state._certification:
        certification.selected = st.toggle(
            str(certification), value=certification.selected
        )


def show_data():
    data = HEADER.substitute()
    data += NAME.substitute(
        first_name=st.session_state._first_name, last_name=st.session_state._last_name
    )
    data += TITLE.substitute(
        email=st.session_state._email,
        role=st.session_state._role,
        location=st.session_state._location,
        linkedin_label=st.session_state._linkedin_label,
        linkedin_link=st.session_state._linkedin_link,
    )
    data += PROFILE.substitute(data=st.session_state._professional_profile)
    data += get_latex_skills(st.session_state._skills)
    data += get_latex_experience(st.session_state._experience)
    data += get_latex_education(st.session_state._education)
    data += get_latex_certification(st.session_state._certification)
    data += TAIL.substitute()

    # st.write(st.session_state)
    st.subheader("Download latex")
    st.download_button("Download Latex file", data, file_name="streamlit_download.tex")
    st.text(data)


def main() -> None:
    configure_page()
    configure_sidebar()
    configure_overview()
    configure_basic_data()
    configure_professional_profile()
    configure_skills()
    configure_experience()
    configure_education()
    configure_certification()
    show_data()


if __name__ == "__main__":
    main()
