import openai
import json

from flask import Flask, render_template, request
from dotenv import dotenv_values

config = dotenv_values(".env");
openai.api_key= config["OPENAI_APIKey"]

app = Flask(__name__,
    template_folder='templates',
    static_url_path='',
    static_folder='static',

)

def get_colors(msg):
    prompt = f"""
    You are a color palette generating assistant that responds to 
    a text prompts for color palettes
    Yiou should generate color palettes that fit the theme, mood or instructions in the prompt
    the palettes should be between 2 and 5 colors
    
    Desired Format: a Json array with hex code of colors
    
    Text:{msg}
    
    Result:
    """

    response = openai.Completion.create(
        model = "gpt-3.5-turbo-instruct",
        prompt = prompt,
        max_tokens = 100,
        #n=3 
    ) 
    colors = json.loads(response['choices'][0]['text'])
    return colors

@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    query = request.form.get("query")
    colors = get_colors(query)
    return{"colors":colors}
    #OpenAI completion call
    #return list of colors


@app.route("/")
def index():

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
