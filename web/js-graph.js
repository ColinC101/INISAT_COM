var nbr = 40;
  // GRAPHE GRAPHE GRAPHE GRAPHE GRAPHE GRAPHE GRAPHE GRAPHE GRAPHE GRAPHE GRAPHE GRAPHE GRAPHE GRAPHE GRAPHE GRAPHE GRAPHE GRAPHE GRAPHE GRAPHE 
  
  if (!!window.EventSource) {
    var source = new EventSource('/events2');
    
    source.addEventListener('open', function(e) {
      //console.log(dateHeure());
      console.log("Debut de la reception des donnees satellite ...");
    }, false);
  
    source.addEventListener('error', function(e) {
      if (e.target.readyState != EventSource.OPEN) {
        //console.log(dateHeure());
        console.log("Reception des donnees satellite interrompue ...");
      }
  }, false);
  
  
  source.addEventListener('CAP_readings2', function(e) {
  
var obj2 = JSON.parse(e.data);
  
    plotChart1(obj2, A1, B1);
    plotChart2(obj2, A2, B2);
    plotChart3(obj2, A3, B3);
    plotChart4(obj2, A4, B4);
    plotChart5(obj2, A5, B5);
    plotChart6(obj2, A6, B6);
    
  }, false);
  }
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
var graph_config1 ='0';
var graph_config2 ='0';
var graph_config3 ='0';
var graph_config4 ='0';
var graph_config5 ='0';
var graph_config6 ='0';
var C1,C2,C3,C4,C5,C6;


var A1, B1, choix_ch1; 
var Chart1, id1='chart1' ;

function validatChart1() {
  choix_ch1 = document.forms["myChart1"]["modu1"].value;
  C1 =1;
    console.log("Le module choisi est :", choix_ch1);

    if (choix_ch1=="0") {graph_config1 ='0';}
    if (choix_ch1=="1") {functionCH1B('Roulis','Tangage','Lacet','Vecteur Euler (°)'); A1 =11; B1=13; graph_config1= 'a';}
    if (choix_ch1=="2") {functionCH1C('W','X','Y','Z','Quaternion');A1 =14; B1=17;graph_config1= 'b';}
    if (choix_ch1=="3") {functionCH1B('X','Y','Z','Vitesse Angulaire (red/s)');A1 =18; B1=20;graph_config1= 'c';}
    if (choix_ch1=="4") {functionCH1B('X','Y','Z','Accelération (m/s²)');A1 =21; B1=23;graph_config1= 'd';}
    if (choix_ch1=="5") {functionCH1B('X','Y','Z','Champs Magnétique (uT)');A1 =24; B1=26;graph_config1= 'e';}
    if (choix_ch1=="6") {functionCH1B('X','Y','Z','Accelération Linéaire (m/s²)');A1 =27; B1=29;graph_config1= 'f';}
    if (choix_ch1=="7") {functionCH1B('X','Y','Z','Vecteur Gravité (m/s²)');A1 =30; B1=32;graph_config1= 'g'}
    if (choix_ch1=="8") {functionCH1A('Température','Température (°c)');A1 =8; B1=8;graph_config1= 'h';}
    if (choix_ch1=="9") {functionCH1A('Pression','Pression (Pa)');A1 =10; B1=10;graph_config1= 'j';}
    if (choix_ch1=="10") {functionCH1A('Altitude','Altitude (m)');A1 =9; B1=9;graph_config1= 'i';}
    if (choix_ch1=="11") {functionCH1A('Vbat','Vbat (V)');A1 =1; B1=1;graph_config1= 'k';}
    if (choix_ch1=="14") {functionCH1A('Icharge','Icharge (A)');A1 =4; B1=4;graph_config1= 'k';}
    if (choix_ch1=="12") {functionCH1A('Tbat','Tbat (°c)');A1 =6; B1=6;graph_config1= 'k';}
    if (choix_ch1=="13") {functionCH1D('+X','-X','+Y','-Y','Z','Luminance');A1 =33; B1=37;graph_config1= 'l';}
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/configGraph1?choix="+graph_config1, true);
    xhr.send();
  
}

// Create Charts



  Chart1 = new Highcharts.Chart({
    chart:{renderTo: id1},
  
    title: {
      text: undefined
    },

    credits: {
    enabled: false
    }
    });
  

  function functionCH1A(x,y) {

    Chart1 = new Highcharts.Chart({
      chart:{renderTo: id1},
      type: 'line',
      series: [
        {
          name: x,
          color: '#101D42',
          //showInLegend: false,
          marker: false,
        },
      
      ],
      
      plotOptions : {
        line: { animation: false,
        dataLabels: { enabled: false }
        },
        
      },
      title: {
        text: undefined
      },
      xAxis: {
        title: {
          text: 'Temps'
        },
        type: 'datetime',
        dateTimeLabelFormats: { second: '%H:%M:%S' }
        
      },
      yAxis: {
        title: {
          text: y
        }
      },
      credits: {
      enabled: false
      }
      });
      Highcharts.setOptions({
      time: {
        timezoneOffset: -60 // time zone offset here in minutes
      }
      });
    
    }
function functionCH1B(x,y,z,w) {

Chart1 = new Highcharts.Chart({
  chart:{renderTo: id1},
  type: 'line',
  series: [
    {
      name: x,
      color: '#101D42',
      //showInLegend: false,
      marker: false,
    },
      
     
    
    {
      name: y,
      color: '#00A6A6',
      marker: false,
   
    },
    {
      name: z,
      color: '#da2c2c',
      marker: false,
    },
  
  
  ],
  
  plotOptions : {
    line: { animation: false,
    dataLabels: { enabled: false }
    },
    
  },
  title: {
    text: undefined
  },
  xAxis: {
    title: {
      text: 'Temps'
    },
    type: 'datetime',
    dateTimeLabelFormats: { second: '%H:%M:%S' }
  },
  yAxis: {
    title: {
      text: w
    }
  },
  credits: {
  enabled: false
  }
  });
  Highcharts.setOptions({
  time: {
    timezoneOffset: -60 // time zone offset here in minutes
  }
  });

}

