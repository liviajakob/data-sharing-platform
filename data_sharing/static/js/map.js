    var map = new ol.Map({
    	target: 'map',
    	controls: ol.control.defaults({
            attributionOptions: {
              target: document.getElementById('myattribution'),
              className: 'myCustomClass'
            }
    
    
    })});

    proj4.defs('EPSG:3413', '+proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +k=1 ' +
    '+x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs');
    var proj3413 = ol.proj.get('EPSG:3413');
    proj3413.setExtent([-4194304, -4194304, 4194304, 4194304]);

    proj4.defs('EPSG:27700', '+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 ' +
        '+x_0=400000 +y_0=-100000 +ellps=airy ' +
        '+towgs84=446.448,-125.157,542.06,0.15,0.247,0.842,-20.489 ' +
        '+units=m +no_defs');
    var proj27700 = ol.proj.get('EPSG:27700');
    proj27700.setExtent([0, 0, 700000, 1300000]);



    map.setView(new ol.View({
      //center: [0, 0],
      zoom: 2, //map resolution
      minZoom: 2,
      maxZoom: 10,
      //projection and units,, default mercator and meters
      //maxZoom: (default: 28)
      //zoomFactor: (default:2)
      //maxResolution: ...calculated by default
      //projection: 'EPSG:3857'//'EPSG:4326'
      extent: [-1037508.3427892,-10037508.3427892, 537508.3427892, 11037508.3427892], //left, bottom ,right, top
      projection: 'EPSG:3857',
      center: [400000, 4000000] //[-4194301, -4194301]
    	
    }));

     var osmSource = new ol.source.OSM(); //get remote data for a layer

     ///layer
     //ol.layer.Tile
     //ol.layer.Image
     //ol.layer.Vector

     var osmLayer = new ol.layer.Tile({
       source: osmSource,
       projection: 'EPSG:3857'

     });
     map.addLayer(osmLayer);

     wms4326 = new ol.layer.Tile({
       source: new ol.source.TileWMS({
         url: 'https://ahocevar.com/geoserver/wms',
         crossOrigin: '',
         params: {
           'LAYERS': 'ne:NE1_HR_LC_SR_W_DR',
           'TILED': true
         },
         projection: 'EPSG:4326'
       })
     });
     //map.addLayer(wms4326);


    var wms = new ol.layer.Tile({
       source: new ol.source.TileWMS({
         url: 'https://ahocevar.com/geoserver/wms',
         crossOrigin: '',
         params: {
           'LAYERS': 'ne:NE1_HR_LC_SR_W_DR',
           'TILED': true
         },
         projection: 'EPSG:4326'
       })
     });

     //map.addLayer(wms);


     var source = new ol.source.OSM({
                 url: 'http://127.0.0.1:8887/tiles3/{z}/{x}/{-y}.png',
                 crossOrigin: null //hack file
         })


     var myLayer = new ol.layer.Tile({
       source: source,
       projection: 'EPSG:4326'

     });
     map.addLayer(myLayer);
     
     
     
     
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
    	
    	
    	
    	//popup
    	
        var popup = new ol.Overlay({
            element: document.getElementById('checkbox')
          });
    
     
        var ol3_sprint_location = ol.proj.transform([-1.20472, 52.93646], 'EPSG:4326', 'EPSG:3857');
        map.addOverlay(popup);
        popup.setPosition(ol3_sprint_location);
     
     

        //////get mouseposition
        
        var mousePositionControl = new ol.control.MousePosition({
            coordinateFormat: ol.coordinate.createStringXY(4),
            projection: 'EPSG:3857', //'EPSG:3857',
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
          map.addLayer(vectorLayer)
          
          
          
////////////////////////////////////////////////////////////////////////////