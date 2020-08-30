from flask import Flask, jsonify, make_response

def register_errors(app):
    app.logger.info('registering error handlers')
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, bad_request)
    app.register_error_handler(404, resource_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(422, unprocessable_entity)
    app.register_error_handler(500, server_error)
    app.register_error_handler(501, method_not_implemented)

def bad_request(error):
    return make_response(jsonify(error=str(error)), 400)

def unauthorized(error):
    return make_response(jsonify(error=str(error)), 401)

def resource_not_found(error):
    return make_response(jsonify(error=str(error)), 404)

def method_not_allowed(error):
    return make_response(jsonify(error=str(error)), 405)

def unprocessable_entity(error):
    return make_response(jsonify(error=str(error)), 422)

def server_error(error):
    return make_response(jsonify(error=str(error)), 500)

def method_not_implemented(error):
    return make_response(jsonify(error=str(error)), 501)
    