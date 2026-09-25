#!/usr/bin/env python3
"""
Circle City Model - Web Application
===================================

A Flask-based web interface for the Circle City AGI Framework.
Provides REST API and web UI for interacting with the AGI system.
"""

from flask import Flask, request, jsonify, render_template_string
import time
import threading
from circle_city_model import CircleCityAGI, create_robot_agi

app = Flask(__name__)

# Initialize AGI systems
print("Initializing Circle City AGI...")
general_agi = CircleCityAGI()
robot_agi = create_robot_agi()
print("AGI systems initialized successfully!")

# Global state
app_state = {
    'last_activity': time.time(),
    'request_count': 0,
    'initialization_time': time.time(),
}


# =============================================================================
# HTML TEMPLATES
# =============================================================================

MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Circle City Model - AGI Interface</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #06b6d4 0%, #2563eb 100%);
            border-radius: 16px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(6, 182, 212, 0.3);
        }
        
        header h1 {
            font-size: 2.5em;
            color: white;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        header p {
            color: rgba(255,255,255,0.9);
            font-size: 1.1em;
        }
        
        .stats-bar {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            margin-bottom: 30px;
            justify-content: center;
        }
        
        .stat-card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            padding: 15px 25px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }
        
        .stat-card .label {
            font-size: 0.85em;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }
        
        .stat-card .value {
            font-size: 1.5em;
            font-weight: bold;
            color: #06b6d4;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .tab {
            padding: 12px 24px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            color: #cbd5e1;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .tab:hover {
            background: rgba(6, 182, 212, 0.2);
            border-color: #06b6d4;
        }
        
        .tab.active {
            background: linear-gradient(135deg, #06b6d4 0%, #2563eb 100%);
            color: white;
            border-color: transparent;
            box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4);
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .panel {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
        }
        
        .panel-title {
            font-size: 1.3em;
            color: #f8fafc;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #94a3b8;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .form-group input,
        .form-group textarea,
        .form-group select {
            width: 100%;
            padding: 12px 16px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            color: #e0e0e0;
            font-size: 1em;
            transition: all 0.3s ease;
        }
        
        .form-group input:focus,
        .form-group textarea:focus,
        .form-group select:focus {
            outline: none;
            border-color: #06b6d4;
            box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1);
        }
        
        .form-group textarea {
            min-height: 100px;
            resize: vertical;
        }
        
        .btn {
            padding: 12px 30px;
            background: linear-gradient(135deg, #06b6d4 0%, #2563eb 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(6, 182, 212, 0.4);
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .response {
            margin-top: 20px;
            padding: 20px;
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            border-left: 4px solid #06b6d4;
        }
        
        .response .label {
            color: #94a3b8;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        
        .response .value {
            color: #f8fafc;
            line-height: 1.6;
            white-space: pre-wrap;
        }
        
        .response .confidence {
            color: #06b6d4;
            font-size: 0.9em;
            margin-top: 10px;
        }
        
        .options-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .option-card {
            padding: 15px;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .option-card:hover {
            border-color: #06b6d4;
            background: rgba(6, 182, 212, 0.1);
        }
        
        .option-card.selected {
            border-color: #06b6d4;
            background: rgba(6, 182, 212, 0.2);
        }
        
        .hypothesis-list {
            margin-top: 20px;
        }
        
        .hypothesis-item {
            padding: 15px;
            background: rgba(255,255,255,0.03);
            border-radius: 10px;
            margin-bottom: 10px;
            border-left: 3px solid #2563eb;
        }
        
        .hypothesis-item .explanation {
            color: #f8fafc;
            margin-bottom: 5px;
        }
        
        .hypothesis-item .meta {
            color: #94a3b8;
            font-size: 0.85em;
        }
        
        .sensor-display {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .sensor-card {
            padding: 15px;
            background: rgba(255,255,255,0.03);
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .sensor-card .name {
            color: #94a3b8;
            font-size: 0.85em;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        
        .sensor-card .value {
            color: #06b6d4;
            font-size: 1.2em;
            font-weight: bold;
        }
        
        .loading {
            color: #06b6d4;
            font-style: italic;
        }
        
        .error {
            color: #ef4444;
            background: rgba(239, 68, 68, 0.1);
            padding: 10px 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        
        .success {
            color: #10b981;
        }
        
        footer {
            text-align: center;
            padding: 20px;
            color: #64748b;
            font-size: 0.85em;
            margin-top: 30px;
        }
        
        @media (max-width: 768px) {
            header h1 {
                font-size: 1.8em;
            }
            
            .stats-bar {
                gap: 10px;
            }
            
            .stat-card {
                padding: 10px 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚡ Circle City Model</h1>
            <p>Compact AGI Framework - 1GB Scale, Human-like Thinking</p>
        </header>
        
        <div class="stats-bar">
            <div class="stat-card">
                <div class="label">Knowledge Nodes</div>
                <div class="value" id="stat-nodes">0</div>
            </div>
            <div class="stat-card">
                <div class="label">Relationships</div>
                <div class="value" id="stat-relationships">0</div>
            </div>
            <div class="stat-card">
                <div class="label">Uptime</div>
                <div class="value" id="stat-uptime">0s</div>
            </div>
            <div class="stat-card">
                <div class="label">Requests</div>
                <div class="value" id="stat-requests">0</div>
            </div>
        </div>
        
        <div class="tabs">
            <div class="tab active" onclick="switchTab('learn')">📚 Learn</div>
            <div class="tab" onclick="switchTab('reason')">🧠 Reason</div>
            <div class="tab" onclick="switchTab('decide')">⚖️ Decide</div>
            <div class="tab" onclick="switchTab('hypothesize')">💡 Hypothesize</div>
            <div class="tab" onclick="switchTab('robotics')">🤖 Robotics</div>
            <div class="tab" onclick="switchTab('stats')">📊 Stats</div>
        </div>
        
        <!-- Learn Tab -->
        <div id="learn-tab" class="tab-content active">
            <div class="panel">
                <h2 class="panel-title">Teach the AGI</h2>
                <div class="form-group">
                    <label>Information to Learn</label>
                    <textarea id="learn-input" placeholder="Enter facts, rules, or general knowledge...\nExample: 'Robots should avoid obstacles'\nExample: 'The sky is blue during the day'"></textarea>
                </div>
                <button class="btn" onclick="learn()">Learn</button>
                <div id="learn-response" class="response" style="display:none;">
                    <div class="label">Result</div>
                    <div class="value" id="learn-result"></div>
                </div>
            </div>
        </div>
        
        <!-- Reason Tab -->
        <div id="reason-tab" class="tab-content">
            <div class="panel">
                <h2 class="panel-title">Ask the AGI</h2>
                <div class="form-group">
                    <label>Question or Statement</label>
                    <input type="text" id="reason-input" placeholder="Ask anything...\nExample: 'What color is the sky?'\nExample: 'What should a robot do?'">
                </div>
                <button class="btn" onclick="reason()">Reason</button>
                <div id="reason-response" class="response" style="display:none;">
                    <div class="label">Answer</div>
                    <div class="value" id="reason-answer"></div>
                    <div class="confidence">Confidence: <span id="reason-confidence"></span></div>
                    <div class="label" style="margin-top:15px;">Method</div>
                    <div class="value" id="reason-method"></div>
                </div>
            </div>
        </div>
        
        <!-- Decide Tab -->
        <div id="decide-tab" class="tab-content">
            <div class="panel">
                <h2 class="panel-title">Decision Making</h2>
                <div class="form-group">
                    <label>Options (comma separated)</label>
                    <input type="text" id="decide-options" placeholder="move forward, turn left, stop">
                </div>
                <div class="form-group">
                    <label>Context (JSON, optional)</label>
                    <input type="text" id="decide-context" placeholder='{"obstacle": "ahead"}'>
                </div>
                <button class="btn" onclick="decide()">Decide</button>
                <div id="decide-response" class="response" style="display:none;">
                    <div class="label">Decision</div>
                    <div class="value" id="decide-choice"></div>
                    <div class="confidence">Confidence: <span id="decide-confidence"></span></div>
                    <div class="label" style="margin-top:15px;">Scores</div>
                    <div class="value" id="decide-scores"></div>
                </div>
            </div>
        </div>
        
        <!-- Hypothesize Tab -->
        <div id="hypothesize-tab" class="tab-content">
            <div class="panel">
                <h2 class="panel-title">Generate Hypotheses</h2>
                <div class="form-group">
                    <label>Observation</label>
                    <input type="text" id="hypothesize-input" placeholder="Example: 'The robot stopped moving'">
                </div>
                <div class="form-group">
                    <label>Number of Hypotheses</label>
                    <input type="number" id="hypothesize-count" value="3" min="1" max="10">
                </div>
                <button class="btn" onclick="hypothesize()">Generate</button>
                <div id="hypothesize-response" class="response" style="display:none;">
                    <div class="label">Hypotheses</div>
                    <div class="hypothesis-list" id="hypothesis-list"></div>
                </div>
            </div>
        </div>
        
        <!-- Robotics Tab -->
        <div id="robotics-tab" class="tab-content">
            <div class="panel">
                <h2 class="panel-title">Robotics Interface</h2>
                <div class="form-group">
                    <label>Sensor Data (JSON)</label>
                    <textarea id="robotics-sensors" placeholder='{\n  "sensors": {\n    "lidar": [0.1, 0.2, 0.5, 1.0, 2.0],\n    "imu": {"orientation": [0,0,0], "acceleration": [0,0,0]}\n  }\n}'></textarea>
                </div>
                <div class="form-group">
                    <label>Goal (optional)</label>
                    <input type="text" id="robotics-goal" placeholder="navigate to next waypoint">
                </div>
                <button class="btn" onclick="robotics()">Process</button>
                <div id="robotics-response" class="response" style="display:none;">
                    <div class="label">Perception</div>
                    <div class="value" id="robotics-perception"></div>
                    <div class="label" style="margin-top:15px;">Goal</div>
                    <div class="value" id="robotics-goal-display"></div>
                    <div class="label" style="margin-top:15px;">Planned Action</div>
                    <div class="value" id="robotics-action"></div>
                    <div class="label" style="margin-top:15px;">Robot State</div>
                    <div class="value" id="robotics-state"></div>
                </div>
            </div>
        </div>
        
        <!-- Stats Tab -->
        <div id="stats-tab" class="tab-content">
            <div class="panel">
                <h2 class="panel-title">System Statistics</h2>
                <div class="form-group">
                    <button class="btn" onclick="loadStats()">Refresh Stats</button>
                </div>
                <div id="stats-response" class="response">
                    <pre id="stats-json"></pre>
                </div>
            </div>
        </div>
    </div>
    
    <footer>
        Circle City Model - Compact AGI Framework | v1.0.0
    </footer>
    
    <script>
        let currentTab = 'learn';
        
        // Switch tabs
        function switchTab(tabName) {
            currentTab = tabName;
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.getElementById(tabName + '-tab').classList.add('active');
            document.querySelector('[onclick="switchTab(\'' + tabName + '\')"]').classList.add('active');
        }
        
        // Update stats
        function updateStats() {
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('stat-nodes').textContent = data.knowledge_nodes;
                    document.getElementById('stat-relationships').textContent = data.relationships;
                    document.getElementById('stat-uptime').textContent = formatUptime(data.uptime_seconds);
                    document.getElementById('stat-requests').textContent = data.stats.request_count;
                });
        }
        
        function formatUptime(seconds) {
            if (seconds < 60) return Math.round(seconds) + 's';
            if (seconds < 3600) return Math.round(seconds/60) + 'm';
            if (seconds < 86400) return Math.round(seconds/3600) + 'h';
            return Math.round(seconds/86400) + 'd';
        }
        
        // Learn
        function learn() {
            const input = document.getElementById('learn-input').value;
            if (!input.trim()) return;
            
            showLoading('learn-response');
            
            fetch('/api/learn', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({information: input})
            })
            .then(r => r.json())
            .then(data => {
                document.getElementById('learn-result').textContent = 'Learned: ' + input.substring(0, 100) + (input.length > 100 ? '...' : '');
                showResponse('learn-response');
                updateStats();
            })
            .catch(error => {
                showError('learn-response', error);
            });
        }
        
        // Reason
        function reason() {
            const input = document.getElementById('reason-input').value;
            if (!input.trim()) return;
            
            showLoading('reason-response');
            
            fetch('/api/reason?query=' + encodeURIComponent(input))
                .then(r => r.json())
                .then(data => {
                    document.getElementById('reason-answer').textContent = data.answer || 'No answer found';
                    document.getElementById('reason-confidence').textContent = (data.confidence * 100).toFixed(1) + '%';
                    document.getElementById('reason-method').textContent = data.method || 'unknown';
                    showResponse('reason-response');
                    updateStats();
                })
                .catch(error => {
                    showError('reason-response', error);
                });
        }
        
        // Decide
        function decide() {
            const options = document.getElementById('decide-options').value;
            if (!options.trim()) return;
            
            showLoading('decide-response');
            
            const context = document.getElementById('decide-context').value;
            
            fetch('/api/decide', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    options: options.split(',').map(o => o.trim()),
                    context: context ? JSON.parse(context) : {}
                })
            })
            .then(r => r.json())
            .then(data => {
                document.getElementById('decide-choice').textContent = data.choice;
                document.getElementById('decide-confidence').textContent = (data.confidence * 100).toFixed(1) + '%';
                document.getElementById('decide-scores').textContent = JSON.stringify(data.scores, null, 2);
                showResponse('decide-response');
                updateStats();
            })
            .catch(error => {
                showError('decide-response', error);
            });
        }
        
        // Hypothesize
        function hypothesize() {
            const input = document.getElementById('hypothesize-input').value;
            const count = document.getElementById('hypothesize-count').value;
            if (!input.trim()) return;
            
            showLoading('hypothesize-response');
            
            fetch('/api/hypothesize?observation=' + encodeURIComponent(input) + '&count=' + count)
                .then(r => r.json())
                .then(data => {
                    const list = document.getElementById('hypothesis-list');
                    list.innerHTML = '';
                    data.forEach((hyp, i) => {
                        const item = document.createElement('div');
                        item.className = 'hypothesis-item';
                        item.innerHTML = `
                            <div class="explanation">${i+1}. ${hyp.explanation}</div>
                            <div class="meta">Confidence: ${(hyp.confidence * 100).toFixed(1)}% | Relationship: ${hyp.relationship}</div>
                        `;
                        list.appendChild(item);
                    });
                    showResponse('hypothesize-response');
                    updateStats();
                })
                .catch(error => {
                    showError('hypothesize-response', error);
                });
        }
        
        // Robotics
        function robotics() {
            const sensors = document.getElementById('robotics-sensors').value;
            const goal = document.getElementById('robotics-goal').value;
            if (!sensors.trim()) return;
            
            showLoading('robotics-response');
            
            try {
                const sensorData = JSON.parse(sensors);
                fetch('/api/robotics', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        sensor_data: sensorData,
                        goal: goal || null
                    })
                })
                .then(r => r.json())
                .then(data => {
                    document.getElementById('robotics-perception').textContent = JSON.stringify(data.perception, null, 2);
                    document.getElementById('robotics-goal-display').textContent = data.goal || 'auto-determined';
                    document.getElementById('robotics-action').textContent = data.plan.action;
                    document.getElementById('robotics-state').textContent = JSON.stringify(data.robot_state, null, 2);
                    showResponse('robotics-response');
                    updateStats();
                })
                .catch(error => {
                    showError('robotics-response', error);
                });
            } catch (e) {
                showError('robotics-response', 'Invalid JSON: ' + e.message);
            }
        }
        
        // Stats
        function loadStats() {
            showLoading('stats-response');
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('stats-json').textContent = JSON.stringify(data, null, 2);
                    showResponse('stats-response');
                })
                .catch(error => {
                    showError('stats-response', error);
                });
        }
        
        // UI Helpers
        function showLoading(elementId) {
            const el = document.getElementById(elementId);
            el.style.display = 'block';
            el.innerHTML = '<div class="loading">Processing...</div>';
        }
        
        function showResponse(elementId) {
            const el = document.getElementById(elementId);
            el.style.display = 'block';
        }
        
        function showError(elementId, error) {
            const el = document.getElementById(elementId);
            el.style.display = 'block';
            el.innerHTML = '<div class="error">Error: ' + error.message + '</div>';
        }
        
        // Initialize
        updateStats();
        setInterval(updateStats, 5000);
        loadStats();
    </script>
