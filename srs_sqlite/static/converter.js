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

function markdown2html(text, card, scaling){
  scaling = scaling || 0.5;

  const pdfUrl = pdf_regex.exec(text);
  if(pdfUrl !== null){
    text = text.replace(pdfUrl[0], "<div class='imageViewer'><canvas id='" + pdfUrl[0].hashCode() + "' /></div>");
    pdfjsLib.getDocument(pdfUrl[1])
      .then(pdf=>pdf.getPage(parseInt(pdfUrl[2])))
      .then(page=>{
        let canvas = document.getElementById(pdfUrl[0].hashCode());
        let context = canvas.getContext('2d');
        const viewport = page.getViewport(scaling);
        canvas.width = viewport.width;
        canvas.height = viewport.height;
        canvas.style.width = "100%";
        canvas.style.height = "100%";
        // wrapper.style.width = Math.floor(viewport.width/scale) + 'pt';
        // wrapper.style.height = Math.floor(viewport.height/scale) + 'pt';

        page.render({canvasContext: context, viewport: viewport});
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
