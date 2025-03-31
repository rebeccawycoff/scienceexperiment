from quart import Quart, render_template, request
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
# Initialize OpenAI client
from openai import AsyncOpenAI
import markdown

client = AsyncOpenAI()

app = Quart(__name__)

@app.route('/', methods=['GET'])
async def index():
    return await render_template('science.html', assistant_reply="")

@app.route('/chat', methods=['POST'])
async def chat():
    try:
        # Get user input from the form
        form_data = await request.form
        user_input = form_data['user_input']
        # Interact with OpenAI API
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"provide a a science experiment using the materials provided in {user_input}"}]
        )
        # Extract the response
        assistant_response = response.choices[0].message.content
        html_response = markdown.markdown(assistant_response)
        # Render the HTML page with the ChatGPT response
        return await render_template('science.html', assistant_reply=html_response)

    except Exception as e:
        # Log any errors
        app.logger.error(f"Error: {e}")
        return await render_template("science.html", assistant_reply="Something went wrong, please try again.")

if __name__ == "__main__":
    app.run(debug=True)