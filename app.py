# app.py
from flask import Flask, render_template, request, jsonify
import random
import math
import uuid

# 🛑 FIX: Explicitly set both template_folder and static_folder.
# - template_folder='backend/templates' to find your HTML files.
# - static_folder='static' to find your CSS/JS files (relative to app.py).
app = Flask(__name__, template_folder='backend/templates', static_folder='static')

# Simple plan generation algorithm:
# - We represent the whole area as a rectangle (width x height with area ~ user_area)
# - We recursively split the rectangle into rooms until required rooms are created
# - Different random split strategies create plan variations
# - Output: list of rooms with positions/width/height and type

def create_base_dimensions(area, target_ratio=1.5):
    """
    Create a base width/height for the floor rectangle from area.
    target_ratio lets us make a rectangular space; adjust for variation.
    """
    height = math.sqrt(area / target_ratio)
    width = area / height
    return int(width), int(height)

def subdivide(rect, room_count, room_types, rng):
    """
    rect: (x, y, w, h)
    room_count: how many rooms left to create
    room_types: types to choose from
    rng: random.Random instance for reproducibility
    Returns list of rooms: dicts with x,y,w,h,type
    """
    rooms = []

    def split_and_create(x, y, w, h, target):
        # base case
        if target == 1:
            rtype = room_types.pop(0) if room_types else rng.choice(
                ["room", "hall", "kitchen"])
            rooms.append({"x": x, "y": y, "w": w, "h": h, "type": rtype})
            return

        # split either horizontally or vertically
        if w > h:
            # vertical split
            split = int(w * (0.3 + rng.random() * 0.4))
            split = max(1, min(w - 1, split))
            left_target = max(1, target // 2)
            right_target = target - left_target
            split_and_create(x, y, split, h, left_target)
            split_and_create(x + split, y, w - split, h, right_target)
        else:
            # horizontal
            split = int(h * (0.3 + rng.random() * 0.4))
            split = max(1, min(h - 1, split))
            top_target = max(1, target // 2)
            bottom_target = target - top_target
            split_and_create(x, y, w, split, top_target)
            split_and_create(x, y + split, w, h - split, bottom_target)

    x, y, w, h = rect
    split_and_create(x, y, w, h, room_count)
    return rooms

def generate_plans(area, rooms_requested, variants=4, seed=None):
    plans = []
    width, height = create_base_dimensions(area, target_ratio=1.5)
    for i in range(variants):
        rng = random.Random((seed or 0) + i)
        # copy list and allow some random ordering of room types
        types_list = list(rooms_requested)
        rng.shuffle(types_list)
        room_count = max(1, len(types_list))
        rooms = subdivide((0, 0, width, height), room_count, types_list[:], rng)
        # Add metadata
        plans.append({
            "id": str(uuid.uuid4())[:8],
            "width": width,
            "height": height,
            "rooms": rooms
        })
    return plans

@app.route("/")
def index():
    # This is the root code you requested. It simply renders the index.html file.
    return render_template("index.html")

@app.route("/floor_select")
def floor_select():
    return render_template("floor_select.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    # expected: { area: number, rooms: ["hall","kitchen",...], variants: 4 }
    area = float(data.get("area", 500))
    rooms = data.get("rooms", ["hall", "kitchen", "bedroom"])
    variants = int(data.get("variants", 4))
    seed = int(data.get("seed", 0))
    plans = generate_plans(area, rooms, variants=variants, seed=seed)
    return jsonify({"plans": plans})

@app.route("/customize/<plan_id>")
def customize(plan_id):
    # In a full app you'd fetch plan by id; for this simple prototype client holds plans.
    return render_template("customize.html", plan_id=plan_id)

# static files served automatically; run app
if __name__ == "_main_":
    app.run(debug=True)