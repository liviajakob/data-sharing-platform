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
    	 displayDataset(feature);
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
       
   
       
       
     function displayDataset(dataset){
    	 console.log('DATASET_CLICKED',dataset.getId());
    	 
    	 // remove other dataset layers
    	 resetDatasetMode();
    	 
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
	    	    	layertype: dataset.get('layers')[i].layertype
	    	     });
	    	     dataset_tilelayers.getLayers().getArray().push(myLayer); //add it to the group layer
    	 }
	    	     $('#infobox').hide();
	    	     $('#toolbox').show();
	    	     displayDetailedInfo(detailedInfo(dataset));
	    	     getLegend(myLayer);
	    	     
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
         //$('#infobox-detailed-content').show();
       }
     
     
     
     
     /*Returns html for info showed when exploring a dataset*/
     function detailedInfo(feature){
  	   title = '<h5>Dataset: '+feature.getId()+'</h5>'
  	   html = '<p>'+"</b>Cite this dataset as: " + feature.get('cite') + "<br> " + "<h6>Layers: </h6>";
  	   layers=feature.get('layers');
	   		for (i = 0; i < layers.length; i++){
	   			html=html.concat('<div style="padding-bottom: 10px;"><input type="checkbox" value="'+layers[i].id+'" id="l_visible" ')
	   			//console.log(layers[i].get('visible'))
	   			if (i==0) html=html.concat('checked')
	   			html=html.concat('> Layer: '+ layers[i].id+ ' | <b>'+layers[i].layertype + ' </b> ')
	   			html=html.concat('<button class="download" data-toggle="tooltip" data-placement="right" data-original-title="Download this layer" id="download-layer" value="'+layers[i].id+'" >Download </button>')
	   			
	   			//html=html.concat('<br><input id="slider" type="range" min="0" max="1"step="0.1" value="1" oninput="getLayerById('+layers[i].id+').setOpacity(this.value)">')
	   			html=html.concat('<br></div>')
	   		}
	   		html=html.slice(0,-2);
	   		html = html.concat("</p>");  	   
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
  	
  	
  	
  	//window.location.href='download';
  	
  	////// DOWNLOAD BUTTON
  	$(document).ready(function(e) {
  		$(document).on('click', '#download-layer', function(e){
  			id_ = $(e.target).prop("value");
  			console.log('id',id_);
  			window.location.href=api_link+'/get_file/'+id_;
  			//window.href('download');
  			//$fileDownload('download')
  		    //.done(function () { alert('File download a success!'); })
  		    //.fail(function () { alert('File download failed!'); });
  			
  			
  			/*$.getJSON('download', function(data) {
  		    	console.log('DATA1')
  		    	console.log(data);
  		    	console.log(typeof data)
  		    	
  		    });*/
  			
  	});
  	});
  	
  	
  	
  	
  	
  	
  	////// LEGEND
  	
  	
function getLegend(layer){
	
	console.log('LAYER',layer);
	
	link = 'get_colours?type='+layer.get('layertype');
	console.log('LINK',link);
	
	$.getJSON(link, function(data) {
		colourvalues=data.values;
		drawColourLegend(data.rgb, data.min, data.max);
  	});
}
  	




var legend  = document.getElementById('legend-bar');
	
function drawColourLegend(colours, min, max){
	
	
	
	console.log("MINMAX",min,max,colours)
    ctx = legend.getContext('2d');
	console.log('fill')
	ctx.clearRect(0, 0, 100, 64);
	//ctx.clearRect(0, 0, canvas.width, canvas.height);
	//console.log('COLOURS',colours)
	
	
	
	for(var i = 0; i <= colours.length; i++) {
	    ctx.beginPath();
	    
	    var color = colours[i];//'rgb(100, ' + i + ', ' + i + ')';
	    ctx.fillStyle = color;
	    
	    //ctx.fillRect(i * 2, 0, 2, 50);
	    ctx.fillRect(0,i, 20, 1);
	    
	    
	}
	
	
	
	//ctx.clearRect(0, 0, canvas.width, canvas.height);
	
	// Write min max text
	
	ctx.fillStyle = "rgb(255,255,255)";
	
	ctx.font="13px Raleway";

	ctx.fillText(min, 30,10);
	maxpos=(colours.length-7)
	ctx.fillText(max, 30, maxpos);
}







legend.onclick = function(e) {
	ctx = legend.getContext('2d');
    //var x = e.offsetX,
        //y = e.offsetY,
        //p = ctx.getImageData(x, y, 1, 1),
        //d = p.data;
    console.log('x',e.offsetX,'y',e.offsetY)
    if (e.offsetX<=20 && e.offsetY<=colourvalues.length){
    	alert(colourvalues[e.offsetY]);
    }
    
};
  	
   
   
     
     
     
     
     
     