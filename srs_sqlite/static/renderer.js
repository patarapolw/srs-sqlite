(function(Handsontable){
  function customRenderer(hotInstance, td, row, column, prop, value, cellProperties) {
    let text = Handsontable.helper.stringify(value);
    td.innerHTML = markdown2html(text, data[row]);

    return td;
  }

  // Register an alias
  Handsontable.renderers.registerRenderer('markdownRenderer', customRenderer);

})(Handsontable);
