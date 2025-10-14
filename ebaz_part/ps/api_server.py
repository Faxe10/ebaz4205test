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
            data = self.fpga.get_data1()
            return jsonify (data, format(data, f'014b'))

        @app.route('/api/get_data2', methods=['GET'])
        def get_dat2():
            data = self.fpga.get_data2()
            return jsonify (data, format(data, f'014b'))

        @app.route('/api/get_data3', methods=['GET'])
        def get_data3():
            data = self.fpga.get_data3()
            return jsonify (data, format(data, f'014b'))

        @app.route('/api/get_data', methods=['GET'])
        def get_data3():
            data_port1 = self.fpga.get_data1()
            data_port2 = self.fpga.get_data2()
            data_port3 = self.fpga.get_data3()
            return_msg  = jsonify ({
                "bitwidth": 14,
                "values": {  # numerisch weiterverarbeitbar
                "data1": f"{data_port1:014b}",
                "data2": f"{data_port2:014b}",
                "data3": f"{data_port3:014b}"
            }})
            return return_msg
if __name__ == '__main__':
    fpga = fpga.FPGA()
    api_server = Api_Server(fpga, host='0.0.0.0', port=8082)
    api_server.app.run(host=api_server.host, port=api_server.port, threaded=True, use_reloader=False)