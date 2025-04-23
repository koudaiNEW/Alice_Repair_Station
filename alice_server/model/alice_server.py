from qq_api import QQ_API
from concurrent.futures import ThreadPoolExecutor
import os,sys
from loguru import logger
os.chdir(sys.path[0])


if __name__ == '__main__':
        threadPool = ThreadPoolExecutor(max_workers=8, thread_name_prefix="main_ThreadPool")
        # 初始化
        qq_server = QQ_API()
        # 业务
        threadPool.submit(qq_server.QQ_Loop)

        logger.success("业务启动成功")
        threadPool.shutdown(wait=True)