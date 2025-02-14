from transformers import pipeline
import pythontopostgreslink
import sys

# this program is a work in progress
# would like to be able to summarize concatenated reviews but their is a token limit restriction
# possible solution is to summarize several portions and the concatenate those and summarize recursively

text = pythontopostgreslink.get_reviews(sys.argv[1])

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
summary = summarizer(text, max_length=150, min_length=40, do_sample=False)
print('summary')
print(summary)
print('summary')
