import traceback
from state import State
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from flask import Flask, Response, request, jsonify
from datetime import datetime

st = State()

# Define the endpoint for the state manipulation
app = Flask(__name__)


@app.route('/states', methods=['POST'])
def states():
    try:
        print(request.get_data())
        req_data = request.get_json(force=True)
        st.check_inc_dec(req_data)
        return jsonify(st.current_state)
    except Exception as err:
        now = datetime.utcnow()
        formated_error = ''.join(traceback.format_exception(etype=type(err), value=err, tb=err.__traceback__))
        print(f'{now.strftime("%d.%m.%Y %H:%M:%S")}: ', formated_error)
        return Response(formated_error, 500)


# Define the endpoint for the metrics
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    app.run(debug=False, port=8080)
