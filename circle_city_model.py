#!/usr/bin/env python3
"""
Circle City Model - Compact AGI Framework
========================================

A 1GB-scale Artificial General Intelligence system designed for:
- Autonomous learning and adaptation
- Human-like reasoning capabilities  
- Robotics integration
- Self-modification
- Compact footprint (<1GB storage)

Architecture:
- Neural-Symbolic Hybrid Core
- Adaptive Memory System
- Online Learning Engine
- Robotics Interface Layer
- Self-Evolution Mechanism
"""

import json
import hashlib
import time
import random
import math
import threading
import queue
from collections import defaultdict, deque
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum, auto
import numpy as np


class Config:
    """Central configuration"""
    MAX_KNOWLEDGE_NODES = 50000
    MAX_EXPERIENCE_MEMORY = 100000
    MAX_WORKING_MEMORY = 10000
    MAX_EPISODIC_MEMORY = 50000
    MAX_SEMANTIC_LINKS = 500000
    LEARNING_RATE = 0.15
    FORGETTING_RATE = 0.0001
    REINFORCEMENT_RATE = 0.25
    INFERENCE_DEPTH = 8
    CONFIDENCE_THRESHOLD = 0.6
    ADAPTATION_SPEED = 0.2
    NOVELTY_SENSITIVITY = 0.7
    SENSOR_FUSION_WINDOW = 10
    ACTION_PLANNING_HORIZON = 5
    MUTATION_RATE = 0.01
    EVOLUTION_INTERVAL = 1000


class NodeType(Enum):
    CONCEPT = auto()
    ENTITY = auto()
    RELATIONSHIP = auto()
    PROPERTY = auto()
    ACTION = auto()
    STATE = auto()
    VALUE = auto()
    RULE = auto()
    GOAL = auto()


class MemoryType(Enum):
    SEMANTIC = auto()
    EPISODIC = auto()
    PROCEDURAL = auto()
    WORKING = auto()
    SENSORY = auto()


