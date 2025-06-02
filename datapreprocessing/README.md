# Rebuild AI - Abstract processing pipeline
This section processes academic paper data to extract and analyze information about AI applications in post-war contexts. The system cleans CSV data of research papers list, then uses Google's Gemini AI to generate structured insights about AI applications, their benefits, risks, and mitigation strategies - with a focus on post-conflict scenarios.

### Key Features
- Data Cleaning: Filters and prepares academic paper data
- AI-Powered Analysis: Uses Google Gemini to extract insights from paper abstracts
- Structured Output: Generates JSON files with categorized information
- Post-War Focus: Identifies applications relevant to conflict recovery and humanitarian efforts

### Prerequisites
- Python 3.8+
- Google Gemini API key
- OpenAI API key
- Pinecone API key
- Required Python packages:

### Clone the repository and select correct path

Clone the repository:
   ```bash
   git clone https://github.com/dadoluca/WarProject-RebuildAI.git
   cd war-use-case-analyzer/datapreprocessing
   ```


### Dependencies
```
pip install google-generativeai openai pinecone-client pydantic python-dotenv
```

### Envirorment
Set up environment variables:
   Create a `.env` file in the project root with:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   PINECONE_INDEX_NAME=war-use-cases
   EMBEDDING_MODEL=text-embedding-ada-002
   ```


### Setup Instructions
#### 1. Data Preparation
Create datasource dir and place your raw CSV files in:
```
datasource/
```
#### 2. Configuration
Update file paths in CleanCSV.py:
```
input_file = "datasource/raw_paper.csv"
output_file = "cleaned/clean_paper.csv"
```
#### 3. Data Cleaning
Run the cleaning script:
```
python CleanCSV.py
```
##### Cleaning Process:
1. Removes abstracts shorter than 100 characters
2. Filters out abstracts with invalid characters
3. Removes abstracts not in English letters
4. Saves cleaned data to output directory

#### 4. AI Processing Configuration
Update CSVToJson-Semantic.py:
```
# Gemini API configuration
client = genai.Client(api_key="YOUR_API_KEY_HERE")

# Input/output directories
input_dir = "cleaned/clean_paper.csv"
output_dir = "result/json_paper.csv"
```
##### Processing Prompt
The system uses a detailed prompt to guide Gemini's analysis:
```
PROCESSING_PROMPT = """
You are an AI application analysis specialist. Strictly follow these rules when processing Input text:

STEP 1: Identify AI application solutions...
STEP 2: Generate benefits for each solution...
STEP 3: Generate risks for each solution...
STEP 4: Generate mitigations for each risk...
"""
```
#### 5. Run AI Analysis
Execute the processing script:
```
python CSVToJson-Semantic.py
```
##### Processing Workflow:
1. Reads cleaned CSV files
2. Sends abstracts to Gemini API with specialized prompt
3. Parses JSON response
4. Generates structured output with:
    - Solutions
    - Benefits
    - Risks
    - Mitigation strategies
5. Saves JSON files to output directory

#### Expected Output JSON Structure
Each processed record generates JSON objects with the following structure:
```
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
##### Output Example
```
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

After the extraction process is completed, four output files will be generated:

- UC.json, which contains the list of solutions
- R.json, which contains the list of risks
- B.json, which contains the list of benefits
- M.json, which contains the list of mitigations

#### 6. Run the UploaderData Class

As the final step, you need to upload the JSON files into the vector database. The `UploaderData` class includes a function called `load_from_json_files(path_to_your_input_source)`, which is invoked in the class’s main method to load JSON files from a specified folder.

The folder must contain the following four files: `UC.json`, `R.json`, `B.json`, and `M.json`.

To run the upload script, use the following command:

```
python UploaderData.py
```
Once the process is complete, a confirmation message will appear in the folder, indicating that everything was successfully uploaded. At this point, the elements will be available in the vector database, under the appropriate namespace.

