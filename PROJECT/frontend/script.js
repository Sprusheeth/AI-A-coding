document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('resumeFile');
    const fileNameDisplay = document.getElementById('file-name');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const jobDescInput = document.getElementById('jobDesc');

    const inputSection = document.getElementById('input-section');
    const loadingSection = document.getElementById('loading-section');
    const errorSection = document.getElementById('error-section');
    const errorMessage = document.getElementById('error-message');
    const retryBtn = document.getElementById('retryBtn');
    const resultsSection = document.getElementById('results-section');

    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    const downloadBtn = document.getElementById('downloadBtn');

    let selectedFile = null;
    let analysisResult = null; // Store for downloading later

    // --- File Upload Logic ---
    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('dragover');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        if (file.type !== "application/pdf") {
            alert("Only PDF files are supported!");
            return;
        }
        selectedFile = file;
        fileNameDisplay.textContent = `📁 ${file.name}`;
        fileNameDisplay.classList.remove('hidden');
        analyzeBtn.disabled = false;
    }

    // --- API Interaction ---
    analyzeBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        // UI Reset
        inputSection.classList.add('hidden');
        errorSection.classList.add('hidden');
        resultsSection.classList.add('hidden');
        loadingSection.classList.remove('hidden');

        // Check if server is reachable
        if (window.location.protocol === 'file:') {
            alert("⚠️ WARNING: You are running this file directly from your system (file://) instead of the Web Server.\n\nPlease open your browser and go strictly to: http://127.0.0.1:5000");
            throw new Error("Cannot fetch from file:// due to Browser Security. Go to http://127.0.0.1:5000");
        }

        try {
            const formData = new FormData();
            formData.append('resume', selectedFile);
            if (jobDescInput.value.trim() !== '') {
                formData.append('job_desc', jobDescInput.value.trim());
            }

            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP Error ${response.status}`);
            }

            analysisResult = await response.json();
            
            // Build UI
            populateUI(analysisResult);
            
            loadingSection.classList.add('hidden');
            resultsSection.classList.remove('hidden');
            
        } catch (error) {
            console.error("Analysis failed:", error);
            loadingSection.classList.add('hidden');
            errorSection.classList.remove('hidden');
            errorMessage.textContent = error.message === 'Failed to fetch' 
                ? "Could not connect to the backend server. Is Python Flask running?" 
                : error.message;
            document.getElementById('setup-warning').style.display = 'block';
        }
    });

    retryBtn.addEventListener('click', () => {
        errorSection.classList.add('hidden');
        inputSection.classList.remove('hidden');
    });

    // --- Tab Switching Logic ---
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.add('hidden'));

            // Add active to clicked
            btn.classList.add('active');
            const targetId = btn.getAttribute('data-tab');
            document.getElementById(targetId).classList.remove('hidden');
        });
    });

    // --- UI Population Logic ---
    let chartInstance = null;

    function populateUI(data) {
        const { analysis, score, suggestions, resume_text } = data;

        // Score Card setup
        const scoreVal = score.score;
        document.getElementById('score-val').textContent = scoreVal;
        document.getElementById('score-explanation').textContent = score.explanation;
        
        const scoreCard = document.getElementById('score-card');
        scoreCard.className = 'card score-wrapper'; // reset
        if (scoreVal >= 75) scoreCard.classList.add('border-green');
        else if (scoreVal >= 50) scoreCard.classList.add('border-amber');
        else scoreCard.classList.add('border-red');

        // Render Chart
        renderChart(score.score_breakdown);

        // Skills
        const skillsContainer = document.getElementById('skills-container');
        skillsContainer.innerHTML = '';
        if (analysis.skills) {
            analysis.skills.forEach(s => {
                const span = document.createElement('span');
                span.className = 'skill-chip';
                span.textContent = s;
                skillsContainer.appendChild(span);
            });
        }

        // Lists (Education, Experience, Strengths, Weaknesses, Suggestions)
        populateList('education-list', analysis.education);
        populateList('experience-list', analysis.experience);
        populateList('strengths-list', analysis.strengths, '✨ ');
        populateList('weaknesses-list', analysis.weaknesses, '🎯 ');
        populateList('suggestions-list', suggestions.suggestions);

        // Missing Skills
        const missingContainerId = document.getElementById('missing-skills-container');
        const missingChips = document.getElementById('missing-chips');
        missingChips.innerHTML = '';
        if (suggestions.missing_skills && suggestions.missing_skills.length > 0) {
            missingContainerId.classList.remove('hidden');
            suggestions.missing_skills.forEach(s => {
                const span = document.createElement('span');
                span.className = 'skill-chip missing';
                span.textContent = s;
                missingChips.appendChild(span);
            });
        } else {
            missingContainerId.classList.add('hidden');
        }

        // Raw Text
        document.getElementById('raw-text').value = resume_text || "";
    }

    function populateList(elementId, items, prefix = '') {
        const ul = document.getElementById(elementId);
        ul.innerHTML = '';
        if (!items || items.length === 0) {
            ul.innerHTML = '<li>None</li>';
            return;
        }
        items.forEach(item => {
            const li = document.createElement('li');
            li.innerHTML = `<span>${prefix}${item}</span>`;
            ul.appendChild(li);
        });
    }

    function renderChart(breakdown) {
        const ctx = document.getElementById('scoreChart').getContext('2d');
        
        if (chartInstance) {
            chartInstance.destroy();
        }

        const labels = Object.keys(breakdown).map(k => k.charAt(0).toUpperCase() + k.slice(1));
        const data = Object.values(breakdown);
        
        // Colors corresponding to score thresholds relative to 25 mapping roughly
        const colors = data.map(v => v >= 18 ? '#10b981' : (v >= 12 ? '#f59e0b' : '#ef4444'));

        chartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Score Area (out of 25)',
                    data: data,
                    backgroundColor: colors,
                    borderRadius: 4,
                }]
            },
            options: {
                indexAxis: 'y', // Horizontal bar chart
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { max: 25, beginAtZero: true },
                    y: { grid: { display: false } }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // --- Download Report ---
    downloadBtn.addEventListener('click', () => {
        if (!analysisResult) return;
        const { analysis, score, suggestions } = analysisResult;
        
        const report = `AI RESUME ANALYSIS REPORT
==========================
File: ${selectedFile.name}
Overall Score: ${score.score}/100

SKILLS: ${analysis.skills ? analysis.skills.join(', ') : ''}

EDUCATION:
${analysis.education ? analysis.education.join('\n') : ''}

EXPERIENCE:
${analysis.experience ? analysis.experience.join('\n') : ''}

STRENGTHS:
${analysis.strengths ? analysis.strengths.map(s => '• ' + s).join('\n') : ''}

WEAKNESSES:
${analysis.weaknesses ? analysis.weaknesses.map(w => '• ' + w).join('\n') : ''}

SUGGESTIONS:
${suggestions.suggestions ? suggestions.suggestions.map((s, i) => `${i+1}. ${s}`).join('\n') : ''}

MISSING SKILLS: ${suggestions.missing_skills ? suggestions.missing_skills.join(', ') : ''}
`;

        const blob = new Blob([report], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `resume_analysis_report.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
});
