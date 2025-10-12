from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import fpga
class Api_Server:
    def __init__(self, fpga,  host='0.0.0.0', port=8082):
        self.app = Flask(__name__)
        CORS(self.app, resources={r"/*": {"origins": "*"}})
        self.host = host
        self.port = port
        self.load_routes()
        self.fpga = fpga

    def load_routes(self):
        app = self.app

        @app.route('/api/get_data1', methods=['GET'])
        def get_data1():
            data = self.fpga.get_data_1()
            return jsonify(data)

        @app.route('/api/get_data2', methods=['GET'])
        def get_dat2():
            data = self.fpga.get_data_2()
            return jsonify(data)

        @app.route('/api/get_data3', methods=['GET'])
        def get_data3():
            data = self.fpga.get_data_3()
            return jsonify(data)

if __name__ == '__main__':
    API_SERVER = Api_Server(fpga, host='0.0.0.0', port=8082)
    API_SERVER.app.run(debug=True)