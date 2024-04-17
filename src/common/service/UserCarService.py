import Main
from common.model.Models import db, Users, UserCar
from flask import redirect, request, render_template
from sqlalchemy import text


class UserCarService:
    def __init__(self):
        self.Mainapp = Main.MainApp
        self.exec_usercars_individual = text(f'SELECT * FROM user_cars WHERE id_user = {self.Mainapp.Username_id}')
    def add_car(self):
        if self.Mainapp.Username == '':
            return redirect('/index')
        else:
            channel_usercars_list = db.session.execute(self.exec_usercars_individual)
            if request.method == 'POST':
                match request.form['button']:
                    case 'add car':
                        car_name = request.form['car_name']
                        add_car = UserCar(id_user = self.Mainapp.Username_id,
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