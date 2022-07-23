from multiprocessing import cpu_count
from configs import server_host, server_port


def max_workers(light_mode: bool = True):
    return 1 if light_mode else cpu_count()


bind = f'{server_host}:{server_port}'
max_requests = 1000
worker_class = 'gthread'
workers = max_workers()
threads = 12