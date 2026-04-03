# ⚡ AI Code Auditor Pro

An AI-powered multi-agent code review system that analyzes GitHub repositories and pull requests using Google Gemini LLMs.

---

## 🚀 Features

* 🔍 **Pull Request Review**

  * Fetches PR diffs from GitHub
  * Performs automated AI-based analysis

* 🧠 **Multi-Agent LLM System**

  * Logic Expert → Finds bugs and edge cases
  * Context Expert → Checks architecture and dependencies
  * Security Expert → Detects vulnerabilities

* 🧾 **Structured Report Generation**

  * Executive Summary
  * Critical Issues
  * Suggested Improvements
  * Security Audit

* 💬 **Interactive Chat**

  * Ask follow-up questions about the code review

* 🖥️ **Dual Interface**

  * Streamlit Web App
  * Command Line Interface (CLI)

---

## 📁 Project Structure

```
.
├── src/
│   ├── app.py
│   ├── main.py
│   ├── github_client.py
│   ├── llm_orchestrator.py
│   ├── prompts.py
│
├── requirements.txt
├── .env   (not included in repo)
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/DigvijayPatil12/llm_code_reviewer.git
cd llm_code_reviewer
```

---

### 2. Install Dependencies

```
pip install -r requirements.txt
```

---

### 3. Setup Environment Variables

Create a `.env` file in the root directory:

```
GITHUB_TOKEN=your_github_token
GOOGLE_API_KEY=your_google_api_key
```

---

### 4. Run Streamlit App

```
streamlit run src/app.py
```

---

### 5. Run CLI Version

```
python src/main.py --repo owner/repo --pr 1
```

Optional:

```
python src/main.py --repo owner/repo --pr 1 --post-comment
```

---

## 🧠 How It Works

1. User provides GitHub repository and PR number
2. GitHub client fetches code/diff
3. Code is sent to multiple AI agents:

   * Logic analysis
   * Context analysis
   * Security analysis
4. Outputs are combined into a final report
5. User can interact via chat for follow-up questions

---

## 🧪 Supported Models

* gemini-2.5-flash (recommended)
* gemini-2.5-pro
* gemini-3-flash-preview

---

## 🔐 Security Notes

* Never commit your `.env` file
* Add `.env` to `.gitignore`
* Use read-only GitHub tokens when possible

---

## ⚠️ Limitations

* Large repositories are partially scanned
* Depends on API rate limits
* PR comment feature requires GitHub token permissions

---

## 📈 Future Improvements

* GitHub PR auto-comment integration
* Parallel LLM execution
* Code quality scoring
* Support for more languages
* Caching for faster responses

---

## 👨‍💻 Author

Digvijay Patil

---

## ⭐ If you found this useful, consider starring the repo!
