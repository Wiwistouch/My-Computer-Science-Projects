// fonction algho tri bulle 
function algho_tri_bulle(tab) {
  var tableau=[...tab]
  for (var index=0;index<tableau.length-1;index++) {
      for (var i=0;i<tableau.length-1-index;i++) {
          if (tableau[i]>tableau[i+1]) {
              [[tableau[i],tableau[i+1]]=[tableau[i+1],tableau[i]]]
          }
      }
  }
    
  return tableau
}


var liste=[]
function liste_random() {
    liste=[]
    var longueur_liste_alea=parseInt(document.alea_liste.longueur.value)
    var min=parseInt(document.alea_liste.minimum.value)
    var max=parseInt(document.alea_liste.maximum.value)
    for (var i=0;i<longueur_liste_alea;i++) {
        liste.push(Math.floor(Math.random() * (max - min + 1)) + min)
    }
    Chartt(liste)
}


function liste_user() {
    var user=document.liste_donne.liste.value
    var user=user.split(",").map(Number)
    Chartt(user)
    return user
}


function liste_user_triee() {
    Chartt(algho_tri_bulle(liste_user()))

}

function anim_liste_user() {
  animation(liste_user())
}

function liste_alea_triee() {
    Chartt(algho_tri_bulle(liste)) 
}

function anim_liste_alea() {
  animation(liste)
}

var chartInstance=false
function Chartt(tableau) {
    if (chartInstance) {
        chartInstance.destroy()
    }

    if (chartInstance2) {
      chartInstance2.destroy()
    }

    chartInstance = new Chart("myChart", {
        type: "bar",
        data: {
          labels: tableau,
          datasets: [{
            backgroundColor: "black",
            data: tableau
          }]
        },
        options: {
          legend: {display: false},
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true
              }
            }]
          }
        }
    })
}


var chartInstance2 = false

async function animation(tabl) {
  var tableau=[...tabl]
  var couleur = [];
  for (var index=0;index<tableau.length;index++) {
    couleur.push("black");
  }

  if (chartInstance) {
    chartInstance.destroy();
  }

  if (chartInstance2) {
    chartInstance2.destroy();
  }
  chartInstance2 = new Chart("myChart", {
    type: "bar",
    data: {
      labels: tableau,
      datasets: [{
        backgroundColor: couleur,
        data: tableau
      }]
    },
    options: {
      legend: { display: false },
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
      }
    }
  });

  // Animation du tri
  for (var index = 0; index < tableau.length - 1; index++) {
    for (var i = 0; i < tableau.length - 1 - index; i++) {
      if (tableau[i] > tableau[i + 1]) {
        couleur[i]="red";
        chartInstance2.data.datasets[0].backgroundColor = couleur;
        chartInstance2.update();

        await new Promise(resolve => setTimeout(resolve, 500));
        
        [tableau[i], tableau[i + 1]] = [tableau[i + 1], tableau[i]];
        chartInstance2.data.datasets[0].data = tableau;
        chartInstance2.update();
        couleur[i] = "black";
        chartInstance2.data.datasets[0].backgroundColor = couleur;
        chartInstance2.update();

        await new Promise(resolve => setTimeout(resolve, 500));
      }
    }
  }
}