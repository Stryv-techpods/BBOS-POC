import logging
import psycopg2
import azure.functions as func
import os
import json

def main(req: func.HttpRequest, res: func.HttpResponse) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError as e:
        logging.error(f"JSON parsing error: {e}")
        return func.HttpResponse(
            "Invalid JSON input. Please provide valid JSON data.",
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

        res = func.HttpResponse(
            "Record added successfully.",
            status_code=200
        )
    except psycopg2.Error as db_error:
        logging.error(f"Database error: {db_error}")
        res = func.HttpResponse(
            "Failed to add record to the database.",
            status_code=500
        )
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        res = func.HttpResponse(
            "An unexpected error occurred.",
            status_code=500
        )
    finally:
        if conn:
            conn.close()

    return res
