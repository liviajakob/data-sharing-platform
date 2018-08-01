/* IceExplorer - Downloads
 * Filename: export.js
 * 
 * This code handles exports and downloads
 * Author: Livia Jakob
 * */


/* EvenListener for Download layer button
 * */
$(document).ready(function(e) {
	$(document).on('click', '#download-layer', function(e){
		val1 = $(e.target).prop("value");
		window.location.href=api_link+'/v1/file?'+val1;
	});
});
	