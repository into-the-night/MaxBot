# MaxBot 🤖🏥

## Features ✨

- Chat with MaxBot regarding your health and symptoms.
- Get curated doctor recommendations based on your symptoms and location (NOTE: The dataset for doctors in MaxBot is NOT REAL and very limited. As this was made for a hackathon, I don't necessarily plan on expanding it either)

## Built With 🛠

- Gemini API for inference and chat
- Llama Index for document indexing
- FastAPI for API deployment
- FastAPI-sessions for session implementation

## How To Use 🚀

Use the deployed version on https://maxbot-9ays.onrender.com/ (NOTE: Since it is deployed on render's free tier, it can delay requests upto 50 seconds)

or Deploy locally:
- Clone the repo in a folder
  
  ```git clone https://github.com/into-the-night/MaxBot.git```
- Create a virtual environment (Recommended)

  ```py -m venv .venv```
- Activate the virtual environment

  ```.venv/Scripts/activate```
- Install requirements

  ```pip install -r requirements.txt```
- Important: Requires a Gemini API key (get yours at: https://aistudio.google.com/app/apikey) and make a ```.env``` file with the following inside:

  ```GOOGLE_API_KEY = *Your API key here*```
- Run using uvicorn

  ```uvicorn app:app --reload```
- Visit http://127.0.0.1:8000

## Author ✍

Made with ♥ by [Abhay Shukla](https://github.com/into-the-night)

## License 📜

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

