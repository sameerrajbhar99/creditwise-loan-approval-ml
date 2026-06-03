document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loan-form');
    const steps = Array.from(document.querySelectorAll('.form-step'));
    const stepIndicators = Array.from(document.querySelectorAll('.step'));
    const progressBar = document.getElementById('progress-bar');
    
    let currentStep = 0;

    // Navigation Buttons
    document.querySelectorAll('.next-btn').forEach(button => {
        button.addEventListener('click', () => {
            if (validateStep(currentStep)) {
                currentStep++;
                updateUI();
            }
        });
    });

    document.querySelectorAll('.prev-btn').forEach(button => {
        button.addEventListener('click', () => {
            currentStep--;
            updateUI();
        });
    });

    function validateStep(index) {
        const currentFormStep = steps[index];
        const inputs = currentFormStep.querySelectorAll('input[required], select[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.checkValidity()) {
                input.reportValidity();
                isValid = false;
            }
        });
        
        return isValid;
    }

    function updateUI() {
        // Update Steps
        steps.forEach((step, index) => {
            step.classList.toggle('active', index === currentStep);
        });

        // Update Indicators
        stepIndicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === currentStep);
            indicator.classList.toggle('completed', index < currentStep);
        });

        // Update Progress Bar
        const progress = (currentStep / (steps.length - 1)) * 100;
        progressBar.style.width = `${progress}%`;
    }

    // Form Submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!validateStep(currentStep)) return;

        const submitBtn = document.querySelector('.submit-btn');
        const submitText = document.querySelector('.submit-text');
        const loader = document.querySelector('.loader');

        // Loading state
        submitBtn.disabled = true;
        submitText.classList.add('hidden');
        loader.classList.remove('hidden');

        // Gather Data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                showResult(result);
            } else {
                alert('Error processing request: ' + (result.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to connect to the server.');
        } finally {
            submitBtn.disabled = false;
            submitText.classList.remove('hidden');
            loader.classList.add('hidden');
        }
    });

    function showResult(result) {
        document.getElementById('form-card').classList.add('hidden');
        const resultCard = document.getElementById('result-card');
        resultCard.classList.remove('hidden');

        const probPercent = (result.probability * 100).toFixed(1);
        const percentageText = document.getElementById('prob-percentage');
        const gaugeFill = document.getElementById('gauge-fill');
        
        const banner = document.getElementById('status-banner');
        const icon = document.getElementById('status-icon');
        const decisionText = document.getElementById('decision-text');
        const decisionSubtext = document.getElementById('decision-subtext');

        // Animate numbers
        let currentProb = 0;
        const targetProb = parseFloat(probPercent);
        const duration = 1500;
        const interval = 20;
        const steps = duration / interval;
        const increment = targetProb / steps;

        const counter = setInterval(() => {
            currentProb += increment;
            if (currentProb >= targetProb) {
                currentProb = targetProb;
                clearInterval(counter);
            }
            percentageText.textContent = `${currentProb.toFixed(1)}%`;
        }, interval);

        // Animate gauge
        // Total dash array is ~125.6 (Pi * radius(40) = 125.6)
        const circumference = 125.6;
        const offset = circumference - (result.probability * circumference);
        
        // Slight delay for smooth animation trigger
        setTimeout(() => {
            gaugeFill.style.strokeDashoffset = offset;
            
            // Color mapping based on probability
            if (result.probability > 0.7) {
                gaugeFill.style.stroke = 'var(--success)';
                percentageText.style.color = 'var(--success)';
            } else if (result.probability > 0.4) {
                gaugeFill.style.stroke = '#f59e0b'; // warning/yellow
                percentageText.style.color = '#f59e0b';
            } else {
                gaugeFill.style.stroke = 'var(--error)';
                percentageText.style.color = 'var(--error)';
            }
        }, 100);

        // Update Text
        if (result.approved) {
            banner.classList.remove('rejected');
            icon.textContent = '✓';
            decisionText.textContent = 'Loan Approved';
            decisionSubtext.textContent = 'Congratulations! Your profile meets our criteria for this loan.';
        } else {
            banner.classList.add('rejected');
            icon.textContent = '✗';
            decisionText.textContent = 'Loan Declined';
            decisionSubtext.textContent = 'Unfortunately, we cannot approve this loan at this time based on your profile.';
        }
    }

    // Reset Flow
    document.getElementById('reset-btn').addEventListener('click', () => {
        document.getElementById('result-card').classList.add('hidden');
        document.getElementById('form-card').classList.remove('hidden');
        
        form.reset();
        currentStep = 0;
        updateUI();
        
        // Reset gauge
        document.getElementById('gauge-fill').style.strokeDashoffset = '125.6';
        document.getElementById('gauge-fill').style.stroke = 'var(--primary)';
        document.getElementById('prob-percentage').style.color = 'var(--text-main)';
        document.getElementById('prob-percentage').textContent = '0%';
    });
});
