function loadNetworks() {
	$('.loading').text('loading').addClass('alert alert-info').css("font-weight","Bold");
	//loading dots
	var originalText=$(".loading").text(),i=0;loadingdots=setInterval(function(){$(".loading").append(".");i++;if(i==4){$(".loading").html(originalText);i=0;}},500);
	$('#name_ip').html('')
	$.ajax({
		url: Flask.url_for('add_network'),
		contentType: "application/json",
		type: 'GET',
		success: function(response) 
			{
				var select = document.getElementById("name_ip");
				var networks = response
				
				for (var ip in networks)
				{
					network = networks[ip]
					json_networks = JSON.stringify({network, ip});
					select.options[select.options.length] = new Option(networks[ip], json_networks);
				}
				
				clearInterval(loadingdots)
				$('.loading').empty().removeClass("alert alert-info");
				$('.message').text('Done').addClass('alert alert-success alert-dismissible').css("font-weight","Bold");	
				setTimeout(function() 
				{
					$('.message').empty().removeClass("alert alert-succes")
				}, 5000);	
            }
	})	
}