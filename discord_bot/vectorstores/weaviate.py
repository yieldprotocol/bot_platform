from typing import Any, Dict, List

import weaviate

from django.conf import settings

from langchain.vectorstores import Weaviate
from langchain.docstore.document import Document


class HybridSearchWeaviate(Weaviate):
    def similarity_search_by_text(
        self, query: str, k: int = 4, **kwargs: Any
    ) -> List[Document]:
        """Return docs most similar to query.

        Args:
            query: Text to look up documents similar to.
            k: Number of Documents to return. Defaults to 4.

        Returns:
            List of Documents most similar to the query.
        """

        content: Dict[str, Any] = {"concepts": [query]}
        if kwargs.get("search_distance"):
            content["certainty"] = kwargs.get("search_distance")
        query_obj = self._client.query.get(self._index_name, self._query_attrs)
        if kwargs.get("where_filter"):
            query_obj = query_obj.with_where(kwargs.get("where_filter"))
        if kwargs.get("additional"):
            query_obj = query_obj.with_additional(kwargs.get("additional"))

        # Perform Hybrid Search
        result = query_obj.with_hybrid(query=query).with_limit(k).do()

        if "errors" in result:
            raise ValueError(f"Error during query: {result['errors']}")
        docs = []
        for res in result["data"]["Get"][self._index_name]:
            text = res.pop(self._text_key)
            docs.append(Document(page_content=text, metadata=res))
        return docs


weaviate_client = weaviate.Client(
    url=settings.WEAVIATE_URL,
    auth_client_secret=weaviate.AuthApiKey(api_key=settings.WEAVIATE_API_KEY),
    additional_headers={"X-OpenAI-Api-Key": settings.OPENAI_API_KEY},
)

weaviate_store = HybridSearchWeaviate(
    weaviate_client,
    settings.WEAVIATE_CODEARENA_INDEX_NAME,
    text_key="text",
    attributes=["url", "source"],
)
