# Altruism-Evolution-Simulation

## How it works

This is a small simulation based on https://www.youtube.com/watch?v=iLX_r_WPrIw 

It simulates the following setup:
- There are 100 houses, each can store 2 critters
- Each critter is either a "coward" or "altruistic"
- Each night, critters go to houses and give birth to 4 children. Then, the parents die.
    - The children have a 50% chance of inheriting a gene from each parent
- Each day, a sibling pod has the chance to encounter a danger
    - One sibling notices the danger.
    - "Coward" critters survive, but their siblings die
    - "Altruistic" critters die, but their siblings survive
- At the end of the day, at most 200 critters are randomly assigned to houses

## How to run:

`python evolusac.py`