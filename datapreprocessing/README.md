# Rebuild AI - Abstract Processing Pipeline

This pipeline processes academic paper data to extract and analyze insights about AI applications in post-war and conflict recovery scenarios. It cleans CSV data containing lists of research papers, then uses Google's Gemini AI to generate structured insights about AI applications, focusing on their benefits, risks, and mitigation strategies.

---

### Key Features

✅ **Data Cleaning**: Filters and prepares academic paper data
✅ **AI-Powered Analysis**: Uses Gemini to extract insights from paper abstracts
✅ **Structured Output**: Generates JSON files with categorized information
✅ **Post-War Focus**: Identifies applications relevant to conflict recovery and humanitarian efforts

---

### Prerequisites

* Python 3.8+
* Google Gemini API key
* OpenAI API key
* Pinecone API key

---

### Installation & Setup

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/dadoluca/WarProject-RebuildAI.git
cd war-use-case-analyzer/datapreprocessing
```

#### 2️⃣ Install Dependencies

```bash
pip install google-generativeai openai pinecone-client pydantic python-dotenv
```

#### 3️⃣ Set Up Environment Variables

Create a `.env` file in the project root with the following content:

```env
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=war-use-cases
EMBEDDING_MODEL=text-embedding-ada-002
```

---

### Workflow

#### 1️⃣ Data Preparation

Place your raw CSV files in:

```
datasource/
```

#### 2️⃣ Configuration

Edit `CleanCSV.py` to update the file paths:

```python
input_file = "datasource/raw_paper.csv"
output_file = "cleaned/clean_paper.csv"
```

#### 3️⃣ Data Cleaning

Run the cleaning script:

```bash
python CleanCSV.py
```

✅ **Cleaning Steps**:

1. Removes abstracts shorter than 100 characters
2. Filters out abstracts with invalid characters
3. Keeps only English-language abstracts
4. Saves cleaned data to the output directory

---

#### 4️⃣ AI Processing Configuration

Edit `CSVToJson-Semantic.py` to set up your Gemini API key and file paths:

```python
# Gemini API configuration
client = genai.Client(api_key="YOUR_API_KEY_HERE")

# Input/output directories
input_dir = "cleaned/clean_paper.csv"
output_dir = "result/json_paper.csv"
```

The processing prompt:

```python
PROCESSING_PROMPT = """
You are an AI application analysis specialist. Strictly follow these rules when processing Input text:

STEP 1: Identify AI application solutions...
STEP 2: Generate benefits for each solution...
STEP 3: Generate risks for each solution...
STEP 4: Generate mitigations for each risk...
"""
```

#### 5️⃣ Run AI Analysis

```bash
python CSVToJson-Semantic.py
```

✅ **Workflow**:

1. Reads cleaned CSV files
2. Sends abstracts to Gemini API with the specialized prompt
3. Parses JSON responses
4. Outputs structured data with:

   * Solutions
   * Benefits
   * Risks
   * Mitigation strategies
5. Saves JSON files to the output directory

---

#### 6️⃣ Expected Output JSON Structure

Each processed record will generate JSON objects like:

```json
{
  "to_embed": "Core summary (10-20 words)",
  "metadata": {
    "id": "Unique identifier (uc1, r1, b1, m1)",
    "title": "Concise title (<=10 words)",
    "description": "Detailed summary (10-50 words)",
    "context": "Keywords + evidence excerpt",
    "source": "Paper title and year"
  }
}
```

Example output:

```json
[
  {
    "to_embed": "Drones deliver medical supplies to wounded in conflict zones",
    "metadata": {
      "id": "uc1",
      "title": "Medical Supply Drones",
      "description": "Drone delivery of medical supplies in conflict areas like Syria, using GPS navigation",
      "context": "Post-war, Infrastructure (evidence: 'used in Syrian refugee camps')",
      "source": "AI in Humanitarian Logistics, 2023"
    }
  },
  {
    "to_embed": "Medical Supply Drones",
    "metadata": {
      "id": "b1",
      "title": "Faster Emergency Response",
      "description": "Reduces medical supply delivery time from hours to minutes in inaccessible areas",
      "context": "Humanitarian, Infrastructure (evidence: 'saves lives in remote conflict zones')",
      "source": "AI in Humanitarian Logistics, 2023"
    }
  }
]
```

The extraction process will generate four output JSON files:

* `UC.json`: List of solutions
* `R.json`: List of risks
* `B.json`: List of benefits
* `M.json`: List of mitigations

---

#### 7️⃣ Uploading Data to Pinecone

The final step involves uploading the JSON files to your vector database.

Run:

```bash
python UploaderData.py
```

The script’s `UploaderData` class uses the `load_from_json_files(path_to_your_input_source)` method to read the JSON files (`UC.json`, `R.json`, `B.json`, and `M.json`) from the specified folder and upload them to Pinecone.

✅ Once done, you’ll see a confirmation message, and your data will be available in the vector database under the appropriate namespace.
