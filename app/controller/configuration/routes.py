from flask_restx import Namespace

static_api = Namespace("static", "[Static Serving] Static Files Serving APIs")

file_api = Namespace("file", "[File] File APIs")

fact_api = Namespace("fact", "[Fact] Fact APIs")
