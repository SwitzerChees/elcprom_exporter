from state import State
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from flask import Flask, Response, request
from datetime import datetime

st = State()

# Define the endpoint for the state manipulation
app = Flask(__name__)


@app.route('/states', methods=['POST'])
def states():
    try:
        print(request.get_data())
        req_data = request.get_json(force=True)
        # manipulate_state(req_data)
        st.check_inc_dec(req_data)
        return Response('Success!', 200)
    except Exception as err:
        now = datetime.utcnow()
        print(f'{now.strftime("%d.%m.%Y %H:%M:%S")}: ', err)
        return Response('Internal Error!', 500)


# Define the endpoint for the metrics
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    app.run(debug=False, port=8080)
