import socket
import urllib.parse
import urllib.request
import json

def getMyIp():
    domain = "tonio-peng.tpddns.cn"
    myaddr = socket.getaddrinfo(domain, 'http')
    myip = myaddr[0][4][0]
    return myip

def initReq(url, values):
    '''
    simple request data from url with values
    '''
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data)
    try:
        res = urllib.request.urlopen(req)
    except:
        raise
    return res



DNSPOD_TOKEN = ''
if os.environ.get('DNSPOD_TOKEN', '') != '':
       DNSPOD_TOKEN = os.environ['DNSPOD_TOKEN']


update_domain = "tonio-peng.top"
DomainListUrl = 'https://dnsapi.cn/Domain.List'
RecordListUrl = 'https://dnsapi.cn/Record.List'
RecordDdnsUrl = 'https://dnsapi.cn/Record.Ddns'
loginInfo = {
'login_token':DNSPOD_TOKEN,
'format': 'json'
}
res = initReq(url=DomainListUrl, values=loginInfo)
i_list=json.loads(res.read().decode())['domains']
domainIDs = {i['name']:i['id'] for i in i_list}

res = initReq(url=RecordListUrl, values={
**loginInfo, **{'domain_id': domainIDs.get(update_domain)}})
i_list = json.loads(res.read().decode())['records']
subdomainInfo = {((i['name'], i['line']) if i['type'] == 'A' else ('invalid', 'invalid')):
                 {'IP': i['value'], 'ID': i['id']}
                 for i in i_list}



updated_ip = getMyIp()
http_data =[{
                **loginInfo,
                **{
                    'domain_id':domainIDs.get(update_domain) ,
                    'record_id': subdomainInfo[('www', '默认')]['ID'],
                    'record_line': '默认',
                    'sub_domain': 'www',
                    'value': updated_ip
                }
            },
{
    **loginInfo,
    **{
        'domain_id':domainIDs.get(update_domain) ,
        'record_id': subdomainInfo[('@', '默认')]['ID'],
        'record_line': '默认',
        'sub_domain': '@',
        'value': updated_ip
    }
}
]
for item in http_data:
    try:
        initReq(url=RecordDdnsUrl, values=item)
    except:
        pass
res = initReq(url=RecordListUrl, values={
**loginInfo, **{'domain_id': domainIDs.get(update_domain)}})
i_list = json.loads(res.read().decode())['records']
subdomainInfo = {((i['name'], i['line']) if i['type'] == 'A' else ('invalid', 'invalid')):
                 {'IP': i['value'], 'ID': i['id']}
                 for i in i_list}


