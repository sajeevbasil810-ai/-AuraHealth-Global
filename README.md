# Circle City Model - Compact AGI Framework

A revolutionary **1GB-scale Artificial General Intelligence** system designed for autonomous learning, adaptation, and human-like reasoning capabilities.

## Overview

The Circle City Model is a **compact yet powerful AGI framework** that:
- Operates within a **1GB storage footprint**
- **Learns autonomously** from experience
- **Adapts** to new environments and situations
- **Reasons** with human-like cognitive capabilities
- **Integrates seamlessly** with robotics and hardware systems
- **Evolves** itself over time through self-modification

## Key Features

### 🧠 Core Capabilities
- **Neural-Symbolic Hybrid Architecture**: Combines the strengths of neural networks and symbolic reasoning
- **Multi-Modal Memory System**: Semantic, episodic, procedural, working, and sensory memory
- **Online Learning Engine**: Continuous learning from new information
- **Advanced Reasoning**: Symbolic logic, probabilistic inference, analogical reasoning, and abductive reasoning
- **Self-Evolution Mechanism**: Ability to modify and improve its own structure

### 🤖 Robotics Integration
- **Sensor Fusion**: Processes data from multiple sensors (LiDAR, IMU, etc.)
- **Autonomous Decision Making**: Makes optimal decisions based on context
- **Action Planning**: Generates and executes action sequences
- **Obstacle Avoidance**: Built-in safety mechanisms
- **Adaptive Behavior**: Adjusts to new environments and conditions

### 🎯 Design Principles
- **Compact**: Entire system fits in ~1GB of storage
- **Powerful**: AGI-level reasoning capabilities
- **Autonomous**: Learns and adapts without external intervention
- **Modifiable**: Can be modified and evolved over time
- **Hardware-Ready**: Designed for robotics and embedded systems

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Circle City AGI                              │
├─────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │  Semantic        │  │   Memory         │  │ Reasoning     │ │
│  │  Network         │  │   System         │  │ Engine        │ │
│  │  (Knowledge)     │  │  (Experience)     │  │  (Inference)  │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
│           │                  │                   │              │
│           └──────────────────┼───────────────────┘              │
│                                  │                                  │
│            ┌─────────────────▼─────────────────┐               │
│            │      Learning Engine                │               │
│            │  (Autonomous Knowledge Acquisition)  │               │
│            └─────────────────┬─────────────────┘               │
│                                  │                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │  Adaptation     │  │  Robotics        │  │ Self-         │ │
│  │  System         │  │  Interface       │  │ Evolution     │ │
│  │  (Change)       │  │  (Hardware)      │  │ (Improvement) │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────┘
```

## Installation

```bash
# Clone the repository
git clone https://github.com/sajeevbasil810-ai/-AuraHealth-Global.git
cd -AuraHealth-Global

# Install dependencies
pip install numpy
```

## Quick Start

```python
from circle_city_model import CircleCityAGI

# Create the AGI system
agi = CircleCityAGI()

# Learn new information
agi.learn("The sky is blue during the day")
agi.learn("Robots should avoid obstacles")

# Reason about the world
response = agi.reason("What color is the sky at noon?")
print(response['answer'])  # "The sky is blue during the day"

# Make decisions
decision = agi.decide(
    ["move forward", "turn left", "stop"],
    context={"obstacle": "ahead"}
)
print(decision['choice'])  # Likely "stop" or "turn left"

# Generate hypotheses
hypotheses = agi.hypothesize("The robot stopped moving")
for hyp in hypotheses:
    print(f"{hyp['explanation']} (confidence: {hyp['confidence']})")
```

## Robotics Usage

```python
from circle_city_model import create_robot_agi

# Create a robotics-optimized AGI
robot_agi = create_robot_agi()

# Process sensor data
sensor_data = {
    'timestamp': time.time(),
    'sensors': {
        'lidar': [0.1, 0.2, 0.3, 0.5, 1.0, 2.0, 3.0],  # Distances in meters
        'imu': {
            'orientation': [0, 0, 0],
            'acceleration': [0, 0, 0],
        },
    },
}

# Get complete robotic response
response = robot_agi.robotic_response(sensor_data)
print(f"Perception: {response['perception']}")
print(f"Action: {response['plan']['action']}")

# Or step-by-step
perception = robot_agi.robotics.process_sensor_data(sensor_data)
plan = robot_agi.robotics.plan_action("navigate to goal")
action = robot_agi.robotics.execute_action(plan['action'])
```

## Advanced Usage

### Memory Operations

```python
# Store information in different memory types
agi.learn("Important fact", source="user")

# Retrieve from memory
results = agi.remember("fact")

# Get working memory context
context = agi.get_working_memory()

# Clear working memory
agi.clear_working_memory()
```

### Adaptation

```python
# Adapt to new environmental conditions
new_environment = {
    'terrain': 'rough',
    'lighting': 'low',
    'temperature': 'cold',
}
adaptation = agi.adapt(new_environment)
print(f"Novelty score: {adaptation['novelty_score']}")
print(f"Adaptation level: {adaptation['adaptation_level']}")
```

### Self-Evolution

```python
# Trigger self-evolution
evolution = agi.evolve()
print(f"Changes made: {len(evolution['changes'])}")
print(f"Improvements: {evolution['improvements']}")

