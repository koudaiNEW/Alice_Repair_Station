from qq_api import QQ_API
from concurrent.futures import ThreadPoolExecutor

if __name__ == '__main__':
        threadPool = ThreadPoolExecutor(max_workers=8, thread_name_prefix="main_ThreadPool")
        # 业务
        qq_server = QQ_API()
        threadPool.submit(qq_server.QQ_Loop)
        
        threadPool.shutdown(wait=True)