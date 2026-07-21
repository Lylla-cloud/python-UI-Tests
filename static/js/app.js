document.addEventListener('DOMContentLoaded', () => {
    const testForm = document.getElementById('test-run-form');
    const startBtn = document.getElementById('start-test-btn');
    const btnText = startBtn.querySelector('.btn-text');

    const monitorSection = document.getElementById('monitor-section');
    const currentRunTarget = document.getElementById('current-run-target');
    const runStatusBadge = document.getElementById('run-status-badge');
    const progressBar = document.getElementById('progress-bar');
    const suiteCardsContainer = document.getElementById('suite-cards-container');
    const terminalBody = document.getElementById('terminal-body');
    const logCountSpan = document.getElementById('log-count');

    const historyTableBody = document.getElementById('history-table-body');
    const refreshHistoryBtn = document.getElementById('refresh-history-btn');

    const modal = document.getElementById('screenshot-modal');
    const modalImage = document.getElementById('modal-image');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const modalOverlay = document.getElementById('modal-overlay');

    let activePollInterval = null;
    let activeTestId = null;

    fetchHistory();

    testForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const targetUrl = document.getElementById('targetUrl').value;
        const browser = document.getElementById('browserSelect').value;
        const headless = document.getElementById('headlessToggle').value === 'true';
        const timeoutSeconds = parseInt(document.getElementById('timeoutSeconds').value, 10) || 10;

        const checkedSuites = Array.from(document.querySelectorAll('input[name="suites"]:checked'))
            .map(cb => cb.value);

        if (checkedSuites.length === 0) {
            alert('Please select at least one test suite to run!');
            return;
        }

        const payload = {
            targetUrl,
            browser,
            headless,
            timeoutSeconds,
            suites: checkedSuites
        };

        setButtonLoading(true);
        clearTerminal();

        try {
            const res = await fetch('/api/tests/run', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!res.ok) {
                throw new Error('Server returned HTTP ' + res.status);
            }

            const data = await res.json();
            activeTestId = data.id;

            monitorSection.classList.remove('hidden');
            currentRunTarget.textContent = `Target: ${data.targetUrl} [Python Selenium, ${data.browser.toUpperCase()}, Headless: ${data.headless}]`;
            updateStatusBadge(data.status);

            startPolling(activeTestId);
        } catch (err) {
            alert('Failed to start test execution: ' + err.message);
            setButtonLoading(false);
        }
    });

    refreshHistoryBtn.addEventListener('click', fetchHistory);

    closeModalBtn.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', closeModal);

    function startPolling(testId) {
        if (activePollInterval) clearInterval(activePollInterval);

        activePollInterval = setInterval(async () => {
            try {
                const res = await fetch(`/api/tests/${testId}`);
                if (!res.ok) return;

                const data = await res.json();
                renderTestProgress(data);

                if (data.status === 'COMPLETED' || data.status === 'COMPLETED_WITH_FAILURES' || data.status === 'FAILED') {
                    clearInterval(activePollInterval);
                    activePollInterval = null;
                    setButtonLoading(false);
                    fetchHistory();
                }
            } catch (err) {
                console.error('Polling error:', err);
            }
        }, 1000);
    }

    function renderTestProgress(data) {
        updateStatusBadge(data.status);

        let progress = 10;
        if (data.status === 'RUNNING') {
            const completedCount = (data.suiteResults || []).length;
            const total = data.totalSuites || 4;
            progress = Math.min(90, 10 + Math.round((completedCount / total) * 80));
        } else if (data.status.startsWith('COMPLETED') || data.status === 'FAILED') {
            progress = 100;
        }
        progressBar.style.width = `${progress}%`;

        suiteCardsContainer.innerHTML = '';
        (data.suiteResults || []).forEach(suite => {
            const card = document.createElement('div');
            card.className = `suite-card status-${suite.status}`;
            card.innerHTML = `
                <div class="suite-card-title">${escapeHtml(suite.suiteName)}</div>
                <div class="suite-card-summary">${escapeHtml(suite.summary || 'Executing...')} (${suite.durationMs || 0}ms)</div>
            `;
            suiteCardsContainer.appendChild(card);
        });

        terminalBody.innerHTML = '';
        let totalLogs = 0;

        (data.logs || []).forEach(log => {
            appendLogLine(log);
            totalLogs++;
        });

        logCountSpan.textContent = `${totalLogs} entries`;
        terminalBody.scrollTop = terminalBody.scrollHeight;
    }

    function appendLogLine(log) {
        const line = document.createElement('div');
        const levelClass = `log-${(log.level || 'info').toLowerCase()}`;
        line.className = `log-line ${levelClass}`;

        const suitePrefix = log.suite ? `[${log.suite}] ` : '';
        line.textContent = `[${log.timestamp}] [${log.level}] ${suitePrefix}${log.message}`;

        if (log.screenshotBase64) {
            const btn = document.createElement('button');
            btn.className = 'log-screenshot-btn';
            btn.textContent = '📷 View Screenshot';
            btn.addEventListener('click', () => showScreenshot(log.screenshotBase64));
            line.appendChild(btn);
        }

        terminalBody.appendChild(line);
    }

    async function fetchHistory() {
        try {
            const res = await fetch('/api/tests/history');
            if (!res.ok) return;

            const runs = await res.json();
            historyTableBody.innerHTML = '';

            if (!runs || runs.length === 0) {
                historyTableBody.innerHTML = '<tr><td colspan="7" class="text-center">No test runs executed yet.</td></tr>';
                return;
            }

            runs.forEach(run => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${escapeHtml(run.id)}</strong></td>
                    <td><a href="${escapeHtml(run.targetUrl)}" target="_blank" style="color: #60a5fa; text-decoration: none;">${escapeHtml(run.targetUrl)}</a></td>
                    <td>${escapeHtml(run.browser.toUpperCase())} ${run.headless ? '(Headless)' : ''}</td>
                    <td>${escapeHtml(run.startTime)}</td>
                    <td>${run.totalDurationMs ? run.totalDurationMs + 'ms' : '-'}</td>
                    <td><span class="badge badge-${(run.status || 'queued').toLowerCase()}">${escapeHtml(run.status)}</span></td>
                    <td>
                        ${run.finalScreenshotBase64 ? `<button class="btn btn-secondary btn-sm" onclick="showScreenshot('${run.finalScreenshotBase64}')">📷 Image</button>` : '-'}
                    </td>
                `;
                historyTableBody.appendChild(tr);
            });
        } catch (err) {
            console.error('Failed to fetch history:', err);
        }
    }

    window.showScreenshot = function(base64Data) {
        modalImage.src = `data:image/png;base64,${base64Data}`;
        modal.classList.remove('hidden');
    };

    function closeModal() {
        modal.classList.add('hidden');
        modalImage.src = '';
    }

    function clearTerminal() {
        terminalBody.innerHTML = '';
        logCountSpan.textContent = '0 entries';
        suiteCardsContainer.innerHTML = '';
        progressBar.style.width = '0%';
    }

    function updateStatusBadge(status) {
        runStatusBadge.textContent = status;
        runStatusBadge.className = `badge badge-${status.toLowerCase()}`;
    }

    function setButtonLoading(isLoading) {
        startBtn.disabled = isLoading;
        if (isLoading) {
            btnText.textContent = 'Running Automation...';
        } else {
            btnText.textContent = 'Execute Test Suite';
        }
    }

    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }
});
