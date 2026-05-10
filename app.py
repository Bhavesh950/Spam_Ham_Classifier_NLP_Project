from flask import Flask , render_template , request
import contractions
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pickle
nltk.download("stopwords")
nltk.download("punkt")

app = Flask(__name__)

# ---------------- LOAD MODEL ---------------- #

with open("best_model.pkl", "rb") as f:
    model = pickle.load(f)
    
# ---------------- PREPROCESS ---------------- #
stop_words = set(stopwords.words("english")) - {"not", "no"}
lemmatize = WordNetLemmatizer()

def preprocess(text):

    new_text = text.lower()
    new_text = contractions.fix(new_text)
    new_text = new_text.translate(str.maketrans("", "", string.punctuation))
    words = word_tokenize(new_text)
    words = [word for word in words if word.isalpha()]
    words = [word for word in words if word not in stop_words]
    words = [lemmatize.lemmatize(word) for word in words]
    return " ".join(words)

# ---------------- THRESHOLD CLASSIFIER ---------------- #

class ThresholdClassifier:
    def __init__(self, model, threshold=0.7):
        self.model = model
        self.threshold = threshold

    def predict(self, text):
        prob = self.model.predict_proba([text])[0][1]      
        
        return "spam" if prob >= self.threshold else "ham"  

    def predict_proba(self, X):
        return self.model.predict_proba([X])

# ---------------- OBJECT ---------------- #
    
sv = ThresholdClassifier(model, threshold=0.6)

# ---------------- Routes ---------------- #
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict" , methods = ["POST"])
def predict():
    message = request.form.get("message" , "")
    clean_text = preprocess(message)
    result = sv.predict(clean_text)
    return render_template("index.html" , message = message , prediction = result)

app.run(debug = True , port =5500)
