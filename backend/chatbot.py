from crewai import Agent, Task, Crew
from typing import List


class Chatbot:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base
        self.setup_crew()
   
    def setup_crew(self):
        self.researcher = Agent(
            role='Project X Knowledge Specialist',
            goal='Provide accurate information about Project X and CoC VJTI',
            backstory="""Expert on Project X and Community of Coders at VJTI.
            Knowledgeable about their events, initiatives, and community impact.""",
            allow_delegation=False
        )
       
        self.writer = Agent(
            role='Community Response Specialist',
            goal='Craft engaging and informative responses about VJTI communities',
            backstory="""Skilled at creating friendly, informative responses about
            technical communities and student initiatives.""",
            allow_delegation=False
        )
       
        self.crew = Crew(
            agents=[self.researcher, self.writer],
            tasks=[]
        )
   
    def process_query(self, user_input: str) -> str:
        search_results = self.knowledge_base.search(user_input)
        context = "\n".join(search_results) if search_results else "No specific information found."
       
        research_task = Task(
            description=f"Research query: {user_input}\nContext: {context}",
            agent=self.researcher
        )
       
        write_task = Task(
            description=f"""Create a friendly, informative response for: {user_input}
            Based on research: {context}
            Keep response concise and focused.""",
            agent=self.writer
        )
       
        self.crew.tasks = [research_task, write_task]
        result = self.crew.kickoff()
       
        return result