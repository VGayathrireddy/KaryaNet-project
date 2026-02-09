// URL of your backend
const API_URL = "http://127.0.0.1:8000/workers"; // change if your FastAPI runs on a different host/port

async function fetchWorkers() {
  try {
    const response = await fetch(API_URL);
    const workers = await response.json();
    displayWorkers(workers);
  } catch (err) {
    console.error("Error fetching workers:", err);
  }
}

function displayWorkers(workers) {
  const container = document.getElementById("service-container");
  container.innerHTML = ""; // clear existing content

  workers.forEach(worker => {
    const card = document.createElement("div");
    card.classList.add("service-card");

    card.innerHTML = `
      <h3>${worker.name}</h3>
      <p>${worker.description}</p>
      <p><strong>Category:</strong> ${worker.category}</p>
      <p><strong>Rating:</strong> ${worker.rating}</p>
      <p><strong>Available:</strong> ${worker.available ? "Yes" : "No"}</p>
    `;

    container.appendChild(card);
  });

  // re-run your IntersectionObserver animation logic
  const cards = document.querySelectorAll('.service-card');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animation = 'fadeUp 0.8s ease forwards';
      }
    });
  }, { threshold: 0.1 });

  cards.forEach(card => observer.observe(card));
}

// Call fetchWorkers when page loads
fetchWorkers();
