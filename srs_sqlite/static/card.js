if(!show){
  document.getElementById('show-area').innerHTML = markdown2html(card.front, card);
} else {
  document.getElementById('show-area').innerHTML = markdown2html(card.back, card);
}
