#!/usr/bin/env python
#
# this is a modified version of the Google App Engine Tutorial
import webapp2, os, urllib, json, urllib, urllib2, jinja2, random

def safeGet(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print "The server couldn't fulfill the request." 
        print "Error code: ", e.code
    except urllib2.URLError, e:
        print "We failed to reach a server"
        print "Reason: ", e.reason
    return None

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values={}
        template = JINJA_ENVIRONMENT.get_template('start.html')
        self.response.write(template.render(template_values))
        
class GoForm(webapp2.RequestHandler):
    def get(self):
        template_values={}
        template = JINJA_ENVIRONMENT.get_template('goform.html')
        self.response.write(template.render(template_values))
   
class TripResponseHandler(webapp2.RequestHandler):
    def post(self):
        vals={}
        vals['page_title']='Roadtrip Results'
        start = self.request.get('origin')
        stop = self.request.get('destination')
        vals['start']=start
        vals['stop']=stop
        if stop:
            result = maps(origin=start, destination=stop)
            json_result = result.read()
            locations = json.loads(json_result)
            vals['duration']=locations['routes'][0]['legs'][0]['duration']['text']
            coordinates=[{'lat':0, "lng":0}]
            steps = locations['routes'][0]['legs'][0]
            vals['start_lat'] = steps['start_location']['lat']
            vals['start_lng'] = steps['start_location']['lng']
            vals['end_lat'] = steps['end_location']['lat']
            vals['end_lng'] = steps['end_location']['lng']
            for step in steps['steps']:
                if abs(step['end_location']['lat']-coordinates[-1]['lat']) >= 0.01:
                    coordinates.append(step['end_location'])
            del coordinates[0]
            weather = []
            baseurl='https://api.darksky.net/forecast/'
            api_key='fc3abee9d0946c4aed4800af3784195e'
            for item in coordinates:
                url = baseurl+api_key+'/%s,%s'%(item['lat'], item['lng'])
                result = urllib2.urlopen(url)
                json_result = result.read()
                r = json.loads(json_result)
                weather.append(r)
            temps=[]
            alerts={}
            for forecast in weather:
                if forecast.has_key('alerts'):
                    for alert in forecast['alerts']:
                        alerts[alert['title']] = alert['description']
                    vals['alert']=alerts
                temps.append(forecast['currently']['apparentTemperature'])
                temps.sort()
            low = temps[0]
            high = temps[-1]
            vals['low']=low
            vals['high']=high
            locations = []
            place_type = self.request.get_all('place_type')
            del coordinates[0]
            for item in coordinates:
                baseurl='https://maps.googleapis.com/maps/api/place/nearbysearch/json'
                parameters={}
                parameters['key']='AIzaSyDdz8U4SjNc8mxD1z3Rg5jLGVXqWQt-Z5E'
                parameters['keyword']=place_type
                parameters['rankby']='prominence'
                url = baseurl + '?location=%s,%s&'%(item['lat'],item['lng']) + urllib.urlencode(parameters)
                result = urllib2.urlopen(url)
                json_result = result.read()
                r = json.loads(json_result)
                locations.append(r)
            IDs = []
            for item in locations:
                for place in item['results']:
                    IDs.append(place['place_id'])
            places={}
            latlng=[]
            final_list = random.sample(IDs, 10)
            for item in final_list:
                url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=%s&key=AIzaSyDdz8U4SjNc8mxD1z3Rg5jLGVXqWQt-Z5E'%(item)
                result = urllib2.urlopen(url)
                json_result = result.read()
                r = json.loads(json_result)
                places[r['result']['url']] = r['result']['name']
                latlng.append(r['result']['geometry']['location']['lat'])
                latlng.append(r['result']['geometry']['location']['lng'])
            vals['lat1']=latlng[0]
            vals['lng1']=latlng[1]
            vals['lat2']=latlng[2]
            vals['lng2']=latlng[3]
            vals['lat3']=latlng[4]
            vals['lng3']=latlng[5]
            vals['lat4']=latlng[6]
            vals['lng4']=latlng[7]
            vals['lat5']=latlng[8]
            vals['lng5']=latlng[9]
            vals['lat6']=latlng[10]
            vals['lng6']=latlng[11]
            vals['lat7']=latlng[12]
            vals['lng7']=latlng[13]
            vals['lat8']=latlng[14]
            vals['lng8']=latlng[15]
            vals['lat9']=latlng[16]
            vals['lng9']=latlng[17]
            vals['lat10']=latlng[18]
            vals['lng10']=latlng[19]                
            vals['latlng'] = latlng
            vals['places'] = places
            template = JINJA_ENVIRONMENT.get_template('tripresults.html')
            self.response.write(template.render(vals))
            
        else:
            vals['prompt'] = "Please enter locations"
            template = JINJA_ENVIRONMENT.get_template('goform.html')
            self.response.write(template.render(vals))


def maps(baseurl='https://maps.googleapis.com/maps/api/directions/json', 
    api_key='AIzaSyB3BijuXXmX-wiGETlgWFeEgHDKTWy75Hg', origin='',
    destination='', params={}):
    params['origin']=origin
    params['destination']=destination
    params['key']=api_key
    url = baseurl+'?'+urllib.urlencode(params)
    return safeGet(url)

application = webapp2.WSGIApplication([ \
                                      ('/tripresults', TripResponseHandler),
                                      ('/goform', GoForm),
                                      ('/.*', MainHandler)
                                      ],
                                     debug=True)

