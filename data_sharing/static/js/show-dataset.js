/* Ice Explorer - Detailed Dataset View
 * Filename: show-dataset.js
 * 
 * Manages all actions when user clicks on a dataset; 
 * - zoom to extent and display dataset and layer information
 * 
 * 1. Reset map
 * 2. Request dataset information
 * 3. Generate Layer objects
 * 4. Display detailed information and layers in infobox
 * 5. Show toolbox
 * 6. Zoom smoothly to extent
 * 7. Set Polygon layer invisible
 * 
 * Author: Livia Jakob
 * */


var colourvalues;


/* Map click EventListener
 * If click is on polygon the corresponding dataset is displayed 
 * 
 **/
map.on('click', function(event) {
	if (clickdatasets){ // click dataset is a state variable disabeling the user to click twice while zooming
		 clickdatasets=false;
		 polyfound=false; // to interrupt the loop when the top polygon is found
	     map.forEachFeatureAtPixel(event.pixel, function(feature, layer) { // loop through features at pixel
	     if (!polyfound && feature && feature.getGeometry().getType() == 'Polygon') {
	    	 polyfound = true
	         featureListener(event, feature); // trigger featureListener
	       }
	     });
	     window.setTimeout(function(){clickdatasets=true;}, 1000); // set back after one second
	}
});
   


/* Display and zoom to dataset extent polygon
 * Remove other displayed layers
 * 
 * */
var featureListener = function(event, feature) {
	// remove other dataset layers
	resetDatasetMode();
	
	// request dataset information with layersinfo
	link='datasets?layerinfo=true&id='+feature.getId()
	 	$.getJSON(link, function(data) { 		
			displayDataset(feature, data.features[0].properties);
	  	});
	  
	// zoom to extent
	map.getView().fit(feature.getGeometry(), {
		  duration: 1000, // smoothly
		  nearest: true
		});
	 
	// set polygon layer invisible
	polylayer.setVisible(false);
};
       

/* Displays a dataset
 * 
 * dataset - the dataset to be displayed in JSON format
 * polygon - the corresponding polygon
 * 
 * */
function displayDataset(polygon, dataset){
    var myLayer; // new layer
    
	polyext = polygon.getGeometry().getExtent(); // extent of tile layer
	layer_groups = dataset.layergroups;
	for (var i = layer_groups.length-1; i >= 0; i--){ // iterate through layer groups
		layer_group=layer_groups[i]
		layers = layer_group.layers; // get all layers of layer group
		for (var e = layers.length-1; e >= 0; e--){ // iterate through layers
			 lyr = layers[e]
			 tileurl = root_link+ '/'+ lyr.tileurl +'/{z}/{x}/{-y}.png'; // generate tiles URL
			 visible=false
			 if (i==0 && e==0){ // Top layer in to layer should be visible
				 visible = true
			 }
			 myLayer = generateLayer(tileurl, lyr, layer_group, visible); // generate layer
		}
	 }
	 map.updateSize();
	 $('#infobox').hide(); // hide small infobox
	 $('#toolbox').show(); // show toolbox
	 displayDetailedInfo(detailedInfo(dataset)); // diplay detailed infobox
	 getLegend(myLayer); // generate Legend
 }
 

/* Generates a new OpenLayers Tile layer object
 * 
 * url - the tile url
 * layer - the layer JSON
 * layer_group - the JSON layer group object
 * visible - boolean variable stating if layer should be visible or not
 * 
 * returns the new layer object
 *  */
function generateLayer(url, layer, layer_group, visible){

	// generate th OpenLayers source
	var source = new ol.source.OSM({
         url: url, // tile URL
         crossOrigin: null //hack file, only necessairy for locally hosted
	     })
	idcom = layer_group.layertype+layer.date //generate a unique ID
	// generate the layer
	myLayer = new ol.layer.Tile({
		source: source,
		projection: projection,
		extent: polyext,
		opacity: 1,
		id: idcom,
		visible: visible,
		layertype: layer_group.layertype,
		layerid: layer_group.id,
		date: layer.date
	 });
	 dataset_tilelayers.getLayers().getArray().push(myLayer); //add layer to the group layer
	 return myLayer; 
}
 


