// var tasteInput = document.getElementById('review_taste').innerText
// console.log(tasteInput)
// var beerData = fetch(`http://127.0.0.1:5000/API/${userInput}`).then(response => response.json())

// from data.js
const tableData = data;
//console.log(tableData)

// get table references
var tbody = d3.select("tbody");

function buildTable(data) {
  // First, clear out any existing data
  tbody.html("");

  // Next, loop through each object in the data
  // and append a row and cells for each value in the row
  data.forEach((dataRow) => {
    // Append a row to the table body
    let row = tbody.append("tr");
    // console.log(dataRow)

    // Loop through each field in the dataRow and add
    // each value as a table cell (td)
    Object.values(dataRow).forEach((val) => {
      let cell = row.append("td");
      cell.text(val);
    });
  });
}

// 1. Create a variable to keep track of all the filters as an object.
var filters = {};

// 3. Use this function to update the filters. 
function updateFilters() {

  
  // 4a. Save the element that was changed as a variable.
  let changedElement = d3.select(this);

  // 4b. Save the value that was changed as a variable.
  let elementValue = changedElement.property("value");
  //console.log(elementValue);
  
  
  tasteData = fetch(`http://127.0.0.1:5000/API/${elementValue}`)
  .then(response => response.json())
  .then(response => console.log(response))
  console.log(tasteData)



  // var beerData = fetch(`http://127.0.0.1:5000/API/name/${elementValue}`)
  //   .then(response => response.json())
  //   .then(response => console.log(response))
  // // console.log(beerData)

  // let tasteInput = document.getElementById('review_taste').innerText
  // console.log(tasteInput)

  // var url = `http://127.0.0.1:5000/API/${elementValue}`
  // const beerTaste = fetch(url)
  // .then((response) => response.json())
  // .then((taste) => {
  //   return taste;
  // });

  // console.log(beerTaste); 

  // var tastePromise = returnFetch(url)
  // console.log(tastePromise)

  // 4c. Save the id of the filter that was changed as a variable.
  let filterId = changedElement.attr("id");
  //console.log(filterId)


  // 5. If a filter value was entered then add that filterId and value
  // to the filters list. Otherwise, clear that filter from the filters object.
  if (elementValue) {
    filters[filterId] = elementValue;
  } else {
    delete filters[filterId];
  }


  // 6. Call function to apply all filters and rebuild the table
  filterTable();

}

// 7. Use this function to filter the table when data is entered.
function filterTable() {

  // 8. Set the filtered data to the tableData.
  let filtered_data = tableData;

  // 9. Loop through all of the filters and keep any data that
  // matches the filter values
  Object.entries(filters).forEach(([key, value]) => {
    filtered_data = filtered_data.filter(row => row[key] == value);
  });

  // 10. Finally, rebuild the table using the filtered data
  buildTable(filtered_data);
}

// 2. Attach an event to listen for changes to each filter
d3.selectAll("input").on("change", updateFilters)

// Build the table when the page loads
buildTable(tableData);

