const displays = document.querySelectorAll('.note-display');
const transitionDuration = 900;


displays.forEach(display => {



  let note = parseInt(display.dataset.note);
  let int = display.dataset.note.split('.');
  int = Number(int)



  let jackcolor=document.getElementById('jack-circle');

  if(note>300)
  {
    jackcolor.style.stroke="rgba(209, 24, 24, 1)";
    
  }
  else if(note>200 && note<=300)
  {
    jackcolor.style.stroke="rgba(238, 77, 135, 1)";
    
  }
  else if(note>150 && note<=200)
  {
    jackcolor.style.stroke="rgba(208, 106, 11, 1)";
    jackaqi.style.color=jackcolor.style.stroke;
  }
  else if(note>100 && note<=150)
  {
    jackcolor.style.stroke="rgba(248, 181, 52, 1)";

  }
  else if(note>50 && note<=100)
  {
    jackcolor.style.stroke="rgba(252, 229, 20, 1)";

    document.getElementById('icon-1').src="https://img.icons8.com/ios-filled/30/000000/reading.png";

    document.getElementById('line-1').innerHTML="Outdoor activities not recommended";
  }
  else
  {
    jackcolor.style.stroke="rgba(169, 240, 17, 1)";

    document.getElementById('icon-2').src="https://img.icons8.com/material-sharp/30/000000/partly-cloudy-day--v1.png";

    document.getElementById('line-2').innerHTML="Air purifier not required";


    document.getElementById('icon-4').src="https://img.icons8.com/material-rounded/30/000000/door-opened.png";

    document.getElementById('line-4').innerHTML="Ventilation open windows";

    document.getElementById('line-3').innerHTML="Pollution mask not required";
  }


  strokeTransition(display, note);

  increaseNumber(display, int, 'int');
});

function strokeTransition(display, note) {
  let progress = display.querySelector('.circle__progress--fill');
  let radius = progress.r.baseVal.value;
  let circumference = 2 * Math.PI * radius;
  let offset = circumference * (note) / 500;
  // jackcolor.style.stroke.setProperty('--jackop',#FF0000);
  progress.style.setProperty('--initialStroke', circumference);
  progress.style.setProperty('--transitionDuration', `${transitionDuration}ms`);

  setTimeout(() => progress.style.strokeDashoffset = offset, 100);
}

function increaseNumber(display, number, className) {
  let element = display.querySelector(`.percent__${className}`),
      
      interval = transitionDuration / number,
      counter = 0;

  let increaseInterval = setInterval(() => {
    if (counter === number) { window.clearInterval(increaseInterval); }

    element.textContent = counter;
    counter++;
  }, interval);
}