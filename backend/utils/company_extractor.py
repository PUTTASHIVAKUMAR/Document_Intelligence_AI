import spacy

nlp = spacy.load("en_core_web_sm")

def extract_companies(text: str):
    doc = nlp(text)
    return list({
        ent.text for ent in doc.ents
        if ent.label_ in ("ORG", "GPE")
    })
