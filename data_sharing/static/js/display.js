
/*Get JSON*/
	$.getJSON('layertypes', function(data) {
        //data is the JSON string
    	console.log('DATA1')
    	console.log(data);
    	console.log(typeof data)
    	displayLayertypes(data)
    });
	

function displayLayertypes(data){
	div = document.getElementById('layertypes');
	layertypes=data.layertypes
	html=''
	for (i in layertypes){
		html = html.concat(layertypes[i].name + ' | ')	
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




/*Get JSON*/
	$.getJSON('data', function(data) {
        //data is the JSON string
    	console.log('DATAA3')
    	console.log(data);
    	console.log(data.features[0].properties.id);
    	console.log(typeof data)
    	displayDatasets(data)
    });
	
	
function displayDatasets(datasets){
	div = document.getElementById('datasets-content');
	datasetsarr=datasets.features
	
	var results = $("#total-result");
	results.append("Total results: " + datasetsarr.length)
	
	
	var list = $("#datasets-list");

	for (i in datasetsarr){
	    var id = datasetsarr[i].properties.id;
		var cite = datasetsarr[i].properties.cite;
		var layers = datasetsarr[i].properties.layers;

		/*Sort by name so that they have the same order*/
		layers.sort(function(a, b) {
		    return a.layertype.localeCompare(b.layertype);
		});

		html= "<tr><td>" + "<b>"+ "Dataset: " + id + "</b> -- Cite this dataset as: " + cite + "<br>" + "<b>Layers: </b>"
		for (l in layers){
			html=html.concat(layers[l].layertype + ' | ')
		}
		html=html.slice(0,-2);
		html = html.concat("</tr></td>");
	    list.append(html);
	}
}