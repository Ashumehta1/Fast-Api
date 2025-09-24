About FastAPI

FastAPI
is a modern, high-performance web framework for building APIs with Python 3.7+ based on standard Python


Key Features

    🚀 Fast: Very high performance, on par with NodeJS & Go (thanks to Starlette and Pydantic).
    📖 Automatic Docs: Built-in Swagger UI and ReDoc documentation.
    🛡 Validation: Automatic request & response validation with Pydantic.
    🔄 Async Ready: Fully supports async and await for concurrency.
    🐍 Pythonic: Uses type hints, making code cleaner, more reliable, and IDE-friendly.
    ✅ Easy Testing: Simple to write unit tests for APIs.


Rule of Thumb

    If you think of your data as rows in a table → use List of Dicts.
    If you think of your data as a dictionary of objects keyed by ID → use Dict of Dicts.
    In my case (API where user enters patient_id and gets details), the Dict of Dicts is more efficient and simpler to handle.

# Python script that converts a list of dicts → dict of dicts using patient_id as the key.
    patients_list = [
    {"patient_id": "P001", "name": "Amit Sharma", "age": 34, "gender": "Male"},
    {"patient_id": "P002", "name": "Neha Verma", "age": 28, "gender": "Female"},
    {"patient_id": "P003", "name": "Rohit Gupta", "age": 45, "gender": "Male"},
    {"patient_id": "P004", "name": "Priya Nair", "age": 37, "gender": "Female"},
    {"patient_id": "P005", "name": "Arjun Mehta", "age": 52, "gender": "Male"}
    ]

    # Convert list of dicts to dict of dicts
    patients_dict = {p["patient_id"]: {k: v for k, v in p.items() if k != "patient_id"} for p in patients_list}
    print(patients_dict)

    output:-
    {
    "P001": {"name": "Amit Sharma", "age": 34, "gender": "Male"},
    "P002": {"name": "Neha Verma", "age": 28, "gender": "Female"},
    "P003": {"name": "Rohit Gupta", "age": 45, "gender": "Male"},
    "P004": {"name": "Priya Nair", "age": 37, "gender": "Female"},
    "P005": {"name": "Arjun Mehta", "age": 52, "gender": "Male"}
    }

    Save as JSON File
        import json
        with open("patients_dict.json", "w") as f:
            json.dump(patients_dict, f, indent=2)

    Now it can directly use patients_dict.json in your FastAPI app
