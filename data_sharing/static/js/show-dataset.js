/* All actions when user clicks on a dataset; zoom to extent and display dataset and layer information */


var colourvalues;


  //////////click interaction//////////////////////////////

//TODO: clickdataset assure that can't be false for a long time...


     /*Zoom to layer on click*/
     var featureListener = function(event, feature) {
    	 //console.log('EVENT',event);
    	 map.getView().fit(feature.getGeometry(), {
    		  duration: 1000,
    		  nearest: true
    		});
    	 polylayer.setVisible(false);
    	 console.log('FID', feature.getId())
    	 filter={'id': feature.getId()}
    	 filter =JSON.stringify(filter)
    	 link='datasets?timelayers=true&filter='+ filter
    	 	$.getJSON(link, function(data) {
				console.log('data', data.features[0].properties);
				displayDataset(feature, data.features[0].properties);
		  	});
    	 
         //console.log(feature.getId());
         //alert("Feature Listener Called");
    	 //clickdatasets=true;
       };

       map.on('click', function(event) {
    	   //console.log('1');
    	 if (clickdatasets){
    		 //console.log('2');
    		 clickdatasets=false;
    		 polyfound=false;
	         map.forEachFeatureAtPixel(event.pixel,
	         function(feature, layer) {

	           if (!polyfound && feature && feature.getGeometry().getType() == 'Polygon') {
	             //feature.setStyle(listenerStyle);
		        	 console.log(feature.getId())
		        	 //console.log(feature.getGeometry().getType())
	        	 polyfound = true
	             featureListener(event, feature);
	             
	           }
	         });
	         window.setTimeout(function(){clickdatasets=true;}, 1000);
	         
         }
       });
       
   
       
       
     function displayDataset(polygon, dataset){
    	 var myLayer;
    	 console.log('DATASET_CLICKED',dataset.id);
    	 
    	 // remove other dataset layers
    	 resetDatasetMode();
    	 
    	 polyext = polygon.getGeometry().getExtent();
    	 console.log('EXTENT',polyext);
    	 //polyext_tr = ol.proj.transformExtent(polyext, ol.proj.get('EPSG:3413'), ol.proj.get('EPSG:3857'))
    	 d_layers = dataset.layers;
    	 console.log(d_layers);
    	 for (var i = d_layers.length-1; i >= 0; i--){
    		 /* TODO: CONFIGURE URL */
    		 layer=d_layers[i]
    		 console.log(layer);
    		 timeseries = layer.timeseries;
    		 for (var e = timeseries.length-1; e >= 0; e--){
    			 series = timeseries[e]
    			 console.log(series);
    			 tileurl = root_link+ '/'+ series.tileurl +'/{z}/{x}/{-y}.png';
    			 console.log(tileurl)
    			 visible=false
    			 if (i==0 && e==0){
    				 visible = true
    			 }
    			 myLayer = generateLayer(tileurl, series, layer, visible);
    			 
    		 }
    		 
    		 
   			//var myLayer = generateLayer(tileurl, layer, i);

    	 }
    	 map.updateSize();
	    	     $('#infobox').hide();
	    	     $('#toolbox').show();
	    	     displayDetailedInfo(detailedInfo(dataset));
	    	     getLegend(myLayer);
     }
     
     
     function generateLayer(url, series, layer, visible){
	     var source = new ol.source.OSM({
             url: url, //'http://127.0.0.1:8887/14/dem/tiles/{z}/{x}/{-y}.png',
             crossOrigin: null //hack file
		     })
		idcom = layer.layertype+series.date
		 myLayer = new ol.layer.Tile({
		   source: source,
		   projection: projection,
			   extent: polyext, 
			   opacity: 1,
			id: idcom,
			visible: visible,
			layertype: layer.layertype,
			layerid: layer.id,
			date: series.date
		 });
		 dataset_tilelayers.getLayers().getArray().push(myLayer); //add it to the group layer
		 console.log("PRINT ID",myLayer.get('id'))
    	 return myLayer;
    	 
     }
     
     
     
     
     
     
     
     
     
     ///////////////////////////////////////
     ///////detailed infobox
     /*$('#infobox-detailed').appendTo(
  	         $('.ol-overlaycontainer')
  	       )
  	$('.ol-overlaycontainer').on('scroll', function(e){
    e.stopPropagation();
    console.log('hi');
    e.browserEvent.preventDefault();
  	});*/

     
     function displayDetailedInfo(info) {
  	   $('#info-title').html(info[0]);
         $('#infobox-detailed-content').html(info[1]);
         $('#infobox-detailed').show();
         //$('#infobox-detailed-content').show();
       }
     
     
     
     
     /*Returns html for info showed when exploring a dataset*/
     function detailedInfo(dataset){
  	   title = '<h5>Dataset: '+dataset.id+'</h5>'
  	   html='';
  	   html=html.concat('<b>Time span:</b> ' + dataset.startdate + ' - ' + dataset.enddate + '<br>')
  	   html=html.concat('<b>Projection:</b> ' + dataset.projection + '<br>')
  	   html=html.concat('<b>Covered area (extent): </b>' + dataset.area + ' km<sup>2</sup>')
  	   html=html.concat("<hr><hr>" + "<h6>Available Layers: </h6>")
  	   layers=dataset.layers;
	   		for (i = 0; i < layers.length; i++){
	   			layer= layers[i]
	   			
	   			html=html.concat('<div class="layer-outer"><div class="collapse-title" data-toggle="collapse" data-target="#l'+layer.layertype+'" aria-expanded="false" class="collapsed">')
	   			
	   			html=html.concat('<b class="upper"> '+layers[i].layertype + ' </b> | (Layer id: '+ layers[i].id+ ')')
	   			html=html.concat('<button class="collapse-button">&times;</button>')
	   			
	   			//html=html.concat('<br><input id="slider" type="range" min="0" max="1"step="0.1" value="1" oninput="getLayerById('+layers[i].id+').setOpacity(this.value)">')
	   			html=html.concat('<br></div><div id="l'+layer.layertype+'" class="collapse show" style="background-color: transparent; border-radius: 4px; padding-top: 15px;">')
	   			
	   			
	   			for (e = 0; e<layer.timeseries.length; e++){
	   				series = layer.timeseries[e]
	   				sid= layer.layertype+series.date
	   				html=html.concat('<div style="padding-bottom: 10px; padding-left: 10px;"><input type="checkbox" value="'+sid+'" id="l_visible" ')
	   				if (i==0 && e==0) html=html.concat('checked')
	   				html=html.concat('>  <b>Date: </b>'+ series. date)
	   				html=html.concat('<button class="download" data-toggle="tooltip" data-placement="right" data-original-title="Download this layer" id="download-layer" value="'+'layer_id='+layer.id+'&date='+series.date+'">Download </button>')
	   				html=html.concat('<br></div>')
	   			}
	   			html = html.concat("</div></div>"); 
	   		}
	   		//html=html.slice(0,-2);
	   		html = html.concat("</div>");  
	   		html = html.concat("<hr><hr><b>Cite this dataset as: </b>" + dataset.cite + "<br>");
  	   return [title, html];
     }
     
     
     
     
     
     //////// DATASET LAYERSWITCHER
     
  	$(document).ready(function(e) {
  		$(document).on('change', '#l_visible', function(e){
  			var checked = $(e.target).prop("checked") //.checked;
  			console.log('prop',$(e.target).prop('checked'))
  			id_ = $(e.target).prop("value");
  			console.log('id',id_);

  			
  			layer_byid = getLayerById(id_);
  			
  			console.log('LAYERBY ID',layer_byid);
  			
        	  if (typeof layer_byid !='undefined' && checked !== layer_byid.getVisible()) {
        	    layer_byid.setVisible(checked);
        	    map.updateSize();
        	    //layer_byid.setZIndex(10);
        	    console.log('SETTING TO', checked);
        	  }
        	  
        	// set legend to toplayer
      		ll_arr = dataset_tilelayers.getLayers().getArray();
    		top_l = getTopVisibleLayer(ll_arr);
    		if (top_l){
    			getLegend(top_l);
    		}
  	});
  	});
  	
  	
  	/*Returns layer with id id_*/
  	function getLayerById(id_){
  			var layer_;
  			
  			dataset_tilelayers.getLayers().forEach(function (lyr) {
  				console.log('length',dataset_tilelayers.getLayers().getArray().length)
  				//console.log('-->',dataset_tilelayers.getLayers().getArray()[1].get('id'))
  				console.log('layer',lyr)
  				console.log(id_, lyr.get('id'))
		            if (id_.toString() === lyr.get('id').toString()) {
		            	console
		                layer_ = lyr;
		            }            
		        });
  			console.log("LAYERBY IS",layer_);
  			return layer_
  	}
  	

     
     