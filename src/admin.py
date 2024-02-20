from flask import render_template, Flask, request, redirect, url_for
from common.model.Models import Users, Station, db
from sqlalchemy.sql import text


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ccs.db"
db.init_app(app)
Username = ''

@app.route('/admin/index', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form['station'] == 'station managment':
            return redirect('/admin/station_managment')
            #return 'hi'
        else:
            pass
    else:        
        return render_template('admin_index.html', username=Username)
    
@app.route('/admin/station_managment')
def station_managment():
    exec = text('SELECT * FROM stations')
    Station_list = db.session.execute(exec)
    #return str(Station_list)
    return render_template('admin_station_managment.html', stations=Station_list)

@app.route('/admin/logout')
def logout():
    global Username
    Username = ''
    return redirect('index') 


@app.route('/admin/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        global Username
        Username = request.form['Username']
        Password = request.form['Password']
        #add_user = Users(username = Username,
        #                password = Password,
        #                role = 'admin')
        #find_users = db.session.execute(text('SELECT username and password from users'))
        find_users = Users.query.filter_by(username=Username).first()

        try:
            #for row in find_users:
                #if row[0] == Username and row[1] == Password:
                    #return redirect('/admin/index')
                #else:
                    #return 'wrong login and password... ' + str(row)
            if find_users.password == Password and find_users.role == 'admin':
                return redirect('/admin/index')
            else:
                return 'wrong password or access denied...' #+ str(find_users)

                
        #except db.exc.NoResultFound:
        except AttributeError:
            return 'wrong login...'
        except Exception as e:
            return str(e)
    else:
        return render_template('admin_login.html')

if __name__ == '__main__':
    app.run(debug=True)