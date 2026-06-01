from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

try:
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
except:
    tasks = []

def time_to_y(hour, minute):
    return (hour + minute / 60) * 100

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        hour = int(request.form["hour"])
        minute = int(request.form["minute"])

        end_hour = int(request.form["end_hour"])
        end_minute = int(request.form["end_minute"])

        color = request.form["color"]

        start = hour * 60 + minute
        end = end_hour * 60 + end_minute

        height = (end - start) * (100 / 60)

        print(name, hour, minute)

        print(time_to_y(hour, minute))

        tasks.append({
            "name": name,
            "y": time_to_y(hour, minute),
            "height": height,
            "color": color,
        
            "hour": hour,
            "minute": minute,

            "end_hour": end_hour,
            "end_minute": end_minute
        })
 
        with open("tasks.json", "w") as f:
            json.dump(tasks, f)

        return redirect("/")

    return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:index>")
def delete(index):
    if 0 <= index < len(tasks):
        tasks.pop(index)

        with open("tasks.json", "w") as f:
            json.dump(tasks, f)

    return redirect("/")


@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):

    if request.method == "POST":

        name = request.form["name"]

        hour = int(request.form["hour"])
        minute = int(request.form["minute"])

        end_hour = int(request.form["end_hour"])
        end_minute = int(request.form["end_minute"])

        color = request.form["color"]

        start = hour * 60 + minute
        end = end_hour * 60 + end_minute

        height = (end - start) * (100 / 60)

        tasks[index] = {
            "name": name,
            "y": time_to_y(hour, minute),
            "height": height,
            "color": color,

            "hour": hour,
            "minute": minute,

            "end_hour": end_hour,
            "end_minute": end_minute
        }

        with open("tasks.json", "w") as f:
            json.dump(tasks, f)

        return redirect("/")

    return render_template(
        "edit.html",
        task=tasks[index]
    )


if __name__ == "__main__":
    app.run(debug=True)