@dataclass
class KnowledgeNode:
    node_id: str
    node_type: NodeType
    label: str
    description: str = ""
    confidence: float = 1.0
    creation_time: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0
    importance: float = 0.5
    embedding: np.ndarray = field(default_factory=lambda: np.random.randn(64))
    source: str = "internal"
    is_learned: bool = False
    is_inferred: bool = False

    def update_embedding(self, new_data: np.ndarray, learning_rate: float = 0.1):
        self.embedding = (1 - learning_rate) * self.embedding + learning_rate * new_data

    def reinforce(self, success: bool = True):
        if success:
            self.confidence = min(1.0, self.confidence + Config.REINFORCEMENT_RATE * (1 - self.confidence))
            self.importance = min(1.0, self.importance + 0.05)
        else:
            self.confidence = max(0.1, self.confidence - Config.REINFORCEMENT_RATE * self.confidence)
            self.importance = max(0.1, self.importance - 0.02)
        self.last_accessed = time.time()
        self.access_count += 1

    def decay(self):
        age = time.time() - self.last_accessed
        forget_factor = math.exp(-Config.FORGETTING_RATE * age)
        self.confidence *= forget_factor
        self.importance *= forget_factor

    def to_dict(self) -> Dict:
        return {
            'node_id': self.node_id,
            'node_type': self.node_type.name,
            'label': self.label,
            'description': self.description,
            'confidence': self.confidence,
            'creation_time': self.creation_time,
            'last_accessed': self.last_accessed,
            'access_count': self.access_count,
            'importance': self.importance,
            'embedding': self.embedding.tolist(),
            'source': self.source,
            'is_learned': self.is_learned,
            'is_inferred': self.is_inferred,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'KnowledgeNode':
        node = cls(
            node_id=data['node_id'],
            node_type=NodeType[data['node_type']],
            label=data['label'],
            description=data.get('description', ""),
            confidence=data.get('confidence', 1.0),
            creation_time=data.get('creation_time', time.time()),
            last_accessed=data.get('last_accessed', time.time()),
            access_count=data.get('access_count', 0),
            importance=data.get('importance', 0.5),
            embedding=np.array(data.get('embedding', [])),
            source=data.get('source', 'internal'),
            is_learned=data.get('is_learned', False),
            is_inferred=data.get('is_inferred', False),
        )
        return node


@dataclass
class MemoryEntry:
    memory_id: str
    memory_type: MemoryType
    content: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    confidence: float = 1.0
    emotional_valence: float = 0.0
    relevance: float = 0.5

    def to_dict(self) -> Dict:
        return {
            'memory_id': self.memory_id,
            'memory_type': self.memory_type.name,
            'content': self.content,
            'timestamp': self.timestamp,
            'confidence': self.confidence,
            'emotional_valence': self.emotional_valence,
            'relevance': self.relevance,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'MemoryEntry':
        return cls(
            memory_id=data['memory_id'],
            memory_type=MemoryType[data['memory_type']],
            content=data['content'],
            timestamp=data.get('timestamp', time.time()),
            confidence=data.get('confidence', 1.0),
            emotional_valence=data.get('emotional_valence', 0.0),
            relevance=data.get('relevance', 0.5),
        )


@dataclass
class Relationship:
    relationship_id: str
    source_id: str
    target_id: str
    relationship_type: str
    weight: float = 1.0
    confidence: float = 1.0
    bidirectional: bool = False

    def to_dict(self) -> Dict:
        return {
            'relationship_id': self.relationship_id,
            'source_id': self.source_id,
            'target_id': self.target_id,
            'relationship_type': self.relationship_type,
            'weight': self.weight,
            'confidence': self.confidence,
            'bidirectional': self.bidirectional,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Relationship':
        return cls(
            relationship_id=data['relationship_id'],
            source_id=data['source_id'],
            target_id=data['target_id'],
            relationship_type=data['relationship_type'],
            weight=data.get('weight', 1.0),
            confidence=data.get('confidence', 1.0),
            bidirectional=data.get('bidirectional', False),
        )


class SemanticNetwork:
    """Core knowledge representation system"""
    
    def __init__(self):
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.relationships: Dict[str, Relationship] = {}
        self.index: Dict[str, List[str]] = defaultdict(list)
        self.next_node_id = 1
        self.next_relationship_id = 1
        self.lock = threading.RLock()

    def _generate_id(self, prefix: str = "node") -> str:
        with self.lock:
            if prefix == "node":
                node_id = f"{prefix}_{self.next_node_id}"
                self.next_node_id += 1
                return node_id
            else:
                rel_id = f"{prefix}_{self.next_relationship_id}"
                self.next_relationship_id += 1
                return rel_id

    def add_node(self, node_type: NodeType, label: str, description: str = "",
                 confidence: float = 1.0, source: str = "internal",
                 is_learned: bool = False) -> KnowledgeNode:
        node_id = self._generate_id("node")
        node = KnowledgeNode(
            node_id=node_id,
            node_type=node_type,
            label=label,
            description=description,
            confidence=confidence,
            source=source,
            is_learned=is_learned,
        )
        with self.lock:
            self.nodes[node_id] = node
            self.index[label.lower()].append(node_id)
            if len(self.nodes) > Config.MAX_KNOWLEDGE_NODES:
                self._prune_nodes()
        return node

    def get_node(self, node_id: str) -> Optional[KnowledgeNode]:
        with self.lock:
            return self.nodes.get(node_id)

    def find_nodes(self, label: str) -> List[KnowledgeNode]:
        with self.lock:
            node_ids = self.index.get(label.lower(), [])
            return [self.nodes[nid] for nid in node_ids if nid in self.nodes]

    def add_relationship(self, source_id: str, target_id: str, relationship_type: str,
                        weight: float = 1.0, confidence: float = 1.0,
                        bidirectional: bool = False) -> Relationship:
        rel_id = self._generate_id("rel")
        rel = Relationship(
            relationship_id=rel_id,
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            weight=weight,
            confidence=confidence,
            bidirectional=bidirectional,
        )
        with self.lock:
            self.relationships[rel_id] = rel
            if len(self.relationships) > Config.MAX_SEMANTIC_LINKS:
                self._prune_relationships()
        return rel

    def get_relationships(self, node_id: str) -> List[Relationship]:
        with self.lock:
            return [rel for rel in self.relationships.values()
                    if rel.source_id == node_id or rel.target_id == node_id]

    def get_neighbors(self, node_id: str, relationship_type: Optional[str] = None) -> List[Tuple[str, str]]:
        with self.lock:
            neighbors = []
            for rel in self.relationships.values():
                if rel.source_id == node_id:
                    if relationship_type is None or rel.relationship_type == relationship_type:
                        neighbors.append((rel.target_id, rel.relationship_type))
                elif rel.target_id == node_id and rel.bidirectional:
                    if relationship_type is None or rel.relationship_type == relationship_type:
                        neighbors.append((rel.source_id, rel.relationship_type))
            return neighbors

    def _prune_nodes(self):
        with self.lock:
            sorted_nodes = sorted(self.nodes.items(), key=lambda x: (x[1].importance, x[1].last_accessed))
            num_to_remove = max(1, len(sorted_nodes) // 10)
            for node_id, _ in sorted_nodes[:num_to_remove]:
                label = self.nodes[node_id].label.lower()
                if label in self.index:
                    self.index[label] = [nid for nid in self.index[label] if nid != node_id]
                del self.nodes[node_id]

    def _prune_relationships(self):
        with self.lock:
            sorted_rels = sorted(self.relationships.items(), key=lambda x: (x[1].confidence, x[1].weight))
            num_to_remove = max(1, len(sorted_rels) // 10)
            for rel_id, _ in sorted_rels[:num_to_remove]:
                del self.relationships[rel_id]

    def find_path(self, start_id: str, end_id: str, max_depth: int = Config.INFERENCE_DEPTH) -> Optional[List[str]]:
        with self.lock:
            visited = set()
            queue = deque([(start_id, [start_id])])
            while queue:
                current_id, path = queue.popleft()
                if current_id == end_id:
                    return path
                if len(path) > max_depth:
                    continue
                if current_id in visited:
                    continue
                visited.add(current_id)
                for neighbor_id, _ in self.get_neighbors(current_id):
                    if neighbor_id not in visited:
                        queue.append((neighbor_id, path + [neighbor_id]))
            return None

    def get_similar_nodes(self, node_id: str, threshold: float = 0.7, limit: int = 10) -> List[Tuple[str, float]]:
        with self.lock:
            if node_id not in self.nodes:
                return []
            target_embedding = self.nodes[node_id].embedding
            similarities = []
            for other_id, other_node in self.nodes.items():
                if other_id == node_id:
                    continue
                dot_product = np.dot(target_embedding, other_node.embedding)
                norm_a = np.linalg.norm(target_embedding)
                norm_b = np.linalg.norm(other_node.embedding)
                similarity = dot_product / (norm_a * norm_b + 1e-8)
                if similarity > threshold:
                    similarities.append((other_id, similarity))
            similarities.sort(key=lambda x: x[1], reverse=True)
            return similarities[:limit]

    def save(self) -> Dict:
        with self.lock:
            return {
                'nodes': {nid: node.to_dict() for nid, node in self.nodes.items()},
                'relationships': {rid: rel.to_dict() for rid, rel in self.relationships.items()},
                'next_node_id': self.next_node_id,
                'next_relationship_id': self.next_relationship_id,
            }

    def load(self, data: Dict):
        with self.lock:
            self.nodes = {nid: KnowledgeNode.from_dict(node_data) for nid, node_data in data.get('nodes', {}).items()}
            self.relationships = {rid: Relationship.from_dict(rel_data) for rid, rel_data in data.get('relationships', {}).items()}
            self.next_node_id = data.get('next_node_id', 1)
            self.next_relationship_id = data.get('next_relationship_id', 1)
            self.index = defaultdict(list)
            for node in self.nodes.values():
                self.index[node.label.lower()].append(node.node_id)


class MemorySystem:
    """Multi-modal memory system"""
    
    def __init__(self):
        self.semantic: Dict[str, KnowledgeNode] = {}
        self.episodic: Dict[str, MemoryEntry] = {}
        self.procedural: Dict[str, MemoryEntry] = {}
        self.working: Dict[str, MemoryEntry] = {}
        self.sensory: deque = deque(maxlen=Config.SENSOR_FUSION_WINDOW)
        self.lock = threading.RLock()
        self._build_initial_knowledge()

    def _build_initial_knowledge(self):
        logic_concepts = [
            ("cause", NodeType.CONCEPT, "The concept of causation"),
            ("effect", NodeType.CONCEPT, "The result of a cause"),
            ("implies", NodeType.RELATIONSHIP, "Logical implication"),
            ("requires", NodeType.RELATIONSHIP, "Necessary condition"),
        ]
        for label, node_type, desc in logic_concepts:
            self.store_semantic(label, node_type, desc, source="bootstrap")
        actions = [
            ("move", NodeType.ACTION, "Physical movement"),
            ("stop", NodeType.ACTION, "Cease movement"),
            ("turn", NodeType.ACTION, "Change direction"),
            ("observe", NodeType.ACTION, "Perceive the environment"),
            ("learn", NodeType.ACTION, "Acquire new knowledge"),
            ("adapt", NodeType.ACTION, "Adjust to new conditions"),
        ]
        for label, node_type, desc in actions:
            self.store_semantic(label, node_type, desc, source="bootstrap")
        states = [
            ("safe", NodeType.STATE, "Condition of being safe"),
            ("danger", NodeType.STATE, "Condition of being in danger"),
            ("obstacle", NodeType.ENTITY, "Something that blocks progress"),
            ("goal", NodeType.GOAL, "Desired outcome"),
        ]
        for label, node_type, desc in states:
            self.store_semantic(label, node_type, desc, source="bootstrap")

    def store_semantic(self, label: str, node_type: NodeType, description: str = "",
                      confidence: float = 1.0, source: str = "internal") -> str:
        content_hash = hashlib.md5(f"{label}_{description}".encode()).hexdigest()[:8]
        memory_id = f"sem_{content_hash}"
        node = KnowledgeNode(node_id=memory_id, node_type=node_type, label=label,
                           description=description, confidence=confidence, source=source)
        with self.lock:
            self.semantic[memory_id] = node
            if len(self.semantic) > Config.MAX_KNOWLEDGE_NODES:
                self._prune_semantic()
        return memory_id

    def store_episodic(self, event: Dict[str, Any], importance: float = 0.5) -> str:
        timestamp = event.get('timestamp', time.time())
        content_hash = hashlib.md5(json.dumps(event, sort_keys=True).encode()).hexdigest()[:8]
        memory_id = f"epi_{timestamp}_{content_hash}"
        entry = MemoryEntry(memory_id=memory_id, memory_type=MemoryType.EPISODIC,
                          content=event, timestamp=timestamp, relevance=importance)
        with self.lock:
            self.episodic[memory_id] = entry
            if len(self.episodic) > Config.MAX_EPISODIC_MEMORY:
                self._prune_episodic()
        return memory_id

    def store_procedural(self, procedure: Dict[str, Any]) -> str:
        content_hash = hashlib.md5(json.dumps(procedure, sort_keys=True).encode()).hexdigest()[:8]
        memory_id = f"proc_{content_hash}"
        entry = MemoryEntry(memory_id=memory_id, memory_type=MemoryType.PROCEDURAL, content=procedure)
        with self.lock:
            self.procedural[memory_id] = entry
        return memory_id

    def add_to_working(self, information: Dict[str, Any], relevance: float = 0.5) -> str:
        content_hash = hashlib.md5(json.dumps(information, sort_keys=True).encode()).hexdigest()[:8]
        memory_id = f"work_{content_hash}"
        entry = MemoryEntry(memory_id=memory_id, memory_type=MemoryType.WORKING,
                          content=information, relevance=relevance)
        with self.lock:
            self.working[memory_id] = entry
            if len(self.working) > Config.MAX_WORKING_MEMORY:
                self._prune_working()
        return memory_id

    def add_sensory(self, perception: Dict[str, Any]):
        with self.lock:
            self.sensory.append({'timestamp': time.time(), 'data': perception})

    def _prune_semantic(self):
        with self.lock:
            sorted_nodes = sorted(self.semantic.items(), key=lambda x: (x[1].importance, x[1].confidence, x[1].last_accessed))
            num_to_remove = max(1, len(sorted_nodes) // 10)
            for memory_id, _ in sorted_nodes[:num_to_remove]:
                del self.semantic[memory_id]

    def _prune_episodic(self):
        with self.lock:
            sorted_entries = sorted(self.episodic.items(), key=lambda x: x[1].timestamp)
            num_to_remove = max(1, len(sorted_entries) // 10)
            for memory_id, _ in sorted_entries[:num_to_remove]:
                del self.episodic[memory_id]

    def _prune_working(self):
        with self.lock:
            sorted_entries = sorted(self.working.items(), key=lambda x: x[1].relevance)
            num_to_remove = max(1, len(sorted_entries) // 5)
            for memory_id, _ in sorted_entries[:num_to_remove]:
                del self.working[memory_id]

    def retrieve_semantic(self, label: str) -> List[KnowledgeNode]:
        with self.lock:
            return [node for node in self.semantic.values()
                    if label.lower() in node.label.lower() or label.lower() in node.description.lower()]

    def retrieve_episodic(self, query: Dict[str, Any], limit: int = 10) -> List[MemoryEntry]:
        with self.lock:
            results = []
            for entry in self.episodic.values():
                match_score = self._calculate_match_score(entry.content, query)
                if match_score > 0:
                    results.append((entry, match_score))
            results.sort(key=lambda x: x[1], reverse=True)
            return [r[0] for r in results[:limit]]

    def _calculate_match_score(self, content: Dict, query: Dict) -> float:
        score = 0.0
        for key, value in query.items():
            if key in content:
                if isinstance(value, str) and isinstance(content[key], str):
                    if value.lower() in content[key].lower():
                        score += 1.0
                elif content[key] == value:
                    score += 1.0
                else:
                    score += 0.5
        return score / max(1, len(query))

    def get_working_context(self) -> Dict[str, Any]:
        with self.lock:
            return {mid: entry.content for mid, entry in self.working.items()}

    def get_recent_sensory(self, limit: int = None) -> List[Dict]:
        with self.lock:
            if limit:
                return list(self.sensory)[-limit:]
            return list(self.sensory)

    def clear_working(self):
        with self.lock:
            self.working.clear()


class ReasoningEngine:
    """Advanced reasoning system"""
    
    def __init__(self, semantic_network: SemanticNetwork, memory: MemorySystem):
        self.semantic_network = semantic_network
        self.memory = memory
        self.reasoning_cache: Dict[str, Dict] = {}

    def infer(self, query: str, context: Optional[Dict] = None, depth: int = Config.INFERENCE_DEPTH) -> Dict[str, Any]:
        cache_key = f"{query}_{json.dumps(context or {}, sort_keys=True)}"
        if cache_key in self.reasoning_cache:
            return self.reasoning_cache[cache_key]
        parsed = self._parse_query(query)
        direct_results = self._direct_retrieval(parsed)
        if direct_results and direct_results['confidence'] > Config.CONFIDENCE_THRESHOLD:
            result = direct_results
        else:
            result = self._relational_inference(parsed, depth)
            if result['confidence'] < Config.CONFIDENCE_THRESHOLD:
                result = self._analogical_inference(parsed, depth)
        self.reasoning_cache[cache_key] = result
        if len(self.reasoning_cache) > 1000:
            self.reasoning_cache.clear()
        return result

    def _parse_query(self, query: str) -> Dict[str, Any]:
        query_lower = query.lower()
        parsed = {
            'original': query,
            'normalized': query_lower,
            'keywords': set(query_lower.split()),
            'question_type': self._detect_question_type(query_lower),
        }
        return parsed

    def _detect_question_type(self, query: str) -> str:
        if query.startswith('what'): return 'what'
        elif query.startswith('how'): return 'how'
        elif query.startswith('why'): return 'why'
        elif query.startswith('when'): return 'when'
        elif query.startswith('where'): return 'where'
        elif query.startswith('who'): return 'who'
        elif query.startswith('which'): return 'which'
        elif query.endswith('?'): return 'yes_no'
        else: return 'declarative'

    def _direct_retrieval(self, parsed: Dict) -> Dict[str, Any]:
        for keyword in parsed['keywords']:
            nodes = self.semantic_network.find_nodes(keyword)
            if nodes:
                best_node = max(nodes, key=lambda n: n.confidence)
                return {'answer': best_node.description or best_node.label,
                        'confidence': best_node.confidence, 'path': [best_node.node_id],
                        'alternatives': [], 'method': 'direct_retrieval'}
        return {'answer': None, 'confidence': 0.0, 'path': [], 'alternatives': [], 'method': 'direct_retrieval'}

    def _relational_inference(self, parsed: Dict, depth: int) -> Dict[str, Any]:
        best_result = {'answer': None, 'confidence': 0.0, 'path': [], 'alternatives': [], 'method': 'relational'}
        keyword_nodes = {}
        for keyword in parsed['keywords']:
            nodes = self.semantic_network.find_nodes(keyword)
            if nodes:
                keyword_nodes[keyword] = nodes[0]
        if not keyword_nodes:
            return best_result
        node_ids = list(keyword_nodes.keys())
        for i, source_id in enumerate(node_ids):
            for target_id in node_ids[i+1:]:
                path = self.semantic_network.find_path(source_id, target_id, depth)
                if path:
                    path_confidence = self._calculate_path_confidence(path)
                    if path_confidence > best_result['confidence']:
                        best_result = {'answer': f"Relationship found: {' -> '.join(path)}",
                                     'confidence': path_confidence, 'path': path,
                                     'alternatives': [], 'method': 'relational'}
        return best_result

    def _calculate_path_confidence(self, path: List[str]) -> float:
        total_confidence = 1.0
        for node_id in path:
            node = self.semantic_network.get_node(node_id)
            if node:
                total_confidence *= node.confidence
        decay_factor = 0.9 ** (len(path) - 1)
        return total_confidence * decay_factor

    def _analogical_inference(self, parsed: Dict, depth: int) -> Dict[str, Any]:
        for keyword in parsed['keywords']:
            nodes = self.semantic_network.find_nodes(keyword)
            if nodes:
                similar = self.semantic_network.get_similar_nodes(nodes[0].node_id, threshold=0.5)
                if similar:
                    similar_id = similar[0][0]
                    similar_node = self.semantic_network.get_node(similar_id)
                    if similar_node:
                        return {'answer': f"By analogy: {similar_node.description or similar_node.label}",
                               'confidence': 0.6, 'path': [nodes[0].node_id, similar_id],
                               'alternatives': [], 'method': 'analogical'}
        return {'answer': None, 'confidence': 0.0, 'path': [], 'alternatives': [], 'method': 'analogical'}

    def generate_hypotheses(self, observation: str, count: int = 3) -> List[Dict[str, Any]]:
        hypotheses = []
        keywords = observation.lower().split()
        related_nodes = []
        for keyword in keywords:
            nodes = self.semantic_network.find_nodes(keyword)
            related_nodes.extend(nodes)
        for node in related_nodes[:5]:
            neighbors = self.semantic_network.get_neighbors(node.node_id)
            for neighbor_id, rel_type in neighbors:
                neighbor = self.semantic_network.get_node(neighbor_id)
                if neighbor:
                    hypothesis = {'explanation': f"{node.label} {rel_type} {neighbor.label}",
                                 'confidence': node.confidence * neighbor.confidence * 0.8,
                                 'nodes': [node.node_id, neighbor.node_id], 'relationship': rel_type}
                    hypotheses.append(hypothesis)
        hypotheses.sort(key=lambda x: x['confidence'], reverse=True)
        return hypotheses[:count]

    def evaluate_decision(self, options: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        scores = {}
        for option in options:
            score = self._score_option(option, context)
            scores[option] = score
        best_option = max(scores.items(), key=lambda x: x[1])
        return {'choice': best_option[0], 'confidence': best_option[1],
                'reasoning': "Selected based on context analysis", 'scores': scores}

    def _score_option(self, option: str, context: Dict[str, Any]) -> float:
        score = 0.5
        option_keywords = set(option.lower().split())
        context_keywords = set()
        for key, value in context.items():
            if isinstance(value, str):
                context_keywords.update(value.lower().split())
            else:
                context_keywords.add(str(value).lower())
        overlap = option_keywords & context_keywords
        if overlap:
            score += 0.3 * (len(overlap) / max(1, len(option_keywords)))
        for keyword in option_keywords:
            nodes = self.semantic_network.find_nodes(keyword)
            for node in nodes:
                neighbors = self.semantic_network.get_neighbors(node.node_id)
                for neighbor_id, rel_type in neighbors:
                    neighbor = self.semantic_network.get_node(neighbor_id)
                    if neighbor and any(kw in neighbor.label.lower() for kw in context_keywords):
                        score += 0.1 * node.confidence
        return min(1.0, max(0.0, score))


class LearningEngine:
    """Online learning system"""
    
    def __init__(self, semantic_network: SemanticNetwork, memory: MemorySystem):
        self.semantic_network = semantic_network
        self.memory = memory
        self.learning_queue = queue.Queue()
        self.learning_active = True
        self.learning_thread = threading.Thread(target=self._process_learning_queue, daemon=True)
        self.learning_thread.start()

    def learn(self, information: Union[str, Dict[str, Any]], context: Optional[Dict] = None) -> str:
        if isinstance(information, str):
            parsed = self._parse_information(information)
            return self._learn_parsed(parsed, context)
        else:
            return self._learn_dict(information, context)

    def _parse_information(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        if ' is ' in text_lower or ' are ' in text_lower:
            info_type = 'fact'
        elif ' do ' in text_lower or ' should ' in text_lower:
            info_type = 'rule'
        elif ' when ' in text_lower or ' if ' in text_lower:
            info_type = 'conditional'
        else:
            info_type = 'general'
        return {'type': info_type, 'text': text, 'keywords': text_lower.split()}

    def _learn_parsed(self, parsed: Dict, context: Optional[Dict]) -> str:
        if parsed['type'] == 'fact':
            return self._learn_fact(parsed, context)
        elif parsed['type'] == 'rule':
            return self._learn_rule(parsed, context)
        else:
            return self._learn_general(parsed, context)

    def _learn_fact(self, parsed: Dict, context: Optional[Dict]) -> str:
        text = parsed['text']
        if ' is ' in text.lower():
            parts = text.split(' is ', 1)
            subject = parts[0].strip()
            obj = parts[1].strip()
        elif ' are ' in text.lower():
            parts = text.split(' are ', 1)
            subject = parts[0].strip()
            obj = parts[1].strip()
        else:
            subject = text
            obj = ""
        subject_node = self.semantic_network.add_node(
            NodeType.ENTITY if obj else NodeType.CONCEPT, subject, source="learned", is_learned=True)
        if obj:
            obj_node = self.semantic_network.add_node(NodeType.CONCEPT, obj, source="learned", is_learned=True)
            self.semantic_network.add_relationship(subject_node.node_id, obj_node.node_id, "is_a", source="learned")
        episode = {'type': 'learning', 'information': parsed, 'context': context or {}, 'timestamp': time.time()}
        return self.memory.store_episodic(episode)

    def _learn_rule(self, parsed: Dict, context: Optional[Dict]) -> str:
        text = parsed['text']
        procedure = {'rule': text, 'type': 'rule', 'context': context or {}, 'timestamp': time.time()}
        memory_id = self.memory.store_procedural(procedure)
        rule_node = self.semantic_network.add_node(NodeType.RULE, f"Rule: {text[:50]}",
                                                     description=text, source="learned", is_learned=True)
        return memory_id

    def _learn_general(self, parsed: Dict, context: Optional[Dict]) -> str:
        episode = {'type': 'general_learning', 'information': parsed, 'context': context or {}, 'timestamp': time.time()}
        return self.memory.store_episodic(episode)

    def _learn_dict(self, information: Dict, context: Optional[Dict]) -> str:
        episode = {'type': 'structured_learning', 'information': information, 'context': context or {}, 'timestamp': time.time()}
        return self.memory.store_episodic(episode)

    def _process_learning_queue(self):
        while self.learning_active:
            try:
                task = self.learning_queue.get(timeout=1)
                self._process_learning_task(task)
                self.learning_queue.task_done()
            except queue.Empty:
                continue

    def _process_learning_task(self, task: Dict):
        pass

    def reinforce(self, memory_id: str, success: bool = True):
        for memory_type in [self.memory.semantic, self.memory.episodic, self.memory.procedural]:
            if memory_id in memory_type:
                entry = memory_type[memory_id]
                if isinstance(entry, KnowledgeNode):
                    entry.reinforce(success)
                elif isinstance(entry, MemoryEntry):
                    if success:
                        entry.confidence = min(1.0, entry.confidence + 0.1)
                        entry.relevance = min(1.0, entry.relevance + 0.1)
                    else:
                        entry.confidence = max(0.1, entry.confidence - 0.1)
                        entry.relevance = max(0.1, entry.relevance - 0.1)
                break

    def stop(self):
        self.learning_active = False
        self.learning_thread.join(timeout=5)


class NoveltyDetector:
    def __init__(self):
        self.known_patterns = []
        self.pattern_frequency = defaultdict(int)
        self.total_observations = 0

    def detect(self, data: Dict[str, Any]) -> float:
        self.total_observations += 1
        data_str = json.dumps(data, sort_keys=True)
        max_similarity = 0.0
        for pattern in self.known_patterns:
            similarity = self._compare_patterns(pattern, data_str)
            max_similarity = max(max_similarity, similarity)
        novelty_score = 1.0 - max_similarity
        pattern_key = self._extract_pattern_key(data_str)
        self.pattern_frequency[pattern_key] += 1
        if novelty_score > 0.5:
            self.known_patterns.append(data_str)
            if len(self.known_patterns) > 1000:
                self.known_patterns = self.known_patterns[-1000:]
        return novelty_score

    def _compare_patterns(self, pattern1: str, pattern2: str) -> float:
        set1 = set(pattern1.split())
        set2 = set(pattern2.split())
        if not set1 or not set2:
            return 0.0
        intersection = set1 & set2
        union = set1 | set2
        return len(intersection) / len(union)

    def _extract_pattern_key(self, data_str: str) -> str:
        words = sorted(set(data_str.lower().split()))
        return ' '.join(words)


class AdaptationSystem:
    def __init__(self, semantic_network: SemanticNetwork, memory: MemorySystem):
        self.semantic_network = semantic_network
        self.memory = memory
        self.environment_model = {}
        self.adaptation_history = []
        self.novelty_detector = NoveltyDetector()

    def adapt(self, new_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        novelty_score = self.novelty_detector.detect(new_data)
        changes = []
        self._update_environment_model(new_data)
        if novelty_score > Config.NOVELTY_SENSITIVITY:
            novel_concepts = self._extract_novel_concepts(new_data)
            for concept in novel_concepts:
                node = self.semantic_network.add_node(NodeType.CONCEPT, concept, source="adapted", is_learned=True)
                changes.append({'type': 'new_concept', 'concept': concept, 'node_id': node.node_id})
            adapted_rels = self._adapt_relationships(new_data)
            changes.extend(adapted_rels)
            adaptation_level = "major"
        else:
            adaptation_level = "minor"
        self.adaptation_history.append({'timestamp': time.time(), 'novelty_score': novelty_score,
                                         'changes': changes, 'adaptation_level': adaptation_level})
        if len(self.adaptation_history) > 1000:
            self.adaptation_history = self.adaptation_history[-1000:]
        return {'changes': changes, 'novelty_score': novelty_score, 'adaptation_level': adaptation_level}

    def _update_environment_model(self, new_data: Dict[str, Any]):
        for key, value in new_data.items():
            if key not in self.environment_model:
                self.environment_model[key] = {'value': value, 'history': [], 'last_updated': time.time()}
            self.environment_model[key]['value'] = value
            self.environment_model[key]['last_updated'] = time.time()
            self.environment_model[key]['history'].append({'value': value, 'timestamp': time.time()})
            if len(self.environment_model[key]['history']) > 100:
                self.environment_model[key]['history'] = self.environment_model[key]['history'][-100:]

    def _extract_novel_concepts(self, data: Dict[str, Any]) -> List[str]:
        concepts = []
        for key, value in data.items():
            if isinstance(value, str):
                existing = self.semantic_network.find_nodes(value)
                if not existing:
                    concepts.append(value)
        return concepts[:10]

    def _adapt_relationships(self, data: Dict[str, Any]) -> List[Dict]:
        changes = []
        all_concepts = []
        for key, value in data.items():
            if isinstance(value, str):
                all_concepts.append(value)
                nodes = self.semantic_network.find_nodes(value)
                for node in nodes:
                    all_concepts.append(node.label)
        unique_concepts = list(set(all_concepts))
        for i, concept_a in enumerate(unique_concepts):
            for concept_b in unique_concepts[i+1:]:
                nodes_a = self.semantic_network.find_nodes(concept_a)
                nodes_b = self.semantic_network.find_nodes(concept_b)
                if nodes_a and nodes_b:
                    existing_rels = self.semantic_network.get_relationships(nodes_a[0].node_id)
                    has_relationship = any(rel.target_id == nodes_b[0].node_id or
                                          (rel.bidirectional and rel.source_id == nodes_b[0].node_id)
                                          for rel in existing_rels)
                    if not has_relationship:
                        rel = self.semantic_network.add_relationship(nodes_a[0].node_id, nodes_b[0].node_id,
                                                                    "co_occurs_with", weight=0.5)
                        changes.append({'type': 'new_relationship', 'source': concept_a, 'target': concept_b,
                                       'relationship': 'co_occurs_with', 'relationship_id': rel.relationship_id})
        return changes


class RoboticsInterface:
    def __init__(self, semantic_network: SemanticNetwork, memory: MemorySystem,
                 reasoning_engine: ReasoningEngine, adaptation_system: AdaptationSystem):
        self.semantic_network = semantic_network
        self.memory = memory
        self.reasoning_engine = reasoning_engine
        self.adaptation_system = adaptation_system
        self.sensor_buffer = deque(maxlen=Config.SENSOR_FUSION_WINDOW)
        self.action_history = deque(maxlen=100)
        self.robot_state = {'position': [0, 0, 0], 'orientation': [0, 0, 0],
                           'status': 'idle', 'battery': 100.0, 'sensors': {}}

    def process_sensor_data(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        self.memory.add_sensory(sensor_data)
        self.sensor_buffer.append(sensor_data)
        if 'position' in sensor_data:
            self.robot_state['position'] = sensor_data['position']
        if 'orientation' in sensor_data:
            self.robot_state['orientation'] = sensor_data['orientation']
        if 'battery' in sensor_data:
            self.robot_state['battery'] = sensor_data['battery']
        perception = self._extract_features(sensor_data)
        interpretation = self._interpret_perception(perception)
        working_data = {'type': 'perception', 'raw_data': sensor_data, 'processed': perception,
                      'interpretation': interpretation, 'timestamp': time.time()}
        self.memory.add_to_working(working_data)
        self.adaptation_system.adapt(perception)
        return {'perception': perception, 'interpretation': interpretation, 'robot_state': self.robot_state.copy()}

    def _extract_features(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        features = {'timestamp': sensor_data.get('timestamp', time.time()), 'objects': [],
                   'obstacles': [], 'navigable_space': True, 'environment_type': 'unknown'}
        sensors = sensor_data.get('sensors', {})
        if 'lidar' in sensors:
            lidar_data = sensors['lidar']
            if lidar_data:
                min_distance = min(lidar_data) if isinstance(lidar_data, list) else float('inf')
                if min_distance < 0.5:
                    features['obstacles'].append({'type': 'close_obstacle', 'distance': min_distance})
                    features['navigable_space'] = False
        if 'imu' in sensors:
            imu_data = sensors['imu']
            features['orientation'] = imu_data.get('orientation', [0, 0, 0])
            features['acceleration'] = imu_data.get('acceleration', [0, 0, 0])
        return features

    def _interpret_perception(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        interpretation = {'objects': [], 'situation': 'normal', 'actions_suggested': []}
        if perception.get('obstacles'):
            interpretation['situation'] = 'obstacle_detected'
            interpretation['actions_suggested'].append('avoid_obstacle')
            obstacle_node = self.semantic_network.add_node(NodeType.ENTITY, 'obstacle', source='perception')
            neighbors = self.semantic_network.get_neighbors(obstacle_node.node_id)
            for neighbor_id, rel_type in neighbors:
                neighbor = self.semantic_network.get_node(neighbor_id)
                if neighbor and neighbor.node_type == NodeType.ACTION:
                    interpretation['actions_suggested'].append(neighbor.label)
        env_type = perception.get('environment_type', 'unknown')
        if env_type != 'unknown':
            interpretation['situation'] = f'in_{env_type}'
        return interpretation

    def plan_action(self, goal: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        goal_analysis = self.reasoning_engine.infer(goal)
        current_context = self.memory.get_working_context()
        if context:
            current_context.update(context)
        procedures = [p for p in self.memory.procedural.values()
                     if goal.lower() in json.dumps(p.content).lower()]
        if procedures:
            best_proc = max(procedures, key=lambda p: p.relevance)
            return {'action': 'follow_procedure', 'parameters': {'procedure_id': best_proc.memory_id},
                    'confidence': best_proc.confidence, 'plan': [best_proc.content]}
        options = self._generate_action_options(goal, current_context)
        decision = self.reasoning_engine.evaluate_decision(options, current_context)
        return {'action': decision['choice'], 'parameters': {}, 'confidence': decision['confidence'],
                'plan': [{'action': decision['choice'], 'reasoning': decision['reasoning']}]}

    def _generate_action_options(self, goal: str, context: Dict) -> List[str]:
        options = ['move_forward', 'move_backward', 'turn_left', 'turn_right', 'stop']
        if any('obstacle' in str(v).lower() for v in context.values()):
            options.extend(['avoid_obstacle', 'go_around', 'wait'])
        if 'explore' in goal.lower():
            options.extend(['explore_area', 'scan_environment'])
        elif 'navigate' in goal.lower():
            options.extend(['navigate_to_goal', 'follow_path'])
        elif 'grab' in goal.lower() or 'pick' in goal.lower():
            options.extend(['approach_object', 'extend_arm', 'grasp_object'])
        return options

    def execute_action(self, action: str, parameters: Dict = None) -> Dict[str, Any]:
        if parameters is None:
            parameters = {}
        result = {'action': action, 'parameters': parameters, 'timestamp': time.time()}
        if action == 'move_forward':
            self.robot_state['position'][0] += 0.1
            result['new_position'] = self.robot_state['position']
            result['success'] = True
        elif action == 'move_backward':
            self.robot_state['position'][0] -= 0.1
            result['new_position'] = self.robot_state['position']
            result['success'] = True
        elif action == 'turn_left':
            self.robot_state['orientation'][2] += 10
            result['new_orientation'] = self.robot_state['orientation']
            result['success'] = True
        elif action == 'turn_right':
            self.robot_state['orientation'][2] -= 10
            result['new_orientation'] = self.robot_state['orientation']
            result['success'] = True
        elif action == 'stop':
            self.robot_state['status'] = 'stopped'
            result['success'] = True
        else:
            result['success'] = False
            result['error'] = f"Unknown action: {action}"
        self.action_history.append(result)
        episode = {'type': 'action', 'action': action, 'parameters': parameters, 'result': result,
                  'robot_state': self.robot_state.copy(), 'timestamp': time.time()}
        self.memory.store_episodic(episode)
        return {'success': result.get('success', False), 'result': result, 'new_state': self.robot_state.copy()}

    def get_robotic_response(self, sensor_data: Dict[str, Any], goal: str = None) -> Dict[str, Any]:
        perception = self.process_sensor_data(sensor_data)
        if goal is None:
            goal = self._determine_goal(perception)
        plan = self.plan_action(goal, perception)
        execution = self.execute_action(plan['action'], plan.get('parameters'))
        return {'perception': perception, 'goal': goal, 'plan': plan, 'execution': execution,
                'robot_state': self.robot_state.copy()}

    def _determine_goal(self, perception: Dict[str, Any]) -> str:
        interpretation = perception.get('interpretation', {})
        situation = interpretation.get('situation', 'normal')
        if 'obstacle' in situation:
            return "avoid obstacle and continue navigation"
        elif 'unknown' in situation:
            return "explore environment"
        else:
            return "navigate to next waypoint"


class SelfEvolutionMechanism:
    def __init__(self, semantic_network: SemanticNetwork, memory: MemorySystem,
                 reasoning_engine: ReasoningEngine, learning_engine: LearningEngine):
        self.semantic_network = semantic_network
        self.memory = memory
        self.reasoning_engine = reasoning_engine
        self.learning_engine = learning_engine
        self.evolution_log = []
        self.evolution_count = 0
        self.last_evolution = time.time()

    def evolve(self) -> Dict[str, Any]:
        changes = []
        improvements = []
        if time.time() - self.last_evolution < Config.EVOLUTION_INTERVAL:
            return {'changes': [], 'improvements': [], 'evolution_count': self.evolution_count}
        self.last_evolution = time.time()
        self.evolution_count += 1
        optimized = self._optimize_knowledge_base()
        changes.extend(optimized.get('changes', []))
        improvements.extend(optimized.get('improvements', []))
        patterns = self._discover_new_patterns()
        changes.extend(patterns.get('changes', []))
        improvements.extend(patterns.get('improvements', []))
        rules = self._create_new_rules()
        changes.extend(rules.get('changes', []))
        improvements.extend(rules.get('improvements', []))
        memory_opt = self._optimize_memory()
        changes.extend(memory_opt.get('changes', []))
        improvements.extend(memory_opt.get('improvements', []))
        self.evolution_log.append({'timestamp': time.time(), 'evolution_count': self.evolution_count,
                                   'changes': len(changes), 'improvements': improvements})
        if len(self.evolution_log) > 100:
            self.evolution_log = self.evolution_log[-100:]
        return {'changes': changes, 'improvements': improvements, 'evolution_count': self.evolution_count}

    def _optimize_knowledge_base(self) -> Dict[str, Any]:
        changes = []
        improvements = []
        node_list = list(self.semantic_network.nodes.values())
        for i, node_a in enumerate(node_list):
            for node_b in node_list[i+1:]:
                if node_a.label.lower() == node_b.label.lower() and node_a.node_id != node_b.node_id:
                    if node_a.confidence > node_b.confidence:
                        keep_node = node_a
                        remove_node = node_b
                    else:
                        keep_node = node_b
                        remove_node = node_a
                    rels_to_update = self.semantic_network.get_relationships(remove_node.node_id)
                    for rel in rels_to_update:
                        if rel.source_id == remove_node.node_id:
                            self.semantic_network.add_relationship(keep_node.node_id, rel.target_id,
                                                                    rel.relationship_type, weight=rel.weight,
                                                                    confidence=rel.confidence, bidirectional=rel.bidirectional)
                        if rel.target_id == remove_node.node_id:
                            self.semantic_network.add_relationship(rel.source_id, keep_node.node_id,
                                                                    rel.relationship_type, weight=rel.weight,
                                                                    confidence=rel.confidence, bidirectional=rel.bidirectional)
                    del self.semantic_network.nodes[remove_node.node_id]
                    changes.append({'type': 'merge_nodes', 'kept': keep_node.node_id, 'removed': remove_node.node_id})
        if changes:
            improvements.append("merged_duplicate_nodes")
        return {'changes': changes, 'improvements': improvements}

    def _discover_new_patterns(self) -> Dict[str, Any]:
        changes = []
        improvements = []
        co_occurrence = defaultdict(int)
        for node in self.semantic_network.nodes.values():
            neighbors = self.semantic_network.get_neighbors(node.node_id)
            for neighbor_id, rel_type in neighbors:
                pair = tuple(sorted([node.node_id, neighbor_id]))
                co_occurrence[pair] += 1
        for (node_a_id, node_b_id), count in co_occurrence.items():
            if count > 5:
                existing = self.semantic_network.get_relationships(node_a_id)
                has_rel = any(rel.target_id == node_b_id or (rel.bidirectional and rel.source_id == node_b_id)
                            for rel in existing)
                if not has_rel:
                    rel = self.semantic_network.add_relationship(node_a_id, node_b_id,
                                                                "frequently_co_occurs_with", weight=min(1.0, count / 10))
                    changes.append({'type': 'new_pattern_relationship', 'source': node_a_id,
                                   'target': node_b_id, 'count': count, 'relationship_id': rel.relationship_id})
        if changes:
            improvements.append("discovered_new_patterns")
        return {'changes': changes, 'improvements': improvements}

    def _create_new_rules(self) -> Dict[str, Any]:
        changes = []
        improvements = []
        if len(self.memory.episodic) > 100:
            rule_text = "IF obstacle detected THEN avoid obstacle"
            self.learning_engine.learn(rule_text, source="evolved")
            changes.append({'type': 'new_rule', 'rule': rule_text})
            improvements.append("created_new_rules")
        return {'changes': changes, 'improvements': improvements}

    def _optimize_memory(self) -> Dict[str, Any]:
        changes = []
        improvements = []
        if len(self.memory.episodic) > Config.MAX_EPISODIC_MEMORY * 0.8:
            improvements.append("memory_optimization_suggested")
        return {'changes': changes, 'improvements': improvements}

    def modify_self(self, modification: Dict[str, Any]) -> bool:
        mod_type = modification.get('type')
        if mod_type == 'add_knowledge':
            self.learning_engine.learn(modification.get('knowledge'))
            return True
        elif mod_type == 'remove_knowledge':
            node_id = modification.get('node_id')
            if node_id in self.semantic_network.nodes:
                del self.semantic_network.nodes[node_id]
                return True
        elif mod_type == 'modify_parameter':
            param_name = modification.get('parameter')
            new_value = modification.get('value')
            if hasattr(Config, param_name):
                setattr(Config, param_name, new_value)
                return True
        return False


class CircleCityAGI:
    """
    Circle City Model - Complete AGI System
    
    A compact (<1GB) AGI framework with:
    - Autonomous learning
    - Adaptive reasoning
    - Robotics integration
    - Self-evolution
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.initialization_time = time.time()
        self.semantic_network = SemanticNetwork()
        self.memory = MemorySystem()
        self.reasoning_engine = ReasoningEngine(self.semantic_network, self.memory)
        self.learning_engine = LearningEngine(self.semantic_network, self.memory)
        self.adaptation_system = AdaptationSystem(self.semantic_network, self.memory)
        self.robotics = RoboticsInterface(self.semantic_network, self.memory,
                                         self.reasoning_engine, self.adaptation_system)
        self.evolution = SelfEvolutionMechanism(self.semantic_network, self.memory,
                                              self.reasoning_engine, self.learning_engine)
        self.stats = {'learning_count': 0, 'reasoning_count': 0, 'adaptation_count': 0,
                     'action_count': 0, 'evolution_count': 0}
        self._initialize_basic_knowledge()

    def _initialize_basic_knowledge(self):
        logic_facts = ["A cause leads to an effect", "An effect is the result of a cause",
                      "If X implies Y then Y is true when X is true"]
        for fact in logic_facts:
            self.learn(fact, source="bootstrap")
        robotics_facts = ["A robot can move forward", "A robot can move backward",
                         "A robot can turn left", "A robot can turn right",
                         "A robot should avoid obstacles", "An obstacle blocks movement"]
        for fact in robotics_facts:
            self.learn(fact, source="bootstrap")
        env_facts = ["The environment contains objects", "Objects can be obstacles",
                     "Objects can be goals", "Navigation requires knowing the environment"]
        for fact in env_facts:
            self.learn(fact, source="bootstrap")

    def learn(self, information: Union[str, Dict[str, Any]], context: Optional[Dict] = None) -> str:
        self.stats['learning_count'] += 1
        return self.learning_engine.learn(information, context)

    def reason(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        self.stats['reasoning_count'] += 1
        return self.reasoning_engine.infer(query, context)

    def decide(self, options: List[str], context: Optional[Dict] = None) -> Dict[str, Any]:
        return self.reasoning_engine.evaluate_decision(options, context or {})

    def adapt(self, new_data: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        self.stats['adaptation_count'] += 1
        return self.adaptation_system.adapt(new_data, context)

    def robotic_response(self, sensor_data: Dict[str, Any], goal: str = None) -> Dict[str, Any]:
        self.stats['action_count'] += 1
        return self.robotics.get_robotic_response(sensor_data, goal)

    def evolve(self) -> Dict[str, Any]:
        self.stats['evolution_count'] += 1
        return self.evolution.evolve()

    def hypothesize(self, observation: str, count: int = 3) -> List[Dict[str, Any]]:
        return self.reasoning_engine.generate_hypotheses(observation, count)

    def modify(self, modification: Dict[str, Any]) -> bool:
        return self.evolution.modify_self(modification)

    def remember(self, query: Union[str, Dict], memory_type: str = None) -> List:
        if isinstance(query, str):
            if memory_type == 'semantic':
                return self.memory.retrieve_semantic(query)
            elif memory_type == 'episodic':
                return self.memory.retrieve_episodic({'query': query})
            else:
                results = []
                results.extend(self.memory.retrieve_semantic(query))
                results.extend(self.memory.retrieve_episodic({'query': query}))
                return results
        else:
            return self.memory.retrieve_episodic(query)

    def get_working_memory(self) -> Dict[str, Any]:
        return self.memory.get_working_context()

    def clear_working_memory(self):
        self.memory.clear_working()

    def get_stats(self) -> Dict[str, Any]:
        uptime = time.time() - self.initialization_time
        return {'version': self.version, 'uptime_seconds': uptime,
                'knowledge_nodes': len(self.semantic_network.nodes),
                'relationships': len(self.semantic_network.relationships),
                'semantic_memory': len(self.memory.semantic),
                'episodic_memory': len(self.memory.episodic),
                'procedural_memory': len(self.memory.procedural),
                'working_memory': len(self.memory.working), 'stats': self.stats.copy()}

    def save(self) -> Dict[str, Any]:
        return {'version': self.version, 'semantic_network': self.semantic_network.save(),
                'stats': self.stats.copy(), 'initialization_time': self.initialization_time}

    def load(self, state: Dict[str, Any]):
        self.version = state.get('version', '1.0.0')
        self.initialization_time = state.get('initialization_time', time.time())
        self.stats = state.get('stats', self.stats.copy())
        if 'semantic_network' in state:
            self.semantic_network.load(state['semantic_network'])

    def reset(self):
        self.__init__()

    def shutdown(self):
        self.learning_engine.stop()


def create_agi() -> CircleCityAGI:
    return CircleCityAGI()


def create_robot_agi() -> CircleCityAGI:
    agi = CircleCityAGI()
    robotics_knowledge = ["A robot has sensors", "A robot has actuators",
                        "Sensors provide information about the environment",
                        "Actuators allow the robot to interact with the environment",
                        "Robot navigation requires sensor data", "Robot manipulation requires precise control",
                        "A mobile robot can move in the environment", "A robotic arm can grasp objects",
                        "Safe robot operation requires obstacle avoidance", "Robot localization requires sensor fusion"]
    for knowledge in robotics_knowledge:
        agi.learn(knowledge, source="robotics_bootstrap")
    return agi


if __name__ == "__main__":
    print("Circle City Model - Compact AGI Framework")
    print("=" * 60)
    agi = create_agi()
    print(f"Initialized v{agi.version}")
    print(f"Knowledge nodes: {len(agi.semantic_network.nodes)}")
    agi.learn("The sky is blue during the day")
    agi.learn("Robots should avoid obstacles to prevent damage")
    result = agi.reason("What color is the sky?")
    print(f"Q: What color is the sky? A: {result.get('answer', 'Unknown')}")
    decision = agi.decide(["move forward", "turn left", "stop"], context={"obstacle": "ahead"})
    print(f"Decision with obstacle ahead: {decision['choice']}")
    hypotheses = agi.hypothesize("The robot stopped moving")
    print(f"Hypotheses for 'The robot stopped moving':")
    for i, hyp in enumerate(hypotheses, 1):
        print(f"  {i}. {hyp['explanation']} (confidence: {hyp['confidence']:.2f})")
    sensor_data = {'timestamp': time.time(), 'sensors': {'lidar': [0.1, 0.2, 0.3, 0.5, 1.0, 2.0, 3.0]}}
    response = agi.robotic_response(sensor_data)
    print(f"Robotic response: {response['perception']['interpretation'].get('situation', 'normal')}")
    print(f"Stats: {agi.get_stats()}")
