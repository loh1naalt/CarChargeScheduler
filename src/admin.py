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
        else:
            pass
    else:        
        return render_template('admin_index.html', username=Username)
    
@app.route('/admin/station_managment', methods = ['POST', 'GET'])
def station_managment():
    global Username
    if Username == '':
        return redirect('/admin/index')
    else:
        exec = text('SELECT * FROM stations')
        Station_list = db.session.execute(exec)
        if request.method == 'POST':
            match request.form['button']:
                case 'remove selected rows':
                    markers = request.form.getlist("table")
                    for i in markers:
                        Station.query.filter_by(id=i).delete()
                        db.session.commit()
                    return redirect('/admin/station_managment')
                case 'submit changes':
                    station_name = request.form['station_name']
                    station_location = request.form['station_location']
                    station_count_of_channels = request.form['station_count_of_channels']
                    add_station = Station(title = station_name,
                                        addressname = station_location,
                                        channels_per_station = station_count_of_channels)
                    if station_name and station_location and station_count_of_channels == '':
                        return redirect('/admin/station_managment')
                    else:
                        db.session.add(add_station)
                        db.session.commit()
                        return redirect('/admin/station_managment')
                case _:
                    return str(request.form['button'])
        else:
            return render_template('admin_station_managment.html', stations=Station_list, username=Username)

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
        find_users = Users.query.filter_by(username=Username).first()

        try:
            if find_users.password == Password and find_users.role == 'admin':
                return redirect('/admin/index')
            else:
                return 'wrong password or access denied...'

                

        except AttributeError:
            return 'wrong login...'
        except Exception as e:
            return str(e)
    else:
        return render_template('admin_login.html')

if __name__ == '__main__':
    app.run(debug=True)