import Main
from common.service.CrudHelper import username
from common.model.Models import db, Users
from flask import redirect, request, render_template
from sqlalchemy import text


class UserService:
    def __init__(self):
        self.exec_user = text('SELECT * FROM users')
        self.exec_station = text('SELECT * FROM stations')
        self.exec_channel = text('SELECT * FROM channels')
        self.Mainapp = Main.MainApp
        self.username = username()

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
            self.Mainapp.Username_id = self.username.username_to_id(self.Mainapp.Username)
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
            Station_list = db.session.execute(self.exec_station)
            channel_list = db.session.execute(self.exec_channel)
            user_list = db.session.execute(self.exec_user)
            if request.method == 'POST':
                if request.form['button'] == 'report':
                    username = request.form['User_select']
                    return f'user {username} have been reported!'
            return render_template('admin_report_page.html',
                                    stations = Station_list,
                                    channel_list = channel_list,
                                    user_list = user_list)
