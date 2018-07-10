    
var clickdatasets = true;
var root_link = 'http://127.0.0.1:8887'; //folder where the datasets are in!
var api_link = 'http://localhost:5002';
var polylayer;
var polylayer_group;
var projection = "EPSG:3413";
var mapcenter = [30665.5, -2039176.688];

var map = new ol.Map({
    target: 'map',
    controls: ol.control.defaults({
    	attributionOptions: {
              target: document.getElementById('attribution'),
              //className: 'myCustomClass',
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
                        projection: 'EPSG:3857',
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
                          // maxZoom: 19
                        
                     })
                    })
                ] //end layers
            })
        ]
    
	});

/* This is the layergroup for the current layers when the user is exploring a dataset */
var dataset_tilelayers = new ol.layer.Group();
map.addLayer(dataset_tilelayers);


/*Projection definitions*/

proj4.defs('EPSG:3413', '+proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +k=1 ' +
    '+x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs');

var proj3413 = ol.proj.get('EPSG:3413');
console.log(proj3413)
    proj3413.setExtent([-5194304, -5194304, 5194304, 5194304]);

proj4.defs('EPSG:3413', '+proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +k=1 ' +
'+x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs');

//const proj3413 = ol.proj.get("EPSG:3413");
//proj3413.setExtent([-4194304, -4194304, 4194304, 4194304]);
    
    
/* Set Map view */
    
map.setView(new ol.View({
      //center: [0, 0],
      zoom: 3, //map resolution
      minZoom: 2,
      //maxZoom: 20,
      //projection and units,, default mercator and meters
      //maxZoom: (default: 28)
      //zoomFactor: (default:2)
      //maxResolution: ...calculated by default
      extent: [-5194304, -5194304, 5194304, 5194304], //left, bottom ,right, top //minx, miny, maxx, maxy
      //extent: ol.proj.get("EPSG:3413").getExtent(),
      projection: "EPSG:3413",
      center: mapcenter // This is the center of greenland. Could be set automatically...
}));



var mapextent = map.getView().calculateExtent();     
     
/////////////// READ AND DISPLAY POLYGONS FROM DATASET GEOJSON
     
 	/*$.getJSON('data', function(data) {
        //data is the JSON string
    	console.log('Make Polygons....')
    	makePolys(data)
    });*/


 	
 	
 	/* Creates the dataset polygons */
     function makePolys(geojsonObject){
    	 console.log(geojsonObject)
    	 
    	 console.log(source)
    	 features = (new ol.format.GeoJSON()).readFeatures(geojsonObject, {
     	      dataProjection: 'EPSG:3413',
       	      featureProjection: 'EPSG:3413'
              	 })

    	if (typeof polylayer !== 'undefined'){
    		console.log('CLEAR')
    		polylayer.getSource().clear();
    		polylayer.getSource().addFeatures(features);
    			
    	}else{ /*Create vectorlayer and grouplayer*/
    		
       	 var source = new ol.source.Vector({
          	 features: features
          	});
           
    		
            polylayer = new ol.layer.Vector({
                title: 'Extents',
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
        
        /*Set to visible*/
        polylayer.setVisible(true);
        
     } //End makePolys
     
     
     
     
     
///////////// HOVER     

     
     
/////////hover interaction, on hover over polygon/////////////////////////////////////////////////     
     var target = map.getTarget();
     var jTarget = typeof target === "string" ? $("#" + target) : $(target);
     // change mouse cursor when over marker
     $(map.getViewport()).on('mousemove', function (e) {
         var pixel = map.getEventPixel(e.originalEvent);
         var hit = map.forEachFeatureAtPixel(pixel, function (feature, layer) {
             return true;
         });
         if (hit) {
             jTarget.css("cursor", "pointer");
         } else {
             jTarget.css("cursor", "");
         }
     });
     
     
   
     

     
//////////////////////////////////////
     ////display infobox
     
     

     $('#infobox').appendTo(
       $('.ol-overlaycontainer')
     );
     
     function displayInfo(info) {
       $('#infobox').html(info);
       $('#infobox').show();
     }     
     
     
var hoverFeature = null;    
       map.on('pointermove', function (evt) {
           var feature = map.forEachFeatureAtPixel(evt.pixel,
        		   
           function (feature, layer) {
               return feature;
           });
           if (feature && feature.getGeometry().getType() == 'Polygon') {
               if(!!hoverFeature && hoverFeature != feature){
            	   hoverFeature.setStyle(polystyle);
               }
               hoverFeature=feature;
               var geometry = feature.getGeometry();
               //calculate center of polygon
               var oo = ol.extent.getCenter(geometry.getExtent());               
               var coord=oo;               
               //popup.setPosition(coord);
               //$(element).popover({
               //    'placement': 'top',
               //        'html': true,
               //        'content': 'id: '+feature.get('id')
               //});
               
               
               //$(element).popover('show');
               feature.setStyle(hoverstyle);
               displayInfo(hoverInfo(feature));
           } else {
               //$(element).popover('dispose');
               if(!!hoverFeature){
            	   hoverFeature.setStyle(polystyle);
               }
               $('#infobox').hide();
               
           }
       });
       
       
     //map.getView().fit(source.getExtent(), map.getSize()); 
     
     

       
            
       /*Returns html for info showed when hovering over*/
       function hoverInfo(feature){
    	   
    	   html = '<h5>Dataset: '+feature.getId()+'</h5><p>';
    	   
    	   "</b> -- Cite this dataset as: " + feature.get('cite') + "<br> " + "<b>Layers: </b>"
    	   layers=feature.get('layers');
    	   html = html.concat('<b>Span: </b>'+feature.get('startdate')+' - '+ feature.get('enddate'))
    	   html = html.concat(' <b>Available Layers: </b><span class="upper">')
	   		for (l in layers){
	   			html=html.concat(layers[l].layertype + ' | ')
	   		}
	   		html=html.slice(0,-2);
	   		html = html.concat('</span>')
	   		html = html.concat("</p>");
    	   
    	   
    	   return html;
       }
       
       
