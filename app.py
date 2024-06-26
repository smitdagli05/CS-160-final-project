import os
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
from flask_cors import CORS
import requests

app = Flask(__name__, static_folder='frontend/disaster-prep-frontend/build', static_url_path='')
CORS(app)

client = OpenAI(api_key="use_your_own_key")

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
        max_tokens=500,
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
        max_tokens=500,
        n=5,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip().lower()

# Function to find the nearest safe spot using the Overpass API
def find_nearest_safe_spot(lat, lon, disaster):
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    node["emergency"="shelter"]["disaster"~"{disaster}"](around:5000,{lat},{lon});
    out;
    """
    response = requests.get(overpass_url, params={"data": query})
    data = response.json()

    if len(data["elements"]) > 0:
        safe_spot = data["elements"][0]
        safe_spot_lat = safe_spot["lat"]
        safe_spot_lon = safe_spot["lon"]
        safe_spot_name = safe_spot.get("tags", {}).get("name", "Unnamed Shelter")
        return safe_spot_lat, safe_spot_lon, safe_spot_name
    else:
        return None, None, None

# API route to update user profile
@app.route("/api/profile", methods=["POST"])
def update_profile():
    data = request.get_json()
    user_id = data.get("user_id")
    home_address = data.get("home_address")
    contact_info = data.get("contact_info")
    considerations = data.get("considerations")

    if user_id and home_address and contact_info:
        user_profiles[user_id] = {
            "home_address": home_address,
            "contact_info": contact_info,
            "considerations": considerations
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
        considerations = user_profile["considerations"]
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
        considerations = user_profile["considerations"]
        likeliest_disaster = get_likeliest_disaster(state, city, street)

        evacuation_prompt_what_you_need = f"Write evacuation guidelines for {likeliest_disaster} in {city}, {state}, with a focus on What You Need. {considerations}"
        evacuation_prompt_things_to_keep_in_mind = f"Write evacuation guidelines for {likeliest_disaster} in {city}, {state}, with a focus on Things To Keep In Mind. {considerations}"
        shelter_prompt_what_you_need = f"Write shelter guidelines for {likeliest_disaster} in {city}, {state}, with a focus on What You Need. {considerations}"
        shelter_prompt_things_to_keep_in_mind = f"Write shelter guidelines for {likeliest_disaster} in {city}, {state}, with a focus on Things To Keep In Mind. {considerations}"
        first_aid_what_you_need = f"Write first aid guidelines for {likeliest_disaster} in {city}, {state}, with a focus on What You Need. {considerations}"
        first_aid_things_to_keep_in_mind = f"Write first aid guidelines for {likeliest_disaster} in {city}, {state}, with a focus on Things To Keep In Mind. {considerations}"

        evacuation_info_what_you_need = generate_content(evacuation_prompt_what_you_need)
        evacuation_info_things_to_keep_in_mind = generate_content(evacuation_prompt_things_to_keep_in_mind)
        shelter_info_what_you_need = generate_content(shelter_prompt_what_you_need)
        shelter_info_things_to_keep_in_mind = generate_content(shelter_prompt_things_to_keep_in_mind)
        first_aid_info_what_you_need = generate_content(first_aid_what_you_need)
        first_aid_info_things_to_keep_in_mind = generate_content(first_aid_things_to_keep_in_mind)

        # Find the nearest safe spot for evacuation
        user_lat = user_profile["home_address"].get("latitude")
        user_lon = user_profile["home_address"].get("longitude")
        safe_spot_lat, safe_spot_lon, safe_spot_name = find_nearest_safe_spot(user_lat, user_lon, likeliest_disaster)

        if safe_spot_lat and safe_spot_lon:
            evacuation_info_additional_resources = f"{safe_spot_lat},{safe_spot_lon}"
        else:
            evacuation_info_additional_resources = "No nearby safe spot found. Please check with local authorities for evacuation instructions."

        return jsonify({
            "disaster": likeliest_disaster,
            "evacuation": {
                "what_you_need": evacuation_info_what_you_need.split("\n"),
                "things_to_keep_in_mind": evacuation_info_things_to_keep_in_mind.split("\n"),
                "additional_resources": evacuation_info_additional_resources
            },
            "shelter": {
                "what_you_need": shelter_info_what_you_need.split("\n"),
                "things_to_keep_in_mind": shelter_info_things_to_keep_in_mind.split("\n"),
                "additional_resources": f"https://www.ready.gov/shelter"
            },
            "first aid": {
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

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(port=3000, debug=True)