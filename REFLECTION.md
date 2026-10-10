# AI Helpdesk Deployment Reflection

### Question 1: System Accuracy & Safeguards
If the assistant gives a wrong deadline and a student misses enrollment, the educational institution retains ultimate legal and administrative responsibility for information published by its official platforms. To prevent catastrophic failure before a real production launch, I would implement a deterministic fallback layer that intercepts deadline-related queries and dynamically fills them directly from a verified database instead of relying on LLM generation, accompanied by a prominent visual disclaimer stating that official academic calendars override chatbot outputs.

### Question 2: Training Data & Intent Classifier Bias
Training an intent classifier on 50 self-written questions introduces severe synthetic domain bias, as my vocabulary and sentence structure do not reflect how real students express themselves (e.g., slang, typos, or local code-switching like Taglish). To fix this, I would replace the synthetic dataset with anonymized real-world inquiry logs from previous enrollment seasons, augmented using synthetic paraphrase expansion with varied linguistic styles, and continuously retrain the model on misclassified live user queries.

### Question 3: Data Privacy Act of 2012 Compliance
Under the Philippine Data Privacy Act of 2012, the school must present an explicit Privacy Notice prior to initiating the chat session, detailing the specific purpose of the processing, user rights, and data retention timelines. The backend must strictly avoid storing Personally Identifiable Information (PII) such as full names, student numbers, phone numbers, or email addresses in raw log files, utilizing automated sanitization filters to scrub sensitive entries before persistence.

### Question 4: Blockchain Technology Extension
Integrating a public or consortium blockchain would allow the assistant to cryptographically verify digital enrollment certificates, transcripts, and official fee receipts directly in the chat interface. However, this is likely not worth the implementation overhead due to high transaction latency, substantial gas cost inefficiencies, and the fact that a standard authenticated REST API linked to the school's existing Student Information System provides a faster, cheaper, and more secure solution.