function functionCH1C(k,x,y,z,w) {

Chart1 = new Highcharts.Chart({
    chart:{renderTo: id1},
    type: 'line',
    series: [
      {
        name: k,
        color: '#101D42',
        //showInLegend: false,
        marker: false,
      },
        
       
      
      {
        name: x,
        color: '#00A6A6',
        marker: false,
     
      },
      {
        name: y,
        color: '#da2c2c',
        marker: false,
      },
    
      {
        
        name: z,
        color: '#dd90d7',
        marker: false,
       
      },
    
    ],
    
    plotOptions : {
      line: { animation: false,
      dataLabels: { enabled: false }
      },
      
    },
    title: {
      text: undefined
    },
    xAxis: {
      title: {
        text: 'Temps'
      },
      type: 'datetime',
      dateTimeLabelFormats: { second: '%H:%M:%S' }
    },
    yAxis: {
      title: {
        text: w
      }
    },
    credits: {
    enabled: false
    }
    });
    Highcharts.setOptions({
    time: {
      timezoneOffset: -60 // time zone offset here in minutes
    }
    });
  
  }

  function functionCH1D(k,x,y,z,j,w) {

    Chart1 = new Highcharts.Chart({
        chart:{renderTo: id1},
        type: 'line',
        series: [
          {
            name: k,
            color: '#101D42',
            //showInLegend: false,
            marker: false,
          },
            
           
          
          {
            name: x,
            color: '#00A6A6',
            marker: false,
         
          },
          {
            name: y,
            color: '#da2c2c',
            marker: false,
          },
        
          {
            
            name: z,
            color: '#dd90d7',
            marker: false,
           
          },
          {
            
            name: j,
            color: '#da8c3c',
            marker: false,
           
          },
        
        ],
        
        plotOptions : {
          line: { animation: false,
          dataLabels: { enabled: false }
          },
          
        },
        title: {
          text: undefined
        },
        xAxis: {
          title: {
            text: 'Temps'
          },
          type: 'datetime',
          dateTimeLabelFormats: { second: '%H:%M:%S' }
        },
        yAxis: {
          title: {
            text: w
          }
        },
        credits: {
        enabled: false
        }
        });
        Highcharts.setOptions({
        time: {
          timezoneOffset: -60 // time zone offset here in minutes
        }
        });
      
      }
    

  //****************************************************************************************************************************************************************************
  function plotChart1(jsonValue, A, B) {
  
    if (C1!==1){
    var keys = Object.keys(jsonValue);
    // console.log(keys);
    //console.log(keys.length);
    var j =0;
    for (var i = A-1; i <B; i++){
      var x = (new Date()).getTime();
      //console.log(x);
      const key = keys[i];
      var y = Number(jsonValue[key]);
     // console.log(y);
    
     
    if(Chart1.series[j].data.length > nbr) {
        Chart1.series[j].addPoint([x, y], true, true, true);
      } else {
        Chart1.series[j].addPoint([x, y], true, false, true);
      }
    
    j = j+1
    }
    }
    C1+=1;
    }
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
var A2, B2, choix_ch2; 
var Chart2, id2='chart2' ;

function validatChart2() {
  choix_ch2 = document.forms["myChart2"]["modu2"].value;
  C2 =1;
    console.log("Le module choisi est :", choix_ch2);
    if (choix_ch2=="0") {graph_config2='0';}
    if (choix_ch2=="1") {functionCH2B('Roulis','Tangage','Lacet','Vecteur Euler (°)'); A2 =11; B2=13;graph_config2='a';}
    if (choix_ch2=="2") {functionCH2C('W','X','Y','Z','Quaternion');A2 =14; B2=17;graph_config2='b';}
    if (choix_ch2=="3") {functionCH2B('X','Y','Z','Vitesse Angulaire (rad/s)');A2 =18; B2=20;graph_config2='c';}
    if (choix_ch2=="4") {functionCH2B('X','Y','Z','Accelération (m/s²)');A2 =21; B2=23;graph_config2='d';}
    if (choix_ch2=="5") {functionCH2B('X','Y','Z','Champs Magnétique (uT)');A2 =24; B2=26;graph_config2='e';}
    if (choix_ch2=="6") {functionCH2B('X','Y','Z','Accelération Linéaire (m/s²)');A2 =27; B2=29;graph_config2='f';}
    if (choix_ch2=="7") {functionCH2B('X','Y','Z','Vecteur Gravité (m/s²)');A2 =30; B2=32;graph_config2='g';}
    if (choix_ch2=="8") {functionCH2A('Température','Température (°c)');A2 =8; B2=8;graph_config2='h';}
    if (choix_ch2=="9") {functionCH2A('Pression','Pression (Pa)');A2 =10; B2=10;graph_config2='j';}
    if (choix_ch2=="10") {functionCH2A('Altitude','Altitude (m)');A2 =9; B2=9;graph_config2='i';}
    if (choix_ch2=="11") {functionCH2A('Vbat','Vbat (V)');A2 =1; B2=1;graph_config2= 'k';}
    if (choix_ch2=="14") {functionCH2A('Icharge','Icharge (A)');A2 =4; B2=4;graph_config2= 'k';}
    if (choix_ch2=="12") {functionCH2A('Tbat','Tbat (°c)');A2 =6; B2=6;graph_config2= 'k';}
    if (choix_ch2=="13") {functionCH2D('+X','-X','+Y','-Y','Z','Luminance');A2 =33; B2=37;graph_config2= 'l';}
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/configGraph2?choix="+graph_config2, true);
    xhr.send();
}

