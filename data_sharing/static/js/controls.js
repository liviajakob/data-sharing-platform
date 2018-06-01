/* JavaScript snippet which adds all the controls to the map */







//////MOUSEPOSITION
        
        var mousePositionControl = new ol.control.MousePosition({
            coordinateFormat: ol.coordinate.createStringXY(4), //precision
            projection: 'EPSG:4313', //'EPSG:3857',
            // comment the following two lines to have the mouse position
            // be placed within the map.
            className: 'custom-mouse-position',
            target: document.getElementById('mouse-position'),
            undefinedHTML: '&nbsp;'
          });
        
        /*var precisionInput = document.getElementById('precision');
        precisionInput.addEventListener('change', function(event) {
          var format = ol.coordinate.createStringXY(event.target.valueAsNumber);
          mousePositionControl.setCoordinateFormat(format);
        });*/
        
        map.addControl(mousePositionControl);
       
        
        







/////CUSTOM CONTOROLS
          
      /**
       * Define a namespace for the application.
       */
      window.app = {};
      var app = window.app;
      
          
      app.RotateNorthControl = function(opt_options) {

        var options = opt_options || {};

        var reset = document.createElement('button');
        reset.innerHTML = 'R';
        
        var nort = document.createElement('button');
        nort.innerHTML = 'N';
        
        //var tool = document.createElement('select');
        //var option = document.createElement('option')
        //option.setAttribute('value', 'hi');
        //var textNode = document.createTextNode(feature.get('NOM'));
        //tool.appendChild(option);
        


        var this_ = this;
        var handleRotateNorth = function() {
        	console.log('ROTATE')
          map.getView().setRotation(90, {duration: 1000});
        };
        
        
        var updatesize= function(){
        	//map.getView().refresh();
        	console.log('UPDATE SIZE');
        	map.getView().setRotation(0, {duration: 1000});
        	//map.getView().fit(map.getView().extent, map.getSize()); 
        }
        
        nort.addEventListener('onchange', handleRotateNorth, false);
        nort.addEventListener('click', handleRotateNorth, false);
        nort.addEventListener('touchstart', handleRotateNorth, false);
        
        reset.addEventListener('click', updatesize, false);
        reset.addEventListener('touchstart', updatesize, false);

        
        var element = document.createElement('div');
        element.className = 'rotate-north ol-unselectable ol-control';
        element.appendChild(nort);
        element.appendChild(reset);
        //element.appendChild(tool);

        
        ol.control.Control.call(this, {
          element: element,
          target: options.target
        });
        
      };
        
        ol.inherits(app.RotateNorthControl, ol.control.Control);

//// ADD CUSTOM CONTROLS
        
        
        map.addControl(new app.RotateNorthControl());
        map.addControl(new ol.control.FullScreen({source: 'fullscreen'}));
 
        
        //layerswitcher
        
        var layerSwitcher = new ol.control.LayerSwitcher({
            tipLabel: 'Layers', // Optional label for button
            enableOpacitySliders: true
        });
        map.addControl(layerSwitcher);