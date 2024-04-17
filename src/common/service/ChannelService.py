import Main
from common.model.Models import db, Users, Channel, ChannelUserCar
from flask import redirect, request, render_template
from sqlalchemy import text

class ChannelService:
    def __init__(self):
        self.exec_channel = text('SELECT * FROM channels')
        self.Mainapp = Main.MainApp
    def order_station(self):
        exec_usercars_filtered = text(f'SELECT * FROM user_cars WHERE id_user = {self.Mainapp.Username_id}')
        if self.Mainapp.Username == '':
            return redirect('/index')
        else:
            channel_list = db.session.execute(self.exec_channel)
            car_list = db.session.execute(exec_usercars_filtered)
            if request.method == 'POST':
                match request.form['button']:
                    case 'Order a station':
                        channel_list.close()
                        car_list.close()
                        markers = request.form.getlist("table")
                        getcar = request.form['Car_selection']
                        for i in markers:
                            channel = Channel.query.filter_by(id=i).first()
                            channel_usercars = ChannelUserCar.query.filter_by(id_channel=i, id_user=self.Mainapp.Username_id).first()
                            if channel.occupiedby is None:
                                if (channel_usercars is None or channel_usercars.id_channel is None or
                                        channel_usercars.id_user_car is None):
                                    add_to_channel_user_car = ChannelUserCar (id_channel = i,
                                                                            id_user = self.Mainapp.Username_id,
                                                                            id_user_car = getcar)
                                    db.session.add(add_to_channel_user_car)
                                else:
                                    channel_usercars.id_user_car = int(getcar)
                                channel.occupancy = True
                                channel.occupiedby = self.Mainapp.Username
                                db.session.commit()

                            elif channel.occupiedby != self.Mainapp.Username:
                                return 'this channel was occupied by someone else! Choose other channel!'

                            else:
                                channel_list.close()

                        return redirect('/user/order_station')
                    case 'Release a station':
                        channel_list.close()
                        car_list.close()
                        markers = request.form.getlist("table")
                        for i in markers:
                            channel = Channel.query.filter_by(id=i).first()
                            if channel.occupiedby == self.Mainapp.Username:
                                ChannelUserCar.query.filter_by(id_channel=i, id_user=self.Mainapp.Username_id).delete()
                                channel.occupancy = False
                                channel.occupiedby = None
                                db.session.commit()
                            else:
                                return "You can't release station, which you didn't occupied!"

                        return redirect('/user/order_station')
                    case _:
                        return str(request.form['button'])
            else:
                return render_template('user_order_station.html', channel=channel_list,
                                       username=self.Mainapp.Username, car_list=car_list)

    def channel_managment(self):
        if self.Mainapp.Username == '' or self.Mainapp.Username_role != 'admin':
            return redirect('/index')
        else:
            channel_list = db.session.execute(self.exec_channel)
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
                    case 'Release a station':
                        markers = request.form.getlist("table")
                        for i in markers:
                            channel = Channel.query.filter_by(id=i).first()
                            channel.occupancy = False
                            channel.occupiedby = None
                            db.session.commit()
                        return redirect('/admin/channel_managment')
                    case _:
                        return str(request.form['button'])
            else:
                return render_template('admin_channel_managment.html', channels=channel_list
                                       , username=self.Mainapp.Username) #channel_station_name=channel_station_name)