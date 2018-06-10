/* All actions when user clicks on a dataset; zoom to extent and display dataset and layer information */


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
    	 d_layers = dataset.get('layers');
    	 console.log(d_layers);
    	 for (var i = d_layers.length-1; i >= 0; i--){
    		 /* TODO: CONFIGURE URL */
	    	 url= root_link+ '/'+ dataset.getId() + '/'+dataset.get('layers')[i].layertype + '/tiles/{z}/{x}/{-y}.png';
	    	 console.log('URL',url);
	    	 
	    	     var source = new ol.source.OSM({
	    	                 url: url, //'http://127.0.0.1:8887/14/dem/tiles/{z}/{x}/{-y}.png',
	    	                 crossOrigin: null //hack file
	    	         })
	     
	    	     var myLayer = new ol.layer.Tile({
	    	       source: source,
	    	       projection: 'EPSG:4326',
	    	    	   extent: polyext, 
	    	    	   opacity: 1,
	    	    	id: dataset.get('layers')[i].id,
	    	    	visible: (i==0),
	    	     });
	    	     dataset_tilelayers.getLayers().getArray().push(myLayer); //add it to the group layer
    	 }
	    	     $('#infobox').hide();
	    	     displayDetailedInfo(detailedInfo(dataset));
	    	     
     }
     
     
     
     
     
     
     
     
     
     ///////////////////////////////////////
     ///////detailed infobox
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
  	   html = '<p>'+"</b>Cite this dataset as: " + feature.get('cite') + "<br> " + "<h6>Layers: </h6>";
  	   layers=feature.get('layers');
	   		for (i = 0; i < layers.length; i++){
	   			html=html.concat('<div><input type="checkbox" value="'+layers[i].id+'" id="l_visible" ')
	   			//console.log(layers[i].get('visible'))
	   			if (i==0) html=html.concat('checked')
	   			html=html.concat('> Layer: '+ layers[i].id+ ' | <b>'+layers[i].layertype + ' </b> </div>')
	   		}
	   		html=html.slice(0,-2);
	   		html = html.concat("</p>");
  	   
	   		
  	   
  	   return [title, html];
     }
     
     
     
     
     
     //////// LAYERSWITCHER
     
  	$(document).ready(function(e) {
  		$(document).on('change', '#l_visible', function(e){
  			var checked = $(e.target).prop("checked") //.checked;
  			console.log('prop',$(e.target).prop('checked'))
  			id_ = $(e.target).prop("value");
  			console.log('id',id_);
  			var layer_byid;
  			
  			dataset_tilelayers.getLayers().forEach(function (lyr) {
  				console.log('length',dataset_tilelayers.getLayers().getArray().length)
  				console.log('-->',dataset_tilelayers.getLayers().getArray()[1].get('id'))
  				console.log('layer',lyr)
  				console.log(id_, lyr.get('id'))
		            if (id_.toString() === lyr.get('id').toString()) {
		                layer_byid = lyr;
		            }            
		        });
  			console.log(layer_byid);
  			
        	  if (typeof layer_byid !='undefined' && checked !== layer_byid.getVisible()) {
        	    layer_byid.setVisible(checked);
        	    //layer_byid.setZIndex(10);
        	    console.log('SETTING TO', checked);
        	  }
  	});
  	});
   
   
     
     
     
     
     
     