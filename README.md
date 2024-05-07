# Disaster Preparedness Web App

This web app is designed to help users prepare for potential natural disasters based on their location. It provides personalized disaster preparedness information, including evacuation guidelines, shelter-in-place instructions, and first aid tips.

## Features

- User profile creation: Users can create a profile by providing their home address, contact information, and any special considerations.
- Likeliest disaster prediction: The app uses the OpenAI API to predict the likeliest natural disaster to occur in the user's location based on their state, city, and street.
- Disaster preparedness information: Users can access personalized disaster preparedness information for the predicted likeliest disaster. The information includes:
  - Evacuation guidelines: What to pack and things to keep in mind during an evacuation.
  - Shelter-in-place instructions: What to have on hand and things to consider when sheltering in place.
  - First aid tips: Essential supplies and important things to remember for administering first aid.
- Nearest safe spot: The app uses the Overpass API to find the nearest safe spot for evacuation based on the user's location and the predicted disaster.
- Chat functionality: Users can interact with the app using a chat interface powered by the OpenAI API to ask questions and get additional information.

## Technologies Used

- Frontend:
  - React: A JavaScript library for building user interfaces.
  - Axios: A promise-based HTTP client for making API requests.
- Backend:
  - Flask: A Python web framework for building the backend API.
  - OpenAI API: Used for generating personalized disaster preparedness content and powering the chat functionality.
  - Overpass API: Used for finding the nearest safe spot for evacuation.
- APIs:
  - OpenAI API: Provides natural language processing capabilities for content generation and chat functionality.
  - Overpass API: Allows querying geographical data to find nearby emergency shelters.

## Getting Started

To run the app locally, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/your-username/disaster-prep-app.git
   ```

2. Install the dependencies:
   ```
   cd disaster-prep-app
   pip install -r requirements.txt
   cd frontend/disaster-prep-frontend
   npm install
   ```

3. Set up the OpenAI API key:
   - Replace `"use_your_own_key"` in the `app.py` file with your actual OpenAI API key.

4. Start the backend server:
   ```
   cd ../..
   python app.py
   ```

5. Start the frontend development server:
   ```
   cd frontend/disaster-prep-frontend
   npm start
   ```

6. Open the app in your browser:
   - Navigate to `http://localhost:3000` to access the app.


## Acknowledgements

- [OpenAI](https://openai.com/) for providing the powerful language model API.
- [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API) for enabling geographical data querying.
- [React](https://reactjs.org/) for the frontend framework.
- [Flask](https://flask.palletsprojects.com/) for the backend framework.

