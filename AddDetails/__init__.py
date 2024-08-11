import logging
import psycopg2
import json
import azure.functions as func
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Log the raw body for debugging
        raw_body = req.get_body().decode('utf-8')
        logging.info(f"Raw request body: {raw_body}")

        # Attempt to parse the JSON body
        req_body = json.loads(raw_body)  # Directly parse the raw body
        logging.info(f"Parsed request body: {req_body}")

    except ValueError as e:
        logging.error(f"JSON parsing error: {e}")
        return func.HttpResponse(
            "Invalid JSON input. Please provide valid JSON data.",
            status_code=400
        )

    if not isinstance(req_body, dict):
        logging.error("Request body is not a JSON object")
        return func.HttpResponse(
            "Invalid JSON format. Expected an object.",
            status_code=400
        )

    name = req_body.get('name')
    email = req_body.get('email')

    if not name or not email:
        return func.HttpResponse(
            "Name and email are required.",
            status_code=400
        )

    conn = None
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT')
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO details (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        cur.close()

        return func.HttpResponse(
            "Record added successfully.",
            status_code=200
        )
    except psycopg2.Error as db_error:
        logging.error(f"Database error: {db_error}")
        return func.HttpResponse(
            "Failed to add record to the database.",
            status_code=500
        )
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return func.HttpResponse(
            "An unexpected error occurred.",
            status_code=500
        )
    finally:
        if conn:
            conn.close()
