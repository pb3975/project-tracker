$('#delete').on('click', function() {
	if (confirm("Are you sure you want to delete this project?")) {
		$.ajax({ url: '/admin/t/<%= project.slug %>', method: 'DELETE', }).done
	}
});