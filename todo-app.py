from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

# Ścieżki do plików JSON przechowujących statusy i zadania
STATUS_FILE = "statuses.json"
TODO_FILE = "todo.json"

# Funkcja do wczytania danych z pliku
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return {}

# Funkcja do zapisu danych do pliku
def save_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file)

# Endpoint główny do renderowania strony
@app.route("/")
def index():
    services = [
        {"name": "BUS GCP", "statuses": ["COMMITTED", "DEV", "PLAB", "INT", "CERT", "PROD"]},
        {"name": "REST GTW Envoy", "statuses": ["COMMITTED", "DEV", "INT", "CERT", "PROD"]},
        {"name": "USG Envoy", "statuses": ["COMMITTED", "DEV", "INT", "CERT", "PROD"]},
        {"name": "SP Envoy", "statuses": ["COMMITTED", "DEV", "INT", "CERT", "PROD"]},
        {"name": "WSDL Proxy C3G", "statuses": ["COMMITTED", "DEV", "CERT", "PROD"]},
        {"name": "SCC Envoy", "statuses": ["COMMITTED", "DEV", "PLAB", "CERT", "PROD"]},
    ]
    statuses = load_data(STATUS_FILE)  # Wczytaj statusy z pliku
    todo_list = load_data(TODO_FILE)  # Wczytaj listę zadań z pliku
    return render_template("index_todo3.html", services=services, statuses=statuses, todo_list=todo_list)

# Endpoint do aktualizacji statusu
@app.route("/update/<service>/<status>")
def update_status(service, status):
    statuses = load_data(STATUS_FILE)  # Wczytaj istniejące statusy

    # Zmień status na przeciwny (toggle)
    if service not in statuses:
        statuses[service] = {}
    statuses[service][status] = not statuses[service].get(status, False)

    save_data(STATUS_FILE, statuses)  # Zapisz zmienione statusy do pliku
    return redirect(url_for("index"))  # Przekieruj z powrotem na stronę główną

# Endpoint do dodawania nowego zadania
@app.route("/add_task", methods=["POST"])
def add_task():
    todo_list = load_data(TODO_FILE)
    task = request.form.get("task")  # Pobierz treść nowego zadania z formularza
    if task:
        todo_list.append({"task": task, "done": False})
        save_data(TODO_FILE, todo_list)
    return redirect(url_for("index"))

# Endpoint do oznaczania zadania jako zrobione i usuwania go
@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    todo_list = load_data(TODO_FILE)
    if 0 <= task_id < len(todo_list):
        del todo_list[task_id]
        save_data(TODO_FILE, todo_list)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

