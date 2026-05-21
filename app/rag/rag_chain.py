from rag.advanced_rag import advanced_retrieval

from rag.web_search import search_web

from llm.generator import generate_answer

from rag.citations import generate_citations


def ask_question(query):

    # -----------------------------------
    # DOCUMENT RETRIEVAL
    # -----------------------------------

    contexts = advanced_retrieval(query)


    # -----------------------------------
    # WEB SEARCH
    # -----------------------------------

    web_results = search_web(query)


    # -----------------------------------
    # ADD WEB RESULTS
    # -----------------------------------

    if web_results:

        for web in web_results:

            contexts.append({

                "chunk": web["content"],

                "score": 0.0,

                "metadata": {
                    "source": web["url"],
                    "chunk_id": "web"
                }
            })


    # -----------------------------------
    # GENERATE ANSWER
    # -----------------------------------

    answer = generate_answer(
        query,
        contexts
    )


    # -----------------------------------
    # GENERATE CITATIONS
    # -----------------------------------

    citations = generate_citations(
        contexts
    )


    # -----------------------------------
    # FINAL RESPONSE
    # -----------------------------------

    return {

        "answer": answer,

        "citations": citations,

        "contexts": contexts
    }