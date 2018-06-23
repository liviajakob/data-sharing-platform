
var page_size = 5;

showData(1);

var currentquery;



/*Get Layertype JSON*/
	$.getJSON('layertypes', function(data) {
        //data is the JSON string
    	displayLayertypes(data)
    });
	

function displayLayertypes(data){
	div = document.getElementById('layertypes');
	layertypes=data.layertypes;
	html='';
	for (i in layertypes){
		html = html.concat(layertypes[i] + ' | ')	
	}
	html=html.slice(0,-2);
	div.append(html)
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
	currentquery=filter;
	url= 'data?' //TODO add the filters here
	url=url +'page='+page+'&'+'page_size='+page_size;
	
	console.log('UROLLL',url)
	/*Get JSON*/
	$.getJSON(url, function(data) {
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
	nextpage = '<button class="page-button" onclick="showData('+next+ ', '+ currentquery +')" id="next-page">&#8250;</button>';
	html="";
	previouspage = '<button class="page-button" onclick="showData('+prev+ ', '+ currentquery +')" id="previous-page">&#8249;</button>';
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
	//fetbid.setStyle(stylecoll);
					
	}//,
	//function(){
    //var fetbid = polylayer.getFeatureById($(this).attr("id"));
    //fetbid.setStyle(cStyle);
	//}
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



