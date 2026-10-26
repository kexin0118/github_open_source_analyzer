import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s-%(levelname)s-%(message)s"
)
logger=logging.getLogger(__name__)

logger.info("开始获取github仓库")
logger.warning("API请求次数不足")
logger.error("请求失败")