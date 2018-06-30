
var page_size = 5;

showData(1);

var currentquery = {};



/*Get Layertype JSON*/
	$.getJSON('layertypes', function(data) {
        //data is the JSON string
    	displayLayertypes(data)
    });
	

function displayLayertypes(data){
	div = document.getElementById('layertypes');
	layertypes=data.layertypes;
	html='<option selected value="">Choose Layertype</option>';
	for (i in layertypes){
		html = html.concat('<option value="'+layertypes[i]+'">'+layertypes[i]+'</option>')	
	}
	console.log(html)
	//html=html.slice(0,-2);
	div.innerHTML =html
}



function filterDatasets() {
	  var input, filter, table, tr, td, i;
	  input = document.getElementById("myInput");
	  filter = input.value.toUpperCase();
	  table = document.getElementById("myTable");
	  tr = table.getElementsByTagName("tr");
	  for (i = 0; i < tr.length; i++) {
	    td = tr[i].getElementsByTagName("td")[0];
	    if (td) {
	      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
	        tr[i].style.display = "";
	      } else {
	        tr[i].style.display = "none";
	      }
	    }       
	  }
	}



function showData(page, filter){
	console.info('Filter', filter)
	if (typeof filter !== 'undefined'){
		currentquery=filter;
	}
	console.info('Filter', currentquery)
	param= JSON.stringify(currentquery)
	url= 'data?' //TODO add the filters here
	url=url +'page='+page+'&'+'page_size='+page_size+'&filter='+param;
	
	console.log('UROLLL',url)
	/*Get JSON*/
	$.getJSON(url, function(data) {
		console.log(data);
    	displayDatasets(data);
    	makePolys(data);
    	displayPages(page, data.features.length);
    });
	
}

	
	
function displayDatasets(datasets){
	div = document.getElementById('datasets-content');
	datasetsarr=datasets.features

	
	var list = $("#datasets-list");
	list.html(''); //set to empty
	for (i in datasetsarr){
	    var id = datasetsarr[i].properties.id;
		var cite = datasetsarr[i].properties.cite;
		var layers = datasetsarr[i].properties.layers;

		/*Sort by name so that they have the same order*/
		layers.sort(function(a, b) {
		    return a.layertype.localeCompare(b.layertype);
		});

		html= "<tr><td value='" + id + "'>" + "<b>"+ "Dataset: " + id + "</b> -- Cite this dataset as: " + cite + "<br> " + "<b>Layers: </b>"
		for (l in layers){
			html=html.concat(layers[l].layertype + ' | ')
		}
		html=html.slice(0,-2);
		html = html.concat("</tr></td>");
	    list.append(html);
	}
	
}


function displayPages(page, displayed_number){
	pageelement = $("#display-pages");
	next = page+1
	prev = page-1
	nextpage = '<button class="page-button" onclick="showData('+next+')" id="next-page">&#8250;</button>';
	html="";
	previouspage = '<button class="page-button" onclick="showData('+prev+')" id="previous-page">&#8249;</button>';
	html+=previouspage
	html+=nextpage;
	pageelement.html(html)
	if (page==1){
		document.getElementById("previous-page").disabled = true;
	}
	
	if (displayed_number<page_size){
		document.getElementById("next-page").disabled = true;
	}
	
	
	var results = $("#total-result");
	results.html("Displaying page: " + page)
	
	
}


////////////////////////////////////////////////////////////////
//// click effect


$(document).ready(function(e) {
	$(document).on('click', 'td', function(){
	id = $(this).attr("value");
	console.log('ID',id);
	var fetbid = polylayer.getSource().getFeatureById(id);
	console.log(fetbid);
	featureListener(e, fetbid);			
	}
	);
});


////////////////////////////////////////////////////////////////
////hover effect


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
		
		
		}//,
		//function(){
		//var fetbid = polylayer.getFeatureById($(this).attr("id"));
		//fetbid.setStyle(cStyle);
		//}
		);
		});



$("#filterDatasets").click( function()
        {
          console.log('buttonclicked');
          console.log($( "#layertypes" ).val());
          filter={}
          console.log('type', typeof $( "#layertypes" ).val())
          if ($( "#layertypes" ).val().length > 0){
        	  filter = {'layertype': $( "#layertypes" ).val()}
          }
          console.log('CHECKED', $("#bytime").is(':checked'))
          if ($("#bytime").is(':checked')){
        	  var dates = $("#timerange").dateRangeSlider("values");
              console.log(dates.min + " " + dates.max);
              maxdate=formatDate(dates.max)
              mindate = formatDate(dates.min)
              filter.startdate = mindate
              filter.enddate = maxdate
          }
          console.log(filter)
          showData(1, filter);
        }
     );

function formatDate(date){
	datefm = new Date(date);
    formdate = date.getFullYear().toString()+'-' + (date.getMonth() + 1) + '-' + date.getDate();
	return formdate
}





//////////// Time range slider

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


$("#bytime").change( function(){
	if (this.checked){
		$("#timerange").fadeTo(100, 1);
	}
	else{
		$("#timerange").fadeTo(100, 0.5);
	}
})

setTimeout(function() {
	document.getElementById("collapse-btn-inner").click()
}, 1000)


