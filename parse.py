from json import load
from random import randint

m = {
    0: "true", 1: "false"
}
with open("points.json", "r") as file:
    f = load(file)["features"]
    for loc in f:
        prop = loc["properties"]
        name = prop.get("name", None)
        if not name:
            continue
        name = name.replace("'", "''")
        cat_name = prop.get("category", "unknown").upper()
        long, lat = loc["geometry"]["coordinates"]
        trufalse = ", ".join(m[randint(0, 1)] for i in range(11))
        print(f"""('{name}', '{cat_name}', {lat}, {long}, {trufalse}),""")

