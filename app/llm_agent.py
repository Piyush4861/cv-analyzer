from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

def ask_llm(context_list, query):
    results = []
    for idx, cv in enumerate(context_list):
        prompt = f"Candidate #{idx+1} info:\n{cv}\n\nAnswer this:\n{query}"
        result = pipe(prompt, max_new_tokens=200)[0]["generated_text"]
        answer = result.split("Answer this:")[-1].strip()
        results.append(f"Candidate #{idx+1}:\n{answer}\n")
    return "\n".join(results)