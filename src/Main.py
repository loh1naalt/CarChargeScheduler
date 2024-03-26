from flask import render_template, Flask, request, redirect
from common.model.Models import Users, Station, Channel, UserCar, db
from sqlalchemy.sql import text
import common.service.CrudHelper as CrudHelper

# changelog
# User.py will be merged to Admin.py, hence, Admin.py will be renamed to Main.py. Since development server can not handle two application at once.
# added occupiedby column to Channel table in ccs.sql
# added CrudHelper module which will slightly improve coding efficency 
# added Car managment page 
# now admins are able to swich betwen user and admin page
# registration into CCS system
# syncing with channel_usercar (partly)
# fixed bug where user can enter the admin page


# notes


# todo



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ccs.db"
db.init_app(app)
Username = ''
Username_role = ''
Username_id = 0

exec_user = text('SELECT * FROM users')
exec_station = text('SELECT * FROM stations')
exec_channel = text('SELECT * FROM channels')
exec_usercars = text('SELECT * FROM user_cars')
exec_channel_usercars = text('SELECT * FROM channel_usercars')

@app.route('/index', methods = ['POST', 'GET'])
def user_index():
    if request.method == 'POST':
        match request.form['index_buttons']:
            case 'Order a station':
                return redirect('/user/order_station')
            case 'car managment':
                return redirect('/user/add_car')
            case 'switch back to admin page':
                return redirect('/admin/index')
            case _:
                pass
    else:
        return render_template('user_index.html', username=Username, Username_role=Username_role)

@app.route('/user/order_station', methods = ['POST', 'GET'])
def order_station():
    global Username
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

@app.route('/user/add_car', methods = ['POST', 'GET'])
def add_car():
    global Username
    if Username == '':
        return redirect('/index')
    else:
        user_id = CrudHelper.username(Username).username_to_id()
        exec_usercars_individual = text(f'SELECT * FROM user_cars WHERE id_user = {user_id}')
        channel_usercars_list = db.session.execute(exec_usercars_individual)
        if request.method == 'POST':
            match request.form['button']:
                case 'add car':
                    car_name = request.form['car_name']
                    add_car = UserCar(id_user = user_id,
                                      carname = car_name)
                    if car_name == '':
                        return redirect('/user/add_car')
                    else:
                        db.session.add(add_car)
                        db.session.commit()
                        return redirect('/user/add_car')
                case 'remove car':
                    markers = request.form.getlist("table")
                    for i in markers:
                        UserCar.query.filter_by(id=i).delete()
                        db.session.commit()
                    return redirect('/user/add_car')
        else:
            return render_template('user_add_car.html', channel_usercars_list=channel_usercars_list)



@app.route('/admin/index', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        match request.form['index_buttons']:
            case 'switch to user account':
                return redirect('/index')
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
    global Username
    if Username == '' or Username_role != 'admin':
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
    if Username == '' or Username_role != 'admin':
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
            return render_template('admin_channel_managment.html', channels=channel_list, username=Username) #channel_station_name=channel_station_name)

@app.route('/admin/report_page', methods = ['POST', 'GET'])
def report_page():
    global Username
    if Username == '' or Username_role != 'admin':
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
                                user_list = user_list)

@app.route('/logout')
def logout():
    global Username
    Username = ''
    Username_role = ''
    return redirect('/index') 


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        global Username, Username_role, Username_id
        Username = request.form['Username']
        Password = request.form['Password']
        find_users = Users.query.filter_by(username=Username).first()
        if find_users != None:
            Username_role = find_users.role
        Username_id = CrudHelper.username(Username).username_to_id()
        sync_user = CrudHelper.channel_usercars(Username_id).sync_user()
        match request.form['button']:
            case 'login':
                try:
                    if sync_user == 0:
                        if find_users.password == Password and find_users.role == 'user':
                                return redirect('/index')
                        
                        elif find_users.password == Password and find_users.role == 'admin':
                                return redirect('/admin/index')                            
                        else:
                            return 'wrong password or access denied...'
                    else:
                        return sync_user


                        

                except AttributeError:
                    return 'wrong login...'
                except Exception as e:
                    return str(e)
            case 'register':
                users = db.session.execute(exec_user)
                for i in users:
                    if i[1] == Username:
                        return f'username {i[1]} exists!'
                if Username and Password == '':
                        return redirect('/login')    
                else:
                    add_user = Users(username=Username,
                                    password=Password,
                                    role = 'user')
                    db.session.add(add_user)
                    db.session.commit()
                    return redirect('/login')

    else:
        return render_template('admin_login.html')
            


@app.route('/test')
def test():
    return f'username is {Username}\n username id is {Username_id}\n username role is {Username_role}'
    #return CrudHelper.channel_usercars(Username_id).sync_user()
if __name__ == '__main__':
    app.run(debug=True)