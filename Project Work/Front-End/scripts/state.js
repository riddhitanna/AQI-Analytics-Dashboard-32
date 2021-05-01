/*
Plot 1
*/
var trace1 = {
    type: 'bar',
    x: [1, 2, 3, 4],
    y: [5, 10, 2, 8],
    marker: {
        color: '#C8A2C8',
        line: {
            width: 2.5
        }
    }
  };

  var data = [ trace1 ];
  
  var layout = { 
    title: 'PM2.5',
    font: {size: 18}
  };
  
  var config = {responsive: true}
  
  Plotly.newPlot('bargraph', data, layout, config );

/*
Plot 2
*/
  var trace2 = {
    type: 'bar',
    x: [1, 2, 3, 4],
    y: [2, 5, 2, 8],
    marker: {
        color: '#C8A2C8',
        line: {
            width: 2.5
        }
    }
  };
  var data = [ trace2 ];
  
  var layout = { 
    title: 'PM10',
    font: {size: 18}
  };
  
  var config = {responsive: true}
  Plotly.newPlot('bargraph-2', data, layout, config );

/*
Plot 3
*/
  var trace3 = {
    type: 'bar',
    x: [1, 2, 3, 4],
    y: [15, 2, 2, 8],
    marker: {
        color: '#C8A2C8',
        line: {
            width: 2.5
        }
    }
  };
  var data = [ trace3 ];
  
  var layout = { 
    title: 'Humidity',
    font: {size: 18},
    
  };
  
  var config = {responsive: true}
  Plotly.newPlot('bargraph-3', data, layout, config );
/*
Plot 4
*/
  var trace4 = {
    type: 'bar',
    x: [1, 2, 3, 4],
    y: [5, 10, 12, 18],
    marker: {
        color: '#C8A2C8',
        line: {
            width: 2.5
        }
    }
  };
  var data = [ trace4 ];
  
  var layout = { 
    title: 'Temperature',
    font: {size: 18}
  };
  
  var config = {responsive: true}
  Plotly.newPlot('bargraph-4', data, layout, config );



  state_list = [
	"Andaman and Nicobar Islands",
	"Andhra Pradesh",
	"Arunachal Pradesh",
	"Assam",
	"Bihar",
	"Chandigarh",
	"Chhattisgarh",
	"Dadra and Nagar Haveli",
	"Daman and Diu",
	"Delhi",
	"Goa",
	"Gujarat",
	"Haryana",
	"Himachal Pradesh",
	"Jammu and Kashmir",
	"Jharkhand",
	"Karnataka",
	"Kerala",
	"Lakshadweep",
	"Madhya Pradesh",
	"Maharashtra",
	"Manipur",
	"Meghalaya",
	"Mizoram",
	"Nagaland",
	"Orissa",
	"Pondicherry",
	"Punjab",
	"Rajasthan",
	"Sikkim",
	"Tamil Nadu",
	"Telangana",
	"Tripura",
	"Uttaranchal",
	"Uttar Pradesh",
	"West Bengal"
  ]
  var x = document.getElementById("states");
  for(var i = 0; i < state_list.length; i++){
    
    var option = document.createElement("option");
    option.text = state_list[i];
    x.add(option);
  }