// Create Charts



  Chart2 = new Highcharts.Chart({
    chart:{renderTo: id2},
  
    title: {
      text: undefined
    },

    credits: {
    enabled: false
    }
    });
  

  function functionCH2A(x,y) {

    Chart2 = new Highcharts.Chart({
      chart:{renderTo: id2},
      type: 'line',
      series: [
        {
          name: x,
          color: '#101D42',
          //showInLegend: false,
          marker: false,
        },
      
      ],
      
      plotOptions : {
        line: { animation: false,
        dataLabels: { enabled: false }
        },
        
      },
      title: {
        text: undefined
      },
      xAxis: {
        title: {
          text: 'Temps'
        },
        type: 'datetime',
        dateTimeLabelFormats: { second: '%H:%M:%S' }
      },
      yAxis: {
        title: {
          text: y
        }
      },
      credits: {
      enabled: false
      }
      });
      Highcharts.setOptions({
      time: {
        timezoneOffset: -60 // time zone offset here in minutes
      }
      });
    
    }
function functionCH2B(x,y,z,w) {

Chart2 = new Highcharts.Chart({
  chart:{renderTo: id2},
  type: 'line',
  series: [
    {
      name: x,
      color: '#101D42',
      //showInLegend: false,
      marker: false,
    },
      
     
    
    {
      name: y,
      color: '#00A6A6',
      marker: false,
   
    },
    {
      name: z,
      color: '#da2c2c',
      marker: false,
    },
  
  
  ],
  
  plotOptions : {
    line: { animation: false,
    dataLabels: { enabled: false }
    },
    
  },
  title: {
    text: undefined
  },
  xAxis: {
    title: {
      text: 'Temps'
    },
    type: 'datetime',
    dateTimeLabelFormats: { second: '%H:%M:%S' }
  },
  yAxis: {
    title: {
      text: w
    }
  },
  credits: {
  enabled: false
  }
  });
  Highcharts.setOptions({
  time: {
    timezoneOffset: -60 // time zone offset here in minutes
  }
  });

}

function functionCH2C(k,x,y,z,w) {

Chart2 = new Highcharts.Chart({
    chart:{renderTo: id2},
    type: 'line',
    series: [
      {
        name: k,
        color: '#101D42',
        //showInLegend: false,
        marker: false,
      },
        
       
      
      {
        name: x,
        color: '#00A6A6',
        marker: false,
     
      },
      {
        name: y,
        color: '#da2c2c',
        marker: false,
      },
    
      {
        
        name: z,
        color: '#dd90d7',
        marker: false,
       
      },
    
    ],
    
    plotOptions : {
      line: { animation: false,
      dataLabels: { enabled: false }
      },
      
    },
    title: {
      text: undefined
    },
    xAxis: {
      title: {
        text: 'Temps'
      },
      type: 'datetime',
      dateTimeLabelFormats: { second: '%H:%M:%S' }
    },
    yAxis: {
      title: {
        text: w
      }
    },
    credits: {
    enabled: false
    }
    });
    Highcharts.setOptions({
    time: {
      timezoneOffset: -60 // time zone offset here in minutes
    }
    });
  
  }

  function functionCH2D(k,x,y,z,j,w) {

    Chart2 = new Highcharts.Chart({
        chart:{renderTo: id2},
        type: 'line',
        series: [
          {
            name: k,
            color: '#101D42',
            //showInLegend: false,
            marker: false,
          },
            
           
          
          {
            name: x,
            color: '#00A6A6',
            marker: false,
         
          },
          {
            name: y,
            color: '#da2c2c',
            marker: false,
          },
        
          {
            
            name: z,
            color: '#dd90d7',
            marker: false,
           
          },
          {
            
            name: j,
            color: '#da8c3c',
            marker: false,
           
          },
        
        ],
        
        plotOptions : {
          line: { animation: false,
          dataLabels: { enabled: false }
          },
          
        },
        title: {
          text: undefined
        },
        xAxis: {
          title: {
            text: 'Temps'
          },
          type: 'datetime',
          dateTimeLabelFormats: { second: '%H:%M:%S' }
        },
        yAxis: {
          title: {
            text: w
          }
        },
        credits: {
        enabled: false
        }
        });
        Highcharts.setOptions({
        time: {
          timezoneOffset: -60 // time zone offset here in minutes
        }
        });
      
      }
  //****************************************************************************************************************************************************************************
  function plotChart2(jsonValue, A, B) {
    if (C2!==1){
    var keys = Object.keys(jsonValue);
    // console.log(keys);
    //console.log(keys.length);
    var j =0;
    for (var i = A-1; i <B; i++){
      var x = (new Date()).getTime();
      //console.log(x);
      const key = keys[i];
      var y = Number(jsonValue[key]);
     // console.log(y);
    
      if(Chart2.series[j].data.length > nbr) {
        Chart2.series[j].addPoint([x, y], true, true, true);
      } else {
        Chart2.series[j].addPoint([x, y], true, false, true);
      }
    j = j+1
    }
    }
    C2+=1;
    }
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
var A3, B3, choix_ch3; 
var Chart3, id3='chart3' ;

