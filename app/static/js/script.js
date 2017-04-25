
(function($, window) {
    // window changed
}).call(this, jQuery, window);


(function($){
  $(function(){
    log.setDefaultLevel('trace') // set log level to trace
    // components initialization
    $('.button-collapse').sideNav();
    $('.modal').modal();
    $('.population-settings').modal();
    $('select').material_select();


    // POPULATION example
    // Update plot with an API call
    function update_plot(target) {
        value = $('#select-'+target)[0].value
        //log.info("Update value " + target + " with "+value)
        url = "/api/v1/param/"+session_id+"/population/"+target+"/"+value
        $.ajax({
            type:"GET",
            url : url
        });
    }
    $('#select-year').change(function(){update_plot('year');});
    $('#select-location').change(function(){update_plot('location');});
    $('#select-year').value="2015"
    $('#select-location').value="World"
  }); // end of document ready
})(jQuery); // end of jQuery name space

jQuery(document).ready(function() {
  bokehAppLoaded();
});

function bokehAppLoaded () {
  if($('.bk-canvas-events').is(':visible')){ //if the container is visible on the page
   log.info("bokeh plot loaded") 
    //$("#bokeh-plot1").show()
    $("#mybk-loader").hide(2)
    //$("#bokeh-plot1").css('visibility', false)
    log.info($("#bokeh-plot1"))
  } else {
    log.trace("bokeh plot loading ...") 
    //$("#bokeh-plot1").hide(1)
    //$("#bokeh-plot1").css('visibility', false)
    setTimeout(bokehAppLoaded, 100); //wait 100 ms, then try again
  }
}
