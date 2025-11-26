import json
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in environment variables.")

genai.configure(api_key=API_KEY)

def _call_llm(prompt: str, model_name: str = "models/gemini-2.5-flash") -> str:
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)

        text = getattr(response, "text", None)
        if not text:
            return "Error: LLM returned no text. Check API key or quota."

        return text.strip()
    except Exception as e:
        return f"Error while calling LLM: {e}"


def _serialize_plan_for_prompt(weekly_plan: dict) -> str:
    try:
        return json.dumps(weekly_plan, indent=2, ensure_ascii=False)
    except TypeError:
        return str(weekly_plan)

def summarize_weekly_plan(weekly_plan: dict, user_profile: dict | None = None) -> str:
    plan_json = _serialize_plan_for_prompt(weekly_plan)

    goal = user_profile.get("goal") if user_profile else None
    activity = user_profile.get("activity_level") if user_profile else None
    daily_cals = user_profile.get("daily_calories") if user_profile else None
    weekly_budget = user_profile.get("weekly_budget") if user_profile else None

    prompt = f"""
You are NutriMate. Generate a clean, structured Markdown summary of a 7-day weekly meal plan.

Include a short, professional introduction at the top with the following format:

## NutriMate Weekly Overview
A brief introduction of 1–2 sentences explaining that you are NutriMate, an AI-powered nutrition assistant providing a structured overview of the user's weekly meal plan.

Then continue with the required structure below.

RULES:
- You MUST output all 7 days: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.
- For each day output EXACTLY:
  - Breakfast (meal name, calories, price)
  - Lunch (meal name, calories, price)
  - Dinner (meal name, calories, price)
  - Daily Total: ___ calories — $___
- Use Markdown headings.
- Use bullet points.
- NO long paragraphs.
- NO skipping days.
- NO combining days.
- NO storytelling outside of the short introduction.
- Keep all the font uniform.

FORMAT:

## NutriMate Weekly Overview
(2-sentence introduction goes here.)

## Weekly Summary

### Monday
- **Breakfast:** ...
- **Lunch:** ...
- **Dinner:** ...
- **Daily Total:** ___ kcal — $___

### Tuesday
(same format)

### Wednesday
(same format)

### Thursday
(same format)

### Friday
(same format)

### Saturday
(same format)

### Sunday
(same format)

## Observations
- Bullet points only.
- Mention variety, high/low calorie days, high/low cost days.

User Info:
- Goal: {goal}
- Activity: {activity}
- Daily Target: {daily_cals}
- Weekly Budget: {weekly_budget}

WEEKLY PLAN JSON:
{plan_json}
"""
    return _call_llm(prompt)



def analyze_budget_and_calories(weekly_plan: dict, user_profile: dict | None = None) -> str:
    plan_json = _serialize_plan_for_prompt(weekly_plan)

    daily_cals = user_profile.get("daily_calories") if user_profile else None
    weekly_budget = user_profile.get("weekly_budget") if user_profile else None
    goal = user_profile.get("goal") if user_profile else None

    prompt = f"""
You are NutriMate. Provide a clean Markdown analysis of budget and calories.

RULES:
- Use headings.
- Use bullet points.
- Keep it short.
- No long paragraphs.
- Keep all the font uniform.

FORMAT:

## Calorie Analysis
- Target: {daily_cals}
- Daily average calories: (infer from plan)
- High-calorie meals:
- Low-calorie meals:
- Days exceeding target:
- Days below target:

## Budget Analysis
- Weekly Budget: ${weekly_budget}
- Estimated Weekly Cost: (infer from plan)
- Most expensive meals:
- Cheapest meals:
- Days that exceed daily budget:

## Recommendations
- 3–6 bullet points for calorie, cost, or meal improvement.

User Goal: {goal}

WEEKLY PLAN JSON:
{plan_json}
"""
    return _call_llm(prompt)



def suggest_alternatives(weekly_plan: dict, user_profile: dict | None = None) -> str:
    plan_json = _serialize_plan_for_prompt(weekly_plan)
    goal = user_profile.get("goal") if user_profile else None

    prompt = f"""
You are NutriMate. Provide clear Markdown suggestions for improving the weekly meal plan.

RULES:
- Use bullet points or numbered list.
- Keep the suggestions simple and practical.
- No paragraphs longer than 2 lines.
- Reference specific meals/days.
- Keep all the font uniform.

FORMAT:

## Suggestions (Goal: {goal})
1. ...
2. ...
3. ...
4. ...
5. ...

Weekly Plan JSON:
{plan_json}
"""
    return _call_llm(prompt)



def answer_user_question(weekly_plan: dict, question: str, user_profile: dict | None = None) -> str:
    plan_json = _serialize_plan_for_prompt(weekly_plan)
    goal = user_profile.get("goal") if user_profile else None

    prompt = f"""
You are NutriMate. Answer the user's question strictly based on the weekly meal plan.

RULES:
- Markdown only.
- Short, clean answers.
- Bullet points allowed.
- Reference specific days and meals.
- No long paragraphs.
- Keep all the font uniform.

FORMAT:

## Answer
(Direct response to user's question)

## Supporting Details
- Bullet point references to meals/days from the plan.

User Question:
\"\"\"{question}\"\"\"

User Goal: {goal}

Weekly Plan JSON:
{plan_json}
"""
    return _call_llm(prompt)
