# python -m streamlit run portal.py in the right directory (cd xxx) or in bash command
import json

import streamlit as st

st.title("Email configurator portal")
st.header(
    'Welcome to this app which you can use to define custom email routing rules.\nE.g., if the subject of an email contains "declaration", then it should go to the finance department.'
)

output_dictionary = {
    "mail_addresses": {},
    "subject_keyphrases": {},
    "body_keyphrases": {},
}
depts_mails = st.text_area(
    "Please enter the department name, together with the emailaddress. declaration:declaration@domain.com."
)
depts_subjects = st.text_area(
    "Please enter the department name, together with the common subject. declaration:Here is my declaration."
)
depts_texts = st.text_area(
    "Please enter the department name, together with the common text. declaration:Please process this declaration."
)


def extract_dictionary(lines: list) -> dict:
    mapping = {}
    for line in lines:
        dept, information = line.split(sep=":")
        if dept not in mapping.keys():
            mapping[dept] = information
    return mapping


def extract_dictionary_with_list(lines: list) -> dict:
    mapping = {}
    for line in lines:
        dept, information = line.split(sep=":")
        if dept not in mapping.keys():
            mapping[dept] = [information]
        else:
            mapping[dept].append(information)
    return mapping


processing = st.button("Process input")

if processing:
    # Split each line to be a new sentence
    depts_mails = depts_mails.splitlines()
    depts_subjects = depts_subjects.splitlines()
    depts_texts = depts_texts.splitlines()

    # A design decision has been made to do a one-to-one mapping of department to mailbox
    # If this should be different, then change the method to the one with list. Both methods
    # seem to have the same code, just one saves it in a list. This would be weird to pass as a boolean
    output_dictionary["mail_addresses"] = extract_dictionary(lines=depts_mails)
    output_dictionary["subject_keyphrases"] = extract_dictionary_with_list(
        lines=depts_subjects
    )
    output_dictionary["body_keyphrases"] = extract_dictionary_with_list(
        lines=depts_texts
    )

    # Output as JSON file with file_name
    file_name = "sample.json"
    with open(file_name, "w") as outfile:
        json.dump(output_dictionary, outfile, indent=4)

        st.write("Processed!")
        st.write("The configuration file will be saved as", file_name)
        st.write(" ")  # ensures nice spacing
        
    with open(file_name) as f:
        st.download_button('Download JSON', f)


st.write("Powered by Streamlit.")
