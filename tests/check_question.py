import spacy

# Load English and Hindi language models
nlp_en = spacy.load("en_core_web_sm")
nlp_hi = spacy.blank("hi")

def is_question(sentence, nlp):
    doc = nlp(sentence)
    for token in doc:
        if token.dep_ == 'ROOT' and token.tag_ == 'VB' and token.pos_ == 'AUX':
            # If the root verb is an auxiliary verb, it's likely a question
            return True
    return False

# Example usage for English
sentence_en = "Have you finished your homework?"
print(is_question(sentence_en, nlp_en))  # Output: True

# Example usage for Hindi
sentence_hi = "क्या तुमने अपना होमवर्क किया है?"
print(is_question(sentence_hi, nlp_hi))  # Output: True
