from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Set up the OpenAI API key directly
client = OpenAI(api_key="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")

# In-memory storage for user profiles
user_profiles = {}

# Function to get the likeliest disaster using the OpenAI API
def get_likeliest_disaster(state, city, street):
    prompt = f"What is the likeliest natural disaster to occur in {city}? Respond with a single word, no whitespaces or hyphens."

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
        max_tokens=150,
        n=5,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].message.content.lower()

# Function to generate content using the OpenAI API
def generate_content(prompt):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
        max_tokens=150,
        n=5,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip().lower()

# API route to update user profile
@app.route("/api/profile", methods=["POST"])
def update_profile():
    data = request.get_json()
    user_id = data.get("user_id")
    home_address = data.get("home_address")
    contact_info = data.get("contact_info")

    if user_id and home_address and contact_info:
        user_profiles[user_id] = {
            "home_address": home_address,
            "contact_info": contact_info
        }
        return jsonify({"message": "Profile updated successfully"})
    else:
        return jsonify({"error": "Invalid request"}), 400

# API route to get the likeliest disaster for a user
@app.route("/api/likeliest-disaster/<user_id>", methods=["GET"])
def get_user_likeliest_disaster(user_id):
    user_profile = user_profiles.get(user_id)
    print("This is the user_profile:", user_profile)
    if user_profile:
        state = user_profile["home_address"]["state"]
        city = user_profile["home_address"]["city"]
        street = user_profile["home_address"]["street"]
        likeliest_disaster = get_likeliest_disaster(state, city, street)
        return jsonify({"likeliest_disaster": likeliest_disaster})
    else:
        return jsonify({"error": "User profile not found"}), 404

# API route to get disaster preparedness information for a user
@app.route("/api/disaster-info/<user_id>", methods=["GET"])
def get_user_disaster_info(user_id):
    user_profile = user_profiles.get(user_id)

    if user_profile:
        state = user_profile["home_address"]["state"]
        city = user_profile["home_address"]["city"]
        street = user_profile["home_address"]["street"]
        likeliest_disaster = get_likeliest_disaster(state, city, street)

        evacuation_prompt_what_you_need = f"Write evacuation guidelines for {likeliest_disaster} in {city}, {state}, with a focus on What You Need:"
        evacuation_prompt_things_to_keep_in_mind = f"Write evacuation guidelines for {likeliest_disaster} in {city}, {state}, with a focus on Things To Keep In Mind:"
        shelter_prompt_what_you_need = f"Write shelter guidelines for {likeliest_disaster} in {city}, {state}, with a focus on What You Need:"
        shelter_prompt_things_to_keep_in_mind = f"Write shelter guidelines for {likeliest_disaster} in {city}, {state}, with a focus on Things To Keep In Mind:"
        first_aid_what_you_need = f"Write first aid guidelines for {likeliest_disaster} in {city}, {state}, with a focus on What You Need:"
        first_aid_things_to_keep_in_mind = f"Write first aid guidelines for {likeliest_disaster} in {city}, {state}, with a focus on Things To Keep In Mind:"

        evacuation_info_what_you_need = generate_content(evacuation_prompt_what_you_need)
        evacuation_info_things_to_keep_in_mind = generate_content(evacuation_prompt_things_to_keep_in_mind)
        shelter_info_what_you_need = generate_content(shelter_prompt_what_you_need)
        shelter_info_things_to_keep_in_mind = generate_content(shelter_prompt_things_to_keep_in_mind)
        first_aid_info_what_you_need = generate_content(first_aid_what_you_need)
        first_aid_info_things_to_keep_in_mind = generate_content(first_aid_things_to_keep_in_mind)

        return jsonify({
            "disaster": likeliest_disaster,
            "evacuation": {
                "what_you_need": evacuation_info_what_you_need.split("\n"),
                "things_to_keep_in_mind": evacuation_info_things_to_keep_in_mind.split("\n"),
                "additional_resources": f"https://www.ready.gov/evacuating-yourself-and-your-family"
            },
            "shelter": {
                "what_you_need": shelter_info_what_you_need.split("\n"),
                "things_to_keep_in_mind": shelter_info_things_to_keep_in_mind.split("\n"),
                "additional_resources": f"https://www.ready.gov/shelter"
            },
            "first_aid": {
                "what_you_need": first_aid_info_what_you_need.split("\n"),
                "things_to_keep_in_mind": first_aid_info_things_to_keep_in_mind.split("\n"),
                "additional_resources": f"https://www.redcross.org/get-help/how-to-prepare-for-emergencies/types-of-emergencies/{likeliest_disaster}.html"
            }
        })
    else:
        return jsonify({"error": "User profile not found"}), 404

# API route for the chat functionality
@app.route("/api/chat", methods=["POST"])
def handle_chat():
    data = request.get_json()
    user_input = data.get("user_input")

    if user_input:
        response = generate_content(user_input)
        return jsonify({"response": response.split("\n")})
    else:
        return jsonify({"error": "Invalid request"}), 400

if __name__ == "__main__":
   app.run(port=8000, debug=True)