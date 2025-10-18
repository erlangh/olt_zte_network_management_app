from netmiko import ConnectHandler
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class TelnetClient:
    """Telnet/SSH Client for ZTE C320 OLT"""
    
    def __init__(self, host: str, username: str, password: str, port: int = 23, device_type: str = "zte_zxros"):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.device_type = device_type
        self.connection = None
    
    def connect(self) -> bool:
        """
        Establish connection to device
        
        Returns:
            True if successful, False otherwise
        """
        try:
            device = {
                'device_type': self.device_type,
                'host': self.host,
                'username': self.username,
                'password': self.password,
                'port': self.port,
                'timeout': 30,
                'session_timeout': 60
            }
            
            self.connection = ConnectHandler(**device)
            logger.info(f"Connected to {self.host}")
            return True
            
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            return False
    
    def disconnect(self):
        """Close connection"""
        if self.connection:
            self.connection.disconnect()
            self.connection = None
            logger.info(f"Disconnected from {self.host}")
    
    def send_command(self, command: str) -> Optional[str]:
        """
        Send command to device
        
        Args:
            command: Command to execute
            
        Returns:
            Command output or None if error
        """
        if not self.connection:
            logger.error("Not connected to device")
            return None
        
        try:
            output = self.connection.send_command(command)
            return output
        except Exception as e:
            logger.error(f"Command execution error: {str(e)}")
            return None
    
    def execute_commands(self, commands: list) -> Dict[str, str]:
        """
        Execute multiple commands
        
        Args:
            commands: List of commands
            
        Returns:
            Dictionary with command: output pairs
        """
        results = {}
        
        for cmd in commands:
            output = self.send_command(cmd)
            results[cmd] = output if output else ""
        
        return results
    
    def configure_onu(self, slot: int, port: int, onu_id: int, config: Dict) -> bool:
        """
        Configure ONU parameters
        
        Args:
            slot: Slot number
            port: Port number
            onu_id: ONU ID
            config: Configuration dictionary
            
        Returns:
            True if successful
        """
        if not self.connection:
            return False
        
        try:
            # Enter config mode
            self.connection.config_mode()
            
            # Build configuration commands for ZTE C320
            commands = []
            
            # Example commands - adjust based on actual ZTE syntax
            if 'name' in config:
                commands.append(f"onu {slot}/{port}:{onu_id} name {config['name']}")
            
            if 'vlan' in config:
                commands.append(f"onu {slot}/{port}:{onu_id} service-port vlan {config['vlan']}")
            
            # Send config commands
            for cmd in commands:
                self.connection.send_config_set([cmd])
            
            # Exit config mode
            self.connection.exit_config_mode()
            
            logger.info(f"ONU {slot}/{port}:{onu_id} configured successfully")
            return True
            
        except Exception as e:
            logger.error(f"ONU configuration error: {str(e)}")
            return False
    
    def authorize_onu(self, slot: int, port: int, sn: str) -> bool:
        """
        Authorize/register an ONU
        
        Args:
            slot: Slot number
            port: Port number
            sn: ONU Serial Number
            
        Returns:
            True if successful
        """
        if not self.connection:
            return False
        
        try:
            self.connection.config_mode()
            
            # ZTE C320 ONU authorization command (example)
            command = f"interface gpon-olt_{slot}/{port}\nonu {sn} type all sn\n"
            self.connection.send_config_set([command])
            
            self.connection.exit_config_mode()
            
            logger.info(f"ONU {sn} authorized on port {slot}/{port}")
            return True
            
        except Exception as e:
            logger.error(f"ONU authorization error: {str(e)}")
            return False
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
