# sales-team-performance-analysis

Sales Team Performance Analysis is a project that automates generating insights for sales representatives, sales team & predicting future trends

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/ramshasuhail46/sales-team-performace-analysis.git
   ```

2. Open the project in Visual Studio Code.

## Running the Application

To run the application locally:

1. Create a python enviorment:
   ```
   python3 -m venv .venv 
   ```
2. Activate the enviorment:
   ```
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip3 install -r requirements.txt
   ```
4. Migrate the changes made for creating superuser (to access admin panel of django):
   ```
   python3 manage.py migrate
   ```
5. Create a superuser to access admin-panel on URL (http://127.0.0.1:8000/admin) by following command:
   ```
   python3 manage.py createsuperuser
   ```
6. Set API KEY in .env 

7. Run the project by following command:
   ```
   python3 manage.py runserver
   ```

8. Open a web browser and navigate to the URL provided in the terminal (usually http://127.0.0.1:8000).

## Usage

The project is built with Django REST Framework to create APIs for uploading and analyzing sales data. It stores the data in a SQLite database. For AI-powered insights, it uses the LangChain framework, which integrates with the ChatGroq AI model. This model analyzes sales data based on customizable prompts, providing performance insights for individual reps, teams, or trends over time. The backend supports data uploads in CSV or JSON formats, which are processed and stored for analysis.

Technology Stack:
    Python, 
    LangChain Framework, 
    ChatGroq model, 
    Django REST Framework

## APIs 

1. File Upload API

    **Endpoint**: POST /api/upload/  
    **Purpose**: Upload CSV or JSON files containing sales data.  
    **Request**:  
      file: The sales data file in CSV or JSON format.  
    **Response**:  
        Success: 200 OK with a message indicating the file was processed.  
        Error: 400 Bad Request for invalid data or file format.  

    Sample Request:  
    POST http://localhost:8000/api/upload/  

    ```
    curl -X POST -F "file=@/path/to/your/sales_performance_data.csv" http://127.0.0.1:8000/api/upload/
    ```
    Sample Response:  
    {  
        "message": "CSV file processed successfully"  
    }  

    

2. Sales Rep Performance API

    **Endpoint**: POST /api/rep_performance/  
    **Purpose**: Get detailed performance analysis for a specific sales representative.  
    **Request**:  
        rep_id: The ID of the sales representative.  
    **Response**:  
        Success: 200 OK with AI-generated performance insights.  
        Error: 404 Not Found if no data is found for the rep.  

    Sample Request:  
    POST http://localhost:8000/api/rep_performance/  
    ```  
    Headers:
    Content-Type: application/json

    Body (raw JSON):
    {
    "rep_id": "203"
    }

    ```
    Sample response:   
    {  
        "insights": "John Doe has generated 50 leads with $20,000 revenue. Suggest improving lead follow-up."  
    }  


3. Team Performance API

    **Endpoint**: GET /api/team_performance/  
    **Purpose**: Get an overall performance summary of the sales team.  
    **Response**:  
        Success: 200 OK with insights on total leads, tours, revenue, and more.  
        Error: 500 Internal Server Error for any processing errors.  

    Sample Request:  
    GET http://localhost:8000/api/team_performance/  

    Sample Response:  
    {  
        "insights": "John Doe has generated 50 leads with $20,000 revenue. Suggest improving lead follow-up."  
    }  



4. Performance Trends API  

    **Endpoint**: POST /api/performance_trends/  
    **Purpose**: Analyze sales performance trends over a specified time period.  
    **Request**:  
        time_period: Must be either "monthly" or "quarterly".  
    **Response**:  
        Success: 200 OK with sales trends and forecasts based on the chosen period.  
        Error: 400 Bad Request for invalid time periods.  
    
    Sample Request:  
    POST http://localhost:8000/api/performance_trends/  

    ```
    Headers:
    Content-Type: application/json

    Body (raw JSON):

    {
    "time_period": "monthly"
    }
    ```
    Sample Response:  
    {  
        "insights": "In the past three months, revenue increased by 10%, leads grew by 15%, and tours booked remained stable. A focus on converting leads to tours is recommended..."  
    }  


## Features

- Flexible Data Analysis: Supports multiple data types (csv, json) with custom prompt generation.  
- Conversation Memory: Uses ConversationSummaryBufferMemory to maintain chat context and summarize key points
- Sales Insight Generation: Offers actionable insights on sales performance (individual, team, or time period)

