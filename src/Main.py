from flask import render_template, Flask, request, redirect, url_for
from common.model.Models import Users, Station, Channel, db
from sqlalchemy.sql import text

# changelog
# User.py will be merged to Admin.py, hence, Admin.py will be renamed to Main.py. Since development server can not handle two application at once.
# added occupiedby column to Channel table in ccs.sql


# notes
# Occupancy should be always at FALSE! Set to true only if someone occupies channel

# todo
# make login page for users
# CRUD car
# user order page. 
# commit if done!


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ccs.db"
db.init_app(app)
Username = ''
exec_user = text('SELECT * FROM users')
exec_station = text('SELECT * FROM stations')
exec_channel = text('SELECT * FROM channels')

@app.route('/index', methods = ['POST', 'GET'])
def user_index():
    if request.method == 'POST':
        match request.form['index_buttons']:
            case 'Order a station':
                return redirect('/user/order_station')
            case 'car managment':
                return redirect('/user/car_managment')
            case _:
                pass
    else:
        return render_template('user_index.html', username=Username)

@app.route('/user/order_station', methods = ['POST', 'GET'])
def order_station():
    global Username, Station_list
    if Username == '':
        return redirect('/index')
    else:
        channel_list = db.session.execute(exec_channel)
        if request.method == 'POST':
            match request.form['button']:
                case 'Order a station':
                    markers = request.form.getlist("table")
                    for i in markers:
                        channel = Channel.query.filter_by(id=i).first()
                        if channel.occupiedby == 'None':
                            channel.occupancy = True
                            channel.occupiedby = Username
                            db.session.commit()
                        elif channel.occupiedby != Username:
                            return 'this channel was occupied by someone else! Choose other channel!'
                    return redirect('/user/order_station')
                case 'Release a station':
                    markers = request.form.getlist("table")
                    for i in markers:
                        channel = Channel.query.filter_by(id=i).first()
                        if channel.occupiedby == Username:
                            channel.occupancy = False
                            channel.occupiedby = 'None'
                            db.session.commit()
                        else:
                            return "You can't release station, which you didn't occupied!"
                    return redirect('/user/order_station')
                case _:
                    return str(request.form['button'])
        else:
            return render_template('user_order_station.html', channel=channel_list, username=Username)


@app.route('/admin/index', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        match request.form['index_buttons']:
            case 'station managment':
                return redirect('/admin/station_managment')
            case 'channel managment':
                return redirect('/admin/channel_managment')
            case 'report':
                return redirect('/admin/report_page')
            case _:
                pass
    else:        
        return render_template('admin_index.html', username=Username)
    
@app.route('/admin/station_managment', methods = ['POST', 'GET'])
def station_managment():
    global Username, Station_list
    if Username == '':
        return redirect('/index')
    else:
        Station_list = db.session.execute(exec_station)
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

@app.route('/admin/channel_managment', methods = ['POST', 'GET'])
def channel_managment():
    global Username, channel_list
    if Username == '':
        return redirect('/index')
    else:
        channel_list = db.session.execute(exec_channel)
        if request.method == 'POST':
            match request.form['button']:
                case 'remove selected rows':
                    markers = request.form.getlist("table")
                    for i in markers:
                        Channel.query.filter_by(id=i).delete()
                        db.session.commit()
                    return redirect('/admin/channel_managment')
                case 'submit changes':
                    channel_parrent_station = request.form['channel_parrent_station']
                    channel_title = request.form['channel_title']
                    channel_price = request.form['channel_price']
                    #try:
                    add_station = Channel(id_station = channel_parrent_station,
                                        title = channel_title,
                                        price = channel_price)
                    if channel_parrent_station and channel_title and channel_price == '':
                        return redirect('/admin/channel_managment')
                    else:
                        db.session.add(add_station)
                        db.session.commit()
                        return redirect('/admin/channel_managment')
                    #except NoReferencedTableError:
                        #return f'Station id {channel_parrent_station} does not exist!!!'
                case 'Release a station':
                    markers = request.form.getlist("table")
                    for i in markers:
                        channel = Channel.query.filter_by(id=i).first()
                        channel.occupancy = False
                        channel.occupiedby = 'None'
                        db.session.commit()
                    return redirect('/admin/channel_managment')
                case _:
                    return str(request.form['button'])
        else:
            return render_template('admin_channel_managment.html', channels=channel_list, username=Username)

@app.route('/admin/report_page', methods = ['POST', 'GET'])
def report_page():
    global Username
    if Username == '':
        return redirect('/index')
    else: 
        Station_list = db.session.execute(exec_station)
        channel_list = db.session.execute(exec_channel)
        user_list = db.session.execute(exec_user)
        if request.method == 'POST':
            if request.form['button'] == 'report':
                username = request.form['User_select']
                return f'user {username} have been reported!'
        return render_template('admin_report_page.html',
                                Statist = Station_list,
                                channel_list = channel_list,
                                user_list = user_lion_list)

@app.route('/logout')
def logout():
    global Username
    Username = ''
    return redirect('/index') 


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        global Username
        Username = request.form['Username']
        Password = request.form['Password']
        find_users = Users.query.filter_by(username=Username).first()

        try:
            if find_users.password == Password and find_users.role == 'user':
                return redirect('/index')
            elif find_users.password == Password and find_users.role == 'admin':
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