from django.shortcuts import render
import json
import urllib2

# Create your views here.
def zabbix_gethost(request):
    url = "http://192.168.2.223:8088/zabbix/api_jsonrpc.php"
    header = {"Content-Type": "application/json"}
    # request json
    data = json.dumps(
    {
        "jsonrpc":"2.0",
        "method":"host.get",
        "params":{
            "output":["hostid","name"],
            "filter":{"host":""}
        },
        "auth":"53d62c997028888714caa69b0a890ecf",
        "id":1,
    })
    # create request object
    request = urllib2.Request(url,data)
    for key in header:
        request.add_header(key,header[key])
    # get host list
    try:
        result = urllib2.urlopen(request)
    except URLError as e:
        if hasattr(e, 'reason'):
            return render(request,'zabbixhosts.html',{'We failed to reach a server.Reason': e.reason})
        elif hasattr(e, 'code'):
            return render(request,'zabbixhosts.html',{'The server could not fulfill the request.Error code': e.code})
    else:
        response = json.loads(result.read())
        result.close()
        return render(request,'zabbixhosts.html',{'Number Of Hosts': len(response['result'])})

    for host in response['result']:
        return render(request,'zabbixhosts.html', {'Host': host['hostid'], 'Host_Name':host['name']})


class GetGrapidAPIView(View):

    def get(self, request, hostid):
        try:
            hostinfo = GameHost.objects.using('res').get(id=hostid)
            if hostinfo.platid == 34:
                hostip = hostinfo.ip2
            else:
                hostip = hostinfo.ip1
            print "hostip: %s" % hostip

            ret = []
            for key in ['system.cpu.util[,idle]', 'net.if.in[eth0]|net.if.in[em1]', 'vm.memory.size[available]', 'icmpping']:
                if '|' in key:
                    key1, key2 = key.split('|')
                    #获取itemid：
                    itemid = Items.objects.using('zab').get(Q(key_field=key1)|Q(key_field=key2), hostid__host=hostip).itemid
                else:
                    #获取itemid：
                    itemid = Items.objects.using('zab').get(key_field=key, hostid__host=hostip).itemid
                print "itemid: %s" % itemid
                graphitems = GraphsItems.objects.using('zab').filter(itemid=itemid)[0]
                graphid = graphitems.graphid.graphid
                print "graphid: %s" % graphid
                ret.append(graphid)
        except Exception,e:
            print e
            ret = []
        return HttpResponse(json.dumps(ret))