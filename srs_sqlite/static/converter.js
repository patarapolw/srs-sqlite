const markdownConverter = new showdown.Converter;
const img_regex = /(?:(?=^)|(?=\s).|^)([^\s<>"\']+\.(?:png|jpg|jpeg|gif))/gi;

function markdown2html(text, card){
  text = text.replace(/\n+/g, "\n\n");
  text = text.replace(img_regex, "<img src='$1' class='imageViewer' />");

  if(card.data){
    let itemData = JSON.parse(card.data);
    // console.log(itemData);
    text = sprintf(text, itemData);
  }

  return markdownConverter.makeHtml(text);
}

function imageUrl2html(text){
  return text.replace(img_regex, "<img src='$1' width=200 />");
}
