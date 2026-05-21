# Temporarily mocked/disabled due to Gemini free-tier quota limits during development testing.
# import google.generativeai as genai
#
# from llm.model_config import configure_genai
#
# configure_genai()
# model = genai.GenerativeModel("models/gemini-2.0-flash")
#
# def generate_answer(query, contexts):
#
#     context_text = ""
#
#     for ctx in contexts:
#
#         context_text += f"""
#
#         CONTENT:
#         {ctx['chunk']}
#
#         SOURCE:
#         {ctx['metadata']['source']}
#         """
#
#     prompt = f"""
#     Answer the user question
#     using ONLY provided context.
#
#     If answer not found,
#     say:
#     "Information not found in documents."
#
#     USER QUESTION:
#     {query}
#
#     CONTEXT:
#     {context_text}
#
#     Give clear structured answer.
#     """
#
#     response = model.generate_content(prompt)
#
#     return response.text

def generate_answer(query, contexts):

    if not contexts:
        return "No relevant information found."

    final_answer = ""

    for idx, ctx in enumerate(contexts[:2], start=1):

        final_answer += f"""
Source {idx}:

{ctx['chunk'][:500]}

"""

    return final_answer