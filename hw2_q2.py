from collections import namedtuple
from enum import Enum
from itertools import zip_longest

Condition = Enum("Condition", ("CURE", "HEALTHY", "SICK", "DYING", "DEAD"))
Agent = namedtuple("Agent", ("name", "category"))


def improve_agent(agent: Agent) -> Agent:
    if agent.category == Condition.SICK:
        return Agent(agent.name, Condition.HEALTHY)
    if agent.category == Condition.DYING:
        return Agent(agent.name, Condition.SICK)

def worsen_agent(agent: Agent) -> Agent:
    if agent.category == Condition.SICK:
        return Agent(agent.name, Condition.DYING)
    if agent.category == Condition.DYING:
        return Agent(agent.name, Condition.DEAD)

def interact(agent1: Agent, agent2: Agent) -> tuple[Agent, Agent]:
    if agent1.category == Condition.CURE and agent2.category != Condition.CURE:
        return agent1, improve_agent(agent2)
    elif agent2.category == Condition.CURE and agent1.category != Condition.CURE:
        return improve_agent(agent1), agent2
    else:
        return worsen_agent(agent1), worsen_agent(agent2)


def meetup(agent_listing: tuple) -> list:
    """Model the outcome of the meetings of pairs of agents.

    The pairs of agents are ((a[0], a[1]), (a[2], a[3]), ...). If there's an uneven
    number of agents, the last agent will remain the same.

    Notes
    -----
    The rules governing the meetings were described in the question. The outgoing
    listing may change its internal ordering relative to the incoming one.

    Parameters
    ----------
    agent_listing : tuple of Agent
        A listing (tuple in this case) in which each element is of the Agent
        type, containing a 'name' field and a 'category' field, with 'category' being
        of the type Condition.

    Returns
    -------
    updated_listing : list
        A list of Agents with their 'category' field changed according to the result
        of the meeting.
    """

    updated_agents, valid_agents = [], []
    for agent in agent_listing:
        if agent.category in [Condition.HEALTHY, Condition.DEAD]:
            updated_agents.append(agent)
        else:
            valid_agents.append(agent)
    
    for agent1, agent2 in zip_longest(valid_agents[::2], valid_agents[1::2]):
        if agent1 and agent2:
            new_agent1, new_agent2 = interact(agent1, agent2)
            updated_agents.extend([new_agent1, new_agent2])
        elif agent1:
            updated_agents.append(agent1)
        elif agent2:
            updated_agents.append(agent2)

    return updated_agents
