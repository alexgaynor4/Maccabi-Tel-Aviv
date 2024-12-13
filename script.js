let allplayers = []; // Declare the players variable outside the initializePage function
// Function to fetch the CSV data and parse it
async function fetchData() {
  const response = await fetch('players.csv');
  const csvData = await response.text();
  parseCSV(csvData);
}

// Function to parse the CSV data into an array of objects
function parseCSV(csvData) {
  const rows = csvData.split('\n');
  const headers = rows[0].split(',');
  for (let i = 1; i < rows.length; i++) {
    const row = rows[i].split(',');
    if (row.length === headers.length) {
      const player = {};
      for (let j = 0; j < row.length; j++) {
        player[headers[j]] = row[j];
        if (j == 1) {
           player['Date of Birth'] = calculateAge(row[j])
        }
      }
      player['Position'] = normalizePosition(player['Position']); // Normalize position
      allplayers.push(player);
    }
  }
}

// Helper function to normalize position data
function normalizePosition(position) {
  const posLower = position.toLowerCase();

  if (posLower.includes('wing spiker') || posLower.includes('wing-spiker')) {
    return 'Outside Hitter';
  } else if (posLower.includes('middle blocker') || posLower.includes('middle-blocker') || posLower.includes('Центральний блокуючий')) {
    return 'Middle Blocker';
  } else if (posLower.includes('setter')) {
    return 'Setter';
  } else if (posLower.includes('libero')) {
    return 'Libero';
  } else if (posLower.includes('opposite')) {
    return 'Opposite';
  } else if (posLower.includes('universal')) {
    return 'Universal';
  } else {
    return 'N/A'; // Just in case there are positions that we didn't consider
  }
}

// Function to get the link for a player
function getPlayerLink(player) {
  // This is just a placeholder function. You'll need to implement this based on your actual logic.
  if (player['volleybox'] && player['volleybox'].includes('https')) {
    return player['volleybox'];
  } else if (player['League Site\r'] && player['League Site\r'].includes('https')) {
    return player['League Site\r'];
  } else {
    return 'None'; // Or whatever you want the default to be
  }
}

function populateTable(players) {
  const tableBody = document.querySelector('#playerTable tbody');
  tableBody.innerHTML = '';

  players.forEach(player => {
    const row = document.createElement('tr');
    const playerLink = getPlayerLink(player); // Get the player link
    let nameCell;

    // Check if playerLink is not 'None'
    if (playerLink !== 'None') {
      nameCell = `<td><a href="${playerLink}" target="_blank">${player.Name}</a></td>`;
    } else {
      nameCell = `<td>${player.Name}</td>`;
    }

    row.innerHTML = `
      ${nameCell}
      <td>${player['Date of Birth']}</td>
      <td>${player.Height}</td>
      <td>${player.Nationality}</td>
      <td>${player.Position}</td>
      <td>${player['Points per Set']}</td>
      <td>${player['Aces per Set']}</td>
      <td>${player['Blocks per Set']}</td>
      <td>${player['Reception Percentage']}</td>
      <td>${player['Attack Percentage']}</td>
    `;
    tableBody.appendChild(row);
  });
}



// Function to filter the table based on player name
function filterByName(players, searchTerm) {
  return players.filter(player =>
    player.Name.toLowerCase().includes(searchTerm.toLowerCase())
  );
}

function getPointsPerSet(player) {
  if (player && player['Points per Set']) {
    const pointsPerSet = player['Points per Set'].split('(')[0];
    return parseFloat(pointsPerSet);
  }
  return NaN;
}

function getAcesPerSet(player) {
  if (player && player['Aces per Set']) {
    const acesPerSet = player['Aces per Set'].split('(')[0];
    return parseFloat(acesPerSet);
  }
  return NaN;
}

function getBlocksPerSet(player) {
  if (player && player['Blocks per Set']) {
    const blocksPerSet = player['Blocks per Set'].split('(')[0];
    return parseFloat(blocksPerSet);
  }
  return NaN;
}

