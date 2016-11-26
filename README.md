# Add markers to map, remotely!

Let's assume that there is a bunch of people in an auditorium. We open http://this.stuff/map on a big screen.
There are already some static data-dependent markers. Some clutter is removed from the map.
Now, everybody can start adding markers by opening http://this.stuff/ on their devices. Nearby markes are grouped
and counted. Markers are not persisted, just kept in memory to survive the map reloads.

Hardcoded for a specific event. At minimum, it is necessary to change location selection geo-limits, 
hardcoded locations, strings, language preferences, Google API keys.

Keywords:

 - Google Maps Javascript API
 - Google Places API Web Service
 - Adding markers, dynamically
 - Location autocomplete
 - Maps API marker grouping, custom grouping icons
 - Generating custom SVG marker icons
 - Static markers with data-dependent shapes
 - Custom label with dynamic data
 - Websockets, keepalive
 - Python, Tornado
 - Bootstrap, jquery ui

Beware: _Google Places API Web Service_ has limited free tier: https://developers.google.com/places/web-service/usage .

MIT license. This weekend hobby project might contain traces of nuts, keys, code examples, etc.
