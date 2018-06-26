exploremode=false;

map.on('click', function(evt){
	//$('#map').css( 'cursor', '');
	//$('#map').cursor('wait');
	if (exploremode){
		getValue(evt);
	}
	
});



var explorebutton = document.getElementById('toggle-explore');
explorebutton.addEventListener('click', function(){
	if (exploremode){
		stopExplore();
	}else{
		startExplore();
		//toplayer=arr[arr.length-1];
		
	}
	
})




function startExplore(){
	console.log('START EXPLORING');
	//swipelayer=layer;
	exploremode=true;
	document.getElementById('map').style.cursor="pointer";
	//$('selector').css({'cursor': 'url(../img/logo.png), pointer'});
	console.log(dataset_tilelayers.getLayers().getArray().length)
	
	explorebutton.style.backgroundColor = "rgba(93, 62, 60, 0.8)";
	$('#toggle-explore').tooltip('hide').attr('data-original-title', 'Stop explore mode')
	
	//change cursor
	document.getElementById('map').classList.add('explore-cursor');
	$('#point-info').show();
}



function getValue(evt){
	coords=map.getCoordinateFromPixel(evt.pixel);
	
	ll_arr = dataset_tilelayers.getLayers().getArray();
	top_l = getTopVisibleLayer(ll_arr);
	if (top_l){
		j_url=api_link +'/get_value/'+top_l.get('id')+'?x='+coords[0]+'&y='+coords[1];
		console.log('TOP',top_l)
		console.log(j_url);
		
        $.getJSON(j_url, function(result) {
        	console.info(result.data);
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


function stopExplore(){
	console.log('STOP EXPLORING');
	if (exploremode){
		
		$("#map").off('click');
		
		document.getElementById('map').classList.remove('explore-cursor');
		explorebutton.style.backgroundColor = "";
		$('#toggle-explore').tooltip('hide').attr('data-original-title', 'Enter explore mode to explore layer values')
		exploremode=false;
		$('#point-value').html('Click on the map to query values of the top layer');
		$('#point-info').hide();
		/*Remove Event Listeners*/
		//map.removeEventListener('click');
		//layer.removeEventListener('precompose');
		//$('#map').unbind('click');
	}
}



////// CHART

function displayChart(data){
	
	ctx = document.getElementById('chart').getContext('2d');
	
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
	            borderColor: '#fff',//"#3d6466",
	            backgroundColor: "#fff"
	        }]
	    },
	    options: {
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
	
	






