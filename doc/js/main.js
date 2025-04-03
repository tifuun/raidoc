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

	toc_wrap = document.getElementById('toc-wrap');
	toc_wrap.addEventListener("click", (e) => {
		if (e.target == toc_wrap) {
			toc_wrap.classList.add('hide');
		}
	})

	toc_button = document.getElementById('toc-button');
	toc_button.addEventListener("click", (e) => {
		toc_wrap.classList.remove('hide');
	})
});