function getReceptionPercentage(player) {
  if (player && player['Reception Percentage']) {
    const receptionPercentage = player['Reception Percentage'].replace('%', '');
    return parseFloat(receptionPercentage);
  }
  return NaN;
}

function getAttackPercentage(player) {
  if (player && player['Attack Percentage']) {
    const attackPercentage = player['Attack Percentage'].replace('%', '');
    return parseFloat(attackPercentage);
  }
  return NaN;
}

function calculateAge(dob) {
  const currentDate = new Date();
  const dobParts = dob.split('/');
  const dobDate = new Date(dobParts[2], dobParts[1] - 1, dobParts[0]);

  let age = currentDate.getFullYear() - dobDate.getFullYear();
  const monthDiff = currentDate.getMonth() - dobDate.getMonth();

  if (monthDiff < 0 || (monthDiff === 0 && currentDate.getDate() < dobDate.getDate())) {
    age--;
  }

  return age.toString();
}

function populatePositions() {
    const positionSelect = document.querySelector('#filterPosition');
    const positions = [...new Set(allplayers.map(player => player.Position))]; // Get unique positions
    positions.forEach(position => {
        const option = document.createElement('option');
        option.value = position;
        option.textContent = position;
        positionSelect.appendChild(option);
    });
}

function populateNationalities() {
    const nationalitySelect = document.querySelector('#filterNationality');
    const nationalities = [...new Set(allplayers.map(player => player.Nationality))]; // Get unique nationalities

    nationalities.forEach(nationality => {
        const option = document.createElement('option');
        option.value = nationality;
        option.textContent = nationality;
        nationalitySelect.appendChild(option);
    });
}

function handleFilterChange() {
  const filterNameInput = document.querySelector('#filterName');
  const filterAttackPercentageInput = document.querySelector('#filterAttackPercentage');
  const filterPointsPerSetInput = document.querySelector('#filterPointsPerSet');
  const filterAcesPerSetInput = document.querySelector('#filterAcesPerSet');
  const filterBlocksPerSetInput = document.querySelector('#filterBlocksPerSet');
  const filterReceptionPercentageInput = document.querySelector('#filterReceptionPercentage');
  const filterAgeInput = document.querySelector('#filterAge');
  const filterPositionSelect = document.querySelector('#filterPosition');
  const filterNationalitySelect = document.querySelector('#filterNationality');


  const name = filterNameInput.value.toLowerCase() || '';
  const attackPercentage = parseFloat(filterAttackPercentageInput.value) || 0;
  const pointsPerSet = parseFloat(filterPointsPerSetInput.value) || 0;
  const acesPerSet = parseFloat(filterAcesPerSetInput.value) || 0;
  const blocksPerSet = parseFloat(filterBlocksPerSetInput.value) || 0;
  const receptionPercentage = parseFloat(filterReceptionPercentageInput.value) || 0;
  const age = parseFloat(filterAgeInput.value) || Infinity;
  const selectedPositions = Array.from(filterPositionSelect.selectedOptions).map(option => option.value);
  const selectedNationalities = Array.from(filterNationalitySelect.selectedOptions).map(option => option.value);

  let filteredPlayers = allplayers.filter(player => {
    const playerAttackPercentage = getAttackPercentage(player);
    const playerPointsPerSet = getPointsPerSet(player);
    const playerAcesPerSet = getAcesPerSet(player);
    const playerBlocksPerSet = getBlocksPerSet(player);
    const playerReceptionPercentage = getReceptionPercentage(player);
    const playerAge = parseInt(player['Date of Birth']);

    return (
      player.Name.toLowerCase().includes(name) &&
      ((playerAttackPercentage >= attackPercentage) || (isNaN(playerAttackPercentage) && attackPercentage === 0)) &&
      ((playerPointsPerSet >= pointsPerSet) || (isNaN(playerPointsPerSet) && pointsPerSet == 0)) &&
      ((playerAcesPerSet >= acesPerSet) || (isNaN(playerAcesPerSet) && acesPerSet == 0)) &&
      ((playerBlocksPerSet >= blocksPerSet) || (isNaN(playerBlocksPerSet) && blocksPerSet == 0)) &&
      ((playerReceptionPercentage >= receptionPercentage) || (isNaN(playerReceptionPercentage) && receptionPercentage === 0)) &&
      playerAge <= age &&
      (selectedPositions.length === 0 || selectedPositions.includes(player.Position)) &&
      (selectedNationalities.length === 0 || selectedNationalities.includes(player.Nationality))
    );
  });
  return filteredPlayers
}


