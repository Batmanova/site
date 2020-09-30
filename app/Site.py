from app import app

if __name__ == '__main__':
    app.debug = True  # enables auto reload during development
    app.run()
