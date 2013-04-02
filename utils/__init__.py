#===============================================================================
# Script provided by Vinod Halaharvi ( vinod.halaharvi@rtpnet.net, vinod.halaharvi@gmail.com )
# RTP Network Services, Inc. / 904-236-6993 ( http://www.rtpnet.net )
# DESCRIPTION: "Makes working with HQApi XML response feel like you are working with Python dict"
#===============================================================================
import xmltodict, json
import sys, os
import collections
import pprint


#get_using_rest
def get_using_rest(url):
  import urllib2, base64
  assert os.environ["hyperic_username"], "Error \n 'hyperic_username' environment variable not found\nPlease make sure you export 'hyperic_username' environment variable in your .bashrc"
  assert os.environ["hyperic_password"], "Error \n 'hyperic_password' environment variable not found\nPlease make sure you export 'hyperic_password' environment variable in your .bashrc"
  assert 'hq' not in os.environ["hyperic_username"], "You cannot use hq account username and/or password to run this script\n Please use your local ldap hyperic username and ldap password\n"
  assert 'csx' not in os.environ["hyperic_password"], "You cannot use hq account username and/or password  to run this script\n Please use your local ldap hyperic username and ldap password\n"
  username=os.environ["hyperic_username"]
  password=os.environ["hyperic_password"]
  base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
  request = urllib2.Request(url.replace(' ', '%20'))
  request.add_header("Authorization", "Basic %s" % base64string)
  result = urllib2.urlopen(request)
  return  result.read()
    

'''
 Class to get HqApiPyObject
'''  
class HqApiPyObject(dict):
  def __init__(self, xml):
    if isinstance(xml, dict):
      self.data = xml
    elif isinstance(xml, str) or isinstance(xml, unicode):
      import xmltodict
      self.data = self.todict(xmltodict.parse(xml))
      self.xml = xml
    else: 
      raise TypeError("Input should be either of type, <type dict> or of type <type string>")
    super(HqApiPyObject, self).__init__(self.data)
    
  '''
   Convert xml input to python dictionary
  ''' 
  def todict(self, input):
    if isinstance(input, list):
      return [self.todict(item) for item in input]
    elif isinstance(input, collections.OrderedDict):
      return HqApiPyObject({self.todict(key): self.todict(value) for key, value in input.items()})
    elif isinstance(input, unicode):
      return input.encode('ascii')

  
  '''
    convert HqApiPyObject or python dict back to xml
  '''  
  def toxml(self, input):
    if isinstance(input, list):
      return [self.todict(item) for item in input]
    elif isinstance(input, collections.OrderedDict):
      return HqApiPyObject({self.todict(key): self.todict(value) for key, value in input.items()})
    elif isinstance(input, unicode):
      return input.encode('ascii')      
      
  '''
    attribute override
  '''
  def __getattr__(self, name):
    try:
      if isinstance(self[name], dict):
        return HqApiPyObject(self[name])
      else:
        return self[name]
    except:
      raise AttributeError
      #return None
  
  def pprint(self, *args, ** kwargs):
    import pprint
    pp = pprint.PrettyPrinter(*args, ** kwargs)
    pp.pprint(self)

