from hyperic.utils import HqApiPyObject
from hyperic.utils import get_using_rest


hqhost='localhost'
platform='hostname.domainname.com'

# Get HqApiPyObject from xml
url='http://%s:7080/hqu/hqapi1/resource/get.hqu?platformName=%s&children=true&verbose=true' % (hqhost, platform)


# For this function to work you need to set two environment variables,  hyperic_username, hyperic_password for eg.
# hyperic_username=<<yourusername>>; export hyperic_username
# hyperic_password=<<yourpassword>>; export hyperic_password
xml = get_using_rest(url)
hqapi = HqApiPyObject(xml)

#Using generator approach
for resource in  hqapi.ResourceResponse.Resource.Resource:
    print resource
    print