////// Generate Detailed Infobox /////////////////////////////////////////////////////

/* Display detailed infobox
 * 
 *  info - an array with length two
 *  	first element: html string of the infobox title
 *  	second element: html string of the infobox content
 *  */
function displayDetailedInfo(info) {
   $('#info-title').html(info[0]);
   $('#infobox-detailed-content').html(info[1]);
   $('#infobox-detailed').show();
}
 
 
 
 
/* Returns an array of length 2 with html string for detailed infobox
 * 
 * Return array:
 * 		[html of title, html of content]
 * */
function detailedInfo(dataset){
	title = '<h5>Dataset: '+dataset.id+'</h5>'
    html='';
    html=html.concat('<b>Time span:</b> ' + dataset.startdate + ' - ' + dataset.enddate + '<br>')
    html=html.concat('<b>Projection:</b> ' + dataset.projection + '<br>')
    html=html.concat('<b>Covered area (extent): </b>' + dataset.area + ' km<sup>2</sup>')
    html=html.concat("<hr><hr>" + "<h6>Available Layers: </h6>")
    layer_groups=dataset.layergroups;
	for (i = 0; i < layer_groups.length; i++){ // generate layergroup display
		layer_group= layer_groups[i]
		html=html.concat('<div class="layer-outer"><div class="collapse-title" data-toggle="collapse" data-target="#l'+layer_group.layertype+'" aria-expanded="false" class="collapsed">')
		html=html.concat('<b class="upper"> '+layer_group.layertype + ' </b> | (Layergroup id: '+ layer_group.id+ ')')
		html=html.concat('<button class="collapse-button">&times;</button>')
		html=html.concat('<br></div><div id="l'+layer_group.layertype+'" class="collapse show" style="background-color: transparent; border-radius: 4px; padding-top: 15px;">')
		for (e = 0; e<layer_group.layers.length; e++){ // generate layers with checkbox
			layer = layer_group.layers[e]
			sid= layer_group.layertype+layer.date
			html=html.concat('<div style="padding-bottom: 10px; padding-left: 10px;"><input type="checkbox" value="'+sid+'" id="l_visible" ')
			if (i==0 && e==0) html=html.concat('checked') // first layer is checked as it is visible
			html=html.concat('>  <b>Date: </b>'+ layer.date)
			html=html.concat('<button class="download" data-toggle="tooltip" data-placement="right" data-original-title="Download this layer" id="download-layer" value="'+'layergroup_id='+layer_group.id+'&date='+layer.date+'">Download </button>')
			html=html.concat('<br></div>')
		}
		html = html.concat("</div></div>"); 
	}
	html = html.concat("</div>");  
	html = html.concat("<hr><hr><b>Cite this dataset as: </b>" + dataset.cite + "<br>");
	return [title, html];
 }
 
 
 

/* EventListener for Infobox Layerswitcher
 * Is triggered on change of a checkbox value
 * Shows and hides the layer; gets a new legend for the top layer
 * */ 
$(document).ready(function(e) {
	$(document).on('change', '#l_visible', function(e){
		var checked = $(e.target).prop("checked") // boolean
		id_ = $(e.target).prop("value");
		layer_byid = getLayerById(id_); // get layer object
		// change visibility
    	if (typeof layer_byid !='undefined' && checked !== layer_byid.getVisible()) {
    	    layer_byid.setVisible(checked);
    	    map.updateSize();
    	}
    	  
    	// generate new legend for the top layer
  		ll_arr = dataset_tilelayers.getLayers().getArray();
		top_l = getTopVisibleLayer(ll_arr);
		if (top_l){
			
			getLegend(top_l); // generate legend
		}
	});
});



/* HELPER METHOD: Returns layer object from id 
 * 
 * id_ - the id of the requested layer
 * */
function getLayerById(id_){
		var layer_;
		dataset_tilelayers.getLayers().forEach(function (lyr) {
	            if (id_.toString() === lyr.get('id').toString()) {
	                layer_ = lyr; // found layer
	            }            
	        });
		return layer_
}
