
import pandas as pd
import textdistance
import re
from collections import Counter
from flask import Flask , render_template, request

app = Flask(__name__)

words = []

with open('autocorrect book.txt','r',encoding='utf-8') as f:
    data = f.read()
    data = data.lower()
    word = re.findall(r'\w+', data)
    words = words + word

V = set(words)
word_freq_dict = Counter(words)
total_word_freq = sum(word_freq_dict.values())
probs = {}


for k in word_freq_dict.keys():
    probs[k] = word_freq_dict[k]/total_word_freq

@app.route('/')
def index():
    return render_template('index.html',suggestions=None)


@app.route('/suggest', methods=['POST'])
def suggest():
    keyword = request.form['keyword'].lower()
    if keyword:
        similarities = [1 - textdistance.Jaccard(qval=2).distance(v, keyword) for v in word_freq_dict.keys()]
        df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
        df.columns = ['Word', 'Prob']
        df['Similarity'] = similarities
        suggestions = df.sort_values(['Similarity', 'Prob'], ascending=False)[['Word', 'Similarity']]
        suggestions_list = suggestions.to_dict('records')  # Convert DataFrame to list of dictionaries
        return render_template('index.html', suggestions=suggestions_list)


if __name__ == '__main__':
    app.run(debug=True)