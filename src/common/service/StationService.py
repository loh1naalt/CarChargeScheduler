import Main
from common.model.Models import db, Station
from flask import redirect, request, render_template
from sqlalchemy import text

class StationService:
    def __init__(self):
        self.exec_station = text('SELECT * FROM stations')
        self.Mainapp = Main.MainApp

    def station_managment(self):
        if self.Mainapp.Username == '' or self.Mainapp.Username_role != 'admin':
            return redirect('/index')
        else:
            Station_list = db.session.execute(self.exec_station)
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
                return render_template('admin_station_managment.html', stations=Station_list,
                                       username=self.Mainapp.Username)
