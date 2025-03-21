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
uv run src/main.py "How to cook Pho?"
```

```
User input: How to cook Pho?
---
DecideAction: response=ActionResponse(thinking_process='I need to search the web to find a good Pho recipe.', action='search', action_input='authentic pho recipe', reason='I need to find information on how to cook Pho to answer the question.')
---
SearchAction: result=DdgSearchResult(title='Pho Recipe (Vietnamese Noodle Soup) - The Woks of Life', href='https://thewoksoflife.com/pho-vietnamese-noodle-soup/', body='Learn how to make authentic pho broth with beef bones, spices, fish sauce, and charred onions and ginger. Follow the steps and tips from a Vietnamese friend and enjoy the fragrant soup with noodles and toppings.')
SearchAction: result=DdgSearchResult(title='Pho (Vietnamese Noodle Soup) Recipe', href='https://www.allrecipes.com/recipe/228443/authentic-pho/', body='Learn how to make pho, a Vietnamese soup with bone broth, rice noodles, and thinly sliced beef, from scratch. Follow the detailed steps and tips to simmer the broth, soak the noodles, and garnish with fresh herbs and sauces.')
SearchAction: result=DdgSearchResult(title='Truly Authentic Vietnamese Pho Recipe - i am a food blog', href='https://iamafoodblog.com/authentic-instant-pot-pho-recipe/', body='Learn how to make authentic Vietnamese pho soup with beef, charred aromatics, and fresh herbs in your Instant Pot. Get tips on broth, noodles, toppings, and variations.')
SearchAction: result=DdgSearchResult(title='Authentic Vietnamese Beef Pho (Pho Bo) Recipe - Craving Tasty', href='https://cravingtasty.com/beef-pho-vietnamese-pho-bo/', body='Learn how to make pho bo, the most popular pho in the West, with a complex and aromatic broth that simmers for hours. Follow the detailed steps and ingredients to create your own pho bo with rice noodles, raw beef, and various garnishes.')
SearchAction: result=DdgSearchResult(title='Vietnamese Pho Recipe (Phở Bò) - Vicky Pham', href='https://vickypham.com/blog/vietnamese-beef-noodle-soup-pho-bo/', body='Clean the bones: Cleaning the bones will get rid of all the impurities and ensure a clear broth. Bring a large pot of water to a rolling boil. Add beef bones and boil for 8 minutes or until foam float to the top. If using marrow bones, boil for only 3 minutes.')
---
DecideAction: response=ActionResponse(thinking_process='The previous research provides a good overview of making pho, including the importance of cleaning the bones and simmering the broth for a long time to extract flavor. However, it lacks specific details on the spices used, the noodle type, and detailed instructions on assembling the final dish. I will perform a search to find a comprehensive recipe that includes these details.', action='search', action_input='authentic pho recipe detailed instructions', reason='To find a comprehensive pho recipe with specific details on spices, noodle type, and assembly instructions for a complete answer.')
---
SearchAction: result=DdgSearchResult(title='Pho Recipe (Vietnamese Noodle Soup) - The Woks of Life', href='https://thewoksoflife.com/pho-vietnamese-noodle-soup/', body='Add 5 quarts fresh water back to the stockpot and bring to a boil. Transfer the bones and meat back to the pot, along with the charred/cleaned ginger and onions. Add the scallions, fish sauce and rock sugar.Reduce the heat to low, and simmer until the beef chuck is tender, about 40 minutes.')
SearchAction: result=DdgSearchResult(title='Authentic Vietnamese Pho Recipe: A Step-by-Step Guide', href='https://phobistrobarrie.com/recipe/vietnamese-pho', body='Step-by-Step Instructions Step 1. Building the Rich Pho Broth. Preheat oven to 425°F (220°C). Place beef bones on a foil-lined baking sheet, spray with oil, and roast for 30-40 minutes until deep brown. ... Pork Pho Recipe: Authentic Vietnamese Noodle Soup. Vietnamese Chicken Noodle Soup (Pho Ga): Authentic Recipe. Address: 649 Yonge St, Unit ...')
SearchAction: result=DdgSearchResult(title='How to Make Authentic Vietnamese Pho (Pho Bo) - Cooking Therapy', href='https://www.cooking-therapy.com/traditional-vietnamese-pho-recipe/', body='How to make authentic beef pho or pho bo. ... This Vietnamese Pho recipe is a detailed guide on how to make your own pho noodle soup. 4.85 from 19 ratings. ... Instructions . Put the beef shank, ox tail, and beef chuck in a large pot with enough water to cover the meat. Bring to a boil. Once the water boils, take the meat out and set aside.')
SearchAction: result=DdgSearchResult(title='Truly Authentic Vietnamese Pho Recipe - i am a food blog', href='https://iamafoodblog.com/authentic-instant-pot-pho-recipe/', body="Fat content. Every good noodle soup needs fat for the broth to stick to the noodle and pho is no exception. If you prefer to control the fat content of your pho (and can wait a few hours before eating) this is a trick I learned from Ivan Ramen's cookbook:. Leave the pho in the fridge until the fat solidifies (typically 4-6 hours)")
SearchAction: result=DdgSearchResult(title='Pho (Vietnamese Noodle Soup) - Allrecipes', href='https://www.allrecipes.com/recipe/228443/authentic-pho/', body="Beef Soup Bones: Use the shank and knee to make the homemade bone broth. Rice Noodles: You should be able to find dry rice noodles at most grocery stores, either in the international aisle or another pantry aisle. Beef: This recipe calls for beef top sirloin.Make sure it's thinly sliced so the hot broth can cook it. Fish Sauce: Fish sauce will give the pho a hint of salty, fishy flavor.")
---
DecideAction: response=ActionResponse(thinking_process='The user wants to know how to cook Pho. I have some information on the ingredients and how to make the broth. I will use this information to create a response.', action='answer', action_input='To cook Pho, you will need beef bones (shank and knee), rice noodles, beef top sirloin, and fish sauce. First, clean the bones by boiling them in a large pot of water for about 8 minutes. Next, roast the beef bones in the oven at 425°F (220°C) for 30-40 minutes until deep brown. Add the bones to a stockpot with 5 quarts of fresh water, charred ginger and onions, scallions, fish sauce, and rock sugar. Simmer until the beef chuck is tender, about 40 minutes. Make sure the beef is thinly sliced so the hot broth can cook it.', reason="I am answering the user's question using the information I have.")
---
AnswerAction: input='To cook Pho, you will need beef bones (shank and knee), rice noodles, beef top sirloin, and fish sauce. First, clean the bones by boiling them in a large pot of water for about 8 minutes. Next, roast the beef bones in the oven at 425°F (220°C) for 30-40 minutes until deep brown. Add the bones to a stockpot with 5 quarts of fresh water, charred ginger and onions, scallions, fish sauce, and rock sugar. Simmer until the beef chuck is tender, about 40 minutes. Make sure the beef is thinly sliced so the hot broth can cook it.'
```

```
uv run src/main.py "Where does the name Vivian come from?"
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
