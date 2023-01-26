# python -m streamlit run form.py in the right directory (cd xxx) or in bash command

import streamlit as st
import json

with st.form("Form amount emailboxes"):
    st.write("Please enter the amount of emailboxes you want to enter.")
    amount_of_mailboxes = st.number_input(label='Enter amount of mailboxes', min_value=1)
    submitted_first = st.form_submit_button("Set")


with st.form("Form emailboxes"):
    amount_of_mailboxes = int(amount_of_mailboxes)

    departments = []
    emailaddresses = []
    keywords = []

    st.write("Please fill in your emailboxes")
    for i in range(0, amount_of_mailboxes): #generate for each mailbox 3 text boxes
        label = 'Mailbox '+str(i+1)
        st.write(label)

        department = st.text_input(label=label+" department", placeholder="Fill in department")
        departments.append(department)

        emailaddress = st.text_input(label=label+" emailaddress", placeholder="Fill in emailaddress")
        emailaddresses.append(emailaddress)

        keyword = st.text_input(label=label+" keywords seperated by \";\"", placeholder="Fill in keywords")
        keywords.append(keyword)

    checkbox_download = st.checkbox("Do you want download your data?")

    submitted = st.form_submit_button("Submit") # Every form must have a submit button.
    if submitted:
        st.write("Download submission", checkbox_download)



def extract_keywords(keywords_per_mailbox: list[str]) -> list:
    keywords_mailbox_list = []
    for mailbox_index in range(0, len(keywords_per_mailbox)):
        keywords = keywords_per_mailbox[mailbox_index]
        print(keywords)
        keywords_list = keywords.split(";")
        keywords_mailbox_list.append(keywords_list)
    return keywords_mailbox_list


if checkbox_download:
    output_dictionary = {
        "departments": [],
        "email_addresses": {},
        "keywords": {},
    }

    output_dictionary["departments"] = departments
    #output_dictionary["email_addresses"] = emailaddresses
    for i in range(0, len(departments)):
        output_dictionary["email_addresses"][departments[i]] = emailaddresses[i]

    #output_dictionary["keywords"] = extract_keywords(keywords_per_mailbox=keywords)
    keys = extract_keywords(keywords_per_mailbox=keywords)
    for i in range(0, len(departments)):
        output_dictionary["keywords"][departments[i]] = keys[i]

    # Output as JSON file with file_name
    file_name = "config.json"
    with open(file_name, "w") as f:
        json.dump(output_dictionary, f, indent=4)

        st.write("Processed!")
        st.write("The configuration file will be saved as", file_name, "locally.")
        st.write(
            'If you are using the portal not using the localhost, you can use the "Download JSON" button below.\nThen it will be saved as a text file.\nPlease change the extension to .json.'
        )
    f.close()

    with open(file_name) as f:
        st.download_button("Download JSON", f)
    f.close()

st.write(" ")  # ensures nice spacing
st.write("Powered by Streamlit.")