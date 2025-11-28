# Agent Workflow (Planner → Data → Insight → Evaluator → Creative)

## 1. Planner Agent
- Understands the task: “Analyze campaign performance”
- Breaks work into subtasks
- Decides which agents to call
- Orchestrates the full workflow

## 2. Data Agent
- Loads the dataset
- Cleans and preprocesses data
- Computes CTR, ROAS, spend, impressions per day
- Aggregates data by campaign
- Returns structured numerical insights

## 3. Insight Agent
- Reads the processed data
- Detects performance drops:
  - ROAS decline
  - CTR decline
  - Budget cut
  - High impressions + low CTR
- Generates hypotheses explaining *why* performance dropped

## 4. Evaluator Agent
- Validates hypotheses using numeric reasoning
- Assigns a confidence score (high/medium/low)
- Removes weak or conflicting insights

## 5. Creative Agent
- Extracts keywords from existing creative_message
- Uses templates to generate 2–3 new creatives
- Returns human-quality ad lines

## 6. Final Output
- insights.json (problem explanation per campaign)
- creatives.json (creative improvement suggestions)