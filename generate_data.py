import pandas as pd
import uuid
import random
from datetime import datetime, timedelta
import qrcode
import os
import json

qr_folder = "qrcodes"
os.makedirs(qr_folder, exist_ok=True)

products = ["PRODUCT A", "PRODUCT B", "PRODUCT C", "PRODUCT D"]

TRACE_CHECKPOINTS = [
    ("Raw Materials", "Warehouse Inbound"),
    ("Pre-Assembly Check", "Inspection Zone"),
    ("Assembly Line", "Line 1 / 2 / 3"),
    ("Soldering", "Solder Station 1 / 2"),
    ("Quality Control", "QC Area 1 / 2 / 3"),
    ("Packaging", "Final Pack Area"),
    ("Distribution", "Outbound Dock"),
    ("End User", "Customer Delivery")
]

def generate_traceability(start_time):
    trace_list = []
    curr_time = start_time
    for step_name, location_hint in TRACE_CHECKPOINTS:
        location = random.choice(location_hint.split(" / ")) if "/" in location_hint else location_hint
        curr_time += timedelta(hours=random.randint(1, 5))
        trace_list.append({
            "step": step_name,
            "location": location,
            "timestamp": curr_time.strftime("%Y-%m-%d %H:%M")
        })
    return trace_list

def generate_batches(per_product=3):
    all_data = []
    for product in products:
        for _ in range(per_product):
            batch_id = str(uuid.uuid4())[:8]
            manufacturer = random.choice(["Factory A", "Factory B", "Factory C"])
            prod_date = datetime.now() - timedelta(days=random.randint(1, 60))
            exp_date = prod_date + timedelta(days=365)
            trace_path = generate_traceability(prod_date)
            trace_str = json.dumps(trace_path)

            all_data.append({
                "product_name": product,
                "batch_id": batch_id,
                "manufacturer": manufacturer,
                "prod_date": prod_date.strftime("%Y-%m-%d"),
                "exp_date": exp_date.strftime("%Y-%m-%d"),
                "traceability": trace_str
            })

    return pd.DataFrame(all_data)

def main():
    df = generate_batches(per_product=3)
    df.to_csv("product_data.csv", index=False)
    public_url = "https://qr-product-trace.onrender.com" 

    for _, row in df.iterrows():
        qr_url = f"{public_url}/product/{row['batch_id']}"
        img = qrcode.make(qr_url)
        img.save(os.path.join(qr_folder, f"{row['batch_id']}.png"))
    print("Data and QR codes generated.")

if __name__ == "__main__":
    main()
