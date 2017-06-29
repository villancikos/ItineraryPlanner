
    var mapInitialLocation = { 
        lat: 51.50770709999999, 
        lng: -0.12877930000001925};
    var map, placesService, infoWindow;
    const markers = [];
    var placesSelected = {};
    var hostnameRegexp = new RegExp('^https?://.+?/');
    // debugger;
    // var csrftoken = Cookies.get('csrftoken');
    // initializing Map
    map = new google.maps.Map(document.getElementById("map"), {
        center: mapInitialLocation,
        zoom: 15,
        mapTypeId: "roadmap"
    }); 
    // init container for the place of interest information
    infoWindow = new google.maps.InfoWindow({
        content: document.getElementById('info-content'),
        // TODO: Check why originally is misplaced.
        pixelOffset: new google.maps.Size(-28,0)
    });
    // init placesService instance 
    placesService = new google.maps.places.PlacesService(map);
    // Create the search box and link it to the UI element.
    var input = document.getElementById("pac-input");
    var searchBox = new google.maps.places.SearchBox(input);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
    // Bias the SearchBox results towards current map's viewport.
    map.addListener("bounds_changed", function() {
        searchBox.setBounds(map.getBounds());
    });
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener("places_changed", function() {
        var places = searchBox.getPlaces();
        if (places.length == 0) {
        return;
        }
        // For each place, get the icon, name and location.
        var bounds = new google.maps.LatLngBounds();
        places.forEach(function(place) {
        if (!place.geometry) {
            console.log("Returned place contains no geometry");
            return;
        }
        populateMarkers(place);
        if (place.geometry.viewport) {
            // Only geocodes have viewport.
            bounds.union(place.geometry.viewport);
        } else {
            bounds.extend(place.geometry.location);
        }
        });
        map.fitBounds(bounds);
    });




// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$('#submitPlaceSelection').on('click', function(e) {
    e.preventDefault();
    var csrftoken = Cookies.get('csrftoken');
    console.log(csrftoken);
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    var json_markers = markers.map(function(place){
        return jsonifyPlace(place);
    });
    var new_input = $('#id_placesToVisit').val(json_markers);
    $.ajax({
        type: "POST",
        url: success_url,
        data: new_input,
        success: function(json) {
            // What we receive from success on server side.
            alert("HELL YEAH!");
            console.log(json);
        },
        error: function(json) {
            // in case of error we get this from server
            console.log(json);
        },
    });
});


function jsonifyPlace(marker){
  var $marker_obj = {
    "place_id": marker.placeResult.place_id,
    "is_hotel": false,
    "name": marker.placeResult.name,
    "lat": marker.position.lat(),
    "lng": marker.position.lng(),
  }
  var marker_json = JSON.stringify($marker_obj, null, 4);
  return marker_json;
}

function addPlaceToList(googlePlace) {
    placesSelected[googlePlace.name] = googlePlace;
    // addSelectedPlaceToSidebar(googlePlace);
}

/* 
//Function to create a Mark on the map and assign it
function initMap() {
  var myLatLng = {lat: -25.363, lng: 131.044};

  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: myLatLng
  });

  var marker = new google.maps.Marker({
    position: myLatLng,
    map: map,
    title: 'Hello World!'
  });
}
*/

function addSelectedPlaceToSidebar(googlePlaceMarker){
  // if the place already exists in our list ignore
  var searchedPlaces = document.getElementById('searchedPlaces');
  if (!searchedPlaces.children.length) {
      var ul = document.createElement('ul');
      ul.className = 'list-group';
  }
  else{
      var ul = searchedPlaces.children[0];
  }
  var name = document.createTextNode(googlePlaceMarker.title);
  var li = document.createElement('li');
  li.className = 'list-group-item';
  li.appendChild(name);
  // inserting click event to display on map
  // var marker = new google.maps.Marker({
  //     position: { 
  //         lat: googlePlace.geometry.location.lat(), 
  //         lng: googlePlace.geometry.location.lng() 
  //     }
  // });
  // marker.placeResult = googlePlace;
  // google.maps.event.addListener(marker, "click", showInfoWindow);
  // setTimeout(dropMarker(marker))

  li.addEventListener('click', function() {
    google.maps.event.trigger(googlePlaceMarker, 'click');
    console.log("clicked");
  }, false);

  // li.onclick = function() {
  //   google.maps.event.trigger(marker, "click");
  // };
  ul.appendChild(li); 
  searchedPlaces.appendChild(ul);
}

