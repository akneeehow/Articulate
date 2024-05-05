const wordText = document.querySelector(".word"),
hintText = document.querySelector(".hint span"),
timeText = document.querySelector(".time b"),
inputField = document.querySelector("input"),
refreshBtn = document.querySelector(".refresh-word"),
checkBtn = document.querySelector(".check-word");
contentBox = document.querySelector(".container .content");
startArea = document.querySelector(".startArea");
scoreArea = document.querySelector(".score");
modalContent = document.querySelector(".modal-content");
scoreAreaTeam1 = document.getElementById("scoreTeam1");
scoreAreaTeam2 = document.getElementById("scoreTeam2");
// Get the modal
var modal = document.getElementById("myModal");
// Get the button that opens the modal
var btn = document.getElementById("myBtn");
// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
// Get the text of modal
var modalText = document.getElementById("modalText");

let correctWord, timer;
let scoreTeam1 = 0;
let scoreTeam2 = 0;
let currentTeam = 1;
let timerStarted = false;
let gameOver = false;
let maxTime = 30;
let timeLeft = maxTime;


const Team1Form = document.getElementById("Team1-form");
const Team2Form = document.getElementById("Team2-form");
const Team1Names = document.getElementById("Team1-names");
const Team2Names = document.getElementById("Team2-names");
const addTeam1Btn = document.getElementById("add-Team1");
const addTeam2Btn = document.getElementById("add-Team2");

const categories = ["Places", "Objects", "Nature", "Food", "Random"];
const getRandomCategory = (TeamScore) => {
  const categoryIndex = TeamScore % categories.length;
  return categories[categoryIndex];
};

Team1Form.addEventListener("submit", (e) => {
  e.preventDefault();
  const TeamName = document.getElementById("Team1-name").value.trim();
  if (TeamName === "") {
    modal.style.display = "block";
    modalContent.classList.add("modal-wrong");
    modalContent.classList.remove("modal-correct");
    return modalText.innerHTML = `<br>Please enter a Team name`;
  }
  if (Team1Names.children.length > 0 && [...Team1Names.children].some(child => child.textContent.trim() === TeamName)) {
    modal.style.display = "block";
    modalContent.classList.add("modal-wrong");
    modalContent.classList.remove("modal-correct");
    return modalText.innerHTML = `<br>Player name already exists. Please enter a unique name'`;
  }
  const listItem = document.createElement("li");
  listItem.textContent = TeamName;
  Team1Names.appendChild(listItem);
  document.getElementById("Team1-name").value = "";
});

Team2Form.addEventListener("submit", (e) => {
  e.preventDefault();
  const TeamName = document.getElementById("Team2-name").value.trim();
  if (TeamName === "") {
    modal.style.display = "block";
    modalContent.classList.add("modal-wrong");
    modalContent.classList.remove("modal-correct");
    return modalText.innerHTML = `<br>Please enter a Team name`;
  }
  if (Team1Names.children.length > 0 && [...Team1Names.children].some(child => child.textContent.trim() === TeamName)) {
    modal.style.display = "block";
    modalContent.classList.add("modal-wrong");
    modalContent.classList.remove("modal-correct");
    return modalText.innerHTML = `<br>Player name already exists. Please enter a different name'`;
  }
  const listItem = document.createElement("li");
  listItem.textContent = TeamName;
  Team2Names.appendChild(listItem);
  document.getElementById("Team2-name").value = "";
});


const initTimer = () => {
  if (!timerStarted) {
    timerStarted = true;
    clearInterval(timer);
    timeLeft = maxTime;
    timer = setInterval(() => {
      if (timeLeft > 0) {
        timeLeft--;
        timeText.innerText = timeLeft;
      } else {
        switchTeam();
      }
    }, 1000);
  }
}

let modalDisplayed = false;


const switchTeam = () => {
  clearInterval(timer);
  timerStarted = false;
  modal.style.display = "block";
  modalContent.classList.remove("modal-correct");
  modalContent.classList.add("modal-wrong");
  if (currentTeam === 1) {
    modalText.innerHTML = `Time off! Now it's Team 2's turn!`;
    currentTeam = 2;
  } else {
    modalText.innerHTML = `Time off! Now it's Team 1's turn!`;
    currentTeam = 1;
  }
  modalDisplayed = true;
}


