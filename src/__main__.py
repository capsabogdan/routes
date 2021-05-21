import json
import os
import secrets
from datetime import datetime

from texts import *

print(welcome_message)
letter = str(input())
format = '%Y-%m-%d'

json_routes = {"key": {'from': 'A', 'to': 'B', 'date': 'date', 'seats': 'seats'}}

json_search_params = {
    'from': " ",
    'to': " ",
    'from_date': " ",
    'to_date': " ",
    'min_seats': " "
}


def createTrip():
    command_letter, source, destination, date, seats = input(text_create_ride).split()
    key_route = secrets.token_hex(nbytes=16)
    json_routes[key_route] = {
        'from': str(source),
        'to': str(destination),
        'date': str(date),
        'seats': str(seats)
    }
    save_route()
    continue_program()


def save_route():
    with open("routes.json", "r+") as file:
        json_data = json.load(file)
        json_data.update(json_routes)
        file.seek(0)
        json.dump(json_data, file, indent=2)


def inject_route(source, destination, date, seats):
    key_route = secrets.token_hex(nbytes=16)
    json_routes[key_route] = {
        'from': '"{}"'.format(source),
        'to': str(destination),
        'date': str(date),
        'seats': str(seats)
    }


def return_trip():
    with open("routes.json", "r+") as file:
        json_data = json.load(file)
        last_route_key = list(json_data.items())[-1][0]
        last_route_json = json_data.get(last_route_key)
        command_letter, date = input(text_return_trip).split()
        key_route = secrets.token_hex(nbytes=16)
        json_routes[key_route] = {
            'from': str(last_route_json.get('to')),
            'to': str(last_route_json.get('from')),
            'date': str(date),
            'seats': str(last_route_json.get('seats'))
        }
        save_route()
    continue_program()


def search_trip():
    filter_search_params()


def inject_json_params(search_params):
    for param in search_params:
        if input_type(param) == int:
            json_search_params['min_seats'] = param
        elif input_type(param) == str and search_params.index(param) == 1:
            json_search_params['from'] = param
        elif input_type(param) == str and search_params.index(param) == 2:
            json_search_params['to'] = param
        elif input_type(param) == datetime.date and search_params.index(param) == 3:
            json_search_params['from_date'] = param
        elif input_type(param) == datetime.date and search_params.index(param) == 4:
            json_search_params['to_date'] = param


def filter_search_params():
    search_params_list = input(text_search_rides).split()
    inject_json_params(search_params_list)
    if len(search_params_list) == 1 and search_params_list[0].upper() == 'S':
        print_all_routes()

    with open("routes.json", "r+") as file:
        json_data = json.load(file)
        all_routes = list(json_data.values())
        filtered_routes_from = []
        filtered_routes_to = []
        filtered_routes_from_date = []
        filtered_routes_between_dates = []
        final_routes = []

        # filter from
    if json_search_params.get('from') != " ":
        for route in all_routes:
            if json_search_params.get('from') == str(route.get('from')):
                filtered_routes_from.append(route)
    else:
        filtered_routes_from_date = json_routes

        # filter to
    if json_search_params.get('to') != " ":
        for route in filtered_routes_from:
            if json_search_params.get('to') == route.get('to'):
                filtered_routes_to.append(route)
    else:
        filtered_routes_to = filtered_routes_from

        # filter from_date
    if json_search_params.get('from_date') != ' ':
        route_date = datetime.strptime(route.get('date'), format)
        param_date_from = datetime.strptime(json_search_params.get('from_date'), format)
        for route in filtered_routes_to:
            if route_date.date() > param_date_from.date():
                filtered_routes_from_date.append(route)
    else:
        filtered_routes_from_date = filtered_routes_to

        # filter between dates
    if json_search_params.get('to_date') != " ":
        route_date = datetime.strptime(route.get('date'), format)
        param_date_from = datetime.strptime(json_search_params.get('from_date'), format)
        param_date_to = datetime.strptime(json_search_params.get('to_date'), format)
        for route in filtered_routes_from_date:
            if param_date_from <= route_date <= param_date_to:
                filtered_routes_between_dates.append(route)
    else:
        filtered_routes_between_dates = filtered_routes_from_date

        # filter min seats
    if json_search_params.get('min_seats') != " ":
        for route in filtered_routes_between_dates:
            seats_param = int(json_search_params.get('min_seats'))
            seats_route = int(route.get('seats'))
            if seats_param <= seats_route:
                final_routes.append(route)
    else:
        final_routes = filtered_routes_between_dates

    if len(search_params_list) != 1 and search_params_list[0].upper() == 'S':
        print_routes(final_routes)

    continue_program()


def print_routes(routes):
    for route in routes:
        result = " ".join(str(value) for value in route.values())
        print(result)


def input_type(input):
    try:
        seats = int(input)
        return int
    except ValueError:
        try:
            datetime.strptime(input, format).date()
            return datetime.date
        except ValueError:
            return str


def print_all_routes():
    with open("routes.json", "r+") as file:
        json_data = json.load(file)
        routes_json = list(json_data.values())
        print_routes(routes_json)


def execute_command(letter):
    if os.path.getsize("routes.json") == 0:
        with open("routes.json", "w") as outfile:
            json.dump(json_routes, outfile)
    check_letter(letter.upper())


def check_letter(letter):
    if letter == 'C':
        createTrip()
    elif letter == 'R':
        return_trip()
    elif letter == 'S':
        search_trip()
    else:
        print('text_invalid_input')
        execute_command(str(input()))


def continue_program():
    continue_option = input(text_continue)
    if continue_option.upper() == 'Y':
        print(text_options)
        execute_command(str(input()))
    else:
        print(text_end_program)


execute_command(letter)
