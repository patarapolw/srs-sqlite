String.prototype.hashCode = function() {
  var hash = 0, i, chr;
  if (this.length === 0) return hash;
  for (i = 0; i < this.length; i++) {
    chr   = this.charCodeAt(i);
    hash  = ((hash << 5) - hash) + chr;
    hash |= 0; // Convert to 32bit integer
  }
  return hash;
};

const markdownConverter = new showdown.Converter;
const img_regex = /(?:(?=^)|(?=\s).|^)([^\s<>"\']+\.(?:png|jpg|jpeg|gif))/gi;
const pdf_regex = /(\/pdf\/.+\.pdf)\/(\d+)/gi;

function markdown2html(text, card){
  const pdfUrl = pdf_regex.exec(text);
  if(pdfUrl !== null){
    text = text.replace(pdfUrl[0], "<canvas id='" + pdfUrl[0].hashCode() + "' class='imageViewer' />");
    pdfjsLib.getDocument(pdfUrl[1])
      .then(pdf=>pdf.getPage(parseInt(pdfUrl[2])))
      .then(page=>{
        let canvas = document.getElementById(pdfUrl[0].hashCode());
        let context = canvas.getContext('2d');
        const viewport = page.getViewport(1);
        const scale = canvas.width / viewport.width;
        let scaledViewport = page.getViewport(scale);

        page.render({canvasContext: context, viewport: scaledViewport});
      });
  }

  text = text.replace(/\n+/g, "\n\n");
  text = text.replace(img_regex, "<img src='$1' class='imageViewer' />");

  if(card.data){
    let itemData = JSON.parse(card.data);
    // console.log(itemData);
    text = sprintf(text, itemData);
  }

  return markdownConverter.makeHtml(text);
}
