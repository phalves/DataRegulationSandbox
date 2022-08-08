class DataSubject:
  def __init__(self,id):
    self.id = id                 # Identification Number
    self.consents = []           # Empty list of consents
    self.personalData = {}       # Dictionary of Personal Data
    self.transactionalData = {}  # Dictionary of Transactional Data