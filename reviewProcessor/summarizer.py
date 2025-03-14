import os
import nest_asyncio
from llama_index.core.schema import TextNode
from llama_index.core import get_response_synthesizer
from llama_index.core import SummaryIndex
from llama_index.llms.groq import Groq
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import psycopg2
from dotenv import load_dotenv

load_dotenv()



GROQ_API_KEY = os.environ.get('groq_key')
os.environ["GROQ_API_KEY"] = GROQ_API_KEY


nest_asyncio.apply()

llm = Groq(model="llama-3.1-8b-instant")

Settings.llm = Groq(model="llama-3.1-8b-instant")
Settings.embed_model = HuggingFaceEmbedding()

conn = psycopg2.connect(database = "starbucksproject", 
                          user = "scott", 
                          host = 'localhost',
                          password = os.environ.get('pg_password'),
                          port = 5432
                        )
cur = conn.cursor()

try:
  cur.execute("SELECT review FROM reviews WHERE rating = 1 LIMIT 20;")
  text = ''
  for row in cur:
    text = text + ' ' + row[0]
      # cur.execute("INSERT INTO negative_words_before_2014 (words, occurrences) VALUES (%s, %s);", (words, count))
    

finally:
  cur.close()
  conn.commit()
  conn.close()

splitter = SentenceSplitter(chunk_size=2048)
chunks = splitter.split_text(text)
nodes = []
for chunk in chunks:
  nodes.append(TextNode(text=chunk))
summary_index = SummaryIndex(nodes)

summary_query_engine = summary_index.as_query_engine(
    response_mode="tree_summarize",
    use_async=True,
)

response = summary_query_engine.query("Summarize the given reviews of Starbucks")
print(response)
