# These libraries are used to manipulate dates 
from datetime import date, datetime 

# Action Types
COMMUNICATION = 'Communication'
EXPLANATION = 'Explanation'
DELETION = 'Deletion'

# Deontic Concepts
OBLIGATION = 'Obligation'
PERMISSION = 'Permission'
PROHIBITION = 'Prohibition'
VIOLATION = 'Violation'
COMPLIANCE = 'Compliance'

class Log:
  def __init__(self):
    #empty log
    self.root = ['Date; Event; Type; Deontic Concept']
    self.filePersistence = False
    

  def configLogPersistence(self,_fileName):
    if _fileName!='':
      self.filePersistence = True
      
      #open file
      self.file = open(_fileName, "w")

    else:
      print('There is no fileName, so the file will not be generated')
  
  def registerAction(self,message,actionType,deonticConcept):
    self.date = datetime.today()
    self.message = message
    self.actionType = actionType
    self.deonticConcept = deonticConcept
    self.root.append(str(self.date)+'; '+str(self.message)+'; '+str(self.actionType)+';  '+str(self.deonticConcept))

    if self.filePersistence==True:
      self.file.write(self.root[-1]) # Save the most recent action

  def printLog(self):
    for action in self.root:
      print(action)
