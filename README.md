# SmartFlow AI — Business Tracking for Township Businesses

> Built entirely with Claude Code — agentic mode, daily iteration.

**Problem:** Small businesses in SA lose track of cash flow — Uber, stock, airtime mixed.

**Solution:** SmartFlow AI auto-categorizes every transaction and gives AI business tips.

### Demo
CLI: `python main.py add expense 120 "Uber to supplier"` → auto tags Transport
Web: `streamlit run dashboard.py` → Dashboard with Income R2500 / Expense R800 / Profit R1700

### Features Built with Claude Code
- [x] SQLite persistence
- [x] AI auto-categorization (no hardcoded rules only — pattern matching)
- [x] AI Insights engine
- [x] Streamlit dashboard with functional navigation: Dashboard, Transactions, Reports, Analytics, Settings, Help
- [x] Fully responsive dark theme

### How I Built It With Claude Code
Day 1: Prompted Claude Code to scaffold CLI + DB
Day 2: Added AI categorization logic via Claude
Day 3: Built dashboard UI — iterated on dark theme to match Figma

Terminal transcript: (attach screenshot)

### Next Steps
- Connect Claude API for natural language queries: "How much did I spend on transport last week?"
- WhatsApp bot integration for spaza shops
- Export to SARS format

Author: Nompumelelo — Actively building with Claude Code
