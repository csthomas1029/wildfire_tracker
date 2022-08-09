from flask import Blueprint, request, Flask, render_template

from app.wildfire_map import wildfire_map

wildfire_routes = Blueprint("wildfire_routes", __name__)

@wildfire_routes.route('/wildfire/map')
def map():
  return render_template('wildfire_map.html')

@wildfire_routes.route('/my-link/')
def my_link():
  return 'Click.'

if __name__ == '__main__':
  wildfire_map.run(debug=True)