const HIGH_DPI_SCALING = 2;

if(!show){
  document.getElementById('show-area').innerHTML = markdown2html(card.front, card, HIGH_DPI_SCALING);
} else {
  document.getElementById('show-area').innerHTML = markdown2html(card.back, card, HIGH_DPI_SCALING);
}
