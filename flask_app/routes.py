from flask_app import app

@app.route("/")
def home():
    return "Flask работает! Ваш бот тоже!"

@app.route("/metrics")
def metrics():
    return "Метрики будут здесь."