function getProperty(player, property) {
  switch (property) {
    case 'name':
      return player.Name || 'N/A';
    case 'age':
      return player['Date of Birth'] || 'N/A';
    case 'pointsPerSet':
      return getPointsPerSet(player).toFixed(2) || 'N/A';
    case 'acesPerSet':
      return getAcesPerSet(player).toFixed(2) || 'N/A';
    case 'blocksPerSet':
      return getBlocksPerSet(player).toFixed(2) || 'N/A';
    case 'receptionPercentage':
      return getReceptionPercentage(player).toFixed(2) || 'N/A';
    case 'attackPercentage':
      return getAttackPercentage(player).toFixed(2) || 'N/A';
    default:
      return 'N/A';
  }
}

function sortByProperty(players, property, sortOrder) {
  return players.sort((a, b) => {
    const valueA = getProperty(a, property);
    const valueB = getProperty(b, property);

    if (valueA === 'NaN') return 1; // Move 'N/A' values to the bottom
    if (valueB === 'NaN') return -1; // Move 'N/A' values to the bottom

    let comparison = 0;
    if (valueA > valueB) {
      comparison = 1;
    } else if (valueA < valueB) {
      comparison = -1;
    }

    // Reverse the comparison if sortOrder is 'desc'
    if (sortOrder === 'desc') {
      comparison *= -1;
    }

    return comparison;
  });
}

function handleSortChange() {
  const sortSelect = document.querySelector('#sortOption');
  const sortOrderIncrease = document.querySelector('#sortOrderIncrease');
  const sortOrder = sortOrderIncrease.checked ? 'asc' : 'desc';
  const selectedOption = sortSelect.value;

  let filteredPlayers = handleFilterChange(); // First, filter the players.

  // Then, sort the filtered players.
  const sortedPlayers = sortByProperty(filteredPlayers, selectedOption, sortOrder);
  populateTable(sortedPlayers); // Finally, populate the table with the sorted, filtered players.
}

// Main function to initialize the page
async function initializePage() {
  await fetchData();
  populateTable(allplayers);
  populatePositions();
  populateNationalities();

  const filterInputs = document.querySelectorAll('#filterName, #filterAttackPercentage, #filterPointsPerSet, #filterAcesPerSet, #filterBlocksPerSet, #filterReceptionPercentage, #filterAge');
  filterInputs.forEach(input => input.addEventListener('input', handleSortChange));

  const filterPositionSelect = document.querySelector('#filterPosition')
  filterPositionSelect.addEventListener('change', handleSortChange);

  const filterNationalitySelect = document.querySelector('#filterNationality');
  filterNationalitySelect.addEventListener('change', handleSortChange);

  const sortSelect = document.querySelector('#sortOption');
  sortSelect.addEventListener('change', handleSortChange);

  const sortOrderIncrease = document.querySelector('#sortOrderIncrease');
  sortOrderIncrease.addEventListener('change', handleSortChange);

  const sortOrderDecrease = document.querySelector('#sortOrderDecrease');
  sortOrderDecrease.addEventListener('change', handleSortChange);
}


// Call the main initialization function
initializePage();