function validatChart3() {
  choix_ch3 = document.forms["myChart3"]["modu3"].value;
  C3 =1;
    console.log("Le module choisi est :", choix_ch3);
    if (choix_ch3=="0") {graph_config3='0';}
    if (choix_ch3=="1") {functionCH3B('Roulis','Tangage','Lacet','Vecteur Euler (°)'); A3 =11; B3=13;graph_config3='a';}
    if (choix_ch3=="2") {functionCH3C('W','X','Y','Z','Quaternion');A3 =14; B3=17;graph_config3='b';}
    if (choix_ch3=="3") {functionCH3B('X','Y','Z','Vitesse Angulaire (rad/s)');A3 =18; B3=20;graph_config3='c';}
    if (choix_ch3=="4") {functionCH3B('X','Y','Z','Accelération (m/s²)');A3 =21; B3=23;graph_config3='d';}
    if (choix_ch3=="5") {functionCH3B('X','Y','Z','Champs Magnétique (uT)');A3 =24; B3=26;graph_config3='e'}
    if (choix_ch3=="6") {functionCH3B('X','Y','Z','Accelération Linéaire (m/s²)');A3 =27; B3=29;graph_config3='f';}
    if (choix_ch3=="7") {functionCH3B('X','Y','Z','Vecteur Gravité (m/s²)');A3 =30; B3=32;graph_config3='g';}
    if (choix_ch3=="8") {functionCH3A('Température','Température (°c)');A3 =8; B3=8;graph_config3='h';}
    if (choix_ch3=="9") {functionCH3A('Pression','Pression (Pa)');A3 =10; B3=10;graph_config3='j';}
    if (choix_ch3=="10") {functionCH3A('Altitude','Altitude (m)');A3 =9; B3=9;graph_config3='i';}
    if (choix_ch3=="11") {functionCH3A('Vbat','Vbat (V)');A3 =1; B3=1;graph_config3= 'k';}
    if (choix_ch3=="14") {functionCH3A('Icharge','Icharge (A)');A3 =4; B3=4;graph_config3= 'k';}
    if (choix_ch3=="12") {functionCH3A('Tbat','Tbat (°c)');A3 =6; B3=6;graph_config3= 'k';}
    if (choix_ch3=="13") {functionCH3D('+X','-X','+Y','-Y','Z','Luminance');A3 =33; B3=37;graph_config3= 'l';}
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/configGraph3?choix="+graph_config3, true);
    xhr.send();
}
// Create Charts



  Chart3 = new Highcharts.Chart({
    chart:{renderTo: id3},
  
    title: {
      text: undefined
    },

    credits: {
    enabled: false
    }
    });
  

  function functionCH3A(x,y) {

    Chart3 = new Highcharts.Chart({
      chart:{renderTo: id3},
      type: 'line',
      series: [
        {
          name: x,
          color: '#101D42',
          //showInLegend: false,
          marker: false,
        },
      
      ],
      
      plotOptions : {
        line: { animation: false,
        dataLabels: { enabled: false }
        },
        
      },
      title: {
        text: undefined
      },
      xAxis: {
        title: {
          text: 'Temps'
        },
        type: 'datetime',
        dateTimeLabelFormats: { second: '%H:%M:%S' }
      },
      yAxis: {
        title: {
          text: y
        }
      },
      credits: {
      enabled: false
      }
      });
      Highcharts.setOptions({
      time: {
        timezoneOffset: -60 // time zone offset here in minutes
      }
      });
    
    }
function functionCH3B(x,y,z,w) {

Chart3 = new Highcharts.Chart({
  chart:{renderTo: id3},
  type: 'line',
  series: [
    {
      name: x,
      color: '#101D42',
      //showInLegend: false,
      marker: false,
    },
      
     
    
    {
      name: y,
      color: '#00A6A6',
      marker: false,
   
    },
    {
      name: z,
      color: '#da2c2c',
      marker: false,
    },
  
  
  ],
  
  plotOptions : {
    line: { animation: false,
    dataLabels: { enabled: false }
    },
    
  },
  title: {
    text: undefined
  },
  xAxis: {
    title: {
      text: 'Temps'
    },
    type: 'datetime',
    dateTimeLabelFormats: { second: '%H:%M:%S' }
  },
  yAxis: {
    title: {
      text: w
    }
  },
  credits: {
  enabled: false
  }
  });
  Highcharts.setOptions({
  time: {
    timezoneOffset: -60 // time zone offset here in minutes
  }
  });

}

function functionCH3C(k,x,y,z,w) {

Chart3 = new Highcharts.Chart({
    chart:{renderTo: id3},
    type: 'line',
    series: [
      {
        name: k,
        color: '#101D42',
        //showInLegend: false,
        marker: false,
      },
        
       
      
      {
        name: x,
        color: '#00A6A6',
        marker: false,
     
      },
      {
        name: y,
        color: '#da2c2c',
        marker: false,
      },
    
      {
        
        name: z,
        color: '#dd90d7',
        marker: false,
       
      },
    
    ],
    
    plotOptions : {
      line: { animation: false,
      dataLabels: { enabled: false }
      },
      
    },
    title: {
      text: undefined
    },
    xAxis: {
      title: {
        text: 'Temps'
      },
      type: 'datetime',
      dateTimeLabelFormats: { second: '%H:%M:%S' }
    },
    yAxis: {
      title: {
        text: w
      }
    },
    credits: {
    enabled: false
    }
    });
    Highcharts.setOptions({
    time: {
      timezoneOffset: -60 // time zone offset here in minutes
    }
    });
  
  }
  function functionCH3D(k,x,y,z,j,w) {

    Chart3 = new Highcharts.Chart({
        chart:{renderTo: id3},
        type: 'line',
        series: [
          {
            name: k,
            color: '#101D42',
            //showInLegend: false,
            marker: false,
          },
            
           
          
          {
            name: x,
            color: '#00A6A6',
            marker: false,
         
          },
          {
            name: y,
            color: '#da2c2c',
            marker: false,
          },
        
          {
            
            name: z,
            color: '#dd90d7',
            marker: false,
           
          },
          {
            
            name: j,
            color: '#da8c3c',
            marker: false,
           
          },
        
        ],
        
        plotOptions : {
          line: { animation: false,
          dataLabels: { enabled: false }
          },
          
        },
        title: {
          text: undefined
        },
        xAxis: {
          title: {
            text: 'Temps'
          },
          type: 'datetime',
          dateTimeLabelFormats: { second: '%H:%M:%S' }
        },
        yAxis: {
          title: {
            text: w
          }
        },
        credits: {
        enabled: false
        }
        });
        Highcharts.setOptions({
        time: {
          timezoneOffset: -60 // time zone offset here in minutes
        }
        });
      
      }
  //****************************************************************************************************************************************************************************
  function plotChart3(jsonValue, A, B) {
    if (C3!==1){
    var keys = Object.keys(jsonValue);
    // console.log(keys);
    //console.log(keys.length);
    var j =0;
    for (var i = A-1; i <B; i++){
      var x = (new Date()).getTime();
      //console.log(x);
      const key = keys[i];
      var y = Number(jsonValue[key]);
     // console.log(y);
    
      if(Chart3.series[j].data.length > nbr) {
        Chart3.series[j].addPoint([x, y], true, true, true);
      } else {
        Chart3.series[j].addPoint([x, y], true, false, true);
      }
    j = j+1
    }
    }
    C3+=1;
  }
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
var A4, B4, choix_ch4; 
var Chart4, id4='chart4' ;

