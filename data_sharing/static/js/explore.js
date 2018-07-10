/* IceExplorer - Explore Tool
 * 
 * This code handles the explore mode in the toolbox
 * Author: Livia Jakob
 * */


exploremode=false; // set explore mode initially to false


/*Add EventListener*/
map.on('click', function(evt){
	if (exploremode){
		getValues(evt); //get values and display results
	}
});


/*Add click EventListener to explore button*/
var explorebutton = document.getElementById('toggle-explore');
explorebutton.addEventListener('click', function(){
	if (exploremode){ //exploremode is a global variable keeping track of the modus
		stopExplore();
	}else{
		startExplore();
	}
})


/*Start Explore Mode*/
function startExplore(){
	exploremode=true; // set global variable
	//document.getElementById('map').style.cursor="pointer"; //change cursor
	
	explorebutton.style.backgroundColor = "rgba(93, 62, 60, 0.8)"; // change button style
	// change tooltip text
	$('#toggle-explore').tooltip('hide').attr('data-original-title', 'Stop explore mode')
	
	//change cursor
	document.getElementById('map').classList.add('explore-cursor');
	$('#point-info').show(); // display window with results
}

/*Stop Explore Mode*/
function stopExplore(){
	if (exploremode){	
		$("#map").off('click');
		//change cursor
		document.getElementById('map').classList.remove('explore-cursor');
		explorebutton.style.backgroundColor = "";
		// change tooltip
		$('#toggle-explore').tooltip('hide').attr('data-original-title', 'Enter explore mode to explore layer values')
		exploremode=false; //set global variable
		//change and hide result box
		$('#point-value').html('Click on the map to query values of the top layer');
		$('#point-info').hide(); //hide result box
	}
}


/* Gets and displays values of a clicked point in the map
 * 
 * evt - the click event
 * */
function getValues(evt){
	//clicked coordinates
	coords=map.getCoordinateFromPixel(evt.pixel);
	console.log(coords[0], coords[1])
	// get top visible layer
	ll_arr = dataset_tilelayers.getLayers().getArray();
	top_l = getTopVisibleLayer(ll_arr);
	
	if (top_l){
		j_url=api_link +'/v1/values?layer_id='+top_l.get('layerid')+'&x='+coords[0]+'&y='+coords[1];
		
        $.getJSON(j_url, function(result) {
        	console.info(result);
        	if (result.data.length<=1){
        		$('#point-value').html('<h6>Value of clicked position:</h6><hr>'
        				+'<p> <strong>Date: </strong>' + result.data[0].x + '<br>'
        				+'<strong>Value: </strong>' + result.data[0].y + '<br>' 
        				+'No timeseries for this layer available</p>');
        	}else{
        		$('#point-value').html('<h6>Timeseries – Value of clicked position over time</h6><hr>'
        				+'<canvas id="chart" style="height: 150px; width: 100%;"></canvas>');
        		displayChart(result.data);
        	} 
         });
		
       
	}else{
		$('#point-value').html('<p>No dataset layer displayed</p>');
	}
}


////// DISPLAY CHART ////////////////////////////////////////////////////

/* Display the data in a Chart.js chart
 * Data is expected in the following format: 
 * 
 * 	[{
 * 		x: 2012-07-27,
 * 		y: 20
 * 	}, {
 * 		x: 2013-07-27,
 * 		y: 10
 * 	}]
 * 
 * */
function displayChart(data){
	//canvas element
	ctx = document.getElementById('chart').getContext('2d');
	//set global styles
	Chart.defaults.global.defaultFontColor = 'white';
	Chart.defaults.global.defaultFontFamily = 'Raleway, sans-serif';
	var scatterChart = new Chart(ctx, {
	    type: 'line',
	    data: {
	        datasets: [{
	            label: ' Value',
	            data: data,
	            borderColor : "#fff",
	            borderWidth : "3",
	            hoverBorderColor : "#000",
	            showLine: false,
	            borderColor: '#fff',
	            backgroundColor: "#fff"
	        }]
	    },
	    options: { // setting styles and display options
	    	  legend: {
	    		    display: false
	    		  },
	        scales: {
	            xAxes: [{
	            	type: 'time',
	                //distribution: 'series',
	                time: {
	                	tooltipFormat: ' MM/DD/YY',
	                	displayFormat:'MM/DD/YY'
	                },
	                ticks:{
	                    fontColor : "#fff",
	                  },
	                gridLines: {
		        		zeroLineColor: "#fff"
		        	}
	            }],
	            yAxes: [{
	                ticks:{
	                    fontColor : "#fff",
	                  },
	                  gridLines: {
	  	        		zeroLineColor: "#fff"
	  	        	}
	            }]
	        }
	    }
	});	
}
	
	