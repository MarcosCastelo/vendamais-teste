class ErrorHandler(Exception):
  def __init__(self, message, code=None):
    self.message = message
    self.code = code
    super().__init__(message)
  
  def to_dict(self):
    return {'error': self.message, 'code': self.code}