function validatChart4() {
  choix_ch4 = document.forms["myChart4"]["modu4"].value;
  C4 =1;
    console.log("Le module choisi est :", choix_ch4);
    if (choix_ch4=="0") {graph_config4='0';}
    if (choix_ch4=="1") {functionCH4B('Roulis','Tangage','Lacet','Vecteur Euler (°)'); A4 =11; B4=13;graph_config4='a';}
    if (choix_ch4=="2") {functionCH4C('W','X','Y','Z','Quaternion');A4 =14; B4=17;graph_config4='b';}
    if (choix_ch4=="3") {functionCH4B('X','Y','Z','Vitesse Angulaire (rad/s)');A4 =18; B4=20;graph_config4='c';}
    if (choix_ch4=="4") {functionCH4B('X','Y','Z','Accelération (m/s²)');A4 =21; B4=23;graph_config4='d';}
    if (choix_ch4=="5") {functionCH4B('X','Y','Z','Champs Magnétique (uT)');A4 =24; B4=26;graph_config4='e';}
    if (choix_ch4=="6") {functionCH4B('X','Y','Z','Accelération Linéaire (m/s²)');A4 =27; B4=29;graph_config4='f';}
    if (choix_ch4=="7") {functionCH4B('X','Y','Z','Vecteur Gravité (m/s²)');A4 =30; B4=32;graph_config4='g';}
    if (choix_ch4=="8") {functionCH4A('Température','Température (°c)');A4 =8; B4=8;graph_config4='h';}
    if (choix_ch4=="9") {functionCH4A('Pression','Pression (Pa)');A4 =10; B4=10;graph_config4='j';}
    if (choix_ch4=="10") {functionCH4A('Altitude','Altitude (m)');A4 =9; B4=9;graph_config4='i';}
    if (choix_ch4=="11") {functionCH4A('Vbat','Vbat (V)');A4 =1; B4=1;graph_config4= 'k';}
    if (choix_ch4=="14") {functionCH4A('Icharge','Icharge (A)');A4 =4; B4=4;graph_config4= 'k';}
    if (choix_ch4=="12") {functionCH4A('Tbat','Tbat (°c)');A4 =6; B4=6;graph_config4= 'k';}
    if (choix_ch4=="13") {functionCH4D('+X','-X','+Y','-Y','Z','Luminance');A4 =33; B4=37;graph_config4= 'l';}    
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/configGraph4?choix="+graph_config4, true);
    xhr.send();
}
// Create Charts



  Chart4 = new Highcharts.Chart({
    chart:{renderTo: id4},
  
    title: {
      text: undefined
    },

    credits: {
    enabled: false
    }
    });
  

  function functionCH4A(x,y) {

    Chart4 = new Highcharts.Chart({
      chart:{renderTo: id4},
      type: 'line',
      series: [
        {
          name: x,
          color: '#101D42',
          //showInLegend: false,
          marker: false,
        },
      
      ],
      
      plotOptions : {
        line: { animation: false,
        dataLabels: { enabled: false }
        },
        
      },
      title: {
        text: undefined
      },
      xAxis: {
        title: {
          text: 'Temps'
        },
        type: 'datetime',
        dateTimeLabelFormats: { second: '%H:%M:%S' }
      },
      yAxis: {
        title: {
          text: y
        }
      },
      credits: {
      enabled: false
      }
      });
      Highcharts.setOptions({
      time: {
        timezoneOffset: -60 // time zone offset here in minutes
      }
      });
    
    }
function functionCH4B(x,y,z,w) {

Chart4 = new Highcharts.Chart({
  chart:{renderTo: id4},
  type: 'line',
  series: [
    {
      name: x,
      color: '#101D42',
      //showInLegend: false,
      marker: false,
    },
      
     
    
    {
      name: y,
      color: '#00A6A6',
      marker: false,
   
    },
    {
      name: z,
      color: '#da2c2c',
      marker: false,
    },
  
  
  ],
  
  plotOptions : {
    line: { animation: false,
    dataLabels: { enabled: false }
    },
    
  },
  title: {
    text: undefined
  },
  xAxis: {
    title: {
      text: 'Temps'
    },
    type: 'datetime',
    dateTimeLabelFormats: { second: '%H:%M:%S' }
  },
  yAxis: {
    title: {
      text: w
    }
  },
  credits: {
  enabled: false
  }
  });
  Highcharts.setOptions({
  time: {
    timezoneOffset: -60 // time zone offset here in minutes
  }
  });

}

