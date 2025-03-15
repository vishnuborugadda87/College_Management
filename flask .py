from flask import Flask, request, redirect, url_for, render_template_string, session, render_template
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def read_users_from_csv(filepath):
    users = {}
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            users[row['username'].strip()] = {
                'password': row['password'].strip(),
                'role': row['role'].strip(),
                'cabin': row['cabin'].strip(),
                'classes': [cls.strip() for cls in row['classes'].split(',')]
            }
    return users


def write_users_to_csv(filepath, users):
    fieldnames = ['username', 'password', 'role', 'cabin', 'classes']
    with open(filepath, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for username, details in users.items():
            writer.writerow({
                'username': username,
                'password': details['password'],
                'role': details['role'],
                'cabin': details['cabin'],
                'classes': ', '.join(details['classes'])
            })


@app.route('/')
def login():
    return render_template('login.html', error=None)


@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['uname']
    password = request.form['pass']
    if username in users and users[username]['password'] == password:
        session['username'] = username
        role = users[username]['role']
        if role == 'faculty':
            return redirect(url_for('homeF', email=username))
        elif role == 'student':
            return redirect(url_for('homeS', email=username))
        else:
            return "Invalid role", 403
    else:
        return render_template('login.html', error='Invalid credentials')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/homeF')
def homeF():
    email = session.get('username', '')
    user = users.get(email, {})
    cabin = user.get('cabin', 'Unknown')
    classes = user.get('classes', [])
    return render_template_string('''
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Faculty Portal - Mallareddy Engineering College</title>
  <style>

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Arial', sans-serif;
    }

    body, html {
      height: 100%;
      background: linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%);
      color: #333;
    }

   
    #header {
      background-color: rgba(1, 10, 53, 0.9);
      width: 100%;
      padding: 15px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: relative;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }

   
    #logoSlot {
      background-color: white;
      border-radius: 50%;
      padding: 8px;
      width: 80px;
      height: 80px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }

    #logoSlot img {
      width: 100%;
      height: auto;
    }


    .title-container {
      text-align: center;
      color: white;
      flex-grow: 1;
      margin-left: 20px;
    }

    .title-container h1 {
      font-size: 2rem;
      margin-bottom: 5px;
      font-weight: 600;
    }

    .title-container h2 {
      font-size: 1.2rem;
      font-weight: 400;
      color: #e0e0e0;
    }


    .button-container {
      display: flex;
      gap: 10px;
    }

    .button-container a button {
      background-color: #007BFF;
      color: white;
      border: none;
      padding: 10px 15px;
      border-radius: 5px;
      font-size: 1rem;
      cursor: pointer;
      transition: background-color 0.3s ease, transform 0.2s;
    }

    .button-container a button:hover {
      background-color: #0056b3;
      transform: translateY(-2px);
    }

  
    .content {
      padding: 30px;
      max-width: 1000px;
      margin: 40px auto;
      background-color: rgba(255, 255, 255, 0.95);
      border-radius: 15px;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    }

    .content p {
      margin-bottom: 15px;
      font-size: 1.2rem;
      line-height: 1.5;
    }

    .content strong {
      color: #007BFF;
    }

    .content ul {
      list-style-type: disc;
      padding-left: 20px;
    }

    .content ul li {
      margin-bottom: 10px;
      font-size: 1.1rem;
    }

  
    footer {
      text-align: center;
      padding: 20px;
      background-color: rgba(1, 10, 53, 0.8);
      color: white;
      font-size: 0.9rem;
    }

  </style>
</head>
<body>


  <header id="header">
    <div id="logoSlot">

            <img src="data:image/jpeg;base64,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" alt="Logo">

    </div>
    <div class="title-container">
      <h1>MALLAREDDY ENGINEERING COLLEGE</h1>
      <h2>Main Campus, Autonomous Institution</h2>
    </div>
    <div class="button-container">
      <a href="{{ url_for('edit_faculty', email=email) }}">
        <button>Edit</button>
      </a>
      <a href="{{ url_for('logout') }}">
        <button>Logout</button>
      </a>
    </div>
  </header>


  <div class="content">
    <p><strong>Name:</strong> {{ email }}</p>
    <p><strong>ID:</strong> {{ email }}</p>
    <p><strong>Cabin:</strong> {{ cabin }}</p>
    <p><strong>Classes:</strong></p>
    <ul>
      {% for cls in classes %}
        <li>{{ cls }}</li>
      {% endfor %}
    </ul>
  </div>
</body>
</html>
    ''', email=email, cabin=cabin, classes=classes)


@app.route('/edit_faculty')
def edit_faculty():
    email = session.get('username', '')
    user = users.get(email, {})
    return render_template_string('''
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Edit Faculty Info</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Arial', sans-serif;
    }

    html, body {
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      background: linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%);
    }

    form {
      display: flex;
      flex-direction: column;
      background-color: rgba(255, 255, 255, 0.95);
      border: 1px solid #ddd;
      border-radius: 15px;
      padding: 40px;
      max-width: 450px;
      width: 100%;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
      text-align: center;
      transition: transform 0.3s ease;
    }

    form:hover {
      transform: translateY(-5px);
    }

    img {
      width: 100px;
      height: auto;
      margin-bottom: 20px;
      border-radius: 50%;
    }

    h2 {
      margin-bottom: 20px;
      font-size: 1.8rem;
      color: #333;
      font-weight: 600;
    }

    label {
      font-size: 14px;
      margin-top: 15px;
      text-align: left;
      font-weight: bold;
      color: #555;
    }

    input[type="text"] {
      border: 1px solid #ccc;
      border-radius: 5px;
      padding: 12px;
      font-size: 1rem;
      width: 100%;
      margin-top: 8px;
      transition: all 0.3s ease;
    }

    input[type="text"]:focus {
      border-color: #007BFF;
      outline: none;
      box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
    }

    input[type="submit"] {
      background-color: #007BFF;
      color: white;
      border: none;
      padding: 14px;
      font-size: 1rem;
      border-radius: 5px;
      margin-top: 30px;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }

    input[type="submit"]:hover {
      background-color: #0056b3;
    }

    .input-container {
      text-align: left;
      margin-bottom: 10px;
    }

    .input-container:last-child {
      margin-bottom: 0;
    }
  </style>
</head>
<body>
  <form action="{{ url_for('save_faculty') }}" method="post">
    <input type="hidden" name="username" value="{{ email }}">
                <img src="data:image/jpeg;base64,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" alt="Logo">

    <h2>Edit Faculty Information</h2>

    <div class="input-container">
      <label for="cabin">Cabin</label>
      <input type="text" id="cabin" name="cabin" value="{{ user.cabin }}">
    </div>

    <div class="input-container">
      <label for="classes">Classes</label>
      <input type="text" id="classes" name="classes" value="{{ ', '.join(user.classes) }}">
    </div>

    <input type="submit" value="Save">
  </form>
</body>
</html>
    ''', email=email, user=user)


@app.route('/save_faculty', methods=['POST'])
def save_faculty():
    username = request.form['username']
    cabin = request.form['cabin']
    classes = [cls.strip() for cls in request.form['classes'].split(',')]
    if username in users:
        users[username]['cabin'] = cabin
        users[username]['classes'] = classes
        write_users_to_csv('users.csv', users)
        return redirect(url_for('homeF', email=username))
    else:
        return "User not found", 404


@app.route('/homeS')
def homeS():
    email = session.get('username', '')
    user = users.get(email, {})
    student_classes = set(user.get('classes', []))
    faculty_info = []
    for uname, info in users.items():
        if info['role'] == 'faculty':
            faculty_classes = set(info['classes'])
            if student_classes & faculty_classes:
                faculty_info.append({"name": uname, "cabin": info["cabin"]})
    return render_template_string('''
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Faculty Information - Mallareddy Engineering College</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Arial', sans-serif;
    }

    body {
      height: 100%;
      background: linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%);
      color: #333;
    }

    #header {
      background-color: rgba(1, 10, 53, 0.9);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 20px;
      color: white;
    }

    #logoSlot {
      background-color: white;
      border-radius: 50%;
      width: 80px;
      height: 80px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    #logoSlot img {
      width: 100%;
      height: auto;
      border-radius: 50%;
    }

    .title-container {
      text-align: center;
      flex-grow: 1;
    }

    .title-container h1 {
      font-size: 2rem;
      margin-bottom: 5px;
      font-weight: bold;
      color: #f0f0f0;
    }

    .title-container h2 {
      font-size: 1.3rem;
      font-weight: 400;
      color: #c0c0c0;
    }

    .logout-btn {
      background-color: #007BFF;
      color: white;
      border: none;
      padding: 12px 20px;
      border-radius: 5px;
      font-size: 1rem;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }

    .logout-btn:hover {
      background-color: #0056b3;
    }

    .info-container {
      padding: 30px;
      max-width: 1000px;
      margin: 40px auto;
      background-color: rgba(255, 255, 255, 0.9);
      box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
      border-radius: 10px;
      text-align: left;
    }

    .info-container p {
      font-size: 1.2rem;
      margin-bottom: 15px;
      line-height: 1.5;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }

    th, td {
      border: 1px solid #ddd;
      padding: 15px;
      text-align: left;
      font-size: 1rem;
    }

    th {
      background-color: #f2f2f2;
      font-weight: bold;
    }

    td {
      background-color: white;
    }

    tr:hover td {
      background-color: #f9f9f9;
    }

    @media (max-width: 768px) {
      #header, .info-container {
        flex-direction: column;
        text-align: center;
      }

      .logout-btn {
        margin-top: 20px;
      }
    }
  </style>
</head>
<body>

  <header id="header">
    <div id="logoSlot">
            <img src="data:image/jpeg;base64,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" alt="Logo">
    </div>
    <div class="title-container">
      <h1>MALLAREDDY ENGINEERING COLLEGE</h1>
      <h2>Main Campus, Autonomous Institution</h2>
    </div>
    <a href="{{ url_for('logout') }}">
      <button class="logout-btn">Logout</button>
    </a>
  </header>

  <div class="info-container">
    <p><strong>Name:</strong> {{ email }}</p>
    <p><strong>Roll No:</strong> {{ email }}</p>

    <table>
      <tr>
        <th>Faculty Name</th>
        <th>Cabin</th>
      </tr>
      {% for faculty in faculty_info %}
      <tr>
        <td>{{ faculty.name }}</td>
        <td>{{ faculty.cabin }}</td>
      </tr>
      {% endfor %}
    </table>
  </div>

</body>
</html>
    ''', email=email, user=user, faculty_info=faculty_info)


users = read_users_from_csv(r'C:\Users\vishn\OneDrive\Desktop\RTRP\user.csv')

if __name__ == '__main__':
    app.run(debug=True)
