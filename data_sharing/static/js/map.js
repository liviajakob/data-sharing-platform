    
var clickdatasets = true;
var root_link = 'http://127.0.0.1:8887';
var projection = 'EPSG:4313';
var api_link = 'http://localhost:5002'


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
    proj3413.setExtent([-5194304, -5194304, 5194304, 5194304]);

    
    
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
      center: [30665.5, -2039176.688] // This is the center of greenland. Could be set automatically...
}));



 
var mapextent = map.getView().calculateExtent();     
     
/////////////// READ AND DISPLAY POLYGONS FROM DATASET GEOJSON
     
 	$.getJSON('data', function(data) {
        //data is the JSON string
    	console.log('Make Polygons....')
    	makePolys(data)
    });

 	console.log('Dataproj', ol.dataProjection)

     function makePolys(geojsonObject){
    	 console.log(geojsonObject)
    	 var source = new ol.source.Vector({
       	  //url: 'datasets/1',
       	  //format: new ol.format.GeoJSON()
       	 features: (new ol.format.GeoJSON()).readFeatures(geojsonObject, {
   	      dataProjection: 'EPSG:3413',
	      featureProjection: 'EPSG:3413'
       	 })
       	 
       	 
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
        
        for (var i = 0, l = source.getFeatures().length; i < l; i++) {
            var feat = source.getFeatures()[i];
            feat.setId(feat.get('id'));
        }
        
        }
     
     
     
     
     
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
	   		for (l in layers){
	   			html=html.concat(layers[l].layertype + ' | ')
	   		}
	   		html=html.slice(0,-2);
	   		html = html.concat("</p>");
    	   
    	   
    	   return html;
       }
       
       

       
       

     

     
     

        
        
        
//////////////////////////////////////////////////
        
        

        /*var bing = new ol.layer.Tile({
            title: 'Aerial Photo',
        	visible: true,
            preload: Infinity,
            source: new ol.source.BingMaps({
              key: 'At5OL80sddUSOspCvAIkyQK0sQ4BLRsjJQ9Mu55m9HgPQp1mUjaq_dJ0A2gdjrmt',
              imagerySet: 'Aerial',
              // use maxZoom 19 to see stretched tiles instead of the BingMaps
              // "no photos at this zoom level" tiles
              // maxZoom: 19
            
         })})*/
        
        //map.addLayer(bing);


       
        
        
        

        
        
        
        //////TOGGLE LAYER
          
          // create a DOM Input helper for the checkbox
          //var layer1 = document.querySelector('#layer_check');
          // and bind its 'checked' property to the layer's 'visible' property

         	/*bing.on('change:visible', function() {
         	  var visible = this.getVisible();
         	  if (visible !== checkbox.checked) {
         		 document.querySelector('#layer_check').checked = visible;
         	  }
         	});*/
  
        
        

         	
         	
         	
         	
         	
         	
         	
         	
/////////////// TRASH
         	
         	
         	


            
            //var extent1 = [-602834.5, -3251176.688, 664165.5, -757176.6880000001]
            //console.log(extent1)
            //ext1 = ol.proj.transformExtent(extent1, ol.proj.get('EPSG:3413'), ol.proj.get('EPSG:3857'));

            // var source = new ol.source.OSM({
            //             url: 'http://127.0.0.1:8887/14/dem/tiles/{z}/{x}/{-y}.png',
            //             crossOrigin: null //hack file
            //     })

             
             //var myLayer = new ol.layer.Tile({
            //   source: source,
            //   projection: 'EPSG:4326',
            //	   extent: extent1, 
            //	   opacity: 1
             //});
             //map.addLayer(myLayer);
             //map.getView().fit(ext1, map.getSize());
            
            
        ////////////////////////////////////////////////////////////////////////////
             
             
             
             
             
             /////// POLYGON /////////////////////////////////////////
             
             /*var extent = [-602834.5, -3251176.688, 664165.5, -757176.6880000001]
             ext = ol.proj.transformExtent(extent, ol.proj.get('EPSG:3413'), ol.proj.get('EPSG:3857'));
             
             //3395
             
             //'EPSG:3413'
             
             var style2 = new ol.style.Style({
             	fill: new ol.style.Fill({
                     color: 'green'
                   }),
             });
             
             var vectorSource = new ol.source.Vector({
                 //create empty vector
             });
             
             var feature = new ol.Feature({
                 geometry: new ol.geom.Polygon.fromExtent(ext),
             });
             feature.setId(1);
           
             
             //vectorSource.addFeature(feature);

             ///second polygon
             
             var extent2 = [-62834.5, -3051176.688, 6004165.5, -7007176.6880000001]
             ext2 = ol.proj.transformExtent(extent2, ol.proj.get('EPSG:3413'), ol.proj.get('EPSG:3857'));
             var feature3 = new ol.Feature({
                 geometry: new ol.geom.Polygon.fromExtent(ext2),
             });
             feature3.setId(2);
             
             vectorSource.addFeature(feature3);
             ///
             console.log(vectorSource);
             
             var vectorLayer2 = new ol.layer.Vector({
                 source: vectorSource,
                 style: geometryStyle,
                 opacity: 0.6
             });
             
             //// third polygon
             
             
             var thing = new ol.geom.Polygon(
            	    [[ol.proj.transform([-16,-22], 'EPSG:4326', 'EPSG:3857'),
            	    ol.proj.transform([-44,-55], 'EPSG:4326', 'EPSG:3857'),
            	    ol.proj.transform([-88,75], 'EPSG:4326', 'EPSG:3857')]]
             );
             

             
             
             var featurething = new ol.Feature({
            	    name: "Thing",
            	    geometry: thing
            });
             vectorSource.addFeature(featurething);*/
         	
         	
         	
         	
         	
         	
         	
         	
         	
         	
         	
         	
         	
            // display popup on hover
            
            ///////popup
            
            //var element = document.getElementById('popup');

            //var popup = new ol.Overlay({
            //    element: element,
            //    positioning: 'bottom-center',
            //    stopEvent: false
            //});
            //map.addOverlay(popup);
            
          ///pointermove event

             
         	
         	
         	
         	
         	
         	
         	
         	
         	
         	
         	
         	
         	
            ///////////
            //checkbox
            
            // create a DOM Input helper for the checkbox
            //var checkbox = document.querySelector('#visible');
            // and bind its 'checked' property to the layer's 'visible' property
            //checkbox.addEventListener('change', function() {
           	//  var checked = this.checked;
           	 // if (checked !== myLayer.getVisible()) {
           	 //   myLayer.setVisible(checked);
           	 // }
           	//});

           	//myLayer.on('change:visible', function() {
           	//  var visible = this.getVisible();
           	//  if (visible !== checkbox.checked) {
           	//    checkbox.checked = visible;
           	//  }
           	//});
           	
           	
           	
           	//layercheckbox
           	
               //var check = new ol.Overlay({
                   //element: document.getElementById('checkbox')
                //// });
           
            
               //var ol3_sprint_location = ol.proj.transform([-1.20472, 52.93646], 'EPSG:4326', 'EPSG:3857');
               //map.addOverlay(check);
               //check.setPosition(ol3_sprint_location);
            
            

                 