function functionCH4C(k,x,y,z,w) {

Chart4 = new Highcharts.Chart({
    chart:{renderTo: id4},
    type: 'line',
    series: [
      {
        name: k,
        color: '#101D42',
        //showInLegend: false,
        marker: false,
      },
        
       
      
      {
        name: x,
        color: '#00A6A6',
        marker: false,
     
      },
      {
        name: y,
        color: '#da2c2c',
        marker: false,
      },
    
      {
        
        name: z,
        color: '#dd90d7',
        marker: false,
       
      },
    
    ],
    
    plotOptions : {
      line: { animation: false,
      dataLabels: { enabled: false }
      },
      
    },
    title: {
      text: undefined
    },
    xAxis: {
      title: {
        text: 'Temps'
      },
      type: 'datetime',
      dateTimeLabelFormats: { second: '%H:%M:%S' }
    },
    yAxis: {
      title: {
        text: w
      }
    },
    credits: {
    enabled: false
    }
    });
    Highcharts.setOptions({
    time: {
      timezoneOffset: -60 // time zone offset here in minutes
    }
    });
  
  }

  function functionCH4D(k,x,y,z,j,w) {

    Chart4 = new Highcharts.Chart({
        chart:{renderTo: id4},
        type: 'line',
        series: [
          {
            name: k,
            color: '#101D42',
            //showInLegend: false,
            marker: false,
          },
            
           
          
          {
            name: x,
            color: '#00A6A6',
            marker: false,
         
          },
          {
            name: y,
            color: '#da2c2c',
            marker: false,
          },
        
          {
            
            name: z,
            color: '#dd90d7',
            marker: false,
           
          },
          {
            
            name: j,
            color: '#da8c3c',
            marker: false,
           
          },
        
        ],
        
        plotOptions : {
          line: { animation: false,
          dataLabels: { enabled: false }
          },
          
        },
        title: {
          text: undefined
        },
        xAxis: {
          title: {
            text: 'Temps'
          },
          type: 'datetime',
          dateTimeLabelFormats: { second: '%H:%M:%S' }
        },
        yAxis: {
          title: {
            text: w
          }
        },
        credits: {
        enabled: false
        }
        });
        Highcharts.setOptions({
        time: {
          timezoneOffset: -60 // time zone offset here in minutes
        }
        });
      
      }
  //****************************************************************************************************************************************************************************
  function plotChart4(jsonValue, A, B) {
    if (C4!==1){
    var keys = Object.keys(jsonValue);
    // console.log(keys);
    //console.log(keys.length);
    var j =0;
    for (var i = A-1; i <B; i++){
      var x = (new Date()).getTime();
      //console.log(x);
      const key = keys[i];
      var y = Number(jsonValue[key]);
     // console.log(y);
    
      if(Chart4.series[j].data.length > nbr) {
        Chart4.series[j].addPoint([x, y], true, true, true);
      } else {
        Chart4.series[j].addPoint([x, y], true, false, true);
      }
    j = j+1
    }
    }
    C4+=1;
    }
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
var A5, B5, choix_ch5; 
var Chart5, id5='chart5' ;

function validatChart5() {
  choix_ch5 = document.forms["myChart5"]["modu5"].value;
    console.log("Le module choisi est :", choix_ch5);
    C5 =1;
    if (choix_ch5=="0") {graph_config5='0';}
    if (choix_ch5=="1") {functionCH5B('Roulis','Tangage','Lacet','Vecteur Euler (°)'); A5 =11; B5=13;graph_config5='a';}
    if (choix_ch5=="2") {functionCH5C('W','X','Y','Z','Quaternion');A5 =14; B5=17;graph_config5='b';}
    if (choix_ch5=="3") {functionCH5B('X','Y','Z','Vitesse Angulaire (rad/s)');A5 =18; B5=20;graph_config5='c';}
    if (choix_ch5=="4") {functionCH5B('X','Y','Z','Accelération (m/s²)');A5 =21; B5=23;graph_config5='d';}
    if (choix_ch5=="5") {functionCH5B('X','Y','Z','Champs Magnétique (uT)');A5 =24; B5=26;graph_config5='e';}
    if (choix_ch5=="6") {functionCH5B('X','Y','Z','Accelération Linéaire (m/s²)');A5 =27; B5=29;graph_config5='f';}
    if (choix_ch5=="7") {functionCH5B('X','Y','Z','Vecteur Gravité (m/s²)');A5 =30; B5=32;graph_config5='g';}
    if (choix_ch5=="8") {functionCH5A('Température','Température (°c)');A5 =8; B5=8;graph_config5='h';}
    if (choix_ch5=="9") {functionCH5A('Pression','Pression (Pa)');A5 =10; B5=10;graph_config5='j';}
    if (choix_ch5=="10") {functionCH5A('Altitude','Altitude (m)');A5 =9; B5=9;graph_config5='i';}
    if (choix_ch5=="11") {functionCH5A('Vbat','Vbat (V)');A5 =1; B5=1;graph_config5= 'k';}
    if (choix_ch5=="14") {functionCH5A('Icharge','Icharge (A)');A5 =4; B5=4;graph_config5= 'k';}
    if (choix_ch5=="12") {functionCH5A('Tbat','Tbat (°c)');A5 =6; B5=6;graph_config5= 'k';}
    if (choix_ch5=="13") {functionCH5D('+X','-X','+Y','-Y','Z','Luminance');A5 =33; B5=37;graph_config5= 'l';}
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/configGraph5?choix="+graph_config5, true);
    xhr.send();
}
// Create Charts



  Chart5 = new Highcharts.Chart({
    chart:{renderTo: id5},
  
    title: {
      text: undefined
    },

    credits: {
    enabled: false
    }
    });
  

  function functionCH5A(x,y) {

    Chart5 = new Highcharts.Chart({
      chart:{renderTo: id5},
      type: 'line',
      series: [
        {
          name: x,
          color: '#101D42',
          //showInLegend: false,
          marker: false,
        },
      
      ],
      
      plotOptions : {
        line: { animation: false,
        dataLabels: { enabled: false }
        },
        
      },
      title: {
        text: undefined
      },
      xAxis: {
        title: {
          text: 'Temps'
        },
        type: 'datetime',
        dateTimeLabelFormats: { second: '%H:%M:%S' }
      },
      yAxis: {
        title: {
          text: y
        }
      },
      credits: {
      enabled: false
      }
      });
      Highcharts.setOptions({
      time: {
        timezoneOffset: -60 // time zone offset here in minutes
      }
      });
    
    }
function functionCH5B(x,y,z,w) {

Chart5 = new Highcharts.Chart({
  chart:{renderTo: id5},
  type: 'line',
  series: [
    {
      name: x,
      color: '#101D42',
      //showInLegend: false,
      marker: false,
    },
      
     
    
    {
      name: y,
      color: '#00A6A6',
      marker: false,
   
    },
    {
      name: z,
      color: '#da2c2c',
      marker: false,
    },
  
  
  ],
  
  plotOptions : {
    line: { animation: false,
    dataLabels: { enabled: false }
    },
    
  },
  title: {
    text: undefined
  },
  xAxis: {
    title: {
      text: 'Temps'
    },
    type: 'datetime',
    dateTimeLabelFormats: { second: '%H:%M:%S' }
  },
  yAxis: {
    title: {
      text: w
    }
  },
  credits: {
  enabled: false
  }
  });
  Highcharts.setOptions({
  time: {
    timezoneOffset: -60 // time zone offset here in minutes
  }
  });

}

