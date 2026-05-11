# **Find & Apply to Jobs Using AI Agents**

## **The problem**

Job hunting in India is broken in a specific way.

You open Naukri, LinkedIn, Instahyre, Hirist, Cutshort. Five tabs. The same recycled JDs from the same consultancies. The product companies you actually want to work at post their best roles on their **own careers pages** first. By the time a recruiter cross-posts to LinkedIn, the role's been filled.

So the real workflow looks like this:

1. Check 20 careers pages by hand. Different layouts, login walls, half don't even have RSS.  
2. For each role you like, rewrite your resume to match the JD.  
3. Draft a cover letter.  
4. Submit.

That's **30–45 minutes per application**. You do five and burn out. You go back to Naukri. The cycle continues.

## **What this workflow does**

An AI agent that runs on your machine (or a ₹400/month VPS) and does the grunt work:

* **Daily at 9 AM IST** \- searches 25 careers pages of your choice  
* **Filters new postings** for ones that match your stack and experience  
* **Telegrams you the top 5** with a one-line reason it fits  
* **On your command** \- fetches the JD, tailors your resume bullets, drafts a cover letter, pulls out the application link, saves it all in a folder  
* **You review and submit.** Always.

That last part is non-negotiable. Fully-automated applications get flagged by ATS systems and tank reply rates. The agent does the prep work. You stay in the loop.

## **The stack \- all free**

| Tool | What it does | Cost |
| ----- | ----- | ----- |
| **Hermes Agent** by Nous Research | Open-source AI agent, runs locally, has memory, schedules tasks | Free, MIT |
| **TinyFish** Search \+ Fetch | Web search and clean page fetching for agents | Free, generous rate limits |
| **OpenRouter** free model tier | Access to capable LLMs (no credit card) | Free |
| **Telegram bot** (optional) | Daily delivery \+ on-the-go commands | Free |

Total monthly cost: **₹0**. If you want it running 24/7 even when your laptop's off, Oracle Free Tier or Hetzner CX11 (\~₹400/month) \- but it's optional.

## **Setup \- about 15 minutes the first time**

### **Step 1 \- Get a free [TinyFish](https://agent.tinyfish.ai/?utm_source=instagram&utm_medium=paid-social&utm_campaign=free-search-fetch-developer-2026q2&utm_term=sukhad) API key**

