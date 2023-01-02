function goBack() {
  window.history.back();
}

function contentOrCampaigns() {
  var content_conteiner = document.getElementById("contentContainer");
  var campaign_conteiner = document.getElementById("campaignsContainer");
  if (campaign_conteiner.style.display === "none") {
    campaign_conteiner.style.display = "block";
    content_conteiner.style.display = "none";    
  } else {
    campaign_conteiner.style.display = "none";
    content_conteiner.style.display = "block"; 
  }; 
}



function add() {
  var box_form = document.getElementById("formAdd");
  if (box_form.style.display === "block") {
      box_form.style.display = "none";
  } else {
      box_form.style.display = "block";
  }; 
}

function edit() {
  var box_form = document.getElementById("formEdit");
  if (box_form.style.display === "block") {
      box_form.style.display = "none";
  } else {
      box_form.style.display = "block";
  }; 
}

function secret() {
  var box_form = document.getElementById("secret");
  if (box_form.style.display === "block") {
      box_form.style.display = "none";
  } else {
      box_form.style.display = "block";
  }; 
}

function filterTwitch() {
  var items, item
  items = document.querySelectorAll(".Twitch")
  items.forEach(function (item) {
      if (item.classList.contains("none")) {
          item.classList.remove("none");
      } else {
          item.classList.add("none");
      }
  });
} 

function filterYoutube() {
  var items, item
  items = document.querySelectorAll(".Youtube")
  items.forEach(function (item) {
      if (item.classList.contains("none")) {
          item.classList.remove("none");
      } else {
          item.classList.add("none");
      }
  });
} 

function filterInstagram() {
  var items, item
  items = document.querySelectorAll(".Instagram")
  items.forEach(function (item) {
      if (item.classList.contains("none")) {
          item.classList.remove("none");
      } else {
          item.classList.add("none");
      }
  });
} 
function myFunction() {
    var input, filter, table, tr, td, i, alltables;
    alltables = document.querySelectorAll("table[data-name=product-table]");
    input = document.getElementById("searchBar");
    filter = input.value.toUpperCase();
    alltables.forEach(function (table) {
        tr = table.getElementsByTagName("tr");
        for (i = 0; i < tr.length; i++) {
            td = tr[i].getElementsByTagName("td")[1];
            if (td) {
                if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                    
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    });
}

function changeView() {
    var items, item
    items = document.querySelectorAll(".tbc")
    items.forEach(function (item) {
        if (item.classList.contains("iteml")) {
            item.classList.remove("iteml");
            var header = document.getElementById('tableHeader');
            header.classList.remove("hideTableHeader");
        } else {
            item.classList.add("iteml");
            var header = document.getElementById('tableHeader');
            header.classList.add("hideTableHeader")
        }
    });
} 


var changHeaderColor = function () {
    if (window.pageYOffset == 0) {
      var el = document.getElementById('header');
      if (el.style.backgroundColor == 'transparent' || el.style.backgroundColor == null) {
        el.style.backgroundColor='#03022C';
      } else {
        el.style.backgroundColor='transparent';
      }
    }
  };
  
  
  window.onscroll = function() {
    scrollWin()
  };
  
  function scrollWin() {
    var el = document.getElementById('header');
    if (window.pageYOffset > 10){   
      el.style.backgroundColor='#03022C';
    } else {   
      el.style.backgroundColor='transparent';
    }
  };
  
  
  window.onload = function() {
    document.getElementById('header').style.backgroundColor = 'transparent';
    var toggle = document.getElementById("nav-menu-button");
    toggle.addEventListener("click", changHeaderColor, false);
    scrollWin()
  }


function downloadCSV(csv, filename) {
    var csvFile;
    var downloadLink;

    // CSV file
    csvFile = new Blob([csv], {type: "text/csv"});

    // Download link
    downloadLink = document.createElement("a");

    // File name
    downloadLink.download = filename;

    // Create a link to the file
    downloadLink.href = window.URL.createObjectURL(csvFile);

    // Hide download link
    downloadLink.style.display = "none";

    // Add the link to DOM
    document.body.appendChild(downloadLink);

    // Click download link
    downloadLink.click();
}

function exportTableToCSV(filename) {
    var csv = [];
    var rows = document.querySelectorAll("table tr");
    
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll("td, th");
        
        for (var j = 0; j < cols.length; j++) 
            row.push(cols[j].innerText);
        
        csv.push(row.join(","));        
    }

    // Download CSV file
    downloadCSV(csv.join("\n"), filename);
}