// Get the place details for a hotel. Show the information in an info window,
// anchored on the marker for the hotel that the user selected.
function showInfoWindow() {
  var marker = this;
  jsonifyPlace(marker);
  console.log("Debugging Marker" , marker);
  placesService.getDetails({ placeId: marker.placeResult.place_id }, 
    function(place,status) {
      if (status !== google.maps.places.PlacesServiceStatus.OK) {
        return;
      }
      infoWindow.open(map, marker);
      buildIWContent(place);
    });
}


// Load the place information into the HTML elements used by the info window.
function buildIWContent(place) {
  document.getElementById("iw-icon").innerHTML =
    '<img class="hotelIcon" ' + 'src="' + place.icon + '"/>';
  document.getElementById("iw-url").innerHTML =
    '<b><a href="' + place.url + '">' + place.name + "</a></b>";
  document.getElementById("iw-address").textContent = place.vicinity;

  if (place.formatted_phone_number) {
    document.getElementById("iw-phone-row").style.display = "";
    document.getElementById("iw-phone").textContent =
      place.formatted_phone_number;
  } else {
    document.getElementById("iw-phone-row").style.display = "none";
  }

  // Assign a five-star rating to the hotel, using a black star ('&#10029;')
  // to indicate the rating the hotel has earned, and a white star ('&#10025;')
  // for the rating points not achieved.
  if (place.rating) {
    var ratingHtml = "";
    for (var i = 0; i < 5; i++) {
      if (place.rating < i + 0.5) {
        ratingHtml += "&#10025;";
      } else {
        ratingHtml += "&#10029;";
      }
      document.getElementById("iw-rating-row").style.display = "";
      document.getElementById("iw-rating").innerHTML = ratingHtml;
    }
  } else {
    document.getElementById("iw-rating-row").style.display = "none";
  }

  // The regexp isolates the first part of the URL (domain plus subdomain)
  // to give a short URL for displaying in the info window.
  if (place.website) {
    var fullUrl = place.website;
    var website = hostnameRegexp.exec(place.website);
    if (website === null) {
      website = "http://" + place.website + "/";
      fullUrl = website;
    }
    document.getElementById("iw-website-row").style.display = "";
    document.getElementById("iw-website").textContent = website;
  } else {
    document.getElementById("iw-website-row").style.display = "none";
  }
}

function populateMarkers(place) {
  //Each found place need an icon.
  var icon = {
    url: place.icon,
    size: new google.maps.Size(80, 80),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(17, 34),
    scaledSize: new google.maps.Size(25, 25)
  };
  // Create marker from place
  var googlePlaceMarker = new google.maps.Marker({
    map: map,
    icon: icon,
    title: place.name,
    position: place.geometry.location,
    animation: google.maps.Animation.DROP,
  });
  // Fill the marker to the global Dict
  googlePlaceMarker.placeResult = place;
  google.maps.event.addListener(googlePlaceMarker, "click", showInfoWindow);
  window.setTimeout(function() {
    markers.push(googlePlaceMarker);
  }, 15000);
  addPlaceToList(place);
  addSelectedPlaceToSidebar(googlePlaceMarker);
  // return googlePlaceMarker;
}

// Helper function to remove all the markers from the map.
function clearOldMarkers(){
  // Clear out the old markers.
    markers.forEach(function(marker) {
      marker.setMap(null);
    });
    markers = [];
}



