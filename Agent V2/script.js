// Vlaamse Codex Agent - Frontend JavaScript

class VlaamseCodexAgentUI {
    constructor() {
        this.isAnalysisRunning = false;
        this.logCount = 1;
        this.startTime = null;
        this.logPollingInterval = null;
        this.lastLogIndex = 0;
        this.isPaused = false;
        
        // DOM Elements
        this.elements = {
            startBtn: document.getElementById('startAnalysis'),
            reopenLogsBtn: document.getElementById('reopenLogs'),
            closeModalBtn: document.getElementById('closeModal'),
            clearLogsBtn: document.getElementById('clearLogs'),
            downloadLogsBtn: document.getElementById('downloadLogs'),
            pausePlayBtn: document.getElementById('pausePlayBtn'),
            pauseStatus: document.getElementById('pauseStatus'),
            logModal: document.getElementById('logModal'),
            loadingOverlay: document.getElementById('loadingOverlay'),
            logContent: document.getElementById('logContent'),
            logCountDisplay: document.getElementById('logCount')
        };
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        console.log('🦁 Vlaamse Codex Agent UI geïnitialiseerd');
    }
    
    bindEvents() {
        // Button events
        this.elements.startBtn.addEventListener('click', () => this.startAnalysis());
        this.elements.reopenLogsBtn.addEventListener('click', () => this.reopenLogs());
        this.elements.closeModalBtn.addEventListener('click', () => this.closeModal());
        this.elements.clearLogsBtn.addEventListener('click', () => this.clearLogs());
        this.elements.downloadLogsBtn.addEventListener('click', () => this.downloadLogs());
        this.elements.pausePlayBtn.addEventListener('click', () => this.togglePause());
        
        // Modal events
        this.elements.logModal.addEventListener('click', (e) => {
            if (e.target === this.elements.logModal) {
                this.closeModal();
            }
        });
        
        // Keyboard events
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.elements.logModal.classList.contains('show')) {
                this.closeModal();
            }
        });
    }
    
    async startAnalysis() {
        if (this.isAnalysisRunning) return;
        
        this.isAnalysisRunning = true;
        this.startTime = new Date();
        this.lastLogIndex = 0;
        
        // Update UI
        this.elements.startBtn.disabled = true;
        
        // Show loading overlay briefly
        this.showLoadingOverlay();
        
        try {
            // Start the real Python agent via Flask API
            const response = await fetch('/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const result = await response.json();
            
            if (response.ok && result.status === 'success') {
                this.hideLoadingOverlay();
                this.showModal();
                this.startLogPolling();
            } else {
                throw new Error(result.message || 'Failed to start analysis');
            }
        } catch (error) {
            console.error('Error starting analysis:', error);
            this.hideLoadingOverlay();
            this.addLogEntry('error', `❌ Fout bij starten analyse: ${error.message}`);
            this.elements.startBtn.disabled = false;
            this.isAnalysisRunning = false;
        }
    }
    
    startLogPolling() {
        // Poll for logs every 500ms
        this.logPollingInterval = setInterval(async () => {
            // Skip polling if paused
            if (this.isPaused) {
                return;
            }
            
            try {
                const response = await fetch('/logs');
                const data = await response.json();
                
                // Add new logs
                if (data.logs && data.logs.length > this.lastLogIndex) {
                    const newLogs = data.logs.slice(this.lastLogIndex);
                    newLogs.forEach(log => {
                        this.addLogEntry('info', log);
                    });
                    this.lastLogIndex = data.logs.length;
                }
                
                // Check if analysis is complete
                if (!data.running && this.isAnalysisRunning) {
                    this.completeAnalysis();
                }
                
            } catch (error) {
                console.error('Error polling logs:', error);
                this.addLogEntry('error', '❌ Verbinding met agent verloren');
                this.completeAnalysis();
            }
        }, 500);
    }
    

    
    showModal() {
        this.elements.logModal.classList.add('show');
        document.body.style.overflow = 'hidden';
        
        // Show the reopen logs button for future use
        this.elements.reopenLogsBtn.style.display = 'inline-flex';
        
        // Setup scroll behavior - only allow scrolling down
        this.setupScrollBehavior();
    }
    
    setupScrollBehavior() {
        const logContent = this.elements.logContent;
        let isAtBottom = true;
        
        // Track if user is at bottom
        logContent.addEventListener('scroll', () => {
            const threshold = 5; // Small threshold for floating point precision
            isAtBottom = logContent.scrollTop >= (logContent.scrollHeight - logContent.clientHeight - threshold);
        });
        
        // Prevent scrolling up when new content is added
        const observer = new MutationObserver(() => {
            if (isAtBottom) {
                this.scrollToBottom();
            }
        });
        
        observer.observe(logContent, {
            childList: true,
            subtree: true
        });
        
        // Store observer for cleanup
        this.scrollObserver = observer;
    }
    
    reopenLogs() {
        this.showModal();
    }
    
    closeModal() {
        this.elements.logModal.classList.remove('show');
        document.body.style.overflow = '';
        
        // Stop log polling
        if (this.logPollingInterval) {
            clearInterval(this.logPollingInterval);
            this.logPollingInterval = null;
        }
        
        // Cleanup scroll observer
        if (this.scrollObserver) {
            this.scrollObserver.disconnect();
            this.scrollObserver = null;
        }
        
        // Reset UI
        this.elements.startBtn.disabled = false;
        this.isAnalysisRunning = false;
        this.isPaused = false;
        this.updatePauseUI();
    }
    
    showLoadingOverlay() {
        this.elements.loadingOverlay.classList.add('show');
    }
    
    hideLoadingOverlay() {
        this.elements.loadingOverlay.classList.remove('show');
    }
    
    completeAnalysis() {
        this.isAnalysisRunning = false;
        
        // Stop log polling
        if (this.logPollingInterval) {
            clearInterval(this.logPollingInterval);
            this.logPollingInterval = null;
        }
        
        // Reset pause state
        this.isPaused = false;
        this.updatePauseUI();
        
        // Update UI
        this.elements.startBtn.disabled = false;
    }
    
    togglePause() {
        this.isPaused = !this.isPaused;
        this.updatePauseUI();
        
        if (this.isPaused) {
            this.addLogEntry('warning', '⏸️ Log updates gepauzeerd - klik op play om te hervatten');
        } else {
            this.addLogEntry('info', '▶️ Log updates hervat');
        }
    }
    
    updatePauseUI() {
        const pauseBtn = this.elements.pausePlayBtn;
        const pauseStatus = this.elements.pauseStatus;
        
        if (this.isPaused) {
            pauseBtn.innerHTML = '<span class="btn-icon">▶️</span>';
            pauseBtn.classList.add('paused');
            pauseBtn.title = 'Hervat log updates';
            pauseStatus.style.display = 'inline';
        } else {
            pauseBtn.innerHTML = '<span class="btn-icon">⏸️</span>';
            pauseBtn.classList.remove('paused');
            pauseBtn.title = 'Pauze log updates';
            pauseStatus.style.display = 'none';
        }
    }
    
    addLogEntry(type, message) {
        const timestamp = this.getTimestamp();
        const logEntry = document.createElement('div');
        
        // Clean up the message (remove timestamp if it's already there)
        let cleanMessage = message;
        if (message.match(/^\[\d{2}:\d{2}:\d{2}\]/)) {
            cleanMessage = message.replace(/^\[\d{2}:\d{2}:\d{2}\]\s*/, '');
        }
        
        // Detect log type based on content
        let logType = type;
        if (cleanMessage.includes('📋 Agent stap')) {
            logType = 'step';
        } else if (cleanMessage.includes('🧠 Codex agent denkt:') || cleanMessage.includes('🧠 ')) {
            logType = 'thinking';
        } else if (cleanMessage.includes('🛠️ codex agent kiest tools:') || cleanMessage.includes('→ ')) {
            logType = 'tool-selection';
        } else if (cleanMessage.includes('✅') && cleanMessage.includes('completed')) {
            logType = 'success';
        } else if (cleanMessage.includes('❌')) {
            logType = 'error';
        } else if (cleanMessage.includes('🚀')) {
            logType = 'start';
        } else if (cleanMessage.includes('📄')) {
            logType = 'document';
        }
        
        logEntry.className = `log-entry ${logType}`;
        
        // Render markdown in the message
        let renderedMessage = cleanMessage;
        if (typeof marked !== 'undefined') {
            try {
                // Configure marked for inline rendering and security
                marked.setOptions({
                    breaks: true,
                    gfm: true,
                    sanitize: false,
                    smartLists: true,
                    smartypants: true
                });
                
                // Check if message contains markdown syntax
                if (this.containsMarkdown(cleanMessage)) {
                    // Use full markdown parsing for block elements like headers
                    renderedMessage = marked.parse(cleanMessage);
                    // Remove wrapping <p> tags if present
                    renderedMessage = renderedMessage.replace(/^<p>|<\/p>$/g, '');
                }
            } catch (error) {
                console.warn('Markdown rendering failed:', error);
                renderedMessage = cleanMessage;
            }
        }
        
        logEntry.innerHTML = `
            <span class="log-timestamp">[${timestamp}]</span>
            <span class="log-message">${renderedMessage}</span>
        `;
        
        this.elements.logContent.appendChild(logEntry);
        
        // Auto scroll to bottom and prevent scrolling up
        this.scrollToBottom();
        
        // Update log count
        this.logCount++;
        this.updateLogCount();
    }
    
    scrollToBottom() {
        this.elements.logContent.scrollTop = this.elements.logContent.scrollHeight;
    }
    
    containsMarkdown(text) {
        // Check for common markdown patterns
        const markdownPatterns = [
            /\*\*.*?\*\*/,  // Bold
            /\*.*?\*/,      // Italic
            /`.*?`/,        // Code
            /\[.*?\]\(.*?\)/, // Links
            /^#{1,6}\s/m,   // Headers
            /^\s*[-*+]\s/m, // Lists
            /^\s*\d+\.\s/m, // Numbered lists
            /```[\s\S]*?```/, // Code blocks
            /~~.*?~~/       // Strikethrough
        ];
        
        return markdownPatterns.some(pattern => pattern.test(text));
    }
    
    clearLogs() {
        // Keep only the initial startup log
        this.elements.logContent.innerHTML = `
            <div class="log-entry startup">
                <span class="log-timestamp">[00:00:00]</span>
                <span class="log-message">🦁 Vlaamse Codex Agent wordt geïnitialiseerd...</span>
            </div>
        `;
        
        this.logCount = 1;
        this.lastLogIndex = 0;
        this.updateLogCount();
    }
    
    downloadLogs() {
        const logs = Array.from(this.elements.logContent.children).map(entry => {
            const timestamp = entry.querySelector('.log-timestamp').textContent;
            const message = entry.querySelector('.log-message').textContent;
            return `${timestamp} ${message}`;
        }).join('\n');
        
        const blob = new Blob([logs], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `vlaamse-codex-agent-logs-${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    

    
    updateLogCount() {
        const text = this.logCount === 1 ? '1 log entry' : `${this.logCount} log entries`;
        this.elements.logCountDisplay.textContent = text;
    }
    
    getTimestamp() {
        if (!this.startTime) return '00:00:00';
        
        const now = new Date();
        const diff = Math.floor((now - this.startTime) / 1000);
        
        const hours = Math.floor(diff / 3600).toString().padStart(2, '0');
        const minutes = Math.floor((diff % 3600) / 60).toString().padStart(2, '0');
        const seconds = (diff % 60).toString().padStart(2, '0');
        
        return `${hours}:${minutes}:${seconds}`;
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.vlaamseCodexAgent = new VlaamseCodexAgentUI();
});

// API utility functions for backend integration
window.VlaamseCodexAPI = {
    async startAnalysis() {
        const response = await fetch('/start', { method: 'POST' });
        return response.json();
    },
    
    async getStatus() {
        const response = await fetch('/status');
        return response.json();
    },
    
    async getLogs() {
        const response = await fetch('/logs');
        return response.json();
    },
    
    async getAnalysis() {
        const response = await fetch('/analysis');
        return response.json();
    }
};
