## Libraries ##
# This library is used to generate a unique identification number
import uuid 

# This library is used to perform adding numbers to months to walk back and forward from the current time
from dateutil.relativedelta import relativedelta 

## Global Static Variables ###
# Consent Status possibilities
AWAITING_AUTHORISATION = 'AwaitingAuthorisation'
AUTHORISED            = 'Authorised'
REJECTED              = 'Rejected'
REVOKED               = 'Revoked'

# Data Subject Rights
DATA_ACCESS        = 'Data Access'
DATA_COPY          = 'Data Copy'
DATA_CORRECTION    = 'Data Correction'
DATA_ANONYMIZATION = 'Data Anonymization'
DATA_PORTABILITY   = 'Data Portability'
DATA_DELETION      = 'Data Deletion'
THIRD_PARTY_SHARING = 'Information regarding the data sharing with a third party'
CONSENT_REVOCATION = 'Request consent revocation'

# Data Controller Rights
DATA_PROCESSING  = 'Data Processing'
DATA_COLLECTING  = 'Data Collecting'
DATA_STORING     = 'Data Storing'

# Consent Class
class Consent:

  # Create Consent Function based on the required information described in the current Data Regulation
  # This function expects to receive the consent purpose, the specific purpose,
  #  the third party sharing purpose (if needed), the data controller information,
  #  how long this consent is valid, and how many months before the creation data 
  #  the Data Controller can get the Data Controller data.
  def createConsent(self, purpose, specificPurpose, thirdParySharingPurpose, criptographyAlgoritm, accessPolicies, storagePlatform, dataController, validForQuantityOfMonths, monthsBeforeTheAcceptance):
    
    # Open Banking API Params
    self.id = uuid.uuid4()                   # Unique Consent ID is generated when the function is called
    self.creationTime = datetime.today()     # Creation Time is generated when the function is called
    self.status = AWAITING_AUTHORISATION 
    self.permissions = ['ReadAccountsBasic','ReadAccountsDetail','ReadBalances','ReadOffers','ReadProducts']
    self.expirationDateTime = self.creationTime + relativedelta(months=validForQuantityOfMonths)
    self.transactionFromDateTime = self.creationTime - relativedelta(months=monthsBeforeTheAcceptance)
    self.transactionToDateTime = self.expirationDateTime
    self.statusUpdatedTime = datetime.today()


    # Data Regulation Params
    # Here you can add the params required for a consent ruled by the data regulation
    self.purpose = purpose
    self.specificPurpose = specificPurpose
    self.thirdParySharingPurpose = thirdParySharingPurpose
    self.dataController = dataController
    self.dataSubjectRights = []
    self.dataControllerRights = []
    self.criptographyAlgoritm = criptographyAlgoritm
    self.accessPolicies = accessPolicies
    self.storagePlatform = storagePlatform

    # Log
    log.registerAction('A new consent term was generated, but it was not accepted yet ID: '+str(self.id)+' Current Status: '+str(self.status),COMMUNICATION,PERMISSION)

  # Accept Concent Function
  # This function aims to change the consent status (folloing the Open Baking API guidelines),
  #  update the Data Subject and the Data Controller Rights (following the Data Regulation guidelines)
  def acceptConsent(self,dataSubject,dataController):
    # Consent atrributes
    self.status = AUTHORISED
    self.startDateTime = datetime.today()
    self.statusUpdatedTime = datetime.today()

    # Data that will be shared
    if len(dataSubject.personalData)>0:
      self.personalData = dataSubject.personalData
    
    if len(dataSubject.transactionalData)>0:
      self.transactionalData = dataSubject.transactionalData

    # Data Subject and Data Controller Rights
    self.dataSubjectRights = [DATA_ACCESS,DATA_COPY,DATA_CORRECTION,
                              DATA_ANONYMIZATION,DATA_PORTABILITY,
                              DATA_DELETION,THIRD_PARTY_SHARING,
                              CONSENT_REVOCATION]
    self.dataControllerRights = [DATA_PROCESSING,
                                 DATA_COLLECTING,
                                 DATA_STORING]
    dataController.isProcessing[dataSubject.id]=True

    log.registerAction('Data Subject '+ dataSubject.id +' accepted the consent term',COMMUNICATION,PERMISSION)
    log.registerAction('Data Subject can now have all foressen rights',EXPLANATION,PERMISSION)
    log.registerAction('Data Controller '+ dataController.id +' can process the Data Subject information from '+str(self.startDateTime.date())+' to '+str(self.expirationDateTime.date()),EXPLANATION,PERMISSION)

  # Revoke Concent Function
  # This function aims to change the consent status (folloing the Open Baking API guidelines),
  #  update the Data Subject and the Data Controller Rights (following the Data Regulation guidelines)
  def revokeConsent(self,dataSubject,dataController):
    if CONSENT_REVOCATION not in self.dataSubjectRights:
      log.registerAction('Data Controller '+ dataController.id +' has not an available consent from '+dataSubject.id,EXPLANATION,PERMISSION)
      return False
    
    # Consent atrributes
    self.status = REVOKED
    self.expirationDateTime = datetime.today()
    self.statusUpdatedTime = datetime.today()
    
    # Data Subject and Data Controller Rights
    self.dataSubjectRights = [DATA_ACCESS,DATA_COPY,DATA_CORRECTION,
                              DATA_ANONYMIZATION,DATA_PORTABILITY,
                              DATA_DELETION]
    self.dataControllerRights = [DATA_STORING]
    dataController.isProcessing[dataSubject.id]=False

    log.registerAction('Data Subject '+ dataSubject.id +'  requested to the Data Controller to revoke his/her consent',COMMUNICATION,PROHIBITION)
    log.registerAction('From now, the Data Controller '+ dataController.id +' cannot collect the Data Subject information',COMMUNICATION,PROHIBITION)
    log.registerAction('From now, the Data Controller '+ dataController.id +' cannot process the Data Subject information',COMMUNICATION,PROHIBITION)
    log.registerAction('From now '+str(self.expirationDateTime.date())+', consent '+ str(self.id) +' is not valid to be used by the data controller',EXPLANATION,PROHIBITION)

    return True