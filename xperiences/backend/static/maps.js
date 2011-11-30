/**
 * Created by PyCharm.
 * User: roi
 * Date: 18/10/11
 * Time: 13:05
 * To change this template use File | Settings | File Templates.
 */

var maps = new Array();
var geocoder = new google.maps.Geocoder();

$.prototype.geopicker = function(params)
{
    var defaults = {};
    params = params || {};
//    Object.update(params,defaults);
//    defaults.update(params);
    var elm = $(this);
    var address_input = defaults['address_field'];
    if(!address_input)
        address_input = elm.attr('address_field');
    var map;
    var init = function()
    {
        var num = Number(new Date());
        var id = 'map' + num;
        $('<div>Update</div>').insertAfter(elm).click(function(){
            var loc = map.getCenter();
            update_location(loc);
        });
        $('<div class="geopicker_map" id="' + id + '"></div>').insertAfter(elm);
        var latlng = elm.val() || '0,0';
        var center = { lat: latlng.split(',')[0], lng: latlng.split(',')[1]};
        map = init_map(id,center,true,update_location);
        if(address_input)
            address_autocomplete(address_input,id, function(location) {
                update_location(location.geometry.location);
            });
    };

    var update_location = function(loc)
    {
        var lat = loc.lat();
        var lng = loc.lng();
        elm.val(lat + ',' + lng);
    };
    
    init();
};

$(document).ready(function()
{
   $('.geopicker').geopicker();
});

function init_map( id , center ,editable,location_changed){
      if (!center) center = new google.maps.LatLng(-34.397, 34.644);
      else center = new google.maps.LatLng(center.lat, center.lng);
      var myOptions = {
        zoom: 8,
        center: center,
        mapTypeId: google.maps.MapTypeId.ROADMAP
      }
      var map = new google.maps.Map(document.getElementById( id ), myOptions);
      maps[ id ] = map;
      var  marker = new google.maps.Marker({
            map: map,
            position: center
        });
    if(editable)
    {
        marker.setDraggable(true);
         google.maps.event.addListener(marker, 'dragend', function(me) {
             if(location_changed)
                location_changed(me.latLng);
        });
    }
     return map;
}

function get_map(id){
    return maps[id];
}

function stringToLocation( str ){
    str = str.replace("(","").replace(")","").replace(" ","");
    str = str.split(",");
    return new google.maps.LatLng(str[ 0 ], str[ 1 ] );
}
function addMarker( map, loc , marker_icon  , tooltip , link ){
    if ( ! marker_icon ) marker_icon = "http://www.google.com/mapfiles/marker.png";
    var marker = new google.maps.Marker({
                                      position: loc,
                                      map: map,
                                      title:tooltip ,
                                      icon: marker_icon
                                    });
    if (link) {
            google.maps.event.addListener(marker, 'click', function() {
                window.location = link;
            });
    }
}

function getLocation(lat , lng){
    return  new google.maps.LatLng( lat, lng );
}
function centerMap( map_id , loc ){
    var map = get_map( map_id );
    map.setCenter( loc);
}

function init_street_view( id , center ){
    var panoramaOptions = {
      position: center,
      pov: {
        heading: 0,
        pitch: 10,
        zoom: 1
      }
    };
    var panorama = new  google.maps.StreetViewPanorama(document.getElementById(id),panoramaOptions);
    //map.setStreetView(panorama);   //   <=== May be needed...
}

function getLocationFromAdrs( address , suc_callback , failed_callback){
        geocoder.geocode( { 'address': address}, function(results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                     var loc = results[0].geometry.location;
                     suc_callback(loc);
          }
          else
          {
                if (failed_callback)  failed_callback(status);
          }
        });
}

function address_autocomplete( input_id , map_id ,changed_callback){
    var input =document.getElementById( input_id );
    var ac = new google.maps.places.Autocomplete(input);
    google.maps.event.addListener(ac, 'place_changed', function() {
        var place = ac.getPlace();
        if (map_id){
            var map = get_map( map_id );
            if (place.geometry.viewport) {
                    map.fitBounds(place.geometry.viewport);
            } else {
                map.setCenter(place.geometry.location);
                map.setZoom(17);
            }
        }
        if ( changed_callback ) changed_callback( place );
    });
}


