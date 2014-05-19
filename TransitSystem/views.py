# Create your views here.
from datetime import datetime


from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from TransitSystem.forms import SearchForm
from models import VehiclePositions, Trips, Routes, StopTimes


@login_required
def home(request):
    return render_to_response('index.html')

@login_required
def findbus(request):
    form=SearchForm(request.POST)
    return render_to_response('findbus.html',{'form':form},context_instance=RequestContext(request))

def searchbus(request):
    if "routeNo" in request.GET:
        tripdetails=[]
        date=request.GET['searchdate']
        time=request.GET['searchtime']
        print date
        dayofweek=datetime.strptime(date,'%Y/%m/%d').weekday()
        if dayofweek<5:
            serviceid=1
        elif dayofweek==6:
            serviceid=2
        else:
            serviceid=3
        print type(time)
        routes=Routes.objects.filter(route_short_name=request.GET['routeNo'])
        for route in routes:
            trips=Trips.objects.filter(route_id=route.route_id,service_id=serviceid)
            for trip in trips:
                result={}
                stops=StopTimes.objects.filter(trip_id=trip.trip_id,stop_sequence=1,arrival_time__gt=time)
                for stop in stops:
                    result['tripName']=trip.trip_headsign
                    result['trip_id']=trip.trip_id
                    result['startTime']=stop.arrival_time
                if result:
                    tripdetails.append(result)
    return render_to_response('results.html',{'stop_times':tripdetails})


def schedule(request):
    if "trip_id" in request.GET:
        stoptimes=[]
        trip_id=request.GET['trip_id']
        schedules=StopTimes.objects.filter(trip_id=trip_id)
        for schedule in schedules:
            stoptime={}
            print schedule.stop_id
            stoptime["stop_name"]=schedule.stop_id.stop_name
            stoptime["arrival_time"]=schedule.arrival_time
            stoptime["departure_time"]=schedule.departure_time
            stoptimes.append(stoptime)
        print stoptimes
    return render_to_response('schedule.html',{'stoptimes':stoptimes})

def locate(request):
    trip_id=request.GET['trip_id']
    stoplocs=StopTimes.objects.filter(trip_id=trip_id)
    if stoplocs:
        stop_locations=[]
        for stoploc in stoplocs:
            stops={}
            stops['lat']=stoploc.stop_id.stop_lat
            stops['lon']=stoploc.stop_id.stop_lon
            stop_locations.append(stops)
    print trip_id
    vp=VehiclePositions.objects.filter(trip_id=trip_id)
    vehiclepos={}
    if vp:
        vehicleposition=vp[0];
        vehiclepos['lat']=vehicleposition.p_latitude
        vehiclepos['lon']=vehicleposition.p_longitude
    return render_to_response('locate.html',{'stoplocations':stop_locations,'vp':vehiclepos})
