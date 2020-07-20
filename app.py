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
        used_for = request.form['for what']

        q = f"select remaining from xp where id = {id}"     # get the remaining amount
        cursor.execute(q)
        remaining = cursor.fetchone()['remaining']
        finalRemaining = int(remaining) - int(spent)
        q = f"update xp set remaining={finalRemaining} where id = {id}"     # updating the remaining amount
        cursor.execute(q)

        q = f"INSERT INTO trans (trans_id, trans_amnt, trans_for) values ('{id}', '{spent}', '{used_for}')"
        cursor.execute(q)
        connection.commit()
        return redirect(f'{id}')

    else:
        try:
            sql = f"select * from xp where id = {id}"   # get the specific record 
            cursor.execute(sql)
            a = [i for i in cursor]

            q_showTrans = f"SELECT * FROM trans WHERE trans_id = {id}"      #get all transactions
            cursor.execute(q_showTrans)
            transactions = [trans for trans in cursor]

            connection.commit()
            data = {'a' : a[0], 'transactions' : transactions}
            return render_template('khaz.html', data= data)
        except Exception as e:
            return "error > {}".format(e)


@app.route('/delete/<id>')
def delete(id):
    q = f"DELETE FROM xp WHERE id={id}"     # delete the specific record
    cursor.execute(q)
    connection.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
