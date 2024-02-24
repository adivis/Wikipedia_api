from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import wikipediaapi, os

load_dotenv()
app = Flask(__name__)

full_url = ""
user_agent = 'Wikipedia-API ('+os.environ.get("MAIL")+')'
print(user_agent)
sections = []
selected_section = {}


def get_page(page_name):
    global full_url

    wiki_wiki = wikipediaapi.Wikipedia(
        user_agent=user_agent,
        language='en',
        extract_format=wikipediaapi.ExtractFormat.HTML
        )
    page_py = wiki_wiki.page(page_name)
    full_url = page_py.fullurl

    return page_py


def call_openai(sys_content, user_content):
    client = OpenAI(
        api_key=os.environ.get("API_KEY")
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": sys_content},
            {"role": "user", "content": user_content}
        ]
    )

    return completion.choices[0].message.content


def get_sections():
    page_py = get_page('Book')
    global sections
    sections = page_py.sections


def get_sub_sections(sections, sub_sections, level=0):
    for s in sections:
        sub_sections.append(s.title)
        get_sub_sections(s.sections, sub_sections, level+1)


@app.route("/")
def hello_world():
    get_sections()
    global sections
    sections_title = []
    for section in sections:
        sections_title.append(section.title)
    return render_template('index.html', data=sections_title)


@app.route("/summarized", methods=['POST'])
def summarize():
    if request.method == 'POST':
        try:
            global sections, selected_section
            selected_section['title'] = request.form['book_sections']

            # removing ` from start and end
            selected_section['title'] = selected_section['title'].replace('`', '')

            sys_content = "You are a helpful assistant."
            user_content = "Summarize in- '"+selected_section['title']+"' section in "+full_url+""

            key = selected_section['title']+"_summarized"
            if key not in selected_section.keys():
                selected_section[key] = call_openai(sys_content, user_content)
            else:
                print("$$$$$$$$$$$")
            return render_template("display_text.html", data={
                "funtionality": "Summarized",
                "text": selected_section[key]
            })

        except Exception as e:
            print('Error! {c}, Message: {m}'.format(c=type(e).__name__, m=str(e)))
            return render_template("display_text.html", data="Error has occured")


@app.route("/paraphrased", methods=['POST'])
def paraphrase():
    if request.method == 'POST':
        try:
            global sections, selected_section
            selected_section['title'] = request.form['book_sections']

            # removing ` from start and end
            selected_section['title'] = selected_section['title'].replace('`', '')
            page_py = get_page('Book')
            section = page_py.section_by_title(selected_section['title'])
            sub_sections = list()
            sub_sections.append(section.title)
            get_sub_sections(section.sections, sub_sections)

            sys_content = "You are a helpful assistant."
            user_content = "Paraphrase " + str(sub_sections) + " sections of " + full_url + " in minimum 100 words each"
            key = selected_section['title']+"_summarized"
            if key not in selected_section.keys():
                selected_section[key] = call_openai(sys_content, user_content)

            return render_template("display_text.html", data={
                "funtionality": "Paraphrased",
                "text": selected_section[key]})

        except Exception as e:
            print('Error! {c}, Message: {m}'.format(c=type(e).__name__, m=str(e)))
            return render_template("display_text.html", data="Error has occured")
