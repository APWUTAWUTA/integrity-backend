document.getElementById("check").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  chrome.scripting.executeScript(
    {
      target: { tabId: tab.id },
      function: () => window.getSelection().toString()
    },
    async (selection) => {
      const text = selection[0].result;

      if (!text) {
        document.getElementById("result").innerText = "Please select some text.";
        return;
      }

      document.getElementById("result").innerText = "Analyzing...";

      try {
        const response = await fetch(
          "https://integrity-backend-el6n.onrender.com",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
          }
        );

        const data = await response.json();
        console.log("API response:", data);


        const color =
  data.confidence === "High" ? "green" :
  data.confidence === "Medium" ? "orange" :
  "red";

document.getElementById("result").innerHTML = `
  <strong>Score:</strong> ${data.score}<br>
  <strong style="color:${color}">
    Confidence: ${data.confidence}
  </strong><br>
  <em>${data.explanation}</em>
`;

      } catch (err) {
        document.getElementById("result").innerText = "Error contacting API.";
      }
    }
  );
});
