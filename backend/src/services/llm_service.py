from langchain_groq import ChatGroq
from src.schemas.chat_schema import LLMResponse
from src.utils.logger import logger
from src.config import GROQ_API_KEY


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=GROQ_API_KEY
)

structured_llm = llm.with_structured_output(LLMResponse)


def generate_search_query(question, history):

    prompt = f"""
You are a search query generator for a company policy assistant.

Your task is to convert the user's latest message into a standalone
search query for retrieving relevant company policy documents.

Conversation history:
{history}

Latest user message:
{question}

Rules:
- If the latest message is a policy-related question, rewrite it as a
  clear standalone search query.
- Resolve references such as "it", "that", "this", "they", etc. using
  the conversation history.
- Preserve the user's actual intent.
- Do not answer the question.
- Do not add information that is not present in the conversation.
- If the message is casual conversation such as "Hi", "Hello",
  "Thanks", "Good morning", etc., return the message itself.
- Return ONLY the search query.
"""

    response = llm.invoke(prompt)

    logger.info("Generating standalone search query")

    return response.content


def generate_answer(question, context, history):

    prompt = f"""
You are a helpful company policy assistant.

Your job is to answer the user's message naturally and accurately.

Conversation history:
{history}

Retrieved company policy context:
{context}

User message:
{question}

Follow these rules carefully:

1. CASUAL CONVERSATION
   If the user is greeting you or making casual conversation, respond
   naturally.

   Examples:
   - "Hi" → "Hi! How can I help you with company policies?"
   - "Hello" → "Hello! How can I help you?"
   - "Good morning" → "Good morning! How can I help you?"
   - "Thanks" → "You're welcome!"

   For casual conversation, do NOT require information from the policy
   context.

   Set:
   has_answer = true

2. POLICY QUESTIONS
   If the user is asking about a company policy, answer ONLY using
   information contained in the retrieved context.

   Do not make up, assume, or infer company policy information.

3. INSUFFICIENT INFORMATION
   If the retrieved context does not contain enough information to
   answer a policy-related question:

   answer = "I don't have information about that."
   has_answer = false

4. CONVERSATION CONTEXT
   Use the conversation history to understand follow-up questions.

   For example:
   User: "How many annual leaves do I get?"
   User: "Can I carry them forward?"

   Understand that "them" refers to annual leaves.

5. ANSWER STYLE
   - Be concise and clear.
   - Use Markdown when useful.
   - Do not mention the retrieval process.
   - Do not mention "context", "chunks", "Pinecone", or internal systems.
   - Do not say that you are an AI unless specifically asked.

Return the response in exactly this structure:

{{
    "answer": "your answer",
    "has_answer": true
}}
"""

    logger.info("Generating answer using LLM")

    return structured_llm.invoke(prompt)