</body>
</html>
"""


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.route('/')
def index():
    """Main web interface"""
    return render_template_string(MAIN_TEMPLATE)


@app.route('/api/learn', methods=['POST'])
def api_learn():
    """Learn new information"""
    app_state['request_count'] += 1
    app_state['last_activity'] = time.time()
    
    data = request.get_json()
    information = data.get('information', '')
    context = data.get('context', None)
    
    if not information:
        return jsonify({'error': 'No information provided'}), 400
    
    memory_id = general_agi.learn(information, context)
    
    return jsonify({
        'success': True,
        'memory_id': memory_id,
        'message': 'Information learned successfully'
    })


@app.route('/api/reason')
def api_reason():
    """Perform reasoning"""
    app_state['request_count'] += 1
    app_state['last_activity'] = time.time()
    
    query = request.args.get('query', '')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    result = general_agi.reason(query)
    
    return jsonify({
        'answer': result.get('answer'),
        'confidence': result.get('confidence', 0),
        'path': result.get('path', []),
        'method': result.get('method', 'unknown')
    })


@app.route('/api/decide', methods=['POST'])
def api_decide():
    """Make a decision"""
    app_state['request_count'] += 1
    app_state['last_activity'] = time.time()
    
    data = request.get_json()
    options = data.get('options', [])
    context = data.get('context', {})
    
    if not options:
        return jsonify({'error': 'No options provided'}), 400
    
    result = general_agi.decide(options, context)
    
    return jsonify({
        'choice': result.get('choice'),
        'confidence': result.get('confidence', 0),
        'reasoning': result.get('reasoning', ''),
        'scores': result.get('scores', {})
    })


@app.route('/api/hypothesize')
def api_hypothesize():
    """Generate hypotheses"""
    app_state['request_count'] += 1
    app_state['last_activity'] = time.time()
    
    observation = request.args.get('observation', '')
    count = int(request.args.get('count', 3))
    
    if not observation:
        return jsonify({'error': 'No observation provided'}), 400
    
    hypotheses = general_agi.hypothesize(observation, count)
    
    return jsonify(hypotheses)


@app.route('/api/robotics', methods=['POST'])
def api_robotics():
    """Process robotics data"""
    app_state['request_count'] += 1
    app_state['last_activity'] = time.time()
    
    data = request.get_json()
    sensor_data = data.get('sensor_data', {})
    goal = data.get('goal', None)
    
    if not sensor_data:
        return jsonify({'error': 'No sensor data provided'}), 400
    
    result = robot_agi.robotic_response(sensor_data, goal)
    
    return jsonify({
        'perception': result.get('perception', {}),
        'goal': result.get('goal', ''),
        'plan': result.get('plan', {}),
        'execution': result.get('execution', {}),
        'robot_state': result.get('robot_state', {})
    })


@app.route('/api/adapt', methods=['POST'])
def api_adapt():
    """Adapt to new environment"""
    app_state['request_count'] += 1
    app_state['last_activity'] = time.time()
    
    data = request.get_json()
    new_data = data.get('data', {})
    
    result = general_agi.adapt(new_data)
    
    return jsonify(result)


@app.route('/api/evolve', methods=['POST'])
def api_evolve():
    """Trigger self-evolution"""
    app_state['request_count'] += 1
    app_state['last_activity'] = time.time()
    
    result = general_agi.evolve()
    
    return jsonify(result)


@app.route('/api/stats')
def api_stats():
    """Get system statistics"""
    app_state['request_count'] += 1
    app_state['last_activity'] = time.time()
    
    stats = general_agi.get_stats()
    stats['app_state'] = {
        'request_count': app_state['request_count'],
        'last_activity': app_state['last_activity'],
        'initialization_time': app_state['initialization_time']
    }
    
    return jsonify(stats)


@app.route('/api/reset', methods=['POST'])
def api_reset():
    """Reset the AGI system"""
    global general_agi, robot_agi
    
    general_agi = CircleCityAGI()
    robot_agi = create_robot_agi()
    
    return jsonify({'success': True, 'message': 'AGI system reset'})


@app.route('/api/health')
def api_health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'uptime': time.time() - app_state['initialization_time']
    })


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Circle City Model - Web Application")
    print("="*60)
    print("\nStarting Flask server...")
    print("Open your browser and navigate to: http://localhost:5000")
    print("\nAPI Endpoints:")
    print("  GET  /              - Web Interface")
    print("  GET  /api/stats    - System Statistics")
    print("  GET  /api/health   - Health Check")
    print("  POST /api/learn    - Learn New Information")
    print("  GET  /api/reason   - Perform Reasoning")
    print("  POST /api/decide   - Make Decision")
    print("  GET  /api/hypothesize - Generate Hypotheses")
    print("  POST /api/robotics - Process Robotics Data")
    print("  POST /api/adapt    - Adapt to Environment")
    print("  POST /api/evolve   - Trigger Self-Evolution")
    print("  POST /api/reset    - Reset AGI System")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
