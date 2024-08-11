import logging
import psycopg2
import azure.functions as func
import os
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request. test')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid input",
            status_code=400
        )

    name = req_body.get('name')
    email = req_body.get('email')

    if not name or not email:
        return func.HttpResponse(
            "Name and email are required",
            status_code=400
        )

    conn = None
    try:
        conn = psycopg2.connect(
            dbname="POSTGRES_DB",
            user="vishnu-madle",
            password="vishnu@123",
            host="POSTGRES_HOST",
            port="POSTGRES_PORT"
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO details (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        cur.close()
        return func.HttpResponse(
            "Record added successfully",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(
            "Failed to add record",
            status_code=500
        )
    finally:
        if conn:
            conn.close()
