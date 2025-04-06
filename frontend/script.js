document.addEventListener('DOMContentLoaded', function() {
    // Simple form animation
    const inputs = document.querySelectorAll('.form-control');
    
    inputs.forEach(input => {
      input.addEventListener('focus', function() {
        this.parentElement.style.transform = 'translateX(5px)';
      });
      
      input.addEventListener('blur', function() {
        this.parentElement.style.transform = 'translateX(0)';
      });
    });
    
    // Form submission and prediction logic
    document.getElementById("hypeForm").addEventListener("submit", async function (e) {
      e.preventDefault();
    
      const data = {
        retail_price: parseFloat(document.getElementById("retailPrice").value),
        sale_price: parseFloat(document.getElementById("salePrice").value),
        release_year: parseInt(document.getElementById("releaseYear").value),
        brand: document.getElementById("brand").value.trim(),
        model: document.getElementById("model").value.trim(),
        edition: document.getElementById("edition").value.trim()
      };
    
      // Create or get result div
      let resultDiv = document.getElementById("result");
      if (!resultDiv) {
        resultDiv = document.createElement("div");
        resultDiv.id = "result";
        resultDiv.className = "result-message";
        document.getElementById("hypeForm").after(resultDiv);
      }
      
      resultDiv.textContent = "Predicting...";
      resultDiv.className = "result-message loading";
    
      try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });
    
        const result = await response.json();
    
        if (response.ok) {
          if (result.prediction === 1) {
            resultDiv.textContent = "🔥 Hyped Sneaker!";
            resultDiv.className = "result-message success";
          } else {
            resultDiv.textContent = "❌ Not Hyped.";
            resultDiv.className = "result-message error";
          }
        } else {
          resultDiv.textContent = `Error: ${result.detail}`;
          resultDiv.className = "result-message error";
        }
      } catch (err) {
        resultDiv.textContent = "Server error. Please make sure the backend is running.";
        resultDiv.className = "result-message error";
        console.error(err);
      }
    });
  });