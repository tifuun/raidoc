function main() {
	var elements = document.getElementsByClassName('asciinema-figure');
	for (var i = 0; i < elements.length; ++i) {
		var elem = elements[i];  
		var cast_uri = elem.firstElementChild.href;
		var caption = elem.firstElementChild.innerHTML;
		elem.innerHTML='<div class="asciinema-player"></div><i class="asciinema-caption"></i>';
		AsciinemaPlayer.create(
			cast_uri,
			elem.children[0],
			{
				preload: true,
				poster: 'npt:99',
				fit: "none"
			}
		);
		elem.children[1].innerHTML = caption;
	}
}

document.addEventListener('DOMContentLoaded', function() {
  main();
});

