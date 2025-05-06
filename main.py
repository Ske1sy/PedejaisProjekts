from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Izveido datubāzi, ja neeksistē
def create_database():
    conn =  sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS recommendations (
                    id INTEGER PRIMARY KEY,
                    goal TEXT,
                    weight FLOAT,
                    height FLOAT,
                    age INTEGER,
                    gender TEXT,
                    calories INTEGER,
                    plan TEXT
                )""")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    goal = request.form.get('goal')
    weight = int(request.form.get('weight'))
    height = int(request.form.get('height'))
    age = int(request.form.get('age'))
    gender = request.form.get('gender')

    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5 # BMR aprēķins vīriešiem
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161 # BMR aprēķins sievietēm 

    if goal == 'lose':
        calories = int(bmr - 500)
        recommendation = f"Lai zaudētu svaru, patērē apmēram {calories} kalorijas dienā. Fokusējies uz proteīniem, dārzeņiem un veselīgiem taukiem."
        plan = "Brokastis: Olu kultenis ar spinātiem. Pusdienas: Vistas fileja ar dārzeņiem. Vakariņas: Lēcu zupa."
    elif goal == 'gain':
        calories = int(bmr + 500)
        recommendation = f"Lai palielinātu masu, patērē apmēram {calories} kalorijas dienā. Iekļauj ogļhidrātus, proteīnus un biežākas ēdienreizes."
        plan = "Brokastis: Auzu pārslas ar pienu un augļiem. Pusdienas: Liellopa gaļa ar rīsiem. Vakariņas: Makaronu salāti ar olīvām un tunzivi."
    else:
        calories = int(bmr)
        recommendation = f"Uzturi svaru ar apmēram {calories} kalorijām dienā. Izvēlies sabalansētu uzturu."
        plan = "Brokastis: Jogurts ar granolu. Pusdienas: Zivs fileja ar dārzeņiem. Vakariņas: Pilngraudu maize ar sieru un tomātiem."

    # Saglabā datubāzē
        conn =  sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO recommendations (goal, weight, height, age, gender, calories, plan) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (goal, weight, height, age, gender, calories, plan))
        conn.commit()

    return render_template('result.html', recommendation=recommendation, plan=plan)

if __name__ == '__main__':
    create_database()
    app.run(debug=True)