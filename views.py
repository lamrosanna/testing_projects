from math import radians
from django.shortcuts import render
import requests
bars=[]
# Create your views here.

def home(request):
        return render(request, 'apitest1/index.html',{
    })
def bar(request): 
    # get location 
    response = requests.get('https://freegeoip.app/json/').json()
    lat = response['latitude']
    lon = response['longitude']
    #get breweries attributed to location
    response2 = requests.get('https://api.openbrewerydb.org/breweries?by_dist='+str(lat)+','+str(lon)+"'").json()
    data={}
    k=0
    #store response
    for item in response2:
        dist = get_dist(lat, lon, float(item['latitude']), float(item['longitude']))
        item['distance']= dist
        pnum = item['phone']
        pformatted = formatPhone(pnum)
        item['phone']= pformatted
        data[k] = item

        k+=1
        #check responses
        print(item['website_url'] )
    #print to page
    return render(request, 'apitest1/bar.html',{
        'barlist': data,
    })

def get_dist(ulat, ulong, blat, blong):
    import math
    coordlat = ulat
    coordlon = ulong
    ulat, ulong, blat, blong = map(radians, [ulat, ulong, blat, blong])
    coord2 = blat, blong
    R = 6371000 #radius of Eath in meters
    deltaphi = blat - ulat
    deltalam = blong - ulong
    a = math.sin(deltaphi/2.0)**2+ math.cos(ulat) * math.cos(blat)*math.sin(deltalam/2.0)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    miles = (R * c)* 0.000621371
    return miles

def formatPhone(x):
    if x is None:
        return "No number listed"
    elif len(x) != 10:
        return "No number listed"
    else:
        phone = x[:3]+'-'+x[3:6]+'-'+x[6:]
        return phone
    #throw error
