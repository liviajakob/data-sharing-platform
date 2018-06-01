     
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
     
     
     ///// PATTERNS
     
     
     
     
     /// PAttern  ////////////////////////////////////////////////////////////////////////////
       /*var canvas = document.createElement('canvas');
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
       }());*/
       

     
     
     
     
     
     
     
     
     
     //var fill = new ol.style.Fill();
     //var style = new ol.style.Style({
     //  fill: fill,
     //  stroke: new ol.style.Stroke({
     //    color: '#333',
     //    width: 2
     //  })
     //});
     
     //var getStackedStyle = function(feature, resolution) {
     //    var id = feature.getId();

     //    fill.setColor(id > 'J' ? pattern2: 'transparent');
         //fill.setColor(pattern)
     //    return style;
     //  };
       
       
       // Create a vector layer that makes use of the style function above…
      // var vectorLayer = new ol.layer.Vector({
      //   source: new ol.source.Vector({
      //     url: 'https://openlayers.org/en/v4.6.5/examples/data/geojson/countries.geojson',
      //     format: new ol.format.GeoJSON()
      //   }),
      //   style: getStackedStyle
      // });
      // console.log("OSM"+vectorLayer)
       //map.addLayer(vectorLayer)