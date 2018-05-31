    
var clickdatasets = true;
var scaleLineControl = new ol.control.ScaleLine();
var root = 'http://127.0.0.1:8887';

var corineUrl = 'http://filotis.itia.ntua.gr/mapserver?SERVICE=WFS&' +
'VERSION=1.1.0&REQUEST=GetFeature&TYPENAME=biotopes_corine&' +
'SRSNAME=EPSG:4326&OUTPUTFORMAT=gml3';
var naturaUrl = 'http://filotis.itia.ntua.gr/mapserver?SERVICE=WFS&' +
'VERSION=1.1.0&REQUEST=GetFeature&TYPENAME=biotopes_natura&' +
'SRSNAME=EPSG:4326&OUTPUTFORMAT=gml3';
var cadastreUrl = 'http://gis.ktimanet.gr/wms/wmsopen/wmsserver.aspx';

var map = new ol.Map({
    target: 'map',
    controls: ol.control.defaults({
    	attributionOptions: {
              target: document.getElementById('attribution'),
              //className: 'myCustomClass',
              collapsible: true,
        }
    }).extend([
          scaleLineControl, 
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
                        type: 'base'
                    }),
                    new ol.layer.Tile({
                        title: 'Aerial Photo',
                    	visible: false,
                    	type: 'base',
                        preload: Infinity,
                        source: new ol.source.BingMaps({
                          key: 'At5OL80sddUSOspCvAIkyQK0sQ4BLRsjJQ9Mu55m9HgPQp1mUjaq_dJ0A2gdjrmt',
                          imagerySet: 'Aerial',
                          // use maxZoom 19 to see stretched tiles instead of the BingMaps
                          // "no photos at this zoom level" tiles
                          // maxZoom: 19
                        
                     })}),
                     new ol.layer.Tile({
                         title: 'Aerial Photo',
                     	visible: false,
                     	type: 'base',
                         preload: Infinity,
                         source: new ol.source.BingMaps({
                           key: 'At5OL80sddUSOspCvAIkyQK0sQ4BLRsjJQ9Mu55m9HgPQp1mUjaq_dJ0A2gdjrmt',
                           imagerySet: 'Aerial',
                           // use maxZoom 19 to see stretched tiles instead of the BingMaps
                           // "no photos at this zoom level" tiles
                           // maxZoom: 19
                         
                         })})
                    
                ]
            })
        ]
    
	});

