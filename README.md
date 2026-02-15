# NLP Prompt Interpreter for Procedural Scene Generation

This project implements a rule-based Natural Language Processing (NLP) system that converts free-form scene descriptions into structured semantic parameters for Procedural Content Generation (PCG) systems such as Unreal Engine 5.

The interpreter extracts structured environmental attributes including:

- Scene type (forest, temple, city, interior)
- Time of day (sunrise, sunset, night, day)
- Weather (mist, rain, snow, clear)
- Mood (mysterious, peaceful, dramatic)
- Density (dense, sparse)
- Lighting intensity
- Scene condition (ruined, intact)
- Object categories
- Confidence scores

The system outputs a structured JSON file (`scene_config.json`) that can be consumed by Unreal Engine Blueprints or PCG graphs.

---

## Requirements

- Python **3.11** (Required)
- pip
- Linux or macOS recommended

Python versions 3.12+ or 3.13+ may cause compatibility issues with spaCy.

Check your Python version:

```
python --version
```

Expected output:

```
Python 3.11.x
```

---

## Installation

Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/nlp-pcg-prompt-interpreter.git
cd nlp-pcg-prompt-interpreter
```

Create a virtual environment using Python 3.11:

Linux/macOS:

```
python3.11 -m venv venv
source venv/bin/activate
```

Windows:

```
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Download the required spaCy language model:

```
python -m spacy download en_core_web_sm
```

Download WordNet data (one-time setup):

Start Python:

```
python
```

Then run:

```python
import nltk
nltk.download("wordnet")
nltk.download("omw-1.4")
exit()
```

---

## Running the Application

Activate the virtual environment and run:

```
python main.py
```

Enter a scene description when prompted.

Example input:

```
Ancient eerie sanctuary at dusk with thick fog
```

The program generates:

```
scene_config.json
```

---

## Example Output

```json
{
  "scene_type": "temple",
  "time_of_day": "sunset",
  "condition": "ruined",
  "weather": "mist",
  "mood": "mysterious",
  "density": "dense",
  "lighting_intensity": "normal",
  "confidence": {
    "scene_type": 0.33,
    "time_of_day": 0.5,
    "condition": 0.17,
    "weather": 1.0,
    "mood": 0.33,
    "density": 0.67
  }
}
```

---

## Project Structure

```
.
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## System Design

The interpreter follows this pipeline:

1. Text preprocessing using spaCy
2. Stopword filtering
3. Lemmatization
4. WordNet synonym expansion via NLTK
5. Ontology-based semantic mapping
6. Confidence scoring using vocabulary coverage
7. JSON export for procedural systems

The system is deterministic, interpretable, reproducible, and designed for stability in procedural generation environments.

---

## Intended Unreal Engine Integration

The generated JSON is designed to integrate with:

- Unreal Engine 5 Blueprints
- UE5 PCG Framework
- Custom procedural generation graphs
- Lighting preset controllers

Workflow:

Natural Language Prompt  
→ Semantic JSON  
→ PCG Parameter Mapping  
→ Procedural Scene Composition  

---

## Limitations

- Ontology coverage determines semantic breadth.
- Confidence scores are heuristic (not probabilistic).
- No trained model is currently implemented.
- Implicit inference is limited to lexical expansion.

---

## Future Work

- Embedding-based semantic similarity matching
- Transformer-based classifier comparison
- CLIP-based asset tagging
- Direct Unreal Engine plugin implementation
- Quantitative evaluation against manually authored scenes

---

## License

For academic and research purposes.
