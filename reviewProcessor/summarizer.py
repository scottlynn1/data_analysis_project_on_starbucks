from transformers import pipeline
import pythontopostgreslink
import sys



text = pythontopostgreslink.get_reviews(sys.argv[1])

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
summary = summarizer(text, max_length=150, min_length=40, do_sample=False)
print('summary')
print(summary)
print('summary')
