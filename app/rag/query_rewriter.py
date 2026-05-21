# Temporarily mocked/disabled due to Gemini free-tier quota limits during development testing.
# import google.generativeai as genai
#
# from llm.model_config import configure_genai
#
# configure_genai()
# model = genai.GenerativeModel("models/gemini-2.0-flash")
#
# def rewrite_query(query):
#
#     prompt = f"""
#     Rewrite the user query
#     to improve document retrieval.
#
#     Query:
#     {query}
#
#     Return only improved query.
#     """
#
#     response = model.generate_content(prompt)
#
#     return response.text.strip()

def rewrite_query(query):
    return query