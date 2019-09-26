from flaskblog import create_app # import from __init__.py

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
