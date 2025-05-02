# import distutils
import setuptools
import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
from crewai_tools import ScrapeWebsiteTool, SeleniumScrapingTool

# Load environment variables first
load_dotenv()

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class SqliCrew():
    """SqliCrew crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, target_website=None): # Accept target_website
        # Initialise LLM with API key
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4", # or "gpt-4-turbo" if available
            temperature=0.3
        )
        self.target_website = target_website
        self.scrape_tool = None
        self.selenium_tool = None

        if self.target_website:
            self.scrape_tool = ScrapeWebsiteTool(website_url=self.target_website)
            self.selenium_tool = SeleniumScrapingTool(website_url=self.target_website)

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def recon_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['recon_agent'],
            llm=self.llm, # Assign the configured LLM
            verbose=True,
            tools=[self.scrape_tool, self.selenium_tool] # Ensure both tools are available
        )

    @agent
    def scanner_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['scanner_agent'],
            llm=self.llm,
            verbose=True
        )
    
    @agent
    def payload_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['payload_agent'],
            llm=self.llm,
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def recon_task(self) -> Task:
        return Task(
            config=self.tasks_config['recon_task'],
            agent=self.recon_agent(),  # Call the agent method to get the Agent object
            output_file='recon.md'
        )

    @task
    def scan_task(self) -> Task:
        return Task(
            config=self.tasks_config['scan_task'],
            agent=self.scanner_agent(),  # Call the agent method to get the Agent object
            output_file='scan.md'
        )
    
    @task
    def payload_task(self) -> Task:
        return Task(
            config=self.tasks_config['payload_task'],
            agent=self.payload_agent(),  # Call the agent method to get the Agent object
            output_file='payload.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SqliCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        if self.target_website:
            self.scrape_tool = ScrapeWebsiteTool(website_url=self.target_website)
            self.selenium_tool = SeleniumScrapingTool(website_url=self.target_website)
        else:
            raise ValueError("Target website URL must be provided before creating the crew.")

        reconnaissance_agent = self.recon_agent()
        reconnaissance_agent.tools = [self.scrape_tool, self.selenium_tool]

        scanner_agent = self.scanner_agent()
        # Scanner agent might not need these tools, but you can add them if needed
        # scanner_agent.tools = [...]

        payload_generator_agent = self.payload_agent()
        # Payload generator agent likely doesn't need these tools
        # payload_generator_agent.tools = [...]

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
            manager_llm=self.llm
        )
