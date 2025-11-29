Kasparro Agentic FB Performance Analyst

This project analyzes a synthetic Facebook Ads dataset using an agent-based workflow.
The goal is to identify campaigns with performance decline, explain why the decline happened, and generate improved ad creatives.

It follows the assignment guidelines for the Applied AI Engineer role at Kasparro and demonstrates:
	•	Data preprocessing and metric computation
	•	Performance diagnosis based on ROAS/CTR
	•	Agentic reasoning structure
	•	Insight generation
	•	Creative message generation
	•	Modular and reproducible workflow


1. Project Structure

kasparro_assignment/
│
├─ data/
│   └─ synthetic_fb_ads_undergarments.csv
│
├─ outputs/
│   ├─ insights.json
│   └─ creatives.json
│
├─ src/
│   ├─ data_agent.py
│   ├─ insight_agent.py
│   ├─ creative_agent.py
│   ├─ evaluator_agent.py
│   └─ orchestrator.py
│
├─ prompts/
│   ├─ planner_prompt.md
│   ├─ insight_prompt.md
│   └─ creative_prompt.md
│
├─ agent_workflow.md
├─ requirements.txt
└─ run.py



2. Agent Workflow Overview

The project uses a 5-agent pipeline:

1. Planner Agent

Breaks the task into steps and orchestrates the whole workflow.

2. Data Agent
	•	Loads the dataset
	•	Cleans missing values
	•	Computes CTR, ROAS
	•	Aggregates performance by date and campaign

3. Insight Agent

Uses structured rules to identify:
	•	ROAS decline
	•	CTR decline
	•	Budget cuts
	•	Audience fatigue
	•	Weak conversion patterns

Generates clear hypotheses for each underperforming campaign.

4. Evaluator Agent
	•	Validates insights
	•	Removes duplicates
	•	Assigns confidence levels

5. Creative Agent
	•	Extracts keywords from creative_message
	•	Generates 2–3 improved ad creatives
	•	Ensures tone and relevance


3. Outputs

insights.json

Contains diagnostic insights for each problematic campaign.

Example:

{
  "Women Cotton Classics": [
    {
      "type": "roas_drop",
      "message": "ROAS dropped from 85.55 to 0.00 (-100.0%). Possible conversion or targeting issue."
    }
  ]
}

creatives.json

Contains newly generated creative text suggestions.

Example:

{
  "Women Cotton Classics": [
    "Experience Cotton comfort designed for everyday wear.",
    "Feel the Soft difference — made for movement and confidence."
  ]
}


4. Running the Project

Activate environment:

source venv/bin/activate

Run full pipeline (after src/ files are filled):

python run.py

Or run individual scripts:

python step1_preview.py
python step3_roas_drop.py
python step5_generate_hypotheses.py
python step6_creatives.py



5. Requirements

pandas
numpy