const initGame = () => {
  if (gameOver) {
    resetGame();
  }
  const TeamScore = currentTeam === 1 ? scoreTeam1 : scoreTeam2;
  const category = getRandomCategory(TeamScore);
  document.getElementById("current-category").textContent = category;
  let randomObj = words[Math.floor(Math.random() * words.length)];
  let wordArray = randomObj.word.split("");
  for (let i = wordArray.length - 1; i > 0; i--) {
    let j = Math.floor(Math.random() * (i + 1));
    [wordArray[i], wordArray[j]] = [wordArray[j], wordArray[i]];
  }
  
  wordText.innerText = wordArray.join("");
  hintText.innerText = randomObj.hint;
  correctWord = randomObj.word.toLowerCase();
  inputField.value = "";
  inputField.setAttribute("maxlength", correctWord.length);
  scoreAreaTeam1.innerHTML = scoreTeam1;
  scoreAreaTeam2.innerHTML = scoreTeam2;
  
  if (scoreTeam1 > 9 || scoreTeam2 > 9) {
    winGame();
  }
  initTimer();
}


const start = () => {
  if (Team1Names.childElementCount === 0 || Team2Names.childElementCount === 0) {
    modal.style.display = "block";
    modalContent.classList.add("modal-wrong");
    modalContent.classList.remove("modal-correct");
    return modalText.innerHTML = `<br>Please add at least one player to each team before starting the game.`;
  }
    contentBox.style.display = "block";
    startArea.style.display = "none";
    Team1Form.style.display = "none";
    Team2Form.style.display = "none";
    initGame();
}

const checkWord = () => {
  let userWord = inputField.value.toLowerCase();
  
  if (!userWord) {
    modal.style.display = "block";
    modalContent.classList.remove("modal-wrong");
    modalContent.classList.remove("modal-correct");
    return modalText.innerHTML = `<br>Please enter the word to check!`;
  }
  
  if (userWord!== correctWord) {
    modal.style.display = "block";
    modalContent.classList.remove("modal-correct");
    modalContent.classList.add("modal-wrong");
    return modalText.innerHTML = `<br>Oops! <b>${userWord}</b> is not a correct word`;
  } else {
    if (currentTeam === 1) {
      scoreTeam1++;
      scoreAreaTeam1.innerHTML = scoreTeam1;
    } else {
      scoreTeam2++;
      scoreAreaTeam2.innerHTML = scoreTeam2;
    }
    modal.style.display = "block";
    modalContent.classList.remove("modal-wrong");
    modalContent.classList.add("modal-correct");
    modalText.innerHTML = `<br>Congrats! <b>${correctWord.toUpperCase()}</b> is the correct word`;

  }
  initGame();
}

const endGame = () => {
  clearInterval(timer);
  modal.style.display = "block";
  modalContent.classList.remove("modal-correct");
  modalContent.classList.add("modal-wrong");
  if (scoreTeam1 > scoreTeam2) {
    modalText.innerHTML = `<br>Congrats Team 1! You WIN THE GAME!!!!!!</center><br>`;
  } else if (scoreTeam2 > scoreTeam1) {
    modalText.innerHTML = `<br>Congrats Team 2! You WIN THE GAME!!!!!!</center><br>`;
  } else {
    modalText.innerHTML = `<br>It's a tie! Both Teams have the same score.</center><br>`;
  }
  setTimeout(() => {
    window.location.href = "/play_now";
  }, 5000);
};

const winGame = () => {
    gameOver = true;
    clearInterval(timer);
    contentBox.style.display = "none";
    startArea.style.display = "block";
    modal.style.display = "block";
    modalContent.classList.add("modal-correct");
    if (scoreTeam1 >= 10) {
      modalText.innerHTML = `<br><center>Congrats Team 1! You WIN THE GAME !!!!!!</center><br>`;
    } else if (scoreTeam2 >= 10) {
      modalText.innerHTML = `<br><center>Congrats Team 2! You WIN THE GAME !!!!!!</center><br>`;
    }
  };

const resetGame = () => {
  gameOver = false;
  scoreTeam1 = 0;
  scoreTeam2 = 0;
  scoreAreaTeam1.innerHTML = scoreTeam1;
  scoreAreaTeam2.innerHTML = scoreTeam2;
  currentTeam = 1;
  timerStarted = false;
  initGame();
}
  
const gridSize = 8;
const grid = document.querySelector('.game-board');

for (let i = 1; i <= gridSize * gridSize; i++) {
  const cell = document.createElement('div');
  cell.classList.add('cell');
  cell.textContent = i;
  grid.appendChild(cell);
}

const cells = Array.from(document.querySelectorAll('.game-board .cell'));
cells.forEach((cell, index) => {
  const row = Math.floor(index / gridSize);
  const col = index % gridSize;
  cell.style.gridColumnStart = col + 1;
  cell.style.gridRowStart = row + 1;
});

refreshBtn.addEventListener("click", initGame);
checkBtn.addEventListener("click", checkWord);
// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
  modalDisplayed = false;
  if (!timerStarted) {
    initTimer();
    initGame();
    timerStarted = true;
  }
}
  
  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }

