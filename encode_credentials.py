# encode_credentials.py

import base64

with open("credentials.json", "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

with open("encoded.txt", "w") as f:
    f.write(encoded)

print("✅ credentials.json を base64 に変換しました。encoded.txt を Render に貼り付けてください。")
