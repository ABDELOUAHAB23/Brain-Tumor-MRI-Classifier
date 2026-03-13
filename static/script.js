document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const imageInput = document.getElementById('image-input');
    const imagePreview = document.getElementById('image-preview');
    const previewSection = document.querySelector('.preview-section');
    const resultSection = document.getElementById('result-section');
    const resultText = document.getElementById('result-text');
    const loadingSection = document.getElementById('loading-section');
    
    let resultChart = null;

    // Show image preview when file is selected
    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                previewSection.classList.remove('d-none');
            };
            reader.readAsDataURL(file);
        }
    });

    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const file = imageInput.files[0];
        if (!file) {
            alert('Please select an image first');
            return;
        }

        // Show loading state
        loadingSection.classList.remove('d-none');
        resultSection.classList.add('d-none');

        // Create form data
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            // Update result text
            resultText.textContent = data.result;

            // Prepare chart data
            const chartData = {
                labels: Object.keys(data.probabilities),
                datasets: [{
                    data: Object.values(data.probabilities),
                    backgroundColor: [
                        '#36A2EB',  // No Tumor
                        '#FF6384',  // Glioma
                        '#FFCE56',  // Meningioma
                        '#4BC0C0'   // Pituitary
                    ],
                    borderWidth: 1
                }]
            };

            // Destroy existing chart if it exists
            if (resultChart) {
                resultChart.destroy();
            }

            // Create new chart
            const ctx = document.getElementById('resultChart').getContext('2d');
            resultChart = new Chart(ctx, {
                type: 'doughnut',
                data: chartData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.raw.toFixed(2);
                                    return `${label}: ${value}%`;
                                }
                            }
                        }
                    }
                }
            });

            // Show result section
            resultSection.classList.remove('d-none');
        } catch (error) {
            alert('Error analyzing image: ' + error.message);
        } finally {
            // Hide loading state
            loadingSection.classList.add('d-none');
        }
    });
});
