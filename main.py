import spacy
import json
from pathlib import Path
from nltk.corpus import wordnet as wn

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ----------------------------
# ONTOLOGY
# ----------------------------

ONTOLOGY = {

    "scene_type": {
        "temple": ["temple", "shrine", "sanctuary"],
        "forest": ["forest", "woods", "jungle", "woodland"],
        "city": ["city", "street", "urban"],
        "interior": ["room", "interior", "hall", "chamber"]
    },

    "time_of_day": {
        "sunrise": ["sunrise", "dawn"],
        "sunset": ["sunset", "dusk", "evening", "twilight"],
        "night": ["night", "midnight"],
        "day": ["day", "noon", "morning", "afternoon"]
    },

    "condition": {
        "ruined": ["ruin", "ruined", "broken", "damaged", "abandoned", "ancient"],
        "intact": ["intact", "clean", "new"]
    },

    "weather": {
        "mist": ["mist", "fog"],
        "snow": ["snow", "snowy"],
        "rain": ["rain", "rainy"],
        "clear": ["clear", "sunny"]
    },

    "mood": {
        "mysterious": ["mysterious", "eerie", "dark"],
        "peaceful": ["peaceful", "calm", "serene"],
        "dramatic": ["dramatic", "intense", "epic"],
        "gloomy": ["gloomy", "somber"]
    },

    "density": {
        "sparse": ["sparse", "empty", "isolated"],
        "dense": ["dense", "crowded", "thick"]
    },

    "lighting_intensity": {
        "bright": ["bright", "vivid"],
        "dim": ["dim", "faint"],
        "dark": ["dark"]
    }
}


# ----------------------------
# SYNONYM EXPANSION
# ----------------------------

def get_synonyms(word):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower().replace("_", " "))
    return synonyms


def expand_tokens(tokens):
    expanded = set(tokens)
    for token in tokens:
        expanded |= get_synonyms(token)
    return expanded


# ----------------------------
# EXTRACTION FUNCTION
# ----------------------------

def extract_keywords(prompt: str) -> dict:
    doc = nlp(prompt.lower())

    # Use stopword filtering instead of POS filtering
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and token.is_alpha
    ]

    expanded_tokens = expand_tokens(tokens)

    result = {}
    confidence = {}

    for category, mappings in ONTOLOGY.items():
        for label, vocab in mappings.items():

            matches = len(set(vocab) & expanded_tokens)

            if matches > 0:
                result[category] = label
                confidence[category] = round(matches / len(vocab), 2)
                break

    # ----------------------------
    # DEFAULTS (for PCG stability)
    # ----------------------------

    result.setdefault("scene_type", "unknown")
    result.setdefault("time_of_day", "day")
    result.setdefault("condition", "intact")
    result.setdefault("weather", "none")
    result.setdefault("mood", "neutral")
    result.setdefault("density", "normal")
    result.setdefault("lighting_intensity", "normal")

    result["confidence"] = confidence

    return result


# ----------------------------
# MAIN
# ----------------------------

if __name__ == "__main__":
    prompt = input("Enter scene description:\n> ")

    extracted = extract_keywords(prompt)

    print("\nExtracted Semantic Tags:")
    print(json.dumps(extracted, indent=2))

    output_path = Path("scene_config.json")
    with open(output_path, "w") as f:
        json.dump(extracted, f, indent=2)

    print(f"\nSaved to {output_path.resolve()}")
