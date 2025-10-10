# uv add openai-agents
from agents import Agent, ModelSettings, TResponseInputItem, Runner, RunConfig
from pydantic import BaseModel

my_agent = Agent(
  name="My agent",
  instructions="classify the question to check if it is a mathematics question and to say 'Shoo Shoo'' with an angry emoji to the user if it is not a mathematics question",
  model="gpt-4o",
  model_settings=ModelSettings(
    store=True
  )
)


agent = Agent(
  name="Agent",
  instructions="always add 1 to the answer",
  model="gpt-4o",
  model_settings=ModelSettings(
    store=True
  )
)


class WorkflowInput(BaseModel):
  input_as_text: str


# Main code entrypoint
async def run_workflow(workflow_input: WorkflowInput):
  state = {

  }
  workflow = workflow_input.model_dump()
  conversation_history: list[TResponseInputItem] = [
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": workflow["input_as_text"]
        }
      ]
    }
  ]
  my_agent_result_temp = await Runner.run(
    my_agent,
    input=[
      *conversation_history
    ],
    run_config=RunConfig(trace_metadata={
      "__trace_source__": "agent-builder",
      "workflow_id": "wf_68e857d32ac881909d5b48cc9ffb62f409f5725b5984cec1"
    })
  )

  conversation_history.extend([item.to_input_item() for item in my_agent_result_temp.new_items])

  my_agent_result = {
    "output_text": my_agent_result_temp.final_output_as(str)
  }
  print(f"My Agent Output: {my_agent_result['output_text']}")
  
  agent_result_temp = await Runner.run(
    agent,
    input=[
      *conversation_history
    ],
    run_config=RunConfig(trace_metadata={
      "__trace_source__": "agent-builder",
      "workflow_id": "wf_68e857d32ac881909d5b48cc9ffb62f409f5725b5984cec1"
    })
  )

  conversation_history.extend([item.to_input_item() for item in agent_result_temp.new_items])

  agent_result = {
    "output_text": agent_result_temp.final_output_as(str)
  }
  print(f"Agent Output: {agent_result['output_text']}")
  
  return agent_result


# Example usage - uncomment to test
async def main():
    # Test with a math question
    test_input = WorkflowInput(input_as_text="What is 5 + 3?")
    result = await run_workflow(test_input)
    print(f"Final Result: {result}")
    
    # Test with a non-math question
    test_input2 = WorkflowInput(input_as_text="What's the weather like?")
    result2 = await run_workflow(test_input2)
    print(f"Final Result 2: {result2}")

# Uncomment the lines below to run the example
# import asyncio
# if __name__ == "__main__":
#     asyncio.run(main())

