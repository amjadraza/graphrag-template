import os
import pandas as pd
import tiktoken
import asyncio
from rich import print
from graphrag.query.indexer_adapters import (
    read_indexer_entities,
    read_indexer_relationships,
    read_indexer_reports,
    read_indexer_text_units,
)
from graphrag.query.context_builder.entity_extraction import EntityVectorStoreKey
from graphrag.query.input.loaders.dfs import store_entity_semantic_embeddings
from graphrag.query.llm.oai.chat_openai import ChatOpenAI
from graphrag.query.llm.oai.embedding import OpenAIEmbedding
from graphrag.query.llm.oai.typing import OpenaiApiType
from graphrag.query.structured_search.local_search.mixed_context import LocalSearchMixedContext
from graphrag.query.structured_search.local_search.search import LocalSearch
from graphrag.query.question_gen.local_gen import LocalQuestionGen
from graphrag.vector_stores.lancedb import LanceDBVectorStore

# 1. Setup LLM
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ["GRAPHRAG_API_KEY"]
llm_model = "gpt-3.5-turbo"
embedding_model = "text-embedding-3-small"
llm = ChatOpenAI(api_key=api_key, model=llm_model, api_type=OpenaiApiType.OpenAI, max_retries=20)
token_encoder = tiktoken.get_encoding("cl100k_base")
text_embedder = OpenAIEmbedding(api_key=api_key, api_type=OpenaiApiType.OpenAI, model=embedding_model, max_retries=20)

# 2. Load the Context
INPUT_DIR = "./inputs/operation dulce"
ENTITY_TABLE = "create_final_nodes"
ENTITY_EMBEDDING_TABLE = "create_final_entities"
RELATIONSHIP_TABLE = "create_final_relationships"
COMMUNITY_REPORT_TABLE = "create_final_community_reports"
TEXT_UNIT_TABLE = "create_final_text_units"
LANCEDB_URI = f"{INPUT_DIR}/lancedb"
COMMUNITY_LEVEL = 2

entity_df = pd.read_parquet(f"{INPUT_DIR}/{ENTITY_TABLE}.parquet")
entity_embedding_df = pd.read_parquet(f"{INPUT_DIR}/{ENTITY_EMBEDDING_TABLE}.parquet")
entities = read_indexer_entities(entity_df, entity_embedding_df, COMMUNITY_LEVEL)

description_embedding_store = LanceDBVectorStore(collection_name="entity_description_embeddings")
description_embedding_store.connect(db_uri=LANCEDB_URI)
store_entity_semantic_embeddings(entities=entities, vectorstore=description_embedding_store)

relationship_df = pd.read_parquet(f"{INPUT_DIR}/{RELATIONSHIP_TABLE}.parquet")
relationships = read_indexer_relationships(relationship_df)

report_df = pd.read_parquet(f"{INPUT_DIR}/{COMMUNITY_REPORT_TABLE}.parquet")
reports = read_indexer_reports(report_df, entity_df, COMMUNITY_LEVEL)

text_unit_df = pd.read_parquet(f"{INPUT_DIR}/{TEXT_UNIT_TABLE}.parquet")
text_units = read_indexer_text_units(text_unit_df)

context_builder = LocalSearchMixedContext(
    community_reports=reports,
    text_units=text_units,
    entities=entities,
    relationships=relationships,
    entity_text_embeddings=description_embedding_store,
    embedding_vectorstore_key=EntityVectorStoreKey.ID,
    text_embedder=text_embedder,
    token_encoder=token_encoder,
)

# 4. Setup Local Search
local_context_params = { "text_unit_prop": 0.5, "community_prop": 0.1, "conversation_history_max_turns": 5, "conversation_history_user_turns_only": True, "top_k_mapped_entities": 10, "top_k_relationships": 10, "include_entity_rank": True, "include_relationship_weight": True, "include_community_rank": False, "return_candidate_context": False, "max_tokens": 12_000, }
llm_params = { "max_tokens": 2_000, "temperature": 0.0, }
search_engine = LocalSearch(
    llm=llm,
    context_builder=context_builder,
    token_encoder=token_encoder,
    llm_params=llm_params,
    context_builder_params=local_context_params,
    response_type="multiple paragraphs",
)

# 5. Run Local Search
async def run_search(query: str):
    result = await search_engine.asearch(query)
    return result

# 6. Question Generation
question_generator = LocalQuestionGen(
    llm=llm,
    context_builder=context_builder,
    token_encoder=token_encoder,
    llm_params=llm_params,
    context_builder_params=local_context_params,
)

async def generate_questions(history):
    questions = await question_generator.agenerate(question_history=history, context_data=None, question_count=5)
    return questions

if __name__ == "__main__":
    query =  "Tell me about Dr. Jordan Hayes"
    result = asyncio.run(run_search(query))
    print(result.response)
    print(result.context_data["entities"].head())
    print(result.context_data["relationships"].head())
    print(result.context_data["reports"].head())
    print(result.context_data["sources"].head())
    if "claims" in result.context_data:
        print(result.context_data["claims"].head())

    history =  [
    "Tell me about Agent Mercer",
    "What happens in Dulce military base?",
    ]
    questions = asyncio.run(generate_questions(history))
    print(questions.response)