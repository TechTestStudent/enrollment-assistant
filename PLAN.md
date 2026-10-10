# Software Development Plan: Bayanihan College Enrollment Helpdesk Assistant

## 1. User Stories

### Story 1: Incoming Freshman
As an incoming freshman, I want to ask questions about admission requirements and deadlines so that I can submit my application accurately and on time.
- **Acceptance Criteria 1:** The assistant provides clear, context-grounded enrollment steps based on `faq.json`.
- **Acceptance Criteria 2:** If asked about deadlines, the assistant states the official submission dates or politely clarifies if information is unavailable.

### Story 2: Parent
As a parent of an incoming student, I want to inquire about tuition fees and payment installment options so that I can prepare our family budget.
- **Acceptance Criteria 1:** The helpdesk assistant returns accurate tuition fee breakdowns and payment schedule policies.
- **Acceptance Criteria 2:** The assistant maintains a helpful, professional tone and refuses to discuss confidential individual financial records.

### Story 3: Registrar Staff
As a registrar staff member, I want the assistant to automatically categorize incoming student queries by intent so that our team can track common helpdesk requests on the dashboard.
- **Acceptance Criteria 1:** Machine learning classification correctly labels student questions into predefined categories (e.g., Admissions, Tuition, General).
- **Acceptance Criteria 2:** Categorized statistics update dynamically on the admin/dashboard view.

---

## 2. Task Backlog

| Task | Category | Status |
| :--- | :--- | :--- |
| Set up Flask backend and ground RAG search on `faq.json` | Backend | Done |
| Implement Machine Learning intent classifier with `scikit-learn` & `joblib` | ML / Analytics | Done |
| Integrate Google GenAI SDK (`google-genai`) using environment variables | AI Integration | Done |
| Fix dynamic path resolution for `faq.json` across cloud environments | Bug Fix | Done |
| Configure production dependencies in `requirements.txt` | DevOps | Done |
| Deploy Flask service to Render with secured `GEMINI_API_KEY` | Deployment | Done |
| Run 10-question evaluation benchmark and document results in `EVAL.md` | Testing | Done |