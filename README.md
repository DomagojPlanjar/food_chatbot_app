# Food Chatbot App

A comprehensive food delivery chatbot application that integrates a FastAPI backend, a Dialogflow chatbot, a MySQL database, and a web frontend.

## Project Structure

- **`backend/`**: Contains the FastAPI backend code for handling API requests and interacting with the database.
- **`chatbot/`**: Contains Dialogflow chatbot configuration files.
- **`frontend/`**: Includes HTML, CSS, and JavaScript files for the web interface.
- **`database/`**: MySQL database schema and structure files.

## Getting Started

### Prerequisites

- Python 3.8+
- Dialogflow account
- [ngrok](https://ngrok.com/) (for HTTPS tunneling)
- MySQL 8.0+, MySQL server, MySQL Workbench

### Setup

1. **Clone the Repository**

   ```sh
   git clone https://github.com/DomagojPlanjar/food_chatbot_app.git
   cd food_chatbot_app
   ```
2. **Set Up a Virtual Environment**

Create and activate virtual environment:

  ```sh
  python -m venv .venv

  # On Windows
  .venv\Scripts\activate

  # On macOS/Linux
  source .venv/bin/activate
  ```
3. **Install dependencies**

Install the required Python packages:
  ```sh
  pip install -r backend/requirements.txt
  ```

4. **Configure the Database**

Firstly, you need to create a connection to your server in MySQL Workbench.
Then, create a new MySQL database called food_delivery:
  ```sql
  CREATE DATABASE food_delivery;
  ```
Then go to File/Open SQL Script and open the .sql file provided in database folder and 
execute the script. Now you should be ready to go. Make sure you update code as instructed
in backend/utils/db_helper.py file when connecting to your database.

5. **Start the Backend Server**

Navigate to 'backend' directory and start the FastAPI server:
  ```sh
  uvicorn main:app --reload
  ```
Make sure you downloaded and installed ngrok as instructed on official website. 
Place ngrok.exe in your backend folder and run this command in new terminal:
  ```sh
  ngrok http 8000
  ```
6. **Set up the Chatbot**
Log in to Dialogflow Console then go to Dialogflow ES and create a new agent. Now go to
agent settings and open Export and Import tab. Click on Restore from ZIP and upload zipped
'converso-chatbot' folder. Dialogflow will process the file and import the configurations
into your agent.
Now go to Fulfillment section and set Webhook URL to the HTTPS URL provided by ngrok (you can
find it in terminal where you ran 'ngrok http 8000' command).
You can test your chatbot in test console on the right side. 
 

## Usage
Open the frontend HTML file index.html in your web browser. 













