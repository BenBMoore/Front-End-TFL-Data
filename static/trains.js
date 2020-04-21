
var map = new mapboxgl.Map({
  container: 'map',
  style: "https://api.maptiler.com/maps/6c5b0dc0-4399-4516-824d-236ab6058258/style.json?key=EZK0qr5GcGShEW6ZFEBA",
  zoom: 10,
  center: [
    -0.088899,
    51.513356
  ]
});
map.loadImage("/static/underground.png", function (error, image) {
  if (error) throw error;
  map.addImage("custom-marker", image);
});

var lines_url = 'http://127.0.0.1:5000/tube-lines';
var stations_url = 'http://127.0.0.1:5000/tube-stations'
var trains_url = 'http://127.0.0.1:5000/tube-trains'

map.on('load', function () {
  /* Style layer: A style layer ties together the source and image and specifies how they are displayed on the map. */
  map.resize();
  map.addSource('tubeLines', { type: 'geojson', data: lines_url });
  map.addLayer({
    'id': 'tubeLines',
    'type': 'line',
    'source': 'tubeLines',
    'paint': {
      'line-width': 2,
      'line-color': ['get', 'color']
    }
  });

  map.addSource('tubeStations', { type: 'geojson', data: stations_url });
  map.addLayer({
    'id': 'tubeStations',
    'type': 'circle',
    'source': 'tubeStations',
    'paint': {
      'circle-radius': 2,
      'circle-color': "#FFFFFF"
    }

  });

  map.on('click', 'tubeStations', function (e) {
    console.log(e.features[0])
    var coordinates = e.features[0].geometry.coordinates.slice();
    var description = e.features[0].properties.description;

    // Ensure that if the map is zoomed out such that multiple
    // copies of the feature are visible, the popup appears
    // over the copy being pointed to.
    while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
      coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
    }
    new mapboxgl.Popup()
      .setLngLat(coordinates)
      .setHTML(description)
      .addTo(map);
  });
  // Change the cursor to a pointer when the mouse is over the places layer.
  map.on('mouseenter', 'tubeStations', function () {
    map.getCanvas().style.cursor = 'pointer';
  });

  // Change it back to a pointer when it leaves.
  map.on('mouseleave', 'tubeStations', function () {
    map.getCanvas().style.cursor = '';
  });

  pull_latest_train_info()

});

var markersArray = []
function pull_latest_train_info() {

  axios.get(trains_url)
    .then(function (response) {
      // handle success
      animationSteps = 0
      response.data.features.forEach(function (train) {
        if (markersArray.find(marker => marker.id === train.properties.title) === undefined) {
          var el = document.createElement('div');
          el.className = 'marker';

          let trainObj = new mapboxgl.Marker(el)
            .setLngLat(train.geometry.coordinates)
            .setPopup(new mapboxgl.Popup({ offset: 25 }) // add popups
              .setHTML('<h3>' + train.properties.title + '</h3><p>' + train.properties.description + '</p>' + train.properties.timeToArrival))
            .addTo(map);

          markersArray.push({
            id: train.properties.title,
            trainObj,
            timeStamp: train.properties.timeStamp,
            route: train.properties.route,
            animStep: 0,
          });
        }
        else {
          marker = markersArray.find(marker => marker.id === train.properties.title)
          //If the train has updated since we last polled the API
          if (train.properties.timeStamp != marker.timeStamp) {
            marker.animStep = 0
            marker.timeStamp = train.properties.timeStamp
            marker.route = route = train.properties.route
            marker.trainObj
              .setLngLat(train.geometry.coordinates)
              .setPopup(null)
              .setPopup(new mapboxgl.Popup({ offset: 25 }) // add popups
                .setHTML('<h3>' + train.properties.title + '</h3><p>' + train.properties.description + '</p>' + train.properties.timeToArrival))
          }
        }
      })
    })
    .catch(function (error) {
      // handle error
      console.log(error);
    });
}

function animateMarker() {
  markersArray.forEach(function (train, index, object) {
    // Check if it's an old train with no more updates
    if (Date.now() - (100 * 1000) > train.timeStamp) {
      train.trainObj.remove()
      object.splice(index, 1);
    }
    // Else update position based on ticks.
    else {
      // Check we haven't reached the end of the route array
      if (train.animStep < train.route.length) {
        train.trainObj.setLngLat(train.route[train.animStep])
        train.animStep++
      }
    }
  })
}

window.setInterval(animateMarker, 10000);

const interval = setInterval(function () {
  // method to be executed;
  pull_latest_train_info()
}, 60000);

const animationInterval = setInterval(function () {
  // method to be executed;
  animateMarker()
}, 500);