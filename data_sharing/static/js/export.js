/* IceExplorer - Downloads
 * Filename: export.js
 * 
 * This code handles exports and downloads
 * Author: Livia Jakob
 * */

var export_btn = document.querySelector('#png');

/* EvenListener for Download view as PNG button
 * */
document.querySelector('#png').addEventListener('click', function() {
        map.once('postcompose', function(event) {
          var canvas = event.context.canvas;
          if (navigator.msSaveBlob) {
            navigator.msSaveBlob(canvas.msToBlob(), 'map.png');
          } else {
            canvas.toBlob(function(blob) {
              saveAs(blob, 'map.png');
            });
          }
        });
        map.renderSync();
      });



/* EvenListener for Download layer button
 * */
$(document).ready(function(e) {
	$(document).on('click', '#download-layer', function(e){
		val1 = $(e.target).prop("value");
		window.location.href=api_link+'/v1/file?'+val1;
	});
});
	