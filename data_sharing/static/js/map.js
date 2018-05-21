BASECOORDS = [-13.9626, 33.7741];

function makeMap() {
    var TILE_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
    var MB_ATTR = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    
    mymap = L.map('llmap');
    //mymap.setView(BASECOORDS, 8);
    //L.tileLayer(TILE_URL, {attribution: MB_ATTR}).addTo(mymap);
    //L.control.scale().addTo(mymap);
    
    //add dataset test
    var myLayer = L.geoJson().addTo(mymap);
    //myLayer.addData(geojsonFeature);
    x = $.getJSON("/datasets/1");
    console.log(x);
    $.getJSON("/datasets/1", function (data) {
    	console.log(data);
    	});
}

var layer = L.layerGroup();




/*function renderData(districtid) {
    $.getJSON("/district/" + districtid, function(obj) {
        var markers = obj.data.map(function(arr) {
            return L.marker([arr[0], arr[1]]);
        });
        mymap.removeLayer(layer);
        layer = L.layerGroup(markers);
        mymap.addLayer(layer);
    });
}*/


$(function() {
    makeMap();
    /*renderData('0');
    $('#distsel').change(function() {
        var val = $('#distsel option:selected').val();
        renderData(val);
    });*/
})




/////////////////////////////TESTS

/*
Example using Sweden Lantmäteriet Topografisk Webbkarta
https://opendata.lantmateriet.se/#apis
*/

/*** INSERT YOUR LANTMÄTERIET API TOKEN BELOW ***/
var crs = new L.Proj.CRS('EPSG:3006',
	'+proj=utm +zone=33 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs',
	{
		resolutions: [
			8192, 4096, 2048, 1024, 512, 256, 128,
			64, 32, 16, 8, 4, 2, 1, 0.5
		],
		origin: [0, 0]
	}),
	map = new L.Map('mapContainer', {
		crs: crs,
	});

L.tileLayer.wms('https://geodatatest.havochvatten.se/geoservices/ows', {
	layers: 'hav-bakgrundskartor:hav-grundkarta',
	format: 'image/png',
	maxZoom: 14,
	minZoom: 0,
	attribution: '&copy; OpenStreetMap contributors <a href="https://www.havochvatten.se/kunskap-om-vara-vatten/kartor-och-geografisk-information/karttjanster.html">Havs- och vattenmyndigheten (Swedish Agency for Marine and Water Management)</a>'
}).addTo(map);

map.setView([55.8, 14.3], 3);


