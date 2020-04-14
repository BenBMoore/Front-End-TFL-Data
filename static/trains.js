
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
    'paint' : {
      'circle-radius' : 2,
      'circle-color' : "#FFFFFF"
    }

  });

  map.addSource('trains', { type: 'geojson', data: trains_url });
  map.addLayer({
    'id': 'trains',
    'type': 'circle',
    'source': 'trains',
    'paint' : {
      'circle-radius' : 4,
      'circle-color' : "#000000"
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
    console.log("mouse entered")
    map.getCanvas().style.cursor = 'pointer';
  });

  // Change it back to a pointer when it leaves.
  map.on('mouseleave', 'tubeStations', function () {
    map.getCanvas().style.cursor = '';
  });

  map.on('click', 'trains', function (e) {
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
  map.on('mouseenter', 'trains', function () {
    console.log("mouse entered")
    map.getCanvas().style.cursor = 'pointer';
  });

  // Change it back to a pointer when it leaves.
  map.on('mouseleave', 'trains', function () {
    map.getCanvas().style.cursor = '';
  });
});