# Direct modification
agi.modify({
    'type': 'modify_parameter',
    'parameter': 'LEARNING_RATE',
    'value': 0.2,
})
```

## System Statistics

```python
stats = agi.get_stats()
print(f"Uptime: {stats['uptime_seconds']} seconds")
print(f"Knowledge nodes: {stats['knowledge_nodes']}")
print(f"Relationships: {stats['relationships']}")
print(f"Learning operations: {stats['stats']['learning_count']}")
```

## Architecture Details

### Semantic Network
The core knowledge representation system using a graph-based approach:
- **Nodes**: Represent concepts, entities, actions, states, rules, and goals
- **Relationships**: Connect nodes with typed relationships (is_a, has_a, causes, requires, etc.)
- **Embeddings**: Each node has a compact 64-dimensional vector for neural operations

### Memory System
Five types of memory inspired by human cognition:
1. **Semantic Memory**: Long-term facts and general knowledge
2. **Episodic Memory**: Specific events and experiences
3. **Procedural Memory**: Skills, procedures, and rules
4. **Working Memory**: Current context and short-term information
5. **Sensory Memory**: Recent perceptions from sensors

### Reasoning Engine
Multiple reasoning strategies:
- **Direct Retrieval**: Fast lookup of known information
- **Relational Inference**: Following chains of reasoning through relationships
- **Analogical Reasoning**: Finding similar past experiences
- **Abductive Reasoning**: Generating hypotheses to explain observations
- **Decision Making**: Evaluating options based on context

### Learning Engine
Continuous learning capabilities:
- **Fact Learning**: Extracting and storing factual information
- **Rule Learning**: Acquiring procedural knowledge
- **Pattern Discovery**: Finding regularities in data
- **Reinforcement Learning**: Strengthening successful knowledge
- **Background Processing**: Asynchronous learning queue

### Adaptation System
Environmental adaptation:
- **Novelty Detection**: Identifying new or unexpected information
- **Environment Modeling**: Maintaining an internal model of the world
- **Concept Creation**: Creating new knowledge for novel situations
- **Relationship Adaptation**: Modifying connections based on new data
- **Adaptation History**: Tracking changes over time

### Robotics Interface
Hardware integration layer:
- **Sensor Processing**: Extracting features from raw sensor data
- **Perception Interpretation**: Understanding the environment
- **Action Planning**: Generating action sequences
- **Action Execution**: Performing actions in the world
- **State Tracking**: Maintaining robot state information

### Self-Evolution Mechanism
Autonomous improvement:
- **Knowledge Optimization**: Merging duplicate concepts
- **Pattern Discovery**: Finding new relationships
- **Rule Creation**: Generating new reasoning rules
- **Memory Optimization**: Managing memory usage
- **Direct Modification**: Self-modification capabilities

## Design Philosophy

### Why "Circle City"?
The name "Circle City" represents:
- **Completeness**: A full, self-contained system
- **Unity**: All components work together seamlessly
- **Continuity**: Continuous learning and evolution
- **Boundary**: A defined, compact system within a limited footprint

### Key Innovations

1. **Compact AGI**: Full AGI capabilities in a 1GB footprint
2. **Autonomous Learning**: No need for pre-programmed instructions
3. **Hardware Ready**: Designed for robotics and embedded systems
4. **Self-Evolving**: Can improve itself over time
5. **Multi-Modal**: Handles various types of information and sensors

### Comparison to Other Systems

| Feature | Circle City | Traditional AI | Large LLMs |
|---------|-------------|---------------|-------------|
| Size | ~1GB | Variable | 10s-100s GB |
| Learning | Autonomous | Supervised | Supervised |
| Adaptation | Built-in | Limited | Limited |
| Reasoning | Multi-modal | Single | Text-only |
| Robotics | Native | Requires integration | Not designed |
| Self-Evolution | Yes | No | No |
| Storage | Compact | Variable | Massive |

## Use Cases

### Robotics
- Autonomous navigation
- Obstacle avoidance
- Object manipulation
- Sensor fusion
- Adaptive behavior

### Embedded Systems
- IoT devices
- Smart appliances
- Industrial control
- Automotive systems

### Research
- AGI experimentation
- Cognitive architecture testing
- Learning algorithm development
- Reasoning system evaluation

### Education
- AI concepts demonstration
- Machine learning teaching
- Robotics education
- Cognitive science research

## Performance

The system is designed for:
- **Fast inference**: Real-time reasoning capabilities
- **Efficient learning**: Online learning with minimal overhead
- **Low memory**: Operates within 1GB RAM
- **Scalability**: Can be extended with additional knowledge and capabilities

## Limitations

As a compact AGI system:
- Limited by the 1GB footprint constraint
- Simplified natural language processing
- Basic sensor processing (no computer vision)
- Limited to text and structured data
- Requires numpy for vector operations

## Future Development

Planned enhancements:
- More sophisticated NLP
- Advanced sensor processing
- Enhanced reasoning strategies
- Improved learning algorithms
- Better adaptation mechanisms
- Expanded robotics support

## License

This project is open source and available for research and development purposes.

## Contributing

Contributions are welcome! Please feel free to submit issues, suggestions, or pull requests.

## Contact

For questions or inquiries, please contact the project maintainers.

---

**Circle City Model** - The Future of Compact AGI

*"A small model with the power of human-like thinking"*
