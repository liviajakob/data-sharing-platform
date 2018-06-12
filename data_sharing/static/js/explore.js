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

      /*swipe.addEventListener('input', function() {
        map.render();
      }, false);*/
      
      /*Render new display*/
    //document.getElementById('map').addEventListener('click')
	
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
        	console.info(result.value);
            $('#point-value').html('<p> <strong>Value: </strong>' + result.value + '</p>');
            
         });
		
       
	}else{
		console.log('oops');
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

