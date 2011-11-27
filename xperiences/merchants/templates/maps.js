/**
 * Created by PyCharm.
 * User: roi
 * Date: 18/10/11
 * Time: 13:05
 * To change this template use File | Settings | File Templates.
 */

var maps = new Array();
var geocoder = new google.maps.Geocoder();


function init_map( id , center ){
      if (!center) center = new google.maps.LatLng(-34.397, 34.644);
      var myOptions = {
        zoom: 8,
        center: center,
        mapTypeId: google.maps.MapTypeId.ROADMAP
      }
      var map = new google.maps.Map(document.getElementById( id ), myOptions);
      maps[ id ] = map;
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


