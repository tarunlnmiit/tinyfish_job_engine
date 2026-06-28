# 🚀 TinyFish Job Engine

An AI-powered job search and application drafting engine that automates the tedious parts of job hunting. It monitors company careers pages, filters roles based on your profile, and drafts tailored application materials.

## ✨ Features

- **Automated Scanning**: Checks target careers pages daily for new postings.
- **AI Scoring**: Matches job descriptions against your resume using LLMs (Mistral, Claude, etc. via OpenRouter).
- **Smart Notifications**: Sends the best-matched roles directly to you (Telegram support included).
- **Application Drafter**: Generates tailored resume bullets and cover letters for specific roles on command.
- **Clean Data**: Leverages [TinyFish](https://agent.tinyfish.ai) for high-quality, LLM-ready web content extraction.

## 🛠 Tech Stack

- **Core**: Python
- **Search & Fetch**: [TinyFish API](https://agent.tinyfish.ai)
- **LLM Engine**: OpenRouter (Mistral AI, Claude, etc.)
- **Automation**: Cron-based scheduling

## 🚀 Setup

1. **Clone the repository**:
   ```bash
   git clone git@github.com:tarunlnmiit/tinyfish_job_engine.git
   cd tinyfish_job_engine
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   Update `config.json` with your API keys and preferences:
   - `TINYFISH_API_KEY`: Get from [agent.tinyfish.ai](https://agent.tinyfish.ai)
   - `OPENROUTER_API_KEY`: Get from [openrouter.ai](https://openrouter.ai)

4. **Target Companies**:
   Add your target career URLs to `companies.json`.

5. **Schedule Scanning**:
   Run `bash setup_cron.sh` to schedule daily scans.

## 📂 Project Structure

- `main.py`: Main entry point for the job engine.
- `scanner.py`: Logic for finding and filtering job postings.
- `drafter.py`: AI-powered drafting for resumes and cover letters.
- `notifier.py`: Telegram and console notification handling.
- `llm_utils.py`: Standardized interface for LLM calls.
- `resume/`: Store your master resume here (Markdown format recommended).

## ⚖️ License

MIT License.

---
*Built with ❤️ for the modern job seeker.*


---

*I turn scattered AI capabilities into tools people can actually run. · Available for AI contract work → [github.com/tarunlnmiit](https://github.com/tarunlnmiit)*
