var export_btn = document.querySelector('#png');
console.log(document.querySelector('#png'));

// PNG
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





	////// DOWNLOAD LAYER BUTTON
	$(document).ready(function(e) {
		$(document).on('click', '#download-layer', function(e){
			val1 = $(e.target).prop("value");
			window.location.href=api_link+'/v1/file?'+val1;
			console.log(api_link+'/v1/file?'+val1)
			//window.href('download');
			//$fileDownload('download')
		    //.done(function () { alert('File download a success!'); })
		    //.fail(function () { alert('File download failed!'); });
			
			

			
	});
	});
	