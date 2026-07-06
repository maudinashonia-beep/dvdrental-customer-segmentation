document.addEventListener("DOMContentLoaded", function () {
    const statusBox = document.getElementById("statusBox");
    const predictionChart = document.getElementById("predictionChart");

    const inputData = {
        store_id: 1,
        active: 1,
        total_payment: 150,
        payment_count: 3,
        average_payment: 50
    };

    fetch('/predict-customer/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(inputData)
    })
    .then(response => response.json())
    .then(data => {

        if (data.prediction !== undefined) {
            statusBox.textContent = `Prediction: ${data.prediction}`;

            // 🔥 AMBIL PROBABILITY (HARUS ADA DARI BACKEND)
            const probabilities = data.probability || [0.5, 0.5];

            // 🔥 BUAT CHART
            new Chart(predictionChart, {
                type: 'bar',
                data: {
                    labels: ['Class 0', 'Class 1'],
                    datasets: [{
                        label: 'Prediction Probability',
                        data: probabilities,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

        } else {
            statusBox.textContent = 'Error: Could not fetch prediction.';
        }
    })
    .catch(error => {
        statusBox.textContent = 'Error: ' + error.message;
    });
});