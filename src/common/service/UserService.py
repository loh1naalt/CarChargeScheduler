import Main
import common.service.CrudHelper as Crudhelper
from common.model.Models import db, Users, ReportedUsersList
from flask import redirect, request, render_template
from sqlalchemy import text


class UserService:
    def __init__(self):
        self.exec_user = text('SELECT * FROM users')
        self.exec_station_id = text('SELECT id FROM stations')
        self.exec_station_address = text('SELECT addressname FROM stations')
        self.exec_channel = text('SELECT * FROM channels')
        self.exec_reported_user_list = text('SELECT * FROM reported_users_list')
        self.Mainapp = Main.MainApp

    def index(self):
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
            return render_template('user_index.html', username=self.Mainapp.Username,
                                    Username_role=self.Mainapp.Username_role)


    def admin_index(self):
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
                    case 'reported users':
                        return redirect('/admin/reported_users')
                    case _:
                        pass
        else:
            return render_template('admin_index.html', username=self.Mainapp.Username,
                                   user_role=self.Mainapp.Username_id)

    def logout(self):
        self.Mainapp.Username = ''
        self.Mainapp.Username_role = ''
        return redirect('/index')

    def login(self):
        if request.method == 'POST':
            self.Mainapp.Username = request.form['Username']
            Password = request.form['Password']
            find_users = Users.query.filter_by(username=self.Mainapp.Username).first()
            if find_users is not None:
                self.Mainapp.Username_role = find_users.role
            self.Mainapp.Username_id = Crudhelper.username_to_id(self.Mainapp.Username)
            match request.form['button']:
                case 'login':
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
                case 'register':
                    users = db.session.execute(self.exec_user)
                    for i in users:
                        if i[1] == self.Mainapp.Username:
                            return f'username {i[1]} exists!'
                    if self.Mainapp.Username and Password == '':
                        return redirect('/login')
                    else:
                        add_user = Users(username=self.Mainapp.Username,
                                             password=Password,
                                             role='user')
                        db.session.add(add_user)
                        db.session.commit()
                        return redirect('/login')

        else:
            return render_template('admin_login.html')

    def report_page(self):
        if self.Mainapp.Username == '' or self.Mainapp.Username_role != 'admin':
            return redirect('/index')
        else:
            Station_list_id = db.session.execute(self.exec_station_id)
            Station_list_address = db.session.execute(self.exec_station_address)
            channel_list = db.session.execute(self.exec_channel)
            user_list = db.session.execute(self.exec_user)
            if request.method == 'POST':
                if request.form['button'] == 'report':
                    station_name = request.form['station_name_select']
                    station_location = request.form['station_location_select']
                    channel_id = request.form['channel_title_select']
                    Username = request.form['User_select']
                    additional_tip = request.form['textfeild']
                    Username_id_selected = Crudhelper.username_to_id(Username)

                    report = ReportedUsersList(
                        id_station = station_name,
                        station_address = station_location,
                        id_channel = channel_id,
                        id_user = Username_id_selected,
                        additional_tip = additional_tip
                    )

                    db.session.add(report)
                    db.session.commit()
                    return redirect('/admin/report_page')

            return render_template('admin_report_page.html',
                                    stations_id = Station_list_id,
                                    stations_address = Station_list_address,
                                    channel_list = channel_list,
                                    user_list = user_list)
    def reported_users(self):
        if self.Mainapp.Username == '' or self.Mainapp.Username_role != 'admin':
            return redirect('/index')
        else:
            ReportedUserslist = db.session.execute(self.exec_reported_user_list)
            if request.method == 'POST':
                if request.form['button'] == 'remove':
                    markers = request.form.getlist("table")
                    for i in markers:
                        ReportedUsersList.query.filter_by(id=i).delete()
                        db.session.commit()
                    return redirect('/admin/reported_users')

            return render_template('admin_reported_users_page.html', reported_users_list = ReportedUserslist)
