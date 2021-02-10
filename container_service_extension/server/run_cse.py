from container_service_extension.server.service import Service
import container_service_extension.common.utils.core_utils as utils
from container_service_extension.installer.config_validator import get_validated_config


def run(config_file_path):
   console_message_printer = utils.ConsoleMessagePrinter()

   config = get_validated_config(
      config_file_name=config_file_path,
      skip_config_decryption=True,
      msg_update_callback=console_message_printer)

   service = Service(
      config_file=config_file_path,
      config=config)
   service.run(msg_update_callback=console_message_printer)


run('/Users/sayloo/Desktop/work/cse/container-service-extension/config.yaml')
