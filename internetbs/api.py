import requests
from urllib.parse import quote

class ApiWrapper():
    """
        A simple wrapper for domain registrant internetbs.net
    """

    VALID_DNS_RECORD_TYPES = {'A', 'AAAA', 'DYNAMIC', 'CNAME', 'MX', 'SRV', 'TXT', 'NS'}
    def __init__ (self, key = None, password = None):
        """
            Instantiates a wrapper object. If no key or password are provided, test credentials are used.
        """
        self.KEY = key or 'testapi'
        self.PASSWORD = password or 'testpass'
        self.URL = 'https://api.internet.bs/'
        # assume we use test credential if none were provided
        if not key or not password:
            self.URL = 'https://testapi.internet.bs'
    
    def __perform_get_request (self, endpoint, params=dict()):
        credentials = {
            'ApiKey' : self.KEY,
            'Password' : self.PASSWORD
        }

        full_params = {
            'ResponseFormat' : 'JSON'
        }
        
        full_params.update(credentials)
        full_params.update(params)

        #or k,v in full_params.items():
        #    full_params[k] = quote(v)

        endpoint = self.URL + endpoint
        response = requests.get(endpoint , params = full_params)

        return response

    
    
    def domain_check(self, domain, raw=False):
        """
            The command is intended to check whether a domain is available for registration or not. The command is not generating any cost.
        """
        endpoint = '/Domain/Check'
        
        params = {
            'Domain' : domain,
        }

        response = self.__perform_get_request(endpoint, params)

        if response.status_code == 200:
            parsed_response = response.json()
            if raw:
                return parsed_response
            else:
                return parsed_response.get('status') == 'AVAILABLE'             
    
    def domain_create(self, domain, contact_info, raw=True, **kwargs):
        """
            The command is intended to register a new domain
        """
        endpoint = '/Domain/Create'

        params = {
            'Domain' : domain
        }

        params.update(contact_info)
        params.update(kwargs)

        response = self.__perform_get_request(endpoint, params)

        if response.status_code == 200:
            parsed_response = response.json()
            if raw:
                return parsed_response
            else:
                return parsed_response['product'][0]['status'] == 'SUCCESS'
    
    def domain_update(self, domain, contact_info, raw=True, **kwargs):
        """
        
        The command is intended to update a domain, including Registrant Contact, Billing Contact, Admin
        Contact, Tech. Contact, registrar locks status, epp auth info, name servers, private whois status, etc...
        
        The command takes exactly the same parameters as domain_create, however only Domain ismandatory, 
        all other parameters are optional and you can update one or more of them at once.
        
        """
        endpoint = '/Domain/Update'

        params = {
            'Domain' : domain
        }

        params.update(contact_info)
        params.update(kwargs)

        response = self.__perform_get_request(endpoint, params)

        if response.status_code == 200:
            parsed_response = response.json()
            if raw:
                return parsed_response
            else:
                return parsed_response['product'][0]['status'] == 'SUCCESS'
    def domain_info(self, domain):

        """
            The command is intended to return full details about a domain name; it includes contact details,
            registrar lock status, private whois status, name servers and so on. 
        """
        endpoint = '/Domain/Info'

        params = {
            'Domain' : domain
        }

        response = self.__perform_get_request(endpoint, params)
        
        if response.status_code == 200:
            parsed_response = response.json()
            return parsed_response
    
    def host_create(self, host, ip_list, raw=True):
        """
            The command is intended to create a host also known as name server or child host.
            
            The host will be created under the same Registry the domain belongs to (.com host under .com
            Registry, .net host under .net Registry, .biz host under .biz Registry and so on...).
            
            You do not need to create a host under a different Registry from the domain extension of the host
            itself as we automatically create it whenever needed. For example you only need to create a host if
            you wish to declare the new name server ns1.example.com under the .com Registry, while you can
            freely use ns1.example.com under any other extension such as .uk or .biz or .info or .fr, etc...
            
            Note that if you are using existing hosts (name servers) already created by your hosting company or
            another Registrar, you won’t need to create them again, actually you won’t even be able to create
            them as you have no authority for the root domain. You can only create hosts for domains that belong
            to you and are managed by us.
        """

        endpoint = '/Domain/Host/Create'

        params = {
            'Host' : host,
            'IP_List' : ",".join(ip_list)
        }

        response = self.__perform_get_request(endpoint, params)

        if response.status_code == 200:
            parsed_response = response.json()
            if raw:
                return parsed_response
            else:
                return parsed_response.get('status') == 'SUCCESS'
    
    def host_info(self, host):
        """
            The command is intended to retrieve existing host (name server) information for a specific host.
        """

        endpoint = '/Domain/Host/Info'

        params = {
            'Host' : host,
        }
        
        response = self.__perform_get_request(endpoint, params)

        if response.status_code == 200:
            parsed_response = response.json()
            return parsed_response

    def host_delete(self, host):
        """
            The command is intended to delete (remove) an unwanted host. Note if your host is currently used
            by one or more domains the operation will fail.
        """

        endpoint = '/Domain/Host/Delete'

        params = {
            'Host' : host,
        }
        
        response = self.__perform_get_request(endpoint, params)

        if response.status_code == 200:
            parsed_response = response.json()
            return parsed_response
    
    def host_update(self, host, ip_list, raw=True):
        """
            The command is intended to update a host; the command is replacing the current list of IP for the
            host with the new one you provide. It is accepting the same parameters as host_create and
            will return the same results.
        """

        endpoint = '/Domain/Host/Update'

        params = {
            'Host' : host,
            'IP_List' : ",".join(ip_list)
        }

        response = self.__perform_get_request(endpoint, params)

        if response.status_code == 200:
            parsed_response = response.json()
            if raw:
                return parsed_response
            else:
                return parsed_response.get('status') == 'SUCCESS'
    
    def dns_add(self, full_record_name, record_type, value=None, raw=False, **kwargs):
        """
            The command is intended to add a new DNS record to a specific zone (domain).
        """

        endpoint = '/Domain/DnsRecord/Add'

        params = {
            'FullRecordName' : full_record_name,
            'Type': record_type,
        }

        params.update(kwargs)

        if record_type not in VALID_DNS_RECORD_TYPES:
            raise ValueError("Accepted values for this argument are: A, AAAA, DYNAMIC, CNAME, MX, SRV, TXT and NS")

        if not value and record_type != 'DYNAMIC':
            raise ValueError("All records except DYNAMIC must have their value")
        
        if record_type == 'DYNAMIC':
            if not kwargs.has_key('DynDnsLogin') or not kwargs.has_key('DynDnsPassword'):
                raise ValueError('DynDNS login and password are required when record type is DYNAMIC')

        if value:
            params['Value'] = value
        
        response = self.__perform_get_request(endpoint, params)

        if response.status_code == 200:
            parsed_response = response.json()
            if raw:
                return parsed_response
            else:
                return parsed_response.get('status') == 'SUCCESS'

    def dns_remove(self, full_record_name, record_type, value=None, raw=False, **kwargs):
        """
            The command is intended to remove a DNS record from a specific zone.
            While the command accepts the same parameters as /Domain/DnsRecord/Add, you only need to pass
            the credentials (API Key and Password), the FullRecordName and Type, all other parameters are
            optional and are required only when there is a possibility of ambiguity, example you may have
            multiple A record for www.example.com for load balancing purposes, consequently you need to pass
            the Value parameter in order to remove the correct A record. If you do not pass any optional
            parameter all matching FullRecordName for the specific Type will be removed.
        """

        endpoint = '/Domain/DnsRecord/Remove'

        params = {
            'FullRecordName' : full_record_name,
            'Type': record_type,
        }

        params.update(kwargs)

        if record_type not in VALID_DNS_RECORD_TYPES:
            raise ValueError("Accepted values for this argument are: A, AAAA, DYNAMIC, CNAME, MX, SRV, TXT and NS")

        if value:
            params['Value'] = value
        
        response = self.__perform_get_request(endpoint, params)

        if response.status_code == 200:
            parsed_response = response.json()
            if raw:
                return parsed_response
            else:
                return parsed_response.get('status') == 'SUCCESS'

        

    def dns_update(self, full_record_name, record_type, value=None, raw=False, **kwargs):
        """
            The command is intended to update an existing DNS record.
            Only the credentials (API Key and Password), FullRecordName, Type and NewValue are required, all
            other parameters are only needed if there is a risk of ambiguity, in particular when you have advanced
            DNS record used for load balancing. We recommend to always passing as many optional parameters
            as possible to avoid updating a different record from the one that you originally intended to
        """

        endpoint = '/Domain/DnsRecord/Update'

        params = {
            'FullRecordName' : full_record_name,
            'Type': record_type,
        }

        params.update(kwargs)


        if record_type not in VALID_DNS_RECORD_TYPES:
            raise ValueError("Accepted values for this argument are: A, AAAA, DYNAMIC, CNAME, MX, SRV, TXT and NS")

        if not value and record_type != 'DYNAMIC':
            raise ValueError("All records except DYNAMIC must have their value")
        
        if record_type == 'DYNAMIC':
            if not kwargs.has_key('DynDnsLogin') or not kwargs.has_key('DynDnsPassword'):
                raise ValueError('DynDNS login and password are required when record type is DYNAMIC')

        if value:
            params['Value'] = value
        
        response = self.__perform_get_request(endpoint, params)

        if response.status_code == 200:
            parsed_response = response.json()
            if raw:
                return parsed_response
            else:
                return parsed_response.get('status') == 'SUCCESS'
