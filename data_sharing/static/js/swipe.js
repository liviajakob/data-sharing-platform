      
var bing = map.getLayers().getArray()[2];

console.log('BINDG',bing);
console.log(map.getLayers().getArray().length)
startSwipe(bing);


function startSwipe(layer){
	var swipe = document.getElementById('swipe');
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

}
