document
  .getElementById("prediction-form")
  .addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent page reload

    // Collect form data
    const interaction_count =
      document.getElementById("interaction_count").value;
    const streak_count = document.getElementById("streak_count").value;
    const volatility_score = document.getElementById("volatility_score").value;

    // Send data to the Flask API
    fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        interaction_count: interaction_count,
        streak_count: streak_count,
        volatility_score: volatility_score,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          document.getElementById(
            "result"
          ).innerHTML = `<span style="color: red;">Error: ${data.error}</span>`;
        } else {
          document.getElementById(
            "result"
          ).innerHTML = `Predicted Coins: <strong>${data.predicted_coins.toFixed(
            2
          )}</strong>`;
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        document.getElementById(
          "result"
        ).innerHTML = `<span style="color: red;">An error occurred. Please try again.</span>`;
      });
  });
