$('.press').click(function ()
	{   
		
		var data = $(this).data('path');
		var ip = data['IP']
		var senddata = JSON.stringify(data)
		var id = $(this).attr('id');
		
 		if (id == 'False')
			{
				$.ajaxSetup({
					beforeSend: function(xhr, settings) {
						if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
							xhr.setRequestHeader("X-CSRFToken", csrf_token);
						}
					}
				});
				$.ajax({
				url: Flask.url_for('play_video'),
				data: senddata,
				dataType: 'json',
				contentType: "application/json",
				type: 'POST',
				success: function(response)
					{	
						console.log(response)
					},
				});	
			} 
		else
			{
				location.href = Flask.url_for('smb_search', {'ip':ip, 'path':data['PATH']+'/'+data['FILE']});
			}
	}
);
