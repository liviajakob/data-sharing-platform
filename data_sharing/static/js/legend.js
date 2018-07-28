/* IceExplorer - Interactive Legend
 * Filename: legend.js
 * 
 * This code created and updates the interactive legend in the toolbox
 * Author: Livia Jakob
 * */


var legend  = document.getElementById('legend-bar');


/* Displays the interactive legend in the toolbar
 * 
 * layer - the layer of which a legend should be displayed
 * */
function getLegend(layer){
	// request colourvalues and corresponding values
	link = 'colours?layergroup_id='+layer.get('layerid');
	$.getJSON(link, function(data) {
		colourvalues=data.values;
		//draw the legend
		drawColourLegend(data.rgb, data.min, data.max);
  	});
	
	//tooltip
	$('#legend-bar').attr("data-original-title", "Click on the legend to see the exact value represented by the clicked colour")
}
  	


/* Draws the colour legend using HTML Canvas
 * 
 * colours - an array of rgb(x,y,z) colour strings
 * min - corresponding value of the first colour
 * max - corresponding value of the ast colour
 * */
function drawColourLegend(colours, min, max){

    ctx = legend.getContext('2d');
	ctx.clearRect(0, 0, 100, 64); // clear to not overwrite with new text

	// draw the colourbar
	for(var i = 0; i <= colours.length; i++) {
	    ctx.beginPath();
	    var color = colours[i];
	    ctx.fillStyle = color;
	    // fill a little rectangle of the current colour
	    ctx.fillRect(0,i, 20, 1);
	}

	// drawing min and max values
	ctx.fillStyle = "rgb(255,255,255)";
	ctx.font="13px Raleway";
	ctx.fillText(min, 30,10);
	maxpos=(colours.length-7)
	ctx.fillText(max, 30, maxpos);
}





/* EventListener for interactivity of legend
 * Displays corresponding value in a tooltip
 * 
 * */
legend.onclick = function(e) {
	ctx = legend.getContext('2d');
    if (e.offsetX<=20 && e.offsetY<=colourvalues.length){
    	$('#legend-bar')
    		.tooltip('hide')
    		.attr("data-original-title", 'Clicked value: '+colourvalues[e.offsetY])
    		.tooltip('show');
    }
    
};
  	
   