LOGIC_PROMPT = """
Analyze the following code diff for logical errors, edge cases, off-by-one errors, and algorithmic efficiency.

IMPORTANT RULES:
- ONLY analyze what is explicitly present in the diff
- DO NOT assume how variables are used outside this snippet
- DO NOT assume user input unless clearly shown
- If context is missing, say: "Insufficient context to determine"
- Avoid speculation

CODE DIFF:
{diff}
"""

CONTEXT_PROMPT = """
Analyze this code diff for architectural consistency, potential side effects, and dependency issues.

IMPORTANT RULES:
- Base your analysis ONLY on the given diff
- DO NOT assume full project structure
- If unsure, explicitly say "Insufficient context"
- Avoid generic statements

CODE DIFF:
{diff}
"""

SECURITY_PROMPT = """
Review this code diff for security vulnerabilities.

IMPORTANT RULES:
- ONLY report vulnerabilities that are clearly exploitable from this diff
- DO NOT assume user input unless explicitly visible
- If a vulnerability depends on missing context, label it as:
  "⚠️ Potential Issue (Needs More Context)"
- Avoid generic OWASP warnings without evidence

CODE DIFF:
{diff}
"""

SYNTHESIS_PROMPT = """
You are the Lead Code Reviewer.

Combine the expert reviews into a single structured Markdown report.

IMPORTANT RULES:
- Remove speculative or weak claims
- Clearly separate:
  - Confirmed Issues
  - ⚠️ Potential Issues (Needs More Context)
- Do NOT exaggerate severity
- Prefer accuracy over completeness

LOGIC REVIEW: {logic}
CONTEXT REVIEW: {context}
SECURITY REVIEW: {security}

Format:

## 📊 Executive Summary
## 🚨 Confirmed Issues
## ⚠️ Potential Issues (Needs More Context)
## 🛠️ Suggested Improvements
## 🔒 Security Audit
"""