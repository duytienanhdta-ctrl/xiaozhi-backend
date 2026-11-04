import asyncio
from logging import getLogger
import os
from urllib.parse import urlparse
from ..config import ConfigManager
from .websocket_proxy import WebSocketProxy

logger = getLogger(__name__)


def run_proxy():
  """在单独的进程中运行代理服务器"""
  try:
    configuration = ConfigManager()
    ws_proxy_url = configuration.get_str("WS_PROXY_URL")

    # Ưu tiên lấy PORT từ môi trường Cloud, nếu không có mới lấy từ config/5000
    env_port = os.environ.get("PORT")
    port = int(env_port) if env_port else (urlparse(ws_proxy_url).port or 5000)

    proxy = WebSocketProxy(
        device_id=configuration.get_str("DEVICE_ID"),
        client_id=configuration.get_str("CLIENT_ID"),
        websocket_url=configuration.get_str("WS_URL"),
        ota_version_url=configuration.get_str("OTA_VERSION_URL"),
        proxy_host="0.0.0.0",
        proxy_port=port,
        token_enable=configuration.get_bool("TOKEN_ENABLE"),
        token=configuration.get_str("TOKEN"),
    )

    # 运行代理服务器
    asyncio.run(proxy.main())

  except KeyboardInterrupt:
    logger.info("代理进程收到中断信号")
  except Exception as e:
    logger.error(f"代理进程异常: {e}")