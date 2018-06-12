      
var bing = map.getLayers().getArray()[2];
var swipemode=false;
var swipelayer;

console.log('BINDG',bing);
console.log(map.getLayers().getArray().length)
//startSwipe(bing);


var swipebutton = document.getElementById('toggle-swipe');
swipebutton.addEventListener('click', function(){
	if (swipemode){
		stopSwipe(swipelayer);
	}else{
		ll_arr = dataset_tilelayers.getLayers().getArray();
		console.log('llarr',ll_arr)
		console.log('llarr1',ll_arr[0])
		top_l = getTopVisibleLayer(ll_arr);
		if (top_l){
			console.log('TOP',top_l)
			startSwipe(top_l);
		}
		//toplayer=arr[arr.length-1];
		
	}
	
})


/*Returns the top visible dataset layer*/
function getTopVisibleLayer(layerarr){
	console.log('layerarr', layerarr);
	console.log('layerarr0', layerarr[0]);
	for (var i = layerarr.length - 1; i >= 0; --i) {
		console.log('layerarr_visible', layerarr[i].getVisible());
		if (layerarr[i].getVisible()){
			console.log('layerarr_ii', layerarr[i]);
			return layerarr[i];
		}
	}
	console.log('returning zero');
	return "";
}


function startSwipe(layer){
	swipelayer=layer;
	swipemode=true;
	var swipe = document.getElementById('swipe');
	console.log(dataset_tilelayers.getLayers().getArray().length)
	swipe.value = 50;
	swipe.style.visibility = 'visible';
	swipebutton.style.backgroundColor = "rgba(93, 62, 60, 0.8)";
	$('#toggle-swipe').tooltip('hide').attr('data-original-title', 'Stop swipe mode')
	
    layer.on('precompose', function(event) {
        var ctx = event.context;
        var width = ctx.canvas.width * (swipe.value / 100);

        ctx.save();
        ctx.beginPath();
        ctx.rect(width, 0, ctx.canvas.width - width, ctx.canvas.height);
        ctx.clip();
      });

      layer.on('postcompose', function(event) {
        var ctx = event.context;
        ctx.restore();
      });

      swipe.addEventListener('input', function() {
        map.render();
      }, false);
      
      /*Render new display*/
      map.render();
}


function stopSwipe(layer){
	if (swipemode){
		swipe.style.visibility = 'hidden';
		swipebutton.style.backgroundColor = "";
		$('#toggle-swipe').tooltip('hide').attr('data-original-title', 'Enter swipe mode to compare the two top layers')
		swipemode=false;
		/*Remove Event Listeners*/
		layer.removeEventListener('postcompose');
		layer.removeEventListener('precompose');
		map.render();
	}
}

