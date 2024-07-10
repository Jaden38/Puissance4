// Les 2 joueurs
const PLAYER1 = "red";
const PLAYER2 = "yellow";

// Fonction qui crée le tableau de jeu
function createBoard(board) {
  // Injecte la feuille de style dans le head
  const linkElement = document.createElement("link");
  linkElement.href = import.meta.url.replace(".js", ".css");
  linkElement.rel = "stylesheet";
  document.head.append(linkElement);
  // Injecte le tableau de jeu sous formes de div
  for (let column = 0; column < 7; column++) {
    const columnElement = document.createElement("div");
    columnElement.className = "column";
    columnElement.dataset.column = column;
    for (let row = 0; row < 6; row++) {
      const cellElement = document.createElement("div");
      cellElement.className = "cell empty";
      cellElement.dataset.column = column;
      columnElement.append(cellElement);
    }
    board.append(columnElement);
  }
}

// Fonction qui effectue le coup d'un joueur
function playMove(board, player, column, row) {
  // On verifie la validité du parametre player.
  if (player !== PLAYER1 && player !== PLAYER2) {
    throw new Error(`player must be ${PLAYER1} or ${PLAYER2}.`);
  }
  // on pointe sur la colonne choisie
  const columnElement = board.querySelectorAll(".column")[column];
  if (columnElement === undefined) {
    throw new RangeError("column must be between 0 and 6.");
  }
  // on pointe sur la ligne choisie
  const cellElement = columnElement.querySelectorAll(".cell")[row];
  if (cellElement === undefined) {
    throw new RangeError("row must be between 0 and 5.");
  }
  // On place le pion
  if (!cellElement.classList.replace("empty", player)) {
    throw new Error("cell must be empty.");
  }
}

// Met les constantes & les fonctions à disposition de la page
export { PLAYER1, PLAYER2, createBoard, playMove };
