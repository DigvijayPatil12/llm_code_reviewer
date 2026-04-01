LOGIC_PROMPT = """
Analyze the following code diff for logical errors, edge cases, off-by-one errors, and algorithmic efficiency.
Focus strictly on the logic, not style.

CODE DIFF:
{diff}
"""

CONTEXT_PROMPT = """
Analyze this code diff for architectural consistency, potential side effects on other components, and dependency issues.
Assume this is part of a larger, scalable system.

CODE DIFF:
{diff}
"""

SECURITY_PROMPT = """
Review this code diff specifically for security vulnerabilities (e.g., OWASP Top 10) and severe code style violations that impede readability.

CODE DIFF:
{diff}
"""

SYNTHESIS_PROMPT = """
You are the Lead Code Reviewer. Summarize these three expert reviews into one cohesive, structured Markdown report.
Filter out redundant points. If the experts disagree, note the discrepancy.

LOGIC REVIEW: {logic}
CONTEXT REVIEW: {context}
SECURITY REVIEW: {security}

The final output MUST be formatted as a Markdown comment suitable for GitHub, including:
## 📊 Executive Summary
## 🚨 Critical Issues
## 🛠️ Suggested Improvements
## 🔒 Security Audit
"""