//map.addControl(new ol.control.OverviewMap());
//ol.control.defaults().extend(new ol.control.OverviewMap());



    
    

    proj4.defs('EPSG:3413', '+proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +k=1 ' +
    '+x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs');
    var proj3413 = ol.proj.get('EPSG:3413');
    proj3413.setExtent([-5194304, -5194304, 5194304, 5194304]);



    map.setView(new ol.View({
      //center: [0, 0],
      zoom: 3, //map resolution
      minZoom: 2,
      maxZoom: 10,
      //projection and units,, default mercator and meters
      //maxZoom: (default: 28)
      //zoomFactor: (default:2)
      //maxResolution: ...calculated by default
      //projection: 'EPSG:3857'//'EPSG:4326'
      extent: [-5194304, -5194304, 5194304, 5194304], //left, bottom ,right, top //minx, miny, maxx, maxy
      //extent: ol.proj.get("EPSG:3857").getExtent(),
      projection: "EPSG:3413", //'',
      center: [30665.5, -2039176.688] //[-4194301, -4194301]
    	
    }));
    
    
    //extent: [-20037508.3427892,-20037508.3427892,20037508.3427892,20037508.3427892]
    //map.getView().fitExtent(extent, map.getSize());


    
    var extent1 = [-602834.5, -3251176.688, 664165.5, -757176.6880000001]
    console.log(extent1)
    //ext1 = ol.proj.transformExtent(extent1, ol.proj.get('EPSG:3413'), ol.proj.get('EPSG:3857'));

     var source = new ol.source.OSM({
                 url: 'http://127.0.0.1:8887/14/dem/tiles/{z}/{x}/{-y}.png',
                 crossOrigin: null //hack file
         })

     
     var myLayer = new ol.layer.Tile({
       source: source,
       projection: 'EPSG:4326',
    	   extent: extent1, 
    	   opacity: 1
     });
     //map.addLayer(myLayer);
     //map.getView().fit(ext1, map.getSize());
    
     
     
     
   /// PAttern  ////////////////////////////////////////////////////////////////////////////
     var canvas = document.createElement('canvas');
     var context = canvas.getContext('2d');

     // Gradient and pattern are in canvas pixel space, so we adjust for the
     // renderer's pixel ratio
     var pixelRatio = ol.has.DEVICE_PIXEL_RATIO;
     
     // Generate a canvasPattern with two circles on white background
     var pattern = (function() {
       canvas.width = 11 * pixelRatio;
       canvas.height = 11 * pixelRatio;
       // white background
       context.fillStyle = 'white';
       context.fillRect(0, 0, canvas.width, canvas.height);
       // outer circle
       context.fillStyle = 'rgba(102, 0, 102, 0.5)';
       context.beginPath();
       context.arc(5 * pixelRatio, 5 * pixelRatio, 4 * pixelRatio, 0, 2 * Math.PI);
       context.fill();
       // inner circle
       context.fillStyle = 'rgb(55, 0, 170)';
       context.beginPath();
       context.arc(5 * pixelRatio, 5 * pixelRatio, 2 * pixelRatio, 0, 2 * Math.PI);
       context.fill();
       return context.createPattern(canvas, 'repeat');
     }());
     
     // Generate a canvasPattern with two circles on white background
     var pattern2 = (function() {
       canvas.width = 5 * pixelRatio;
       canvas.height = 5 * pixelRatio;
       // transparent background
       context.fillStyle = 'transparent';
       context.fillRect(0, 0, canvas.width, canvas.height);
       // outer circle
       context.fillStyle = 'black';
       context.beginPath();
       context.arc(5 * pixelRatio, 5 * pixelRatio, 0.5 * pixelRatio, 0, 2 * Math.PI);
       context.fill();

       return context.createPattern(canvas, 'repeat');
     }());
     
     
     var fill = new ol.style.Fill();
     var style = new ol.style.Style({
       fill: fill,
       stroke: new ol.style.Stroke({
         color: '#333',
         width: 2
       })
     });
     
     var getStackedStyle = function(feature, resolution) {
         var id = feature.getId();

         fill.setColor(id > 'J' ? pattern2: 'transparent');
         //fill.setColor(pattern)
         return style;
       };
       
       
       // Create a vector layer that makes use of the style function above…
       var vectorLayer = new ol.layer.Vector({
         source: new ol.source.Vector({
           url: 'https://openlayers.org/en/v4.6.5/examples/data/geojson/countries.geojson',
           format: new ol.format.GeoJSON()
         }),
         style: getStackedStyle
       });
       console.log("OSM"+vectorLayer)
       //map.addLayer(vectorLayer)
       
       
       
