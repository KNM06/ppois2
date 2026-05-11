import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from core.VacuumCleaner import VacuumCleaner
from core.Room import Room
from core.exceptions import VacuumException

app = Flask(__name__)
app.secret_key = "lab4_secret_key"

def load_rooms(filename: str = "rooms_state.json") -> list[Room]:
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Room.from_dict(r) for r in data]
        except (json.JSONDecodeError, IOError):
            pass
    return [Room("Гостиная", 40), Room("Спальня", 15), Room("Кухня", 150)]

def save_rooms(rooms: list[Room], filename: str = "rooms_state.json") -> None:
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in rooms], f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Ошибка при сохранении комнат: {e}")

vacuum = VacuumCleaner.load_state()
rooms = load_rooms()

@app.route("/")
def index():
    return render_template("index.html", vacuum=vacuum, rooms=rooms)

@app.route("/power", methods=["POST"])
def toggle_power():
    try:
        vacuum.power_button.press()
        vacuum.save_state()
    except VacuumException as e:
        flash(str(e), "error")
    return redirect(url_for("index"))

@app.route("/mode", methods=["POST"])
def change_mode():
    try:
        level = int(request.form.get("level", 1))
        vacuum.mode_button.press(level)
        vacuum.save_state()
    except (ValueError, VacuumException) as e:
        flash(str(e), "error")
    return redirect(url_for("index"))

@app.route("/clean", methods=["POST"])
def clean():
    try:
        room_idx = int(request.form.get("room_idx"))
        if 0 <= room_idx < len(rooms):
            target_room = rooms[room_idx]
            collected = vacuum.clean_room(target_room)
            for r in rooms:
                r.accumulate_dust()
            
            vacuum.save_state()
            save_rooms(rooms)
            if collected > 0:
                flash(f"Уборка в '{target_room.name}' завершена. Собрано {collected} ед. пыли.", "success")
            else:
                flash(f"В '{target_room.name}' уже чисто.", "success")
    except (VacuumException, ValueError) as e:
        flash(str(e), "error")
    return redirect(url_for("index"))


@app.route("/attachment/change", methods=["POST"])
def change_attachment():
    try:
        idx = int(request.form.get("attachment_idx"))
        vacuum.change_attachment(idx)
        vacuum.save_state()
    except (ValueError, VacuumException) as e:
        flash(str(e), "error")
    return redirect(url_for("index"))

@app.route("/attachment/add", methods=["POST"])
def add_attachment():
    name = request.form.get("name")
    if name and name.strip():
        vacuum.add_attachment(name.strip())
        vacuum.save_state()
        flash(f"Насадка '{name}' добавлена.", "success")
    else:
        flash("Название насадки не может быть пустым.", "error")
    return redirect(url_for("index"))

@app.route("/attachment/delete/<int:idx>", methods=["POST"])
def delete_attachment(idx):
    try:
        vacuum.remove_attachment(idx)
        vacuum.save_state()
        flash("Насадка удалена.", "success")
    except (VacuumException, ValueError) as e:
        flash(str(e), "error")
    return redirect(url_for("index"))


@app.route("/room/add", methods=["POST"])
def add_room():
    name = request.form.get("name")
    try:
        dust = int(request.form.get("dust", 0))
        if name:
            rooms.append(Room(name, dust))
            save_rooms(rooms)
            flash(f"Комната '{name}' добавлена.", "success")
    except ValueError:
        flash("Некорректное значение пыли.", "error")
    return redirect(url_for("index"))

@app.route("/room/delete/<int:idx>", methods=["POST"])
def delete_room(idx):
    if 0 <= idx < len(rooms):
        removed = rooms.pop(idx)
        save_rooms(rooms)
        flash(f"Комната '{removed.name}' удалена.", "success")
    return redirect(url_for("index"))


@app.route("/maintenance/full", methods=["POST"])
def full_maintenance():
    vacuum.maintenance()
    vacuum.save_state()
    flash("Полное техническое обслуживание выполнено (контейнер очищен, фильтр заменен, мотор выключен).", "success")
    return redirect(url_for("index"))

@app.route("/maintenance/empty", methods=["POST"])
def empty_container():
    vacuum.empty_container()
    vacuum.save_state()
    flash("Контейнер очищен.", "success")
    return redirect(url_for("index"))

@app.route("/maintenance/filter", methods=["POST"])
def replace_filter():
    vacuum.replace_filter()
    vacuum.save_state()
    flash("Фильтр заменен.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)