function functionCH5C(k,x,y,z,w) {

Chart5 = new Highcharts.Chart({
    chart:{renderTo: id5},
    type: 'line',
    series: [
      {
        name: k,
        color: '#101D42',
        //showInLegend: false,
        marker: false,
      },
        
       
      
      {
        name: x,
        color: '#00A6A6',
        marker: false,
     
      },
      {
        name: y,
        color: '#da2c2c',
        marker: false,
      },
    
      {
        
        name: z,
        color: '#dd90d7',
        marker: false,
       
      },
    
    ],
    
    plotOptions : {
      line: { animation: false,
      dataLabels: { enabled: false }
      },
      
    },
    title: {
      text: undefined
    },
    xAxis: {
      title: {
        text: 'Temps'
      },
      type: 'datetime',
      dateTimeLabelFormats: { second: '%H:%M:%S' }
    },
    yAxis: {
      title: {
        text: w
      }
    },
    credits: {
    enabled: false
    }
    });
    Highcharts.setOptions({
    time: {
      timezoneOffset: -60 // time zone offset here in minutes
    }
    });
  
  }

  function functionCH5D(k,x,y,z,j,w) {

    Chart5 = new Highcharts.Chart({
        chart:{renderTo: id5},
        type: 'line',
        series: [
          {
            name: k,
            color: '#101D42',
            //showInLegend: false,
            marker: false,
          },
            
           
          
          {
            name: x,
            color: '#00A6A6',
            marker: false,
         
          },
          {
            name: y,
            color: '#da2c2c',
            marker: false,
          },
        
          {
            
            name: z,
            color: '#dd90d7',
            marker: false,
           
          },
          {
            
            name: j,
            color: '#da8c3c',
            marker: false,
           
          },
        
        ],
        
        plotOptions : {
          line: { animation: false,
          dataLabels: { enabled: false }
          },
          
        },
        title: {
          text: undefined
        },
        xAxis: {
          title: {
            text: 'Temps'
          },
          type: 'datetime',
          dateTimeLabelFormats: { second: '%H:%M:%S' }
        },
        yAxis: {
          title: {
            text: w
          }
        },
        credits: {
        enabled: false
        }
        });
        Highcharts.setOptions({
        time: {
          timezoneOffset: -60 // time zone offset here in minutes
        }
        });
      
      }
  //****************************************************************************************************************************************************************************
  function plotChart5(jsonValue, A, B) {
    if (C5!==1){
    var keys = Object.keys(jsonValue);
    // console.log(keys);
    //console.log(keys.length);
    var j =0;
    for (var i = A-1; i <B; i++){
      var x = (new Date()).getTime();
      //console.log(x);
      const key = keys[i];
      var y = Number(jsonValue[key]);
     // console.log(y);
    
      if(Chart5.series[j].data.length > nbr) {
        Chart5.series[j].addPoint([x, y], true, true, true);
      } else {
        Chart5.series[j].addPoint([x, y], true, false, true);
      }
    j = j+1
    }
    }
    C5+=1;
    }
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
var A6, B6, choix_ch6; 
var Chart6, id6='chart6' ;

function validatChart6() {
  choix_ch6 = document.forms["myChart6"]["modu6"].value;
    console.log("Le module choisi est :", choix_ch6);
    C6 =1;
    if (choix_ch6=="0") {graph_config6='0';}
    if (choix_ch6=="1") {functionCH6B('Roulis','Tangage','Lacet','Vecteur Euler (°)'); A6 =11; B6=13;graph_config6='a';}
    if (choix_ch6=="2") {functionCH6C('W','X','Y','Z','Quaternion');A6 =14; B6=17;graph_config6='b';}
    if (choix_ch6=="3") {functionCH6B('X','Y','Z','Vitesse Angulaire (rad/s)');A6 =18; B6=20;graph_config6='c';}
    if (choix_ch6=="4") {functionCH6B('X','Y','Z','Accelération (m/s²)');A6 =21; B6=23;graph_config6='d';}
    if (choix_ch6=="5") {functionCH6B('X','Y','Z','Champs Magnétique (uT)');A6 =24; B6=26;graph_config6='e';}
    if (choix_ch6=="6") {functionCH6B('X','Y','Z','Accelération Linéaire (m/s²)');A6 =27; B6=29;graph_config6='f';}
    if (choix_ch6=="7") {functionCH6B('X','Y','Z','Vecteur Gravité (m/s²)');A6 =30; B6=32;graph_config6='g';}
    if (choix_ch6=="8") {functionCH6A('Température','Température (°c)');A6 =8; B6=8;graph_config6='h';}
    if (choix_ch6=="9") {functionCH6A('Pression','Pression (Pa)');A6 =10; B6=10;graph_config6='j';}
    if (choix_ch6=="10") {functionCH6A('Altitude','Altitude (m)');A6 =9; B6=9;graph_config6='i';}
    if (choix_ch6=="11") {functionCH6A('Vbat','Vbat (V)');A6 =1; B6=1;graph_config6= 'k';}
    if (choix_ch6=="14") {functionCH6A('Icharge','Icharge (A)');A6 =4; B6=4;graph_config6= 'k';}
    if (choix_ch6=="12") {functionCH6A('Tbat','Tbat (°c)');A6 =6; B6=6;graph_config6= 'k';}
    if (choix_ch6=="13") {functionCH6D('+X','-X','+Y','-Y','Z','Luminance');A6 =33; B6=37;graph_config6= 'l';}
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/configGraph6?choix="+graph_config6, true);
    xhr.send();

}
// Create Charts



  Chart6 = new Highcharts.Chart({
    chart:{renderTo: id6},
  
    title: {
      text: undefined
    },

    credits: {
    enabled: false
    }
    });
  

  function functionCH6A(x,y) {

    Chart6 = new Highcharts.Chart({
      chart:{renderTo: id6},
      type: 'line',
      series: [
        {
          name: x,
          color: '#101D42',
          //showInLegend: false,
          marker: false,
        },
      
      ],
      
      plotOptions : {
        line: { animation: false,
        dataLabels: { enabled: false }
        },
        
      },
      title: {
        text: undefined
      },
      xAxis: {
        title: {
          text: 'Temps'
        },
        type: 'datetime',
        dateTimeLabelFormats: { second: '%H:%M:%S' }
      },
      yAxis: {
        title: {
          text: y
        }
      },
      credits: {
      enabled: false
      }
      });
      Highcharts.setOptions({
      time: {
        timezoneOffset: -60 // time zone offset here in minutes
      }
      });
    
    }
