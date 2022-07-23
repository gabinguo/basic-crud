import os

basedir: str = os.path.abspath(os.path.dirname(__file__))
static_file_loc: str = os.path.join(basedir, 'static')
server_host: str = "0.0.0.0"
server_port: int = 5000