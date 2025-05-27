from flask import Flask, jsonify, send_from_directory
import threading
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the correct agent from Agent V2. 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Agent V2'))
from vlaamsecodexagent import VlaamseCodexAgent

app = Flask(__name__)

# Global state
state = {
    'running': False,
    'logs': [],
    'results': {}
}

class LogCapture:
    def __init__(self):
        self.original_stdout = sys.stdout
        
    def write(self, text):
        if text.strip():
            state['logs'].append(text.strip())
        self.original_stdout.write(text)
        
    def flush(self):
        self.original_stdout.flush()

log_capture = LogCapture()

@app.route('/')
def index():
    return send_from_directory('Agent V2', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('Agent V2', filename)

@app.route('/start', methods=['POST'])
def start_analysis():
    if state['running']:
        return jsonify({'status': 'error', 'message': 'Already running'}), 400
    
    state['running'] = True
    state['logs'].clear()
    state['results'].clear()
    
    def run_agent():
        try:
            sys.stdout = log_capture
      
            
            agent = VlaamseCodexAgent()
            agent.voer_uit()
            
            state['results'] = {
                'completed_at': datetime.now().isoformat(),
                'status': 'success'
            }

            
        except Exception as e:
            print(f"❌ Error: {e}")
            state['results'] = {'error': str(e)}
        finally:
            state['running'] = False
            sys.stdout = log_capture.original_stdout
    
    threading.Thread(target=run_agent, daemon=True).start()
    return jsonify({'status': 'success'})

@app.route('/logs')
def get_logs():
    return jsonify({
        'logs': state['logs'],
        'running': state['running'],
        'count': len(state['logs'])
    })

@app.route('/status')
def get_status():
    return jsonify({
        'running': state['running'],
        'log_count': len(state['logs']),
        'has_results': bool(state['results'])
    })

@app.route('/analysis')
def get_analysis():
    if not state['results']:
        return jsonify({'status': 'no_results'}), 404
    return jsonify({'status': 'success', 'results': state['results']})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000) 