function functionCH6B(x,y,z,w) {

Chart6 = new Highcharts.Chart({
  chart:{renderTo: id6},
  type: 'line',
  series: [
    {
      name: x,
      color: '#101D42',
      //showInLegend: false,
      marker: false,
    },
      
     
    
    {
      name: y,
      color: '#00A6A6',
      marker: false,
   
    },
    {
      name: z,
      color: '#da2c2c',
      marker: false,
    },
  
  
  ],
  
  plotOptions : {
    line: { animation: false,
    dataLabels: { enabled: false }
    },
    
  },
  title: {
    text: undefined
  },
  xAxis: {
    title: {
      text: 'Temps'
    },
    type: 'datetime',
    dateTimeLabelFormats: { second: '%H:%M:%S' }
  },
  yAxis: {
    title: {
      text: w
    }
  },
  credits: {
  enabled: false
  }
  });
  Highcharts.setOptions({
  time: {
    timezoneOffset: -60 // time zone offset here in minutes
  }
  });

}

function functionCH6C(k,x,y,z,w) {

Chart6 = new Highcharts.Chart({
    chart:{renderTo: id6},
    type: 'line',
    series: [
      {
        name: k,
        color: '#101D42',
        //showInLegend: false,
        marker: false,
      },
        
       
      
      {
        name: x,
        color: '#00A6A6',
        marker: false,
     
      },
      {
        name: y,
        color: '#da2c2c',
        marker: false,
      },
    
      {
        
        name: z,
        color: '#dd90d7',
        marker: false,
       
      },
    
    ],
    
    plotOptions : {
      line: { animation: false,
      dataLabels: { enabled: false }
      },
      
    },
    title: {
      text: undefined
    },
    xAxis: {
      title: {
        text: 'Temps'
      },
      type: 'datetime',
      dateTimeLabelFormats: { second: '%H:%M:%S' }
    },
    yAxis: {
      title: {
        text: w
      }
    },
    credits: {
    enabled: false
    }
    });
    Highcharts.setOptions({
    time: {
      timezoneOffset: -60 // time zone offset here in minutes
    }
    });
  
  }

  function functionCH6D(k,x,y,z,j,w) {

    Chart6 = new Highcharts.Chart({
        chart:{renderTo: id6},
        type: 'line',
        series: [
          {
            name: k,
            color: '#101D42',
            //showInLegend: false,
            marker: false,
          },
            
           
          
          {
            name: x,
            color: '#00A6A6',
            marker: false,
         
          },
          {
            name: y,
            color: '#da2c2c',
            marker: false,
          },
        
          {
            
            name: z,
            color: '#dd90d7',
            marker: false,
           
          },
          {
            
            name: j,
            color: '#da8c3c',
            marker: false,
           
          },
        
        ],
        
        plotOptions : {
          line: { animation: false,
          dataLabels: { enabled: false }
          },
          
        },
        title: {
          text: undefined
        },
        xAxis: {
          title: {
            text: 'Temps'
          },
          type: 'datetime',
          dateTimeLabelFormats: { second: '%H:%M:%S' }
        },
        yAxis: {
          title: {
            text: w
          }
        },
        credits: {
        enabled: false
        }
        });
        Highcharts.setOptions({
        time: {
          timezoneOffset: -60 // time zone offset here in minutes
        }
        });
      
      }

  //****************************************************************************************************************************************************************************
  function plotChart6(jsonValue, A, B) {
    if (C6!==1){
    var keys = Object.keys(jsonValue);
    // console.log(keys);
    //console.log(keys.length);
    var j =0;
    for (var i = A-1; i <B; i++){
      var x = (new Date()).getTime();
      //console.log(x);
      const key = keys[i];
      var y = Number(jsonValue[key]);
     // console.log(y);
    
      if(Chart6.series[j].data.length > nbr) {
        Chart6.series[j].addPoint([x, y], true, true, true);
      } else {
        Chart6.series[j].addPoint([x, y], true, false, true);
      }
    j = j+1
    }
    }
    C6+=1;
  }
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  // FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS FONCTIONS 
/*
  window.onbeforeunload = function(){ // alerte avant la fermuture de la page
    return "any"    
  }

*/
    
  
var intv = 5;
window.onload = function() { // same as window.addEventListener('load', (event) => {
  intv = localStorage.getItem("gph_interval")
  document.forms["myForm0"]["grph_Temps"].value = intv;
  document.getElementById("intvGr_").innerHTML = ("Période d'acquisition actuelle : "+intv+" secondes").fontcolor("green");
};


function validateForm0() {
  var  T_cons = document.forms["myForm0"]["grph_Temps"].value;
    if ((T_cons<5) || (T_cons>3600)) {
 
      document.getElementById("intvGr_").innerHTML = ("rien").fontcolor("transparent");
      setTimeout(function(){document.getElementById("intvGr_").innerHTML = ("Veuillez choisir une periode entre 5 et 3600 secondes !").fontcolor("red"); },200); }
    else {

    localStorage.setItem("gph_interval", T_cons);
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      var obj = this.responseText;
      document.getElementById("intvGr_").innerHTML = (".").fontcolor("white");
      setTimeout(function(){document.getElementById("intvGr_").innerHTML = (obj).fontcolor("green"); },100);
      }}
      xhr.open("GET", "/t_graph?choix="+T_cons, true);
      xhr.send();
    }
  }


  setInterval(function(){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/user", true);
    xhr.send();
  
  },300000);