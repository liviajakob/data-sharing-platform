/* IceExplorer - Initial Map
 * Filename: map.js
 * 
 * This code initialises the map and changes map features
 * Author: Livia Jakob
 * */


var clickdatasets = true;
var root_link = 'http://127.0.0.1:8887'; //folder where the datasets are in!
var api_link = 'http://localhost:5002'; // external api
var polylayer;
var polylayer_group;
var projection = "EPSG:3413";
var mapcenter = [30665.5, -2039176.688]; // centre of the map; centre of Greenland



/* Creating the OpenLayers map object with two base layers
 * */
var map = new ol.Map({
    target: 'map',
    controls: ol.control.defaults({
    	attributionOptions: {
              target: document.getElementById('attribution'),
              collapsible: true,
        }
    }).extend([
    	new ol.control.ScaleLine(), 
          new ol.control.OverviewMap(),
    ]), 
        layers: [
        	new ol.layer.Group({
                title: 'Base maps',
                layers: [
                    new ol.layer.Tile({
                        title: 'Open Street Map',
                        source: new ol.source.OSM(),
                        type: 'base',
                        visible:false
                    }),
                    new ol.layer.Tile({
                        title: 'Aerial Photo',
                    	visible: true,
                    	type: 'base',
                        preload: Infinity,
                        source: new ol.source.BingMaps({
                          key: 'At5OL80sddUSOspCvAIkyQK0sQ4BLRsjJQ9Mu55m9HgPQp1mUjaq_dJ0A2gdjrmt',
                          imagerySet: 'Aerial',
                          // use maxZoom 19 to see stretched tiles instead of the BingMaps
                          // "no photos at this zoom level" tiles
                          maxZoom: 19
                        
                     })
                    })
                ] //end layers
            })
        ]
    
	});


/* Create the layergroup for the data layers in the dataset explore view
 * */
var dataset_tilelayers = new ol.layer.Group();
map.addLayer(dataset_tilelayers);


/* Projection definitions
 * */
proj4.defs('EPSG:3413', '+proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +k=1 ' +
    '+x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs');
var proj3413 = ol.proj.get('EPSG:3413');
    proj3413.setExtent([-5194304, -5194304, 5194304, 5194304]);

    
/* Set map view 
 * */ 
map.setView(new ol.View({
      zoom: 3, //map resolution
      minZoom: 2,
      extent: ol.proj.get("EPSG:3413").getExtent(),
      projection: "EPSG:3413",
      center: mapcenter // This is the globally set centre of the map
}));     

/* Save the initial view in a variable for the refresh button
 * */
var mapextent = map.getView().calculateExtent();  
 	

/* Creates the dataset polygons 
 * 
 * geojsonObject - a geojson with polygons of the dataset
 * */
function makePolys(geojsonObject){
	 features = (new ol.format.GeoJSON()).readFeatures(geojsonObject, {
 	      dataProjection: projection,
   	      featureProjection: projection
          	 })
    // Check if polylayer exists, if yes remove its features and add the new features
	if (typeof polylayer !== 'undefined'){ 
		polylayer.getSource().clear(); // clear polylayer
		polylayer.getSource().addFeatures(features); // add new features
			
	}else{ // Create new vectorlayer and grouplayer
	   	var source = new ol.source.Vector({
	      	 features: features
	      	});
	    polylayer = new ol.layer.Vector({
	            title: 'Extents', // for the ol-layerswitcher
	            source: source,
	            style: geometryStyle,
	        })   
	    polylayer_group = new ol.layer.Group({
	        	title: 'Datasets',
	        	layers: [polylayer]
	        })
	    map.addLayer(polylayer_group);
		
	}
	
    /*Set Layer ID*/
    for (var i = 0, l = polylayer.getSource().getFeatures().length; i < l; i++) {
        var feat = polylayer.getSource().getFeatures()[i];
        feat.setId(feat.get('id'));
    }
    
    /* Set polygon layer to visible
     * */
    polylayer.setVisible(true);
    
} // end makePolys()
 
 
 

//// generate hover effect and infobox //////////////////////////////////////
     
/* Append ol-overlaycontainer class to infobox
 * */
$('#infobox').appendTo(
   $('.ol-overlaycontainer')
);


/* Sets the infobox to visible and displays the info in the infobox
 * 
 * info - a html string with the infobox content
 * */
function displayInfo(info) {
   $('#infobox').html(info);
   $('#infobox').show();
}     
     
    
var hoverFeature = null; // current hover feature, tracked to set style back
//map targets
var target = map.getTarget();
var jTarget = typeof target === "string" ? $("#" + target) : $(target);


/* EvenListener for displaying the hover infobox and changing the polygon style on hover
 * */
map.on('pointermove', function (evt) {
	
	   /*Get the top feature, undefined if it doesn't hover over a polygon
		* */
	   var feature = map.forEachFeatureAtPixel(evt.pixel, function (feature, layer) {
	       return feature;
	   });
	   
	   /* Check if it as hovered over a polygon
	    * */
	   if (feature && feature.getGeometry().getType() == 'Polygon') {
		   /* change the mouse cursor to pointer if over a polygon
		    * this should indicate that the user can click on the polygon
		    * */
		   jTarget.css("cursor", "pointer");
		   
		   /* In case it is changed from one polygone directly to the next one
		    * */
		   if(!!hoverFeature && hoverFeature != feature){
			   hoverFeature.setStyle(polystyle); // change other polygon style back
		   }
		   // set hover style
		   feature.setStyle(hoverstyle);
		   // generate and display small infobox
		   displayInfo(hoverInfo(feature));
		   // set the new polygon to hoverFeauture
		   hoverFeature=feature;
	   } else {
		   /* change the mouse cursor back to default if over a polygon
		    * */
		   jTarget.css("cursor", "");
		   // change the style back
		   if(!!hoverFeature){
			   hoverFeature.setStyle(polystyle);
			   hoverFeature = null;
		   }
		   // hide small infobox
		   $('#infobox').hide();
	       
	   }
});
       
     

       
            
/* Returns html for info showed when hovering over
 * 
 * feature - an OpenLayers dataset feature
 * */
function hoverInfo(feature){
	html = '<h5>Dataset: '+feature.getId()+'</h5><p>';
	layers=feature.get('layergroups');
	html = html.concat('<b>Span: </b>'+feature.get('startdate')+' - '+ feature.get('enddate'))
	html = html.concat(' <b>Available Layers: </b><span class="upper">')
	for (l in layers){ // display layertypes
   		html=html.concat(layers[l].layertype + ' | ')
   	}
   	html=html.slice(0,-2); // remove last ' | ' character
   	html = html.concat('</span></p>')
	return html;
}       
