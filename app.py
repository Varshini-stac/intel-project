from flask import Flask, render_template, abort
import pandas as pd
import json
import os

app = Flask(__name__)
df = pd.read_csv("product_data.csv")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/product/<batch_id>")
def product(batch_id):
    record = df[df["batch_id"] == batch_id]
    if record.empty:
        abort(404)

    product_info = record.iloc[0].to_dict()
    product_info["traceability"] = json.loads(product_info["traceability"])

    return render_template("product.html", product=product_info, traceability=product_info["traceability"])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)
