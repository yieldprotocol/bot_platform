import logging

import weaviate
from django.conf import settings

from langchain.chat_models import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.vectorstores import Weaviate
from langchain.chains import RetrievalQAWithSourcesChain

from discord_bot.vectorstores.weaviate import weaviate_store

from .prompt import PROMPT

multiquery_retriever = MultiQueryRetriever.from_llm(
    retriever=weaviate_store.as_retriever(),
    llm=ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=settings.OPENAI_API_KEY,
    ),
)

qa_with_sources_chain = RetrievalQAWithSourcesChain.from_chain_type(
    ChatOpenAI(
        model_name="gpt-4", temperature=0, openai_api_key=settings.OPENAI_API_KEY
    ),
    chain_type="stuff",
    chain_type_kwargs=dict(prompt=PROMPT),
    retriever=multiquery_retriever,
    return_source_documents=True,
)


def run_qa_pipeline(query):
    # Santize the question by removing any trailing question marks
    cleaned_query = query.rstrip("?")

    result = qa_with_sources_chain(
        {"question": cleaned_query}, return_only_outputs=True
    )

    answer = result["answer"]
    source_ids = result["sources"]
    source_docs = result["source_documents"]

    source_urls = set()
    for d in source_docs:
        metadata = d.metadata
        source_id = metadata["source"]
        url = metadata["url"]
        if source_id in source_ids:
            source_urls.add(url)

    return dict(answer=answer, source_urls=source_urls, source_docs=source_docs)
