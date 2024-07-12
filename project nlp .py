import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def generate_summary():
    try:
        
        text = input_text.get("1.0", "end")
        num_sentences = int(num_sentences_entry.get())

       
        if not text.strip():
            messagebox.showwarning("Warning", "Input text is empty.")
            return

        
        summary = summarize_text(text, num_sentences)

        
        output_text.delete("1.0", "end")
        output_text.insert("1.0", summary)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def summarize_text(text, num_sentences):
    sentences = text.split('.')
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences)
    sentence_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
    sentence_scores = [(i, score) for i, score in enumerate(sentence_similarity.mean(axis=1))]
    top_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:num_sentences]
    top_sentences = sorted(top_sentences, key=lambda x: x[0])
    summary = '. '.join([sentences[i] for i, _ in top_sentences])
    return summary

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            input_text.delete("1.0", "end")
            input_text.insert("1.0", text)

def clear_text():
    input_text.delete("1.0", "end")
    output_text.delete("1.0", "end")

root = tk.Tk()
root.title("Text Summarizer")


input_text = scrolledtext.ScrolledText(root, width=60, height=10, wrap=tk.WORD)
input_text.grid(row=0, column=0, padx=10, pady=10)


num_sentences_label = tk.Label(root, text="Number of Sentences:")
num_sentences_label.grid(row=1, column=0, padx=10, pady=(0,5))
num_sentences_entry = tk.Entry(root)
num_sentences_entry.grid(row=1, column=1, padx=10, pady=(0,5))
num_sentences_entry.insert(0, "2")  # Default value


output_text = scrolledtext.ScrolledText(root, width=60, height=10, wrap=tk.WORD)
output_text.grid(row=2, column=0, padx=10, pady=(0,10))


summarize_button = tk.Button(root, text="Summarize", command=generate_summary)
summarize_button.grid(row=3, column=0, padx=10, pady=(0,10))


upload_button = tk.Button(root, text="Upload File", command=load_file)
upload_button.grid(row=4, column=0, padx=10, pady=(0,10))


clear_button = tk.Button(root, text="Clear", command=clear_text)
clear_button.grid(row=5, column=0, padx=10, pady=(0,10))

root.mainloop()
