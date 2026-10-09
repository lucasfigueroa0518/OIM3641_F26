"""Small lead-note parser. Extracts people and companies from one inbound note."""

import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Lead note parser", layout="centered")
st.title("Lead note parser")
st.write(
    "Paste an inbound note. The model pulls out the person and the company "
    "so you can match the lead to an account before you decide if it is qualified."
)

@st.cache_resource
def load_ner():
    return pipeline(
        "token-classification",
        model="dslim/bert-base-NER",
        aggregation_strategy="simple",
    )


LABELS = {
    "PER": "Person",
    "ORG": "Company",
    "LOC": "Place",
    "MISC": "Other",
}

note = st.text_input(
    "Inbound note",
    placeholder="Maya Chen from Northwind Logistics asked for a demo",
)

if st.button("Extract", type="primary"):
    text = note.strip()
    if not text:
        st.error("Paste a note first. An empty message has nothing to extract.")
    else:
        try:
            entities = load_ner()(text)
        except Exception as exc:
            st.error(f"The model call failed: {exc}")
        else:
            grouped: dict[str, list[str]] = {}
            for entity in entities:
                label = LABELS.get(entity["entity_group"], entity["entity_group"])
                grouped.setdefault(label, []).append(
                    f"{entity['word']} ({entity['score']:.0%})"
                )

            people = grouped.get("Person", [])
            companies = grouped.get("Company", [])
            if not people and not companies:
                st.warning(
                    "No person or company found. The note may be too vague to match to an account."
                )
            if people:
                st.subheader("Person")
                for item in people:
                    st.write(item)
            if companies:
                st.subheader("Company")
                for item in companies:
                    st.write(item)
            extras = [
                (label, items)
                for label, items in grouped.items()
                if label not in {"Person", "Company"}
            ]
            for label, items in extras:
                st.subheader(label)
                for item in items:
                    st.write(item)
