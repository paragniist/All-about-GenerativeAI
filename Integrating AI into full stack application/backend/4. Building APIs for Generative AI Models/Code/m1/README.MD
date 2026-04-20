# Prerequisites

For creating an API using FastAPI, you need:

1. **Python 3.7+**: Ensure you have Python 3.7 or later installed on your system.
   - You can download Python from [python.org](https://www.python.org/downloads/).

2. **Package Manager (pip)**: Ensure you have `pip` installed to manage Python packages.
   - `pip` is included with Python installations from python.org.

3. **FastAPI**: Install the FastAPI framework.
   ```sh
   pip install fastapi
   ```

4. **ASGI Server (Uvicorn)**: Install an ASGI server to run your FastAPI application.
   ```sh
   pip install uvicorn
   ```

5. **Text Editor or IDE**: Use a text editor or IDE for writing your code. Popular choices include:
   - Visual Studio Code
   - PyCharm
   - Sublime Text

6. **Basic Knowledge of Python**: Familiarity with Python programming, including functions, classes, and type hints.

### Optional Tools

1. **Virtual Environment**: Use a virtual environment to manage dependencies.
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

2. **HTTP Client**: Use an HTTP client for testing your API endpoints.
   - Tools like `curl`, Postman, or HTTPie can be useful. You can also test from the browser with Swagger.

3. **Version Control (Git)**: Use Git for version control and GitHub for repository hosting.

These prerequisites will help you set up and create a FastAPI application efficiently.