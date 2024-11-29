from app.website import create_app

app = create_app()

# you only want to run this server IF you actually run this file directly
if __name__ == '__main__':
    # every time we can a change to our python code, it will rerun the web server
    # turn debug to false when running server
    app.run(debug=True)
    