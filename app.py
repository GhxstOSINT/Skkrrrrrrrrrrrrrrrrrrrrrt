from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def etos():
    _h = [
        0x43, 0x54, 0x46, 0x7b, 0x62, 0x34, 0x6c, 0x34, 0x6e, 0x63, 
        0x33, 0x64, 0x5f, 0x71, 0x75, 0x30, 0x74, 0x33, 0x73, 0x5f, 
        0x6d, 0x34, 0x73, 0x74, 0x33, 0x72, 0x7d
    ]
    return ''.join(chr(b) for b in _h)

conn = sqlite3.connect(':memory:', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS aurors (username TEXT, password TEXT, clearance TEXT)")
cursor.execute("DELETE FROM aurors") 
cursor.execute("INSERT INTO aurors VALUES ('dawlish', 'Obliviate_Dragon_99!@#', 'Level_10')")
conn.commit()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Ministry of Magic - Secure Portal</title>
    <style>
        body { font-family: 'Courier New', monospace; background-color: #0d1117; color: #c9d1d9; display: flex; flex-direction: column; align-items: center; padding-top: 50px; }
        .terminal { background-color: #161b22; border: 1px solid #30363d; padding: 30px; border-radius: 6px; width: 450px; box-shadow: 0 4px 15px rgba(0,0,0,0.8); }
        input[type="text"], input[type="password"] { width: 90%; padding: 10px; margin: 10px 0; background: #0d1117; border: 1px solid #30363d; color: #58a6ff; font-family: monospace; }
        input[type="submit"] { background: #238636; color: white; padding: 10px 20px; border: none; cursor: pointer; font-weight: bold; width: 100%; margin-top: 10px;}
        input[type="submit"]:hover { background: #2ea043; }
        .error { color: #f85149; }
        .success { color: #3fb950; font-size: 1.2em; }
        .query-debug { color: #8b949e; font-size: 0.8em; margin-top: 20px; border-top: 1px dashed #30363d; padding-top: 10px; word-break: break-all; }
    </style>
</head>
<body>
    <div class="terminal">
        <h2 style="color: #58a6ff; text-align: center;">[ AUROR LOGIN ]</h2>

        <form method="POST">
            <label>Username (Wand ID):</label><br>
            <input type="text" name="username" required autocomplete="off"><br>
            <label>Password (Incantation):</label><br>
            <input type="password" name="password" required autocomplete="off"><br>
            <input type="submit" value="Authenticate">
        </form>

        {% if message %}
            <div style="margin-top: 20px; text-align: center;">
                {{ message|safe }}
            </div>
        {% endif %}

        {% if debug_query %}
            <div class="query-debug">
                <strong>[Goblin Debugger] Executed Query:</strong><br>
                {{ debug_query }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ""
    debug_query = ""

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        blacklist = ['--', '#']
        waf_triggered = False
        
        for item in blacklist:
            if item in username or item in password:
                waf_triggered = True
                break
                
        if waf_triggered:
            message = "<span class='error'>[!] WAF BLOCKED: Malicious payload detected.</span>"
        else:
            query = f"SELECT * FROM aurors WHERE username = '{username}' AND password = '{password}'"
            debug_query = query 

            try:
                cursor.execute(query)
                user = cursor.fetchone()

                if user:
                    message = f"<span class='success'>Access Granted.<br><br>Welcome, {user[0]}.<br><br><strong>{etos()}</strong></span>"
                else:
                    message = "<span class='error'>Access Denied. Invalid credentials.</span>"
            except Exception as e:
                message = f"<span class='error'>[Database Syntax Error]<br>{e}</span>"

    return render_template_string(HTML_TEMPLATE, message=message, debug_query=debug_query)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)