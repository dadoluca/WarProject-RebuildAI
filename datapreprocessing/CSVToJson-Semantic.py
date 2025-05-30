from google import genai
import pandas as pd
import json
import re
import os

# Configuration
client = genai.Client(api_key="AIzaSyAd_u59ZRpDOKHwzWa3nogCseYsFOgdfDc")
#model = genai.GenerativeModel('gemini-2.0-flash')
input_dir = "datasource/groups_95_2"
output_dir = "result/json_95"

id_counter_uc = 0
id_counter_r = 0
id_counter_b = 0
id_counter_m = 0

PROCESSING_PROMPT = """
 You are an AI application analysis specialist. Strictly follow these rules when processing Input text：

**Input text**: {Input_text}

**Processing Rules**:

STEP 1: Identify use cases for AI applications,for each AI Application Use Case you find or summarize or generate based on the input text:
Output a JSON object with these fields:
{{
  "to_embed": "[A 10-20 word core summary including: application area + technology used + beneficiaries]",
  "title": "[A concise title summarizing the AI application use case in <=10 words]",
  "type": "use",
  "description": "[A 10-50 word summary describing application area (country/region/field) + implementation method (framework/algorithm/tool)]",
  "context_is_post_war": true/false,
  "context_ keywords_areas": "Keyword1,Keyword2",
  "context_evidence_excerpt": "Direct text excerpt supporting post-war status"
}}
 “context_is_post_war” should be true if any of the following apply: 
mentions conflict zones (e.g., Syria, Ukraine)
includes keywords: “post-war”, “post-conflict”, “refugee”, “reconstruction”
involves humanitarian aid or war-related legacy issues
“context_ keywords_areas” must pick 2-3 keywords from: ["Post-conflict", "Post-war", "Humanitarian", "Infrastructure", "peacebuilding","conflict recovery","war-affected","humanitarian crisis","Data Collection", "Accountability"]
 Include a direct excerpt from the article as “context_evidence_excerpt”

STEP 2: For each AI Application Use Case from STEP 1, generate its Benefit(s):
For each benefit, output a JSON object with these fields:
{{
  "to_embed": "[title of AI application use case from STEP 1]",
  "title": "[A concise title summarizing the benefit in <=10 words]",
  "type": "benefit",	
  "description": "[A 10-50 word summary of how it benefits (e.g., human rights, privacy, society, etc.)]",
  "context_is_post_war": true/false,
  "context_ keywords_areas": "Keyword1,Keyword2",
  "context_evidence_excerpt": "Direct text excerpt supporting post-war status"
}}
(same context judgment as Step 1)

STEP 3: For each AI Application Use Case from STEP 1, generate its Risk(s):
For each risk, output a JSON object with these fields:
{{
  "to_embed": "[title of AI application use case from STEP 1]",
  "title": "[A concise title summarizing the risk in <=10 words]",
  "type": "risk",
  "description": "[A 10-50 word summary of the risk and how it causes harm (e.g., human rights, privacy, social impact)]",
  "context_is_post_war": true/false,
  "context_ keywords_areas": "Keyword1,Keyword2",
  "context_evidence_excerpt": "Direct text excerpt supporting post-war status"
}}
(same context judgment as Step 1)

STEP 4: For each Risk from STEP 3, generate its Mitigation(s) :
For each mitigation, output a JSON object with these fields:
{{
  "to_embed": "[title of risk of AI application from STEP 3]",
  "title": "[A concise title summarizing the mitigation strategy in <=10 words]",
  "type": "mitigate",
  "description": "[A 10-50 word summary of how the mitigation reduces or prevents the risk]",
  "context_is_post_war": true/false,
  "context_ keywords_areas": "Keyword1,Keyword2",
  "context_evidence_excerpt": "Direct text excerpt supporting post-war status"
 }}
(same context judgment as Step 1)


**Output Requirements**:
- Strict JSON format without Markdown
- Preserve original technical terms
- Empty fields if information unavailable

**JSON Schema**:
{{
  "title": "Drones for Medical Supply Delivery",
  "to_embed": "Drones deliver medical supplies like blood to wounded people in conflict zones, as tested in Rwanda.",
  "description": "Drones deliver medical supplies, such as blood to wounded individuals, in conflict zones, as demonstrated in Rwanda, improving access to critical care in areas where traditional logistics are disrupted.",
  "context_is_post_war": true,
  "context_ keywords_areas": "Post-war, Infrastructure",
  "context_evidence_excerpt":"anti-trafficking in Moldova, Ukraine crisis"
}}
"""

def process_row(row, idx):
    """Process single CSV row with enhanced error handling"""
    try:
        inputText= row['abstract']
        # Generate AI analysis
        response = client.models.generate_content(model="gemini-2.0-flash",
            contents=PROCESSING_PROMPT.format(Input_text=inputText)
        )
        
        # Extract JSON from response
        json_match = re.search(r'\[.*\]', response.text, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON detected in response")
            
        ai_data = json.loads(json_match.group())
        print(f"Processed row {idx}: {ai_data}")
        
        result_list = []
        for item in ai_data:
            id_type=""
            id_counter=0
            if item.get("type") == "use":
                id_type="uc";
                global id_counter_uc
                id_counter_uc +=1
                id_counter=id_counter_uc
            elif item.get("type") == "benefit":
                id_type="b";
                global id_counter_b
                id_counter_b+=1
                id_counter=id_counter_b
            elif item.get("type") == "risk":
                id_type="r";
                global id_counter_r
                id_counter_r +=1
                id_counter=id_counter_r
            elif item.get("type") == "mitigate":
                id_type="m";
                global id_counter_m
                id_counter_m +=1
                id_counter=id_counter_m
            else:
                id_type=""
                id_counter +=1
            dict_item= {
                        "to_embed": item.get("to_embed", ""),
                        "metadata": {
                            "id": id_type+f"{id_counter}",  # Generate sequential ID
                            "title": item.get("title", ""),
                            "description": item.get("description", ""),
                            "context": item.get("context_keywords_areas", "")+"("+item.get("context_evidence_excerpt", "")+")",
                            "source": row['title'] + ', ' +  str(row['year']) # Directly from CSV
                        }
                    }
            result_list.append(dict_item)
        
        # Build final object
        return result_list
        
    except Exception as e:
        print(f"Error processing record {idx}: {str(e)}")
        return None



# Main processing
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]

for csv_file in csv_files:
    csv_path = os.path.join(input_dir, csv_file)
    df = pd.read_csv(csv_path)
    output = []

    #df = pd.read_csv("datasource/groups_97/threshold_clean_97_group_1.csv")
    for idx, row in df.iterrows():
        if pd.isna(row['abstract']):
            continue
        processed = process_row(row, idx)
        if processed:
            output.append(processed)
            # Create output JSON filename
    json_filename = os.path.splitext(csv_file)[0] + '.json'
    json_path = os.path.join(output_dir, json_filename)
    # Save results
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)