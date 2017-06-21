var bigBen = { lat: 51.510357, lng: -0.116773 };
window.onload = function() {
  initAutocomplete();
};
var placesSelected = {};
function addPlaceToList(googlePlace) {
    placesSelected[googlePlace.title] = googlePlace;
    addSelectedPlaceToSidebar(googlePlace);
    console.log(placesSelected);
}

function addSelectedPlaceToSidebar(googlePlace){
    // properties I want:
    // title, position.lat, position.lng.
    var searchedPlaces = document.getElementById('searchedPlaces');
    if (!searchedPlaces.children.length) {
        var ul = document.createElement('ul');
        ul.className = 'list-group';
    }
    else{
        var ul = searchedPlaces.children[0];
    }
    var name = document.createTextNode(googlePlace.title);
    var li = document.createElement('li');
    li.className = 'list-group-item';
    li.appendChild(name);
    ul.appendChild(li);
    searchedPlaces.appendChild(ul);
}

function initAutocomplete() {
  var map = new google.maps.Map(document.getElementById("map"), {
    center: bigBen,
    zoom: 13,
    mapTypeId: "roadmap"
  });

  // Create the search box and link it to the UI element.
  var input = document.getElementById("pac-input");
  var searchBox = new google.maps.places.SearchBox(input);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  // Bias the SearchBox results towards current map's viewport.
  map.addListener("bounds_changed", function() {
    searchBox.setBounds(map.getBounds());
  });

  var markers = [];
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener("places_changed", function() {
    var places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }

    // Clear out the old markers.
    markers.forEach(function(marker) {
      marker.setMap(null);
    });
    markers = [];

    // For each place, get the icon, name and location.
    var bounds = new google.maps.LatLngBounds();
    places.forEach(function(place) {
      if (!place.geometry) {
        console.log("Returned place contains no geometry");
        return;
      }
      var icon = {
        url: place.icon,
        size: new google.maps.Size(80, 80),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25)
      };
      var googlePlace = new google.maps.Marker({
        map: map,
        icon: icon,
        title: place.name,
        position: place.geometry.location
      });
      addPlaceToList(googlePlace);
      // Create a marker for each place.
      markers.push(
        new google.maps.Marker({
          map: map,
          icon: icon,
          title: place.name,
          position: place.geometry.location
        })
      );

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
  });
}
