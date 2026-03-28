import re
import json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

prices = re.findall(r"\d[\d\s]*,\d{2}", text)
products = re.findall(r"\d+\.\n(.+)", text)
total_match = re.search(r"ИТОГО:\n([\d\s]+,\d{2})", text)
total = total_match.group(1) if total_match else None
date_match = re.search(r"\d{2}\.\d{2}\.\d{4}", text)
date = date_match.group() if date_match else None
time_match = re.search(r"\d{2}:\d{2}:\d{2}", text)
time = time_match.group() if time_match else None
payment_match = re.search(r"Банковская карта", text)
payment = payment_match.group() if payment_match else None

data = {
    "products": products,
    "prices": prices,
    "total": total,
    "date": date,
    "time": time,
    "payment_method": payment
}

print(json.dumps(data, indent=4, ensure_ascii=False))