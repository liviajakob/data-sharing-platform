/* IceExplorer - Map Geometry Style
 * 
 * This defines the style of geometries on the map
 * Author: Livia Jakob
 * */
 


/* Generic method to get style of a geometry
 * 
 * feature - a geometry; LineString, Polygon or Point
 * */
 function geometryStyle(feature){
	    var
	        style = [],
	        geometry_type = feature.getGeometry().getType(),
	        white = [255,255,255, 1],
        blue = [95,158,160,1],
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
 
 
 
 /* Hoverstyle
  * Creates a darker style when hovering over a Polygon
  * 
  * */
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
 
 // general parameter
 white = [255,255,255, 1],
 blue = [95,158,160,1],
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
 