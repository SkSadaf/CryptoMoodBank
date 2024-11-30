let moods = [];
let rewards = [];
const daysInMonth = 30;

function generateRandomRewards() {
  return Math.floor(Math.random() * 16) + 5;
}

function addMood() {
  const moodSelect = document.getElementById("mood");
  const mood = moodSelect.value;
  if (moods.length < daysInMonth) {
    moods.push(mood);
  }

  if (moods.length % 7 === 0 || moods.length === daysInMonth) {
    updateStats();
  }
}

function updateStats() {
  const weeklyStatsDiv = document.getElementById("weeklyStats");
  const monthlyStatsDiv = document.getElementById("monthlyStats");
  const totalRewardsDiv = document.getElementById("totalRewards");

  weeklyStatsDiv.innerHTML = "";
  monthlyStatsDiv.innerHTML = "";
  totalRewardsDiv.innerHTML = "";

  let moodCounts = { happy: 0, sad: 0, neutral: 0 };
  let weeklyRewards = [];
  let totalRewards = 0;

  for (let i = 0; i < moods.length; i++) {
    moodCounts[moods[i]]++;

    if ((i + 1) % 7 === 0 || i + 1 === daysInMonth) {
      const weekNumber = Math.floor(i / 7) + 1;
      const happyDays = moodCounts.happy;
      const sadDays = moodCounts.sad;
      const neutralDays = moodCounts.neutral;
      const reward = generateRandomRewards();
      weeklyRewards.push(reward);

      weeklyStatsDiv.innerHTML += `<div>Week ${weekNumber} Stats:
                Happy Days: ${happyDays}, Sad Days: ${sadDays}, Neutral Days: ${neutralDays},
                Coin Reward: ${reward} coins</div>`;

      moodCounts = { happy: 0, sad: 0, neutral: 0 };
    }
  }

  const totalMoodCounts = moods.reduce((acc, mood) => {
    acc[mood] = (acc[mood] || 0) + 1;
    return acc;
  }, {});

  monthlyStatsDiv.innerHTML = `Happy Days: ${totalMoodCounts.happy || 0},
        Sad Days: ${totalMoodCounts.sad || 0},
        Neutral Days: ${totalMoodCounts.neutral || 0}`;

  totalRewards = weeklyRewards.reduce((acc, reward) => acc + reward, 0);
  totalRewardsDiv.innerHTML = `${totalRewards} coins`;
}