Go to [Tinyfish](https://agent.tinyfish.ai/?utm_source=instagram&utm_medium=paid-social&utm_campaign=free-search-fetch-developer-2026q2&utm_term=sukhad). Sign up. Copy your API key. No credit card.

[TinyFish](https://agent.tinyfish.ai/?utm_source=instagram&utm_medium=paid-social&utm_campaign=free-search-fetch-developer-2026q2&utm_term=sukhad) just launched on May 4, 2026 \- Search and Fetch are free with generous rate limits across the API, MCP, SDKs, and CLI.

### **Step 2 \- Get a free OpenRouter key**

Go to [openrouter.ai](https://openrouter.ai/). Sign up. Create an API key. No card needed. We'll use the model `openrouter/free`, which auto-routes to whatever capable free model is available (Llama, DeepSeek, GLM, Qwen variants).

### **Step 3 \- Install Hermes Agent**

curl \-fsSL https://hermes-agent.nousresearch.com/install.sh | bash  
hermes setup

The setup wizard will ask which provider \- pick OpenRouter, paste your key, select `openrouter/free`.

### **Step 4 \- Add TinyFish as an MCP tool**

Get [Tinyfish](https://agent.tinyfish.ai/?utm_source=instagram&utm_medium=paid-social&utm_campaign=free-search-fetch-developer-2026q2&utm_term=sukhad) API Key \- sign up, no card, generous rate limits.

hermes mcp add tinyfish https://mcp.tinyfish.ai

Paste your [TinyFish](https://agent.tinyfish.ai/?utm_source=instagram&utm_medium=paid-social&utm_campaign=free-search-fetch-developer-2026q2&utm_term=sukhad) API key when prompted. Now Hermes has Search and Fetch.

### **Step 5 \- (Optional) Connect Telegram**

hermes gateway

Follow the wizard. It'll walk you through creating a Telegram bot via @BotFather. Now your agent can text you \- and you can text it back from anywhere.

### **Step 6 \- Give the agent its two jobs**

Open Hermes:

hermes

Paste **Prompt A** (the daily scan) \- see below. Hermes will turn it into a cron job. Then paste **Prompt B** (the application drafter), which Hermes will save as a skill it can run on demand.

## **The prompts**

### **Prompt A \- Daily scan (runs every morning)**

Daily at 9:00 AM IST, do the following:

1\. Use [TinyFish](https://agent.tinyfish.ai/?utm_source=instagram&utm_medium=paid-social&utm_campaign=free-search-fetch-developer-2026q2&utm_term=sukhad) Search to find new postings on the careers pages  
   of the companies in my target list (see below).

2\. Filter for roles posted in the last 24 hours.

3\. For each new role, use [TinyFish](https://agent.tinyfish.ai/?utm_source=instagram&utm_medium=paid-social&utm_campaign=free-search-fetch-developer-2026q2&utm_term=sukhad) Fetch on the URL. Extract:  
   \- Title  
   \- Location (and remote policy if mentioned)  
   \- Stack and required experience  
   \- Application URL

4\. Match against my resume below. Score each on:  
   \- Stack overlap (40%)  
   \- Experience match (30%)  
   \- Role seniority (20%)  
   \- Company quality (10%)

5\. Telegram me the top 5 ranked roles. Format each as:  
   \#N | \<Company\> | \<Role\> | \<Location\> | \<Stack\>  
   Why it fits: \<one line\>  
   Apply: \<URL\>

   Reply "apply to \#N" to draft the application.

My target companies (replace with your own list of 15–30):  
\[paste careers page URLs, one per line\]

My resume:  
\[paste your resume here as plain text\]

**How to build your target list:** spend 30 minutes once. Open your LinkedIn, look at where people two levels above you work. Browse YC's "Who's Hiring" thread. Check `layoffs.fyi`'s "still hiring" page. Pick 15–30 companies you'd actually want an offer from. Paste their `/careers` URLs into the prompt.

### **Prompt B \- Application drafter (on-demand)**

Save this as a Hermes skill named `draft-application`:

When I reply "apply to \#N", do the following for role \#N from this morning's list:

1\. Use [TinyFish](https://agent.tinyfish.ai/?utm_source=instagram&utm_medium=paid-social&utm_campaign=free-search-fetch-developer-2026q2&utm_term=sukhad) Fetch on the role URL to get the full JD.

2\. Rewrite my resume bullets to mirror the JD's language and emphasized  
   skills. Keep all bullets truthful \- don't invent experience. Output  
   as \`resume\_\<company\>.md\`.

3\. Draft a one-page cover letter:  
   \- Open with the specific reason this role fits (not generic)  
   \- Two short paragraphs: relevant experience, why this company  
   \- Close with a clear ask  
   Output as \`cover\_letter\_\<company\>.md\`.

4\. Extract from the JD page:  
   \- The application URL (or careers email)  
   \- Any hiring manager / recruiter name mentioned in the posting  
   \- Any "for questions, contact X" line  
   Output as \`application\_info.txt\`.

5\. Save all three files to \~/job-applications/\<company\>-\<date\>/.  
   Telegram me the folder path.

I will review everything and submit manually.

## **Customizing for your situation**

### **If you're a fresher / 0–2 YOE**

Build your target list from companies known to hire juniors aggressively \- Indian SaaS companies, large product engineering orgs, and ed-tech / dev-tools startups tend to have structured early-career pipelines.

Add to Prompt A: *"Filter for roles requiring 0–2 years of experience or 'fresher' or 'new grad'."*

### **If you want remote-first / USD roles**

Build your list from remote-first companies \- many YC startups, dev tools companies, and infra/devops players hire globally with India-friendly remote policies.

Add to Prompt A: *"Filter for roles that explicitly allow 'remote anywhere', 'remote worldwide', or 'remote India'."*

### **If you're senior (8+ YOE) and targeting Staff/Principal**

Build your list from data infra, dev tools, and enterprise SaaS companies where senior IC ladders go deep.

Add to Prompt A: *"Filter for Staff, Principal, Lead, or Architect titles. Skip anything below Senior."*

## **Why each piece matters**

**Why Hermes** \- most agents are stateless. Hermes has persistent memory, so it learns which roles you skip, which DMs got replies, which JD patterns you respond to. It gets sharper week over week. It also has a built-in cron scheduler, so the "daily at 9 AM" part is one config line, not a separate Airflow setup.

**Why TinyFish** \- careers pages are the worst HTML on the internet. Cookie banners, anti-bot pages, JS-rendered listings, modal popups asking you to subscribe. Generic fetch tools return 80% junk. TinyFish Fetch does a real browser render and returns clean Markdown, so the model isn't burning tokens parsing nav bars. Search is also tuned for agent retrieval \- JSON results, rank-stable, fast. Both are free with generous rate limits.

**Why OpenRouter free** \- you don't need GPT-5 to extract a job title and match it against a resume. Free Llama 3.3 70B or DeepSeek does this fine. When you outgrow free, you swap one config line.

## **Pro tips**

* **Run on a free VPS** \- Oracle Cloud Free Tier gives you a permanent free VM. Hermes runs on it forever, your laptop stays off.  
* **Find the hiring manager yourself** \- for shortlisted roles, spend 5 min on LinkedIn or the founder's Twitter and DM them when you apply. Reply rate goes up dramatically. The agent shouldn't guess at this \- wrong-person DMs hurt you.  
* **Add layoffs.fyi \-\> "still hiring"** \- that page lists companies actively hiring during slow markets. Add 5–10 to your list each month.  
* **Track what works** \- Hermes remembers across sessions. Tell it: *"these JD patterns got me interviews last month \- weight them higher."*  
* **Don't bulk-apply** \- five thoughtful applications a day beats 50 auto-submitted ones. The whole point of this workflow is *better signal*, not *more volume*.  
* **Customize the resume per role manually too** \- the agent gives you a strong draft. Spend 5 minutes editing. That's where the human edge still matters.

## **What this is *not***

* **Not auto-apply.** You hit submit. Always. ATS systems flag automated submissions, and trust me, "I let an AI apply to 500 jobs" is now a meme on r/cscareerquestions, not a strategy.  
* **Not a recruiter replacement.** It surfaces roles. The conversation is still on you.  
* **Not magic.** If your resume is weak or your stack doesn't match the market, this workflow shows you that faster \- but it doesn't fix it.

What it *does* do is collapse the most painful part of job hunting \- the manual surveillance and per-application grunt work \- from hours per day to a five-minute review.

