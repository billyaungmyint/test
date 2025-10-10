import asyncio
import sys
import os

# Add the current directory to Python path to import from openai-agentkit.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the functions from the main file
import importlib.util
spec = importlib.util.spec_from_file_location("agentkit", "openai-agentkit.py")
agentkit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agentkit)

async def test_agent_output():
    """Test function to demonstrate printing agent outputs"""
    
    # Test 1: Math question
    print("=== Test 1: Math Question ===")
    result1 = await agentkit.run_workflow(agentkit.WorkflowInput(input_as_text="What is 10 + 5?"))
    print(f"Final output: {result1['output_text']}")
    print()
    
    # Test 2: Non-math question  
    print("=== Test 2: Non-Math Question ===")
    result2 = await agentkit.run_workflow(agentkit.WorkflowInput(input_as_text="Tell me about the weather"))
    print(f"Final output: {result2['output_text']}")
    print()
    
    # Test 3: Show complete result structure
    print("=== Test 3: Complete Result Structure ===")
    result3 = await agentkit.run_workflow(agentkit.WorkflowInput(input_as_text="Calculate 7 * 8"))
    print(f"Complete result: {result3}")

if __name__ == "__main__":
    asyncio.run(test_agent_output())