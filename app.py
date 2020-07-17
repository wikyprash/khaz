from flask import Flask, render_template, request, redirect
from pymysql import connect, cursors

connection = connect(host='localhost',
                     user='root',
                     password='Prash',
                     db='khaz',
                     charset='utf8mb4',
                     cursorclass=cursors.DictCursor)

cursor = connection.cursor()

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        amount = request.form['amount']
        try:
            sql = f"insert into xp (title, amount, remaining) values ('{title}', '{amount}', {amount})"
            cursor.execute(sql)
            connection.commit()
        except:
            return "something wrong"
        return redirect('/')
    else:
        sql = "SELECT * from xp"    # get all data from the table
        cursor.execute(sql)
        a = list(cursor)
        if len(a) == 0:
            return render_template('index.html', mpty="there is not khazes, \n don't be shy create one")
        else:
            return render_template('index.html', data=a)


@app.route('/<id>', methods=['GET', 'POST'])
def khaz(id):
    if request.method == 'POST':
        spent = request.form['how much']
        q = f"select remaining from xp where id = {id}"     # get the remaining amount
        cursor.execute(q)
        remaining = cursor.fetchone()['remaining']
        finalRemaining = int(remaining) - int(spent)
        q = f"update xp set remaining={finalRemaining} where id = {id}"     # updating the remaining amount
        cursor.execute(q)
        connection.commit()
        return redirect(f'{id}')

    else:
        try:
            sql = f"select * from xp where id = {id}"   # get the specific record 
            cursor.execute(sql)
            connection.commit()
            a = [i for i in cursor]
            return render_template('khaz.html', data=a[0])
        except Exception as e:
            return "error > {}".format(e)


@app.route('/<id>/delete')
def delete(id):
    q = f"DELETE FROM xp WHERE id={id}"     # delete the specific record
    cursor.execute(q)
    connection.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
