class HelloAgentsException(Exception):
    """HelloAgents的基础异常类"""
    pass

class ToolException(HelloAgentsException):
    """工具相关异常"""
    pass