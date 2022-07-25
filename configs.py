import os

basedir: str = os.path.abspath(os.path.dirname(__file__))
static_file_loc: str = os.path.join(basedir, 'static')
uploaded_file_loc: str = os.path.join(basedir, 'uploaded_file')
server_host: str = "0.0.0.0"
server_port: int = 5000
