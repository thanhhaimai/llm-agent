# LLM Agent

Implement LLM Agents after reading: https://zacharyhuang.substack.com/p/llm-agent-internal-as-a-graph-tutorial

# Setup

Run `setup/setup.sh` to set up the development environment

NOTE: The setup script is idempotent, so it's okay if you re-run it.

# The plan

- [x] Setup `uv`
- [x] Setup `pytest`
- [x] Setup presubmit
- [x] Simple prototype that can call Gemini
- [x] Simple prototype that can call DuckDuckGo
- [x] Design a graph of agent
- [x] Implement Decide node
- [x] Implement Search node
- [x] Implement Answer node

# Example output

```
uv run src/main.py
```

```
User input: Where does the name Vivian come from?
---
DecideAction: response=ActionResponse(thinking_process='The question is about the origin of the name Vivian. I need to find information about the etymology and history of the name.', action='search', action_input='origin of the name Vivian', reason='I need to search the web to gather information about the etymology and history of the name Vivian.')
---
SearchAction: result=DdgSearchResult(title='Vivian (personal name) - Wikipedia', href='https://en.wikipedia.org/wiki/Vivian_(personal_name)', body='Vivian (and variants such as Vivien and Vivienne) is a given name, and less often a surname, derived from a Latin name of the Roman Empire period, masculine Vivianus and feminine Viviana, which survived into modern use because it is the name of two early Christian female martyrs as well as of a male saint and bishop.')
SearchAction: result=DdgSearchResult(title='Meaning, origin and history of the name Vivian', href='https://www.behindthename.com/name/vivian', body='Saint Vivian was a French bishop who provided protection during the Visigoth invasion of the 5th century. It has been occasionally used as an English (masculine) name since the Middle Ages. In modern times it is also used as a feminine name, in which case it is either an Anglicized form of Bébinn or a variant of Vivien 2.')
SearchAction: result=DdgSearchResult(title='Vivian Name Meaning: Origin, Popularity, & Significance', href='https://nameoftheyear.com/vivian-name-meaning/', body="Vivian Name Origin & Meaning If ya're interested in the origin & meaning of the name Vivian, ya've come to the right place. In this section, we'll explore the Latin roots of the name & its various connotations. We'll also discuss the historical usage of Vivian as a masculine & feminine name, as well as some popular variants & nicknames. Latin Roots & Meaning The name Vivian is derived ...")
SearchAction: result=DdgSearchResult(title='Vivian - Baby Name Meaning, Origin, and Popularity', href='https://nameberry.com/b/girl-baby-name-vivian', body='Vivian is a girl\'s name of Latin origin meaning "life". Vivian is the 87 ranked female name by popularity.')
SearchAction: result=DdgSearchResult(title='Vivian: Name Meaning, Popularity and Info on BabyNames.com', href='https://babynames.com/name/vivian', body='The name Vivian is primarily a female name of Latin origin that means Alive. Click through to find out more information about the name Vivian on BabyNames.com.')
---
DecideAction: response=ActionResponse(thinking_process='The previous research provides a solid foundation for answering the question. The name Vivian is derived from Latin roots, specifically the Latin name Vivianus (masculine) and Viviana (feminine), meaning "alive". I will formulate an answer based on this information.', action='answer', action_input='The name Vivian comes from the Latin name Vivianus (masculine) and Viviana (feminine), which mean "alive".', reason='The existing research provides a direct answer to the question, making it unnecessary to search for further information.')
---
AnswerAction: input='The name Vivian comes from the Latin name Vivianus (masculine) and Viviana (feminine), which mean "alive".'
```
