"""
MCP Reasoner
============
The reasoning layer - all LLM interactions go through here.

Responsibilities:
- Making decisions based on context
- Generating plans
- Interpreting user intent
- Providing responses

This separation ensures LLM calls are isolated and controllable.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class Reasoner:
    """
    The LLM reasoning component of MCP.

    All AI reasoning is centralized here, making it easy to:
    - Swap models
    - Add logging/monitoring
    - Implement caching
    - Control costs
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def reason(self, prompt: str, context: str = "", temperature: float = 0.7) -> str:
        """
        Core reasoning method - send a prompt to the LLM.

        Args:
            prompt: The main instruction/question
            context: Additional context to include
            temperature: Creativity level (0-1)

        Returns:
            The LLM's response
        """
        messages = []

        if context:
            messages.append({
                "role": "system",
                "content": f"Context:\n{context}"
            })

        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Reasoning error: {str(e)}"

    def interpret_intent(self, user_input: str, context: str = "") -> dict:
        """
        Interpret what the user wants to do.

        Returns a structured intent object.
        """
        prompt = f"""Analyze this user input and determine their intent.

User input: {user_input}

Return a JSON object with:
- "type": one of ["question", "command", "goal", "clarification"]
- "action": what they want to do
- "details": any specific details

Only return the JSON, nothing else."""

        response = self.reason(prompt, context, temperature=0.3)

        # Parse JSON (simple extraction)
        try:
            import json
            # Find JSON in response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass

        return {"type": "question", "action": user_input, "details": ""}

    def generate_plan(self, goal: str, context: str = "") -> list[str]:
        """
        Generate a plan for achieving a goal.

        Returns a list of steps.
        """
        prompt = f"""Create a plan to achieve this goal:

Goal: {goal}

Return a numbered list of 3-5 concrete steps.
Only return the list, nothing else."""

        response = self.reason(prompt, context, temperature=0.3)

        steps = []
        for line in response.strip().split('\n'):
            line = line.strip()
            if line and line[0].isdigit():
                step = line.split('.', 1)[-1].strip()
                if step:
                    steps.append(step)

        return steps if steps else [f"Complete: {goal}"]

    def decide_action(self, situation: str, options: list[str], context: str = "") -> str:
        """
        Make a decision given a situation and options.

        Returns the chosen option.
        """
        options_str = "\n".join(f"- {opt}" for opt in options)
        prompt = f"""Given this situation, choose the best option.

Situation: {situation}

Options:
{options_str}

Return only the chosen option text, nothing else."""

        response = self.reason(prompt, context, temperature=0.3)
        return response.strip()

    def generate_response(self, query: str, context: str = "") -> str:
        """
        Generate a helpful response to a query.
        """
        prompt = f"""You are a helpful coding assistant. Answer this query:

{query}

Be concise and provide code examples when appropriate."""

        return self.reason(prompt, context, temperature=0.7)
