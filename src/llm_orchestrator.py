import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from prompts import LOGIC_PROMPT, CONTEXT_PROMPT, SECURITY_PROMPT, SYNTHESIS_PROMPT

class LLMOrchestrator:
    def __init__(self, model_name: str = "gemini-2.5-flash", strictness: float = 0.2):
        # Initializing agents with the 2.5/3.0 series models
        self.logic_expert = ChatGoogleGenerativeAI(model=model_name, temperature=strictness)
        self.context_expert = ChatGoogleGenerativeAI(model=model_name, temperature=strictness + 0.1)
        self.security_expert = ChatGoogleGenerativeAI(model=model_name, temperature=strictness)
        
        # The Lead Reviewer / Synthesis Model
        self.synthesis_model = ChatGoogleGenerativeAI(model=model_name, temperature=0.3)
        
        # Dedicated model for the interactive chat
        self.chat_model = ChatGoogleGenerativeAI(model=model_name, temperature=0.4)

    def generate_review(self, diff_content: str) -> str:
        """Runs the multi-agent ensemble pipeline."""

        # 🔥 Context guard
        diff_content = f"""
IMPORTANT CONTEXT:
- This is a PARTIAL CODE DIFF, not the full repository
- Missing files, definitions, and validations may exist
- Do NOT assume user input unless explicitly shown

CODE:
{diff_content}
"""

        # 1. Logic Expert Analysis
        logic_review = self.logic_expert.invoke(
            [HumanMessage(content=LOGIC_PROMPT.format(diff=diff_content))]
        ).content

        # 2. Context Expert Analysis
        context_review = self.context_expert.invoke(
            [HumanMessage(content=CONTEXT_PROMPT.format(diff=diff_content))]
        ).content

        # 3. Security Expert Analysis
        security_review = self.security_expert.invoke(
            [HumanMessage(content=SECURITY_PROMPT.format(diff=diff_content))]
        ).content

        # 🔥 Synthesis guard
        synthesis_input = f"""
NOTE:
- Only include issues that are clearly supported by the diff
- If unsure, mark as "⚠️ Potential Issue (Needs More Context)"
- Avoid assumptions

LOGIC REVIEW:
{logic_review}

CONTEXT REVIEW:
{context_review}

SECURITY REVIEW:
{security_review}
"""

        # 4. Final Synthesis
        final_report = self.synthesis_model.invoke(
            [HumanMessage(content=SYNTHESIS_PROMPT.format(
                logic=logic_review,
                context=context_review,
                security=security_review
            ) + synthesis_input)]
        ).content

        return final_report

    def answer_followup(self, diff_content: str, report: str, question: str) -> str:
        """Handles the interactive chat session about the specific codebase."""
        prompt = f"""
You are the Lead Code Reviewer. You just provided a code review report based on a GitHub codebase.
The developer has a follow-up question. Answer it clearly, using code snippets if necessary.

--- ORIGINAL CODE ---
{diff_content}

--- YOUR GENERATED REPORT ---
{report}

--- DEVELOPER'S QUESTION ---
{question}
"""
        return self.chat_model.invoke([HumanMessage(content=prompt)]).content