class DataController:
  def __init__(self,id,contact,communiactionChannel):
    self.id = id
    self.consents = []
    self.contact = contact
    self.communiactionChannel = communiactionChannel
    self.isProcessing = {} #Dictionary DataSubjectID:Boolean