/* Ice Explorer - Sidebar Display
 * Filename: sidebar-display.js
 * 
 * Manages display and filter / pagination options of the sidebar
 * 
 * Author: Livia Jakob
 * */


var page_size = 5;
var currentquery = ''; // saves the current query
showData(); // initially show data of first page





/* Requests datasets and shows them in list in the sidebar
 * 
 * page - page nr, default is 1
 * filter - optional filteroptions, a URL string (e.g. '&id=4')
 * 
 * */
function showData(page=1, filter){
	if (typeof filter !== 'undefined'){ // if filter options given
		currentquery=filter;
	}else{
		filter='';
	}
	url= 'datasets?' +'page='+page+'&'+'page_size='+page_size+filter;
	//Get datasets JSON
	$.getJSON(url, function(data) {
    	displayDatasets(data.features); // display datasets in list
    	makePolys(data); // create map polygons of the datasets
    	displayPages(page, data.features.length); // create page button HTML
    });
}

	
/* Displays datasets in a list in the sidebar
 * 
 * datasetsarr - and array of dataset information in JSON format
 * */
function displayDatasets(datasetsarr){
	div = document.getElementById('datasets-content');

	var list = $("#datasets-list");
	list.html(''); //set to empty
	for (i in datasetsarr){
	    var id = datasetsarr[i].properties.id;
		var layers = datasetsarr[i].properties.layergroups;
		var startdate = datasetsarr[i].properties.startdate;
		var enddate = datasetsarr[i].properties.enddate;

		/* Sort by layertype name so that they have the same order
		 * e.g. DEM will be displayed first
		 * */
		layers.sort(function(a, b) {
		    return a.layertype.localeCompare(b.layertype);
		});
		// create list entry
		html= "<tr><td value='" + id + "'>" + "<b>"+ "Dataset | </b> id: " + id + "<br>" 
		html=html.concat(startdate + ' - ' + enddate)
		html=html.concat("<br> " + "<b>Available Layertypes: </b><span class='upper'>")
		// add available layertypes
		for (l in layers){
			html=html.concat(layers[l].layertype + ', ')
		}
		html=html.slice(0,-2); // remove last '|' character
		html = html.concat("</span></tr></td>");
	    list.append(html); // append to html
	}
}


/* Creates the HTML for the page buttons
 * 
 * page - page number, e.g. 1
 * displayed_number - number of entries displayed in the page
 * */
function displayPages(page, displayed_number){
	pageelement = $("#display-pages");
	next = page+1
	prev = page-1
	nextpage = '<button class="page-button" onclick="showData('+next+')" id="next-page">&#8250;</button>';
	previouspage = '<button class="page-button" onclick="showData('+prev+')" id="previous-page">&#8249;</button>';
	html=previouspage+nextpage;
	pageelement.html(html)
	// disable button previous page if we're on the first page
	if (page==1){
		document.getElementById("previous-page").disabled = true;
	}
	// disable button next page if page is not full
	if (displayed_number<page_size){
		document.getElementById("next-page").disabled = true;
	}
	
	var results = $("#total-result");
	results.html("Displaying page: " + page)
	
	
}



/* Click EventListener for dataset list entries
 * Indetifies the corresponding polygon and then trigger the change to the dataset explore view of the dataset
 * 
 * */
$(document).ready(function(e) {
	$(document).on('click', 'td', function(){
		id = $(this).attr("value");
		var fetbid = polylayer.getSource().getFeatureById(id); // get corresponding dataset polygon
		featureListener(e, fetbid); // trigger the change to the dataset explore view			
	});
});



/* EventListener for hover effect
 * Changes style of the corresponding polygon on the map when hovering over a dataset in the list
 * */
$(document).ready(function($) {
	$(document).on('mouseenter mouseleave', 'td', function(){
		id = $(this).attr("value");
		var fetbid = polylayer.getSource().getFeatureById(id);
		//featureListener(event, fetbid);
		if (fetbid.getStyle() === hoverstyle){
			fetbid.setStyle(geometryStyle(fetbid));
		}else{
			fetbid.setStyle(hoverstyle);
		}
	});
});




/////// Filtering ////////////////////////////////////////////////////////


/* EventListener for filter button
 * Requests and displays filtered datasets
 * 
 * */
$("#filterDatasets").click( function(){
	filter='' // filter string
	
	if ($( "#layertypes" ).val().length > 0){ // check if a layertype is chosen
		filter +='&layertype='+$( "#layertypes" ).val() // add to filter URL
	}
	// time filter
	if ($("#bytime").is(':checked')){ // check if enabled
		var dates = $("#timerange").dateRangeSlider("values");
	    maxdate=formatDate(dates.max) // right side of slider
	    mindate = formatDate(dates.min) // left side of slider
	    filter+= '&startdate='+mindate+'&enddate='+maxdate
	}
	showData(1, filter); // show data of page one
});


/* Brings the data into YYYY-MM-DD format
 * 
 * date - a JavaScrop date object
 * */
function formatDate(date){
	datefm = new Date(date);
    formdate = date.getFullYear().toString()+'-' + (date.getMonth() + 1) + '-' + date.getDate();
	return formdate
}



/* Get all layertypes for the filter options
 * 
 * */
$.getJSON('layertypes', function(data) {
    //data is a JSON string
	displayLayertypes(data.layertypes)
});
	

/* Displays HTML select with layertypes as options
 * 
 * layertypes - array with layertypes
 * 
 * */
function displayLayertypes(layertypes){
	div = document.getElementById('layertypes');
	html='<option selected value="">Choose Layertype</option>';
	for (i in layertypes){
		html = html.concat('<option value="'+layertypes[i]+'">'+layertypes[i]+'</option>')	
	}
	div.innerHTML = html;
}



/* Creat date range silder for filtering
 * 
 * */
$("#timerange").dateRangeSlider({
	range:{
	    min: {days: 1}
	  },
	  bounds:{
		    min: new Date(2016, 0, 1),
		    max: new Date(2019, 1, 31)
	},
	defaultValues:{
	    min: new Date(2017, 0, 1),
	    max: new Date(2018, 11, 31)
	  },
		arrows:false
});



/* Fade in / Fade out time slider when ticking and unticking the checkbox
 * */
$("#bytime").change( function(){
	if (this.checked){
		$("#timerange").fadeTo(100, 1);
	}
	else{
		$("#timerange").fadeTo(100, 0.5);
	}
})

/* Collapse filtering options after 1 second when loading the page
 * */
setTimeout(function() {
	document.getElementById("collapse-btn-inner").click()
}, 1000)


