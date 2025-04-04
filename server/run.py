from app.main import create_app # Import the function that creates your app

app = create_app() # Actually create the app using that function

if __name__ == '__main__': # Run this only if file is executed directly
    app.run(debug=True) # Start Flask in debug mode (auto-reload + error messages)
