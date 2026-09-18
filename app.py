import os
import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advance Number Lookup</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
            background: #0f172a; 
            color: #f8fafc; 
            display: flex; 
            justify-content: center; 
            padding: 20px; 
        }
        .container { 
            max-width: 500px; 
            width: 100%; 
            background: #1e293b; 
            padding: 25px; 
            border-radius: 12px; 
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5); 
        }
        h2 { margin-top: 0; color: #38bdf8; }
        input { 
            width: 100%; 
            padding: 12px; 
            margin: 12px 0; 
            border-radius: 8px; 
            border: 1px solid #334155; 
            background: #0f172a; 
            color: #fff; 
            font-size: 16px;
            box-sizing: border-box; 
        }
        button { 
            width: 100%; 
            padding: 12px; 
            background: #0284c7; 
            color: #fff; 
            border: none; 
            border-radius: 8px; 
            font-weight: 600; 
            font-size: 16px;
            cursor: pointer; 
        }
        button:hover { background: #0369a1; }
        pre { 
            background: #020617; 
            padding: 15px; 
            border-radius: 8px; 
            overflow-x: auto; 
            white-space: pre-wrap; 
            font-size: 13px; 
            color: #4ade80; 
            border: 1px solid #1e293b;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Advance Number Lookup</h2>
        <form method="POST">
            <input type="text" name="num" placeholder="Phone number enter karein..." required>
            <button type="submit">Search Details</button>
        </form>
        {% if result %}
        <h3>Lookup Result:</h3>
        <pre>{{ result }}</pre>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        target_number = request.form.get("num", "").strip()
        if target_number:
            try:
                # Backend me anurix.py ko run karke number input pass karta hai
                process = subprocess.Popen(
                    ["python", "anurix.py"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate(input=f"{target_number}\n", timeout=30)
                output = stdout if stdout else stderr
            except Exception as e:
                output = f"Execution Error: {str(e)}"
    return render_template_string(HTML_TEMPLATE, result=output)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
  
