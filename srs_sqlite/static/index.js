let hot;
let pageNumber = 1;
let data;

readSearchBarValue(document.getElementById('search-bar').value);

document.body.addEventListener('keydown', (e)=>{
  e = e || window.event;
  const key = e.which || e.keyCode;
  const keyF = 102;
  const keyf = 70;

  if((key === keyf || key === keyF) && (e.ctrlKey || e.metaKey)){
    e.preventDefault();
    document.getElementById('search-bar').focus();
  }
});

document.getElementById('search-bar').addEventListener('keyup', (e)=>{
  pageNumber = 1;
  readSearchBarValue(e.target.value);
});

document.getElementById('previous-all').onclick = ()=>{
  pageNumber = 1;
  readSearchBarValue(document.getElementById('search-bar').value);
}

document.getElementById('previous').onclick = ()=>{
  pageNumber--;
  readSearchBarValue(document.getElementById('search-bar').value);
}

document.getElementById('next-all').onclick = ()=>{
  pageNumber = -1;
  readSearchBarValue(document.getElementById('search-bar').value);
}

document.getElementById('next').onclick = ()=>{
  pageNumber++;
  readSearchBarValue(document.getElementById('search-bar').value);
}

document.getElementById('new-record').onclick = ()=>{
  insertEmptyRow();
};

window.addEventListener('resize', ()=>{
  const container = document.getElementById('handsontable-container');
  const dimension = getTrueWindowDimension();

  Object.assign(container.style, dimension);
  Object.assign(document.getElementsByClassName('wtHolder')[0].style, dimension);
});

function fetchAll(){
  fetch('/api/all/' + pageNumber).then((response)=>{
    response.json().then((response_json)=>{
      data = response_json.data;
      loadData();
      setPageNav(response_json.pages);
    });
  });
}

function readSearchBarValue(queryString){
  if(!queryString){
    fetchAll()
  } else {
    fetch('/api/search/' + pageNumber, {
      method: 'POST',
      headers: {
        "Content-Type": "application/json; charset=utf-8"
      },
      body: JSON.stringify({
        q: queryString
      })
    }).then((response)=>{
      response.json().then((response_json)=>{
        data = response_json.data;
        loadData();
        setPageNav(response_json.pages);
      });
    });
  }
}

function setPageNav(pages){
  pageNumber = pages.number;

  document.getElementById('page-label-current').innerHTML = pages.from + '-' + pages.to;
  document.getElementById('page-label-total').innerHTML = pages.total;

  if(pages.from > 1){
    document.getElementById('previous-all').disabled = false;
    document.getElementById('previous').disabled = false;
  } else {
    document.getElementById('previous-all').disabled = true;
    document.getElementById('previous').disabled = true;
  }

  if(pages.to < pages.total){
    document.getElementById('next-all').disabled = false;
    document.getElementById('next').disabled = false;
  } else {
    document.getElementById('next-all').disabled = true;
    document.getElementById('next').disabled = true;
  }
}

function getTrueWindowDimension(){
  return {
    height: (window.innerHeight
      - document.getElementById('nav-area').offsetHeight
      - 10) + 'px',
    width: window.innerWidth + 'px'
  };
}

function loadData() {
  if(hot) hot.destroy();

  const container = document.getElementById('handsontable-container');
  const dimension = getTrueWindowDimension();

  Object.assign(container.style, dimension);

  let actualConfig = {
    columns: [],
    data: data,
    afterChange: (changes, source)=>{
      sendChanges(changes, source);
    },
    beforeRemoveRow: (index, amount, physicalRows)=>{
      if(data[index].id){
        if(confirm('Are you sure you want to remove ' + data[index].id + ': ' + data[index].front + '?')){
          fetch('/api/delete/' + data[index].id, {
            method: 'DELETE'
          }).then(response=>{
            if(response.status === 303){
              response.json().then(response_json=>{
                alert('Removed ' + response_json.id +': ' + response_json.front);
              });
            } else {
              alert('Not removed from database (refresh to reload).');
            }
          }).catch(error => console.error(`Fetch Error =\n`, error));
        } else {
          return false;
        }
      }
    }
  };

  Object.keys(defaultConfig).forEach((key)=>{
    if(config[key] === undefined){
      config[key] = defaultConfig[key];
    }
  })
  Object.assign(actualConfig, config);

  if(actualConfig.columns.length === 0){
    const renderers = actualConfig.renderers;

    if(typeof renderers === 'string'){
      config.colHeaders.forEach((item, index)=>{
        actualConfig.columns.push({
          data: item,
          renderer: renderers
        });
      });
    } else if(renderers !== null && typeof renderers === 'object') {
      config.colHeaders.forEach((item, index)=>{
        actualConfig.columns.push({
          data: item,
          renderer: renderers[item]
        });
      });
    } else {
      config.colHeaders.forEach((item, index)=>{
        actualConfig.columns.push({
          data: key
        });
      });
    }
  }

  hot = new Handsontable(document.getElementById('handsontable-area'), actualConfig);

  if(config.maxColWidth && !config.colWidths){
    let colWidths = [];
    [...Array(hot.countCols()).keys()].map(i => {
      const thisColWidth = hot.getColWidth(i);
      if(thisColWidth > config.maxColWidth){
        colWidths.push(config.maxColWidth);
      } else {
        if(config.minColWidths !== undefined){
          if(thisColWidth > (config.minColWidths[i] || 0)){
            colWidths.push(thisColWidth);
          } else {
            colWidths.push(config.minColWidths[i])
          }
        }
      }
    });

    hot.updateSettings({
      colWidths: colWidths
    });

    actualConfig.colWidths = config.colWidths = colWidths;
  }
}

function sendChanges(changes, source){
  if(source === 'edit' && changes[0][2] !== changes[0][3]){
    const rowEdited = changes[0][0];
    const fieldEdited = changes[0][1];
    const newData = changes[0][3];
    const recordId = data[rowEdited].id;

    const payload = {
      id: recordId,
      fieldName: fieldEdited,
      data: newData
    };

    fetch('/api/edit', {
      method: 'POST',
      headers: {
        "Content-Type": "application/json; charset=utf-8"
      },
      body: JSON.stringify(payload)
    }).then(response=>{
      if(response.status === 201){
        response.json().then(response_json=>{
          data[rowEdited].id = response_json.id;
        });
      } else {
        alert('Not added. (Have you edited the "front"?)');
      }
    }).catch(error => console.error(`Fetch Error =\n`, error));
  }
}

function insertEmptyRow(){
  // data.splice(0, 0, {});  The data is already inserted.
  hot.alter('insert_row', 0);
}
