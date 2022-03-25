// Chart.js scripts

let dataLine = JSON.parse(document.getElementById('mylistjson').textContent);



var defaultDataLine=[];


for (let i = 0; i < 13; i++){
  defaultDataLine.push(dataLine[i]);
}



// const myArray = dataa.split(",");
// var res = [];
// for (let i = 0; i < myArray.length; i++){
//   let str = myArray[i].replace(/\s/g, '');
//   if(i==0){
//     str = str.substring(1);
//   }else if(i==(myArray.length-1)){
//      str=str.slice(0, -1);
//   }
//   str=parseInt(str);
//   res.push(str);
 
// }
// console.log(typeof res)

              
// for(var i in dataa)
//     console.log(dataa[i]);
//     //res.push(dataa[i]);


let months=["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", 
	"Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

let dates=[];

    var today = new Date();
 

for (let i = 0; i < 12; i++) {
    var date = new Date();
    var first = new Date(date.getTime() - ((12-i) * 24 * 60 * 60 * 1000));
    var month=months[first.getMonth()];
    var dat=first.getDate();
    var newDate=dat+" "+month;
    dates.push(newDate);
}
var month=months[today.getMonth()];
var dat=today.getDate();
var newDate=dat+" "+month;
dates.push(newDate);


// -- Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';
// -- Area Chart Example
var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: dates,
    datasets: [{
      label: "Tarihli Satım",
      lineTension: 0.3,
      backgroundColor: "rgba(2,117,216,0.2)",
      borderColor: "rgba(2,117,216,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(2,117,216,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(2,117,216,1)",
      pointHitRadius: 20,
      pointBorderWidth: 2,
      data: defaultDataLine,
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false
        },
       
      }],
      yAxes: [{
       
        gridLines: {
          color: "rgba(0, 0, 0, .125)",
        }
      }],
    },
    legend: {
      display: false
    }
  }
});






