// Chart.js scripts



// -- Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';
// -- Area Chart Example





let dataa = JSON.parse(document.getElementById('mylistjson2').textContent);
var defaultData=[];
var defaultData1=[];
// console.log(dataa);
// console.log(typeof dataa);

for (let i = 0; i < 2; i++){
    defaultData.push(dataa[i]);
}
for (let i = 2; i < 4; i++){
    defaultData1.push(dataa[i]);
}






// -- Bar Chart Example
var ctx = document.getElementById("myPieChart1");
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ["Gelir", "Gider"],
    datasets: [{
      data: defaultData,
      backgroundColor: ['#28a745', '#dc3545'],
    }],
  },
});

// -- Pie Chart Example
var ctx = document.getElementById("myPieChart2");
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ["Gelir", "Gider"],
    datasets: [{
      data: defaultData1,
      backgroundColor: ['#28a745', '#dc3545'],
    }],
  },
});
