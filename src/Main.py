from flask import render_template, Flask, request, redirect
from common.model.Models import Users, Station, Channel, UserCar, ChannelUserCar, db
from sqlalchemy.sql import text
import common.service.CrudHelper as CrudHelper
# custom service modules
from common.service import UserService, ChannelService, UserCarService, StationService

# changelog
# this code have been rewritten (From now this file server as controller, the functions are in the scripts on service folder)




# todo
# sort non-occupied channels
# some exceptions at Car_select
# parrent station id sorting

# bootstrap


class MainApp:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ccs.db"
    db.init_app(app)
    Username = ''
    Username_role = ''
    Username_id = 0

    @app.route('/login', methods = ['POST', 'GET'])
    def login():
        userservice = UserService.UserService()
        return userservice.login()

    @app.route('/logout')
    def logout():
        userservice = UserService.UserService()
        return userservice.logout()

    @app.route('/admin/index', methods = ['POST', 'GET'])
    def admin_index():
        userservice = UserService.UserService()
        return userservice.admin_index()

    @app.route('/user/order_station', methods=['POST', 'GET'])
    def order_station():
        channelservice = ChannelService.ChannelService()
        return channelservice.order_station()


    @app.route('/user/add_car', methods=['POST', 'GET'])
    def add_car():
        usercarservice = UserCarService.UserCarService()
        return usercarservice.add_car()


    @app.route('/admin/station_managment', methods=['POST', 'GET'])
    def station_managment():
        stationservice = StationService.StationService()
        return stationservice.station_managment()

    @app.route('/admin/channel_managment', methods=['POST', 'GET'])
    def channel_managment():
        channelservice = ChannelService.ChannelService()
        return channelservice.channel_managment()
    @app.route('/admin/report_page', methods = ['POST', 'GET'])
    def report_page():
        userservice = UserService.UserService()
        return userservice.report_page()
    @app.route('/index', methods=['POST', 'GET'])
    def index():
        userservice = UserService.UserService()
        return userservice.index()

# @app.route('/test')
# def test():
#     return f'username is {Username}\n username id is {Username_id}\n username role is {Username_role}'
#     #return CrudHelper.channel_usercars(Username_id).sync_user()

if __name__ == '__main__':
    mainapp = MainApp
    mainapp.app.run(debug=True)