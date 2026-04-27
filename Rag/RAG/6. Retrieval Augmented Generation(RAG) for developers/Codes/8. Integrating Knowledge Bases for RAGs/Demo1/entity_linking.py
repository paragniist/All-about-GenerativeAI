
#######################################################################################################
# Part 1 - Load and Process Unstructured Data
#######################################################################################################

import spacy
import pandas as pd

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Sample unstructured text
text = """
Apple Inc. is an American multinational technology company headquartered in Cupertino, California.
Apple was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in April 1976.
"""

# Sample structured knowledge base as a DataFrame
data = {
    "Entity": ["Apple Inc.", "Steve Jobs", "Steve Wozniak", "Ronald Wayne"],
    "Type": ["Organization", "Person", "Person", "Person"],
    "Description": [
        "American multinational technology company",
        "Co-founder of Apple Inc.",
        "Co-founder of Apple Inc.",
        "Co-founder of Apple Inc."
    ]
}
knowledge_base = pd.DataFrame(data)

# Display the knowledge base
print("Knowledge Base:")
print(knowledge_base)

#######################################################################################################

#######################################################################################################
# Part 2 - Perform Named Entity Recognition (NER)
#######################################################################################################

# Process the text with spaCy
doc = nlp(text)

# Extract entities
entities = [(ent.text, ent.label_) for ent in doc.ents]

# Display extracted entities
print("\nExtracted Entities:")
for entity in entities:
    print(entity)

#######################################################################################################

#######################################################################################################
# Part 3 - Link Entities to Structured Knowledge Base
#######################################################################################################


# Function to link entities to the knowledge base
def link_entities(entities, knowledge_base):
    linked_data = []
    for entity, label in entities:
        match = knowledge_base[knowledge_base["Entity"] == entity]
        if not match.empty:
            linked_data.append({
                "Entity": entity,
                "Label": label,
                "Description": match["Description"].values[0]
            })
    return linked_data

# Link entities
linked_entities = link_entities(entities, knowledge_base)

# Display linked entities
print("\nLinked Entities:")
for linked_entity in linked_entities:
    print(linked_entity)

#######################################################################################################

#######################################################################################################
# Part 4 - Print the Aligned Data
#######################################################################################################

# Display aligned data
print("\nAligned Data:")
for linked_entity in linked_entities:
    print(f"Entity: {linked_entity['Entity']}, Label: {linked_entity['Label']}, Description: {linked_entity['Description']}")

#######################################################################################################
