/* IceExplorer - Swipe Tool
 * Filename: swipe.js
 * 
 * This code handles the swipe mode in the toolbox
 * Author: Livia Jakob
 * */

var swipemode=false; //set swipe mode initially to false
var swipelayer; //current swipe layer


/*Add click EventListener to swipe button*/
var swipebutton = document.getElementById('toggle-swipe');
swipebutton.addEventListener('click', function(){
	if (swipemode){ //swipemode is a global variable keeping track of the modus
		stopSwipe(swipelayer);
	}else{ // start swipe mode
		ll_arr = dataset_tilelayers.getLayers().getArray(); //all layers
		top_l = getTopVisibleLayer(ll_arr);
		if (top_l){
			startSwipe(top_l);
		}
	}
	
})


/*Start Swipe Mode
 * 
 * layer - the top visible layer the swipe mode will be bound to
 * */
function startSwipe(layer){
	/*Set global variables*/
	swipelayer=layer;
	swipemode=true;
	
	/*Get swiper HTML element*/
	var swipe = document.getElementById('swipe');
	swipe.value = 50; //default value is set in the middle
	swipe.style.visibility = 'visible'; //set to visible
	swipebutton.style.backgroundColor = "rgba(93, 62, 60, 0.8)"; // change button style
	/*Change the tooltip*/
	$('#toggle-swipe').tooltip('hide').attr('data-original-title', 'Stop swipe mode')
	
	/* Set EventListeners
	 * With precompose and postcompose EventListeners
	 * */
    layer.on('precompose', function(event) {
        var ctx = event.context; //get ol map canvas
        /* Calculate where the slider is on the canvas element
         * this calculates the width of the transparent part of the map*/
        var width = ctx.canvas.width * (swipe.value / 100);

        ctx.save(); //save the canvas element (to be able to restore)
        ctx.beginPath();
        // draw rectangle over the side left of the slider position
        ctx.rect(width, 0, ctx.canvas.width - width, ctx.canvas.height);
        ctx.clip(); // turns the rectangle into a clipping path
      });

	
    layer.on('postcompose', function(event) {
      var ctx = event.context;
      ctx.restore(); // restore the canvas context
    });

      swipe.addEventListener('input', function() {
        map.render(); // render to display changes
      }, false);
      
      /*Initial render to display swipe*/
      map.render();
      
}//End of startSwipe()


/* Stop Swipe Mode
 * 
 * layer - the swipe mode is bound to this layer
 * */
function stopSwipe(layer){
	if (swipemode){
		swipe.style.visibility = 'hidden'; //hide swiper
		swipebutton.style.backgroundColor = ""; //style button back to default
		//Change the tooltip
		$('#toggle-swipe').tooltip('hide').attr('data-original-title', 'Enter swipe mode to compare the two top layers')
		swipemode=false; //set global variable
		/*Remove Event Listeners*/
		layer.removeEventListener('postcompose');
		layer.removeEventListener('precompose');
		map.render(); //render new display
	}
}


/* HELPER METHOD: Returns the top visible layer in layerarr, 
 * an empty string when no visible layer is found
 * 
 * layerarr - array with all layers
 * */
function getTopVisibleLayer(layerarr){
	/*Iterate backwards because highest layer is at the back*/
	for (var i = layerarr.length - 1; i >= 0; --i) {
		if (layerarr[i].getVisible()){ //check if visible
			return layerarr[i]; //return if visible
		}
	}
	return ""; // when no layer is visible or array is empty
}


