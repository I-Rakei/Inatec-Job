from flask import Flask, render_template, request, redirect, url_for, session, flash
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
  
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'ismael'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_SSL_CIPHER'] = 'TLS_AES_256_GCM_SHA384'
app.config['MYSQL_DATABASE_AUTH_PLUGIN'] = 'caching_sha2_password'

mysql = MySQL(app)

# Create MySQL table
with app.app_context():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            turma VARCHAR(255) NOT NULL,
            year INT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loggedin')
def home():
    return render_template('user/user.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        turma = request.form['turma']
        year = int(request.form['year'])

        # Insert user data into the MySQL database
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password, turma, year) VALUES (%s, %s, %s, %s)', (username, password, turma, year))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        # Check if the user exists in the MySQL database
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password_candidate):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/cursos')
def cursos():
    return render_template('cursos.html')

@app.route('/user/cursos')
def cursosUser():
    return render_template('user/cursos.html')

@app.route('/user/horario', methods=['GET', 'POST'])
def horario():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM horario_semana')
    horarios = cursor.fetchall() 
    conn.close()
    print(horarios)   
    return render_template('user/horarios.html', horarios=horarios) 


if __name__ == '__main__':
    app.run(debug=True)

def create_horarios():
    conn = mysql.connect()
    curosr=conn.cursor()
    cursor.execute( '''Create table horario_semana (horario_id INT AUTO_INCREMENT PRIMARY KEY,
                   seg VARCHAR(50)NOT NULL,
                   ter VARCHAR(50)NOT NULL, 
                   quar VARCHAR(50)NOT NULL,
                   quin VARCHAR(50)NOT NULL,
                   sext VARCHAR(50)NOT NULL,
                   sab VARCHAR(50)NOT NULL);''')
    conn.commit()
    conn.close()