////////////////////////////////////////////////////////////////////////////
     
     
     
     
     
     /////// POLYGON /////////////////////////////////////////
     
     var extent = [-602834.5, -3251176.688, 664165.5, -757176.6880000001]
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
     vectorSource.addFeature(featurething);
     
     
     
     /////////////// POLYGONS FROM DATASET GEOJSON
     
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
     
     
     
     
     
     

     
     
     /////////hover interaction/////////////////////////////////////////////////     
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
     
     
     //////////click interaction//////////////////////////////
     
     /*Zoom to layer on click*/
     var featureListener = function(event, feature) {
    	 console.log('EVENT',event);
    	 map.getView().fit(feature.getGeometry(), {
    		  duration: 1000,
    		  nearest: true
    		});
    	 polylayer.setVisible(false);
    	 displayDataset(feature)
         //console.log(feature.getId());
         //alert("Feature Listener Called");
    	 clickdatasets=true;
       };

       map.on('click', function(event) {
    	 if (clickdatasets){
    		 clickdatasets=false;
    		 polyfound=false;
	         map.forEachFeatureAtPixel(event.pixel,
	         function(feature, layer) {

	           if (!polyfound && feature && feature.getGeometry().getType() == 'Polygon') {
	             //feature.setStyle(listenerStyle);
		        	 console.log(feature.getId())
		        	 console.log(feature.getGeometry().getType())
	        	 polyfound = true
	             featureListener(event, feature);
	             
	           }
	         });
         }
       });
       
       
       
     function displayDataset(dataset){
    	 console.log('DATASET_CLICKED',dataset.getId());
    	 polyext = dataset.getGeometry().getExtent();
    	 console.log('EXTENT',polyext);
    	 //polyext_tr = ol.proj.transformExtent(polyext, ol.proj.get('EPSG:3413'), ol.proj.get('EPSG:3857'))
    	 
    	 url= root+ '/'+ dataset.getId() + '/'+dataset.get('layers')[0].layertype + '/tiles/{z}/{x}/{-y}.png';
    	 console.log('URL',url);
    	 
    	     var source = new ol.source.OSM({
    	                 url: url, //'http://127.0.0.1:8887/14/dem/tiles/{z}/{x}/{-y}.png',
    	                 crossOrigin: null //hack file
    	         })
     
    	     var myLayer = new ol.layer.Tile({
    	       source: source,
    	       projection: 'EPSG:4326',
    	    	   extent: polyext, 
    	    	   opacity: 1
    	     });
    	     map.addLayer(myLayer);
    	     $('#infobox').hide();
    	     displayDetailedInfo(detailedInfo(dataset));
     }
     
    // display popup on hover
       
       ///////popup
       
       var element = document.getElementById('popup');

       var popup = new ol.Overlay({
           element: element,
           positioning: 'bottom-center',
           stopEvent: false
       });
       map.addOverlay(popup);
       
     ///pointermove event
      
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
               popup.setPosition(coord);
               $(element).popover({
                   'placement': 'top',
                       'html': true,
                       'content': 'id: '+feature.get('id')
               });
               
               
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
     
     
  //////////////////////////////////////
       ////display infobox
       
       

       $('#infobox').appendTo(
         $('.ol-overlaycontainer')
       );
       
       function displayInfo(info) {
         $('#infobox').html(info);
         $('#infobox').show();
       }
       
            
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
       
       
       
       ///////////////////////////////////////
       ///////detailed infoxox
       $('#infobox-detailed').appendTo(
    	         $('.ol-overlaycontainer')
    	       )

       
       function displayDetailedInfo(info) {
    	   $('#info-title').html(info[0]);
           $('#infobox-detailed-content').html(info[1]);
           $('#infobox-detailed').show();
           $('#infobox-detailed-content').show();
         }
       
       
       
       
       /*Returns html for info showed when exploring a dataset*/
       function detailedInfo(feature){
    	   title = '<h5>Dataset: '+feature.getId()+'</h5>'
    	   html = '<p>'+"</b> -- Cite this dataset as: " + feature.get('cite') + "<br> " + "<b>Layers: </b>";
    	   layers=feature.get('layers');
	   		for (l in layers){
	   			html=html.concat(layers[l].layertype + ' | ')
	   		}
	   		html=html.slice(0,-2);
	   		html = html.concat("</p>");
    	   
    	   
    	   return [title, html];
       }
         
       
       
       
       
       
       
       
     
     
     ////////////////////// STYLE
     
     function geometryStyle(feature){
    	    var
    	        style = [],
    	        geometry_type = feature.getGeometry().getType(),
    	        white = [255,255,255, 1],//[95,158,160,1],
    	        blue = [95,158,160,1],// [25,25,112, 1],
    	        width = 3;
    	        
    	    style['LineString'] = [
    	        new ol.style.Style({
    	            stroke: new ol.style.Stroke({
    	                color: white, width: width + 2
    	            })
    	        }),
    	        new ol.style.Style({
    	            stroke: new ol.style.Stroke({
    	                color: blue, width: width
    	            })
    	        })
    	    ],
    	    style['Polygon'] = [
    	        new ol.style.Style({
    	            fill: new ol.style.Fill({ color: [255, 255, 255, 0.2] })
    	        }),
    	        new ol.style.Style({
    	            stroke: new ol.style.Stroke({
    	                color: white, width: width
    	            })
    	        }),
    	        new ol.style.Style({
    	            stroke: new ol.style.Stroke({
    	                color: blue, width: width
    	            })
    	        })
    	    ],
    	    style['Point'] = [
    	        new ol.style.Style({
    	            image: new ol.style.Circle({
    	                radius: width * 2,
    	                fill: new ol.style.Fill({color: blue}),
    	                stroke: new ol.style.Stroke({
    	                    color: white, width: width / 2
    	                })
    	            })
    	        })
    	    ];
    	    
    	    return style[geometry_type];
    	}
     
     
     /*Hoverstyle for polygons*/
     
     var hoverstyle = [
	        new ol.style.Style({
	            fill: new ol.style.Fill({ color: [95,158,160, 0.4] })
	        }),
	        new ol.style.Style({
	            stroke: new ol.style.Stroke({
	                color: 'white', width: 4
	            })
	        }),
	        new ol.style.Style({
	            stroke: new ol.style.Stroke({
	                color: [61, 100, 102,1], width: 3.5
	            })
	        })
	    ];
     
     white = [255,255,255, 1],//[95,158,160,1],
     blue = [95,158,160,1],// [25,25,112, 1],
     width = 3;
     
     var polystyle = [
	        new ol.style.Style({
	            fill: new ol.style.Fill({ color: [255,255,255, 0.2] })
	        }),
	        new ol.style.Style({
	            stroke: new ol.style.Stroke({
	                color: 'white', width: width
	            })
	        }),
	        new ol.style.Style({
	            stroke: new ol.style.Stroke({
	                color: blue, width: width
	            })
	        })
	    ];
     
     
     
     //////////////////////
     
     
     ///////////
     //checkbox
     
     // create a DOM Input helper for the checkbox
     var checkbox = document.querySelector('#visible');
     // and bind its 'checked' property to the layer's 'visible' property
     checkbox.addEventListener('change', function() {
    	  var checked = this.checked;
    	  if (checked !== myLayer.getVisible()) {
    	    myLayer.setVisible(checked);
    	  }
    	});

    	myLayer.on('change:visible', function() {
    	  var visible = this.getVisible();
    	  if (visible !== checkbox.checked) {
    	    checkbox.checked = visible;
    	  }
    	});
    	
    	
    	
    	//layercheckbox
    	
        var check = new ol.Overlay({
            element: document.getElementById('checkbox')
          });
    
     
        var ol3_sprint_location = ol.proj.transform([-1.20472, 52.93646], 'EPSG:4326', 'EPSG:3857');
        map.addOverlay(check);
        check.setPosition(ol3_sprint_location);
     
     

        //////get mouseposition
        
        var mousePositionControl = new ol.control.MousePosition({
            coordinateFormat: ol.coordinate.createStringXY(4), //precision
            projection: 'EPSG:4313', //'EPSG:3857',
            // comment the following two lines to have the mouse position
            // be placed within the map.
            className: 'custom-mouse-position',
            target: document.getElementById('mouse-position'),
            undefinedHTML: '&nbsp;'
          });
        
        /*var precisionInput = document.getElementById('precision');
        precisionInput.addEventListener('change', function(event) {
          var format = ol.coordinate.createStringXY(event.target.valueAsNumber);
          mousePositionControl.setCoordinateFormat(format);
        });*/
        
        map.addControl(mousePositionControl);
       
        
        
          
          /////custom controls
          
      /**
       * Define a namespace for the application.
       */
      window.app = {};
      var app = window.app;
      
          
      app.RotateNorthControl = function(opt_options) {

        var options = opt_options || {};

        var reset = document.createElement('button');
        reset.innerHTML = 'R';
        
        var nort = document.createElement('button');
        nort.innerHTML = 'N';
        
        //var tool = document.createElement('select');
        //var option = document.createElement('option')
        //option.setAttribute('value', 'hi');
        //var textNode = document.createTextNode(feature.get('NOM'));
        //tool.appendChild(option);
        


        var this_ = this;
        var handleRotateNorth = function() {
        	console.log('ROTATE')
          map.getView().setRotation(90, {duration: 1000});
        };
        
        
        var updatesize= function(){
        	//map.getView().refresh();
        	console.log('UPDATE SIZE');
        	map.getView().setRotation(0, {duration: 1000});
        	//map.getView().fit(map.getView().extent, map.getSize()); 
        }
        
        nort.addEventListener('onchange', handleRotateNorth, false);
        nort.addEventListener('click', handleRotateNorth, false);
        nort.addEventListener('touchstart', handleRotateNorth, false);
        
        reset.addEventListener('click', updatesize, false);
        reset.addEventListener('touchstart', updatesize, false);

        
        var element = document.createElement('div');
        element.className = 'rotate-north ol-unselectable ol-control';
        element.appendChild(nort);
        element.appendChild(reset);
        //element.appendChild(tool);

        
        ol.control.Control.call(this, {
          element: element,
          target: options.target
        });
        
      };
        
        ol.inherits(app.RotateNorthControl, ol.control.Control);

//// ADD CONTROLS
        
        
        map.addControl(new app.RotateNorthControl());
        map.addControl(new ol.control.FullScreen({source: 'fullscreen'}));
 
        
        //layerswitcher
        
        var layerSwitcher = new ol.control.LayerSwitcher({
            tipLabel: 'Layers', // Optional label for button
            enableOpacitySliders: true
        });
        map.addControl(layerSwitcher);
        
        
        
//////////////////////////////////////////////////
        
        

        var bing = new ol.layer.Tile({
            title: 'Aerial Photo',
        	visible: true,
            preload: Infinity,
            source: new ol.source.BingMaps({
              key: 'At5OL80sddUSOspCvAIkyQK0sQ4BLRsjJQ9Mu55m9HgPQp1mUjaq_dJ0A2gdjrmt',
              imagerySet: 'Aerial',
              // use maxZoom 19 to see stretched tiles instead of the BingMaps
              // "no photos at this zoom level" tiles
              // maxZoom: 19
            
         })})
        
        map.addLayer(bing);


        