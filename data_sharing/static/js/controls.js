/* IceExplorer - OpenLayer controls
 * Filename: controls.js
 * 
 * This code adds all the controls to the map and creates custom controls
 * Author: Livia Jakob
 * */


/* Add control showing the mouse position
 * 
 *  */
var mousePositionControl = new ol.control.MousePosition({
    coordinateFormat: ol.coordinate.createStringXY(4), //precision
    projection: projection,
    className: 'custom-mouse-position',
    target: document.getElementById('mouse-position'),
    undefinedHTML: '&nbsp;'
  });

map.addControl(mousePositionControl);
map.addControl(new ol.control.FullScreen({source: 'fullscreen'}));




/* Add Layerswitcher from the ol-layerswitcher plugin
 * 
 * */
var layerSwitcher = new ol.control.LayerSwitcher({
	tipLabel: 'Layers', // Optional label for button
	enableOpacitySliders: true
});
map.addControl(layerSwitcher);




/* Enable all tooltips on the page
 * Using bootstrap tooltips
 * */
$(function () {
	  $('[data-toggle="tooltip"]').tooltip()
	})
$('.ol-zoom-in, .ol-zoom-out').tooltip({
    placement: 'right'
  });
$('.custom-reset').tooltip({
    placement: 'right'
  });
$('.ol-full-screen-false').tooltip({
    placement: 'left'
  });
$('.ol-full-screen-true').tooltip({
    placement: 'left'
  });
$('.ol-overviewmap button').tooltip({
    placement: 'right'
  });
$('.toggle-swipe').tooltip({
    placement: 'right'
  });





/* 
 * Create custom controls
 * */
      
//Define a namespace for the application.
window.app = {};
var app = window.app;
  
/* Create Reset Button */      
app.ResetControl = function(opt_options) {
	var options = opt_options || {};
	var reset = document.createElement('button');
	reset.className = 'custom-reset';
	reset.title = 'Reset Map';
	
	var refresh= function(){
		//zoom out
		map.getView().fit(mapextent, {duration: 1000}); 
		
		//show extents
		polylayer.setVisible(true);
		
		//remove layers and reset
		resetDatasetMode();
		clickdatasets=true;
	}
	
	// add EventListeners
	reset.addEventListener('onchange', refresh, false);
	reset.addEventListener('click', refresh, false);
	reset.addEventListener('touchstart', refresh, false);
	
	// create div to display button
	var element = document.createElement('div');
	element.className = 'refresh-control ol-unselectable ol-control';
	element.appendChild(reset);
	ol.control.Control.call(this, {
		element: element,
	    target: options.target
	});
};
    
ol.inherits(app.ResetControl, ol.control.Control); // inherit
map.addControl(new app.ResetControl()); // add to map


/* Resets the dataset explore mode 
 * 
 * (resets tool modes and removes layers)
 * */
function resetDatasetMode(){
	//stop swipe mode
	stopSwipe(swipelayer);
	//stop get values mode
	stopGetValuesMode();
	//hide toolbox
	$('#toolbox').hide();
	//hide infobox
	$('#infobox-detailed').hide();
	//remove layers
	removeLayers();
}

/* Removes all layers in the eyplore dataset view
 * */
function removeLayers(){
	while(dataset_tilelayers.getLayers().getArray().length > 0) {
		dataset_tilelayers.getLayers().getArray().pop(); // remove
	}
}


   