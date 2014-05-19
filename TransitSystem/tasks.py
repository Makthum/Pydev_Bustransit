from __future__ import absolute_import
import urllib
from celery import task
from TransitSystem import gtfs_realtime_pb2
from TransitSystem.models import Trips, Routes, VehiclePositions
import django.core.exceptions
from django.core.exceptions import ObjectDoesNotExist

__author__ = 'zarroc'


@task(name='loadrealtimedata')
def load_realtime():
    files=urllib.urlretrieve("http://rtu.york.ca/gtfsrealtime/VehiclePositions","/home/zarroc/workspace/bustransit/Bustransit/TransitSystem/VehiclePositions")
    print files[0]
    print files[1]
    print "File Downloaded"
    f = open("/home/zarroc/workspace/bustransit/Bustransit/TransitSystem/VehiclePositions", "rb")
    data=gtfs_realtime_pb2.FeedMessage()
    data.ParseFromString(f.read())
    for entity in data.entity:
        ventity=entity.vehicle
        try:
            print ventity.trip.trip_id
            trip=Trips.objects.get(trip_id=ventity.trip.trip_id)
            if ventity.trip.route_id !="":
                route=Routes.objects.get(route_id=ventity.trip.route_id)
            if trip.trip_id==599516:
                print ventity.position.latitude
                print ventity.position.longitude
            vp=VehiclePositions.objects.filter(trip_id=trip.trip_id)
            if not vp.exists():
                vp=VehiclePositions(route_id=None,trip_id=trip,p_latitude=ventity.position.latitude,p_longitude=ventity.position.longitude,p_bearing=ventity.position.bearing,p_speed=ventity.position.speed)
            else:
                vp=vp[0]
                vp.p_latitude=ventity.position.latitude
                vp.p_longitude=ventity.position.longitude
                vp.p_bearing=ventity.position.bearing
                vp.p_speed=ventity.position.speed
            vp.save()
        except ObjectDoesNotExist:
            print "trip id not found"
            
