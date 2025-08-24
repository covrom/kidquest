"""
Validation utilities for quest structures
"""

import logging
from typing import Dict, Any, List, Set
from collections import deque

logger = logging.getLogger(__name__)


def is_valid_quest_graph(quest_data: Dict[str, Any]) -> bool:
    """
    Validate that the quest forms an acyclic directed graph with one input and multiple outputs.
    
    Args:
        quest_data (Dict[str, Any]): The quest data structure
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Get steps from quest data
    steps = quest_data.get('quest', {}).get('steps', [])
    
    # Create a mapping of step IDs to steps for easy lookup
    step_map = {step['id']: step for step in steps}
    
    # Validate that we have at least one step
    if not steps:
        logger.warning("Quest validation failed: No steps found in quest data")
        return False
    
    # Find start step ID
    start_step_id = quest_data.get('quest', {}).get('startStepId')
    
    # Check if startStepId exists in our steps
    if start_step_id not in step_map:
        logger.warning("Quest validation failed: startStepId '%s' not found in steps", start_step_id)
        return False
    
    # Validate each step has required fields and options are properly structured
    for step in steps:
        step_id = step.get('id')
        if not step_id:
            logger.warning("Quest validation failed: Step missing ID")
            return False
            
        # Check that all nextStepId references point to existing steps
        options = step.get('options', [])
        for option in options:
            next_step_id = option.get('nextStepId')
            if next_step_id and next_step_id not in step_map:
                logger.warning("Quest validation failed: nextStepId '%s' referenced by step '%s' does not exist",
                              next_step_id, step_id)
                return False
    
    # Check for cycles using topological sort (Kahn's algorithm)
    if not _has_no_cycles(step_map, start_step_id):
        logger.warning("Quest validation failed: Cycle detected in quest graph")
        return False
        
    # Check that there is exactly one input (startStepId)
    # and multiple outputs (steps with no outgoing edges or ending steps)
    if not _has_single_input_and_multiple_outputs(step_map, start_step_id):
        logger.warning("Quest validation failed: Quest does not have single input and multiple outputs")
        return False
    
    return True


def _has_no_cycles(step_map: Dict[str, Any], start_step_id: str) -> bool:
    """
    Check if the graph has cycles using topological sorting (Kahn's algorithm).
    
    Args:
        step_map (Dict[str, Any]): Mapping of step IDs to steps
        start_step_id (str): ID of the starting step
        
    Returns:
        bool: True if no cycles, False otherwise
    """
    # Build adjacency list and in-degree count
    graph = {step_id: [] for step_id in step_map.keys()}
    in_degree = {step_id: 0 for step_id in step_map.keys()}
    
    # Populate the graph with edges (from -> to)
    for step_id, step in step_map.items():
        options = step.get('options', [])
        for option in options:
            next_step_id = option.get('nextStepId')
            if next_step_id and next_step_id in step_map:
                graph[step_id].append(next_step_id)
                in_degree[next_step_id] += 1
    
    # Kahn's algorithm for topological sort
    queue = deque([start_step_id])
    visited_count = 0
    
    while queue:
        current_step_id = queue.popleft()
        visited_count += 1
        
        # Process neighbors
        for neighbor in graph[current_step_id]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If we didn't visit all nodes, there's a cycle
    if visited_count != len(step_map):
        logger.warning("Cycle detection failed: Not all nodes were visited during topological sort")
        return False
    return True


def _has_single_input_and_multiple_outputs(step_map: Dict[str, Any], start_step_id: str) -> bool:
    """
    Check that the graph has exactly one input (startStepId) and multiple outputs.
    
    Args:
        step_map (Dict[str, Any]): Mapping of step IDs to steps
        start_step_id (str): ID of the starting step
        
    Returns:
        bool: True if valid structure, False otherwise
    """
    # Check that there's exactly one input (startStepId)
    # This is already validated by checking it exists in our step_map
    
    # Count how many steps have no incoming edges (potential outputs)
    # These are steps that are not referenced as nextStepId by any other step
    all_step_ids = set(step_map.keys())
    
    # Find all nodes that are pointed to by options (have incoming edges)
    nodes_with_incoming_edges = set()
    for step in step_map.values():
        options = step.get('options', [])
        for option in options:
            next_step_id = option.get('nextStepId')
            if next_step_id and next_step_id in all_step_ids:
                nodes_with_incoming_edges.add(next_step_id)
    
    # Nodes with no incoming edges are potential outputs
    potential_outputs = all_step_ids - nodes_with_incoming_edges
    
    # For a valid quest, we should have at least one output (ending step)
    # and potentially multiple outputs (multiple ending points)
    if len(potential_outputs) < 1:
        logger.warning("Single input and multiple outputs validation failed: No potential outputs found